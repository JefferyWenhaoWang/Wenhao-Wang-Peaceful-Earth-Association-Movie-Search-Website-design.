import os
import sqlite3
import sys

import click
import requests
from flask import Flask, request, g, session, redirect, url_for, render_template, jsonify, flash
from flask_github import GitHub
from flask_sqlalchemy import SQLAlchemy

# Set the path for the database file
import dbutil

database_path = os.path.join(os.path.dirname(__file__), 'data.db')

# sqlite URI compatible
WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'

app = Flask(__name__)
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'secret string')
# Flask-SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', prefix + database_path)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# GitHub-Flask
# Register your OAuth application on https://github.com/settings/applications/new
# You normally need to save these values as environment variables
app.config['GITHUB_CLIENT_ID'] = 'caa85c800f00991d0f4c'
app.config['GITHUB_CLIENT_SECRET'] = 'dab1a6843ee8ee0727a4b590b6735c1f585f4c89'

db = SQLAlchemy(app)
github = GitHub(app)


def initialize_database(db_file, create_table_sql):
    """
    Initialize the SQLite database and create tables if they don't exist.

    Args:
    - db_file: Path to the SQLite database file.
    - create_table_sql: SQL statement to create tables.

    Returns:
    - conn: SQLite connection object.
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        cursor.execute(create_table_sql)
        conn.commit()
        print("Database and tables created successfully!")
    except sqlite3.Error as e:
        print(f"Error: {e}")
    finally:
        if conn:
            conn.close()
    return conn


db_file = "example.db"
# Create User table
create_table_sql = """
    CREATE TABLE User (
        id INTEGER PRIMARY KEY,
        github_username TEXT NOT NULL UNIQUE,
        github_user_id INTEGER NOT NULL
    );
    """
initialize_database(db_file, create_table_sql)
# Create Movie table
create_table_sql = """
    CREATE TABLE Movie (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    director TEXT,
    actors TEXT,
    release_date DATE
);
    """
initialize_database(db_file, create_table_sql)
# Create Category table
create_table_sql = """
    CREATE TABLE Category (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL UNIQUE
    );
    """
initialize_database(db_file, create_table_sql)
# Create Movie_Category table
create_table_sql = """
    CREATE TABLE Movie_Category (
        movie_id INTEGER,
        category_id INTEGER,
        FOREIGN KEY (movie_id) REFERENCES Movie(id),
        FOREIGN KEY (category_id) REFERENCES Category(id),
        PRIMARY KEY (movie_id, category_id)
    );
    """
initialize_database(db_file, create_table_sql)
# Create User_Favorite_Movie table
create_table_sql = """
    CREATE TABLE User_Favorite_Movie (
        github_user_id INTEGER NOT NULL,
        movie_id INTEGER,
        FOREIGN KEY (github_user_id) REFERENCES User(id),
        FOREIGN KEY (movie_id) REFERENCES Movie(id),
        PRIMARY KEY (github_user_id, movie_id)
    );
    """
initialize_database(db_file, create_table_sql)
# Create Movie_Review table
create_table_sql = """
    CREATE TABLE Movie_Review (
        id INTEGER PRIMARY KEY,
        github_user_id INTEGER,
        movie_id INTEGER,
        rating INTEGER,
        comment TEXT,
        FOREIGN KEY (github_user_id) REFERENCES User(id),
        FOREIGN KEY (movie_id) REFERENCES Movie(id)
    );
    """
initialize_database(db_file, create_table_sql)


# Connect to the database
def connect_to_database(db_file):
    conn = sqlite3.connect(db_file)
    return conn


# Close the database connection
def close_connection(conn):
    conn.close()


conn = connect_to_database(db_file)


@app.cli.command()
@click.option('--drop', is_flag=True, help='Create after drop.')
def initdb(drop):
    """Initialize the database."""
    if drop:
        db.drop_all()
    db.create_all()
    click.echo('Initialized database.')


class User(db.Model):
    # __tablename__ = 'user'  # Specify the table name as 'user'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    username = db.Column(db.String(100))
    access_token = db.Column(db.String(200))


@app.before_request
def before_request():
    g.user = None
    if 'user_id' in session:
        g.user = User.query.filter_by(user_id=session['user_id']).first()
        print(User.query.filter_by(user_id=session['user_id']).first())


@app.route('/')
def index():

    if g.user:
        is_login = True
        response = github.get('user')
        avatar = response['avatar_url']
        username = response['name']
        url = response['html_url']
        user_id = response['id']
        session['user_id'] = user_id
        session['username'] = username

        return render_template('main.html', is_login=is_login, avatar=avatar, username=username, url=url,user_id=user_id)

    is_login = False
    return render_template('index.html', is_login=is_login)


@app.route('/star/helloflask')
def star():
    github.put('user/starred/greyli/helloflask', headers={'Content-Length': '0'})
    flash('Star success.')
    return redirect(url_for('index'))


@github.access_token_getter
def token_getter():
    user = g.user
    if user is not None:
        return user.access_token


@app.route('/callback/github')
@github.authorized_handler
def authorized(access_token):
    if access_token is None:
        flash('Login failed.')
        return redirect(url_for('index'))

    print(access_token)
    response = github.get('user', access_token=access_token)
    username = response['login']  # get username
    user_id = response['id']

    print(username)
    user = User.query.filter_by(username=username).first()

    if user is None:
        user = User(username=username, access_token=access_token, user_id=user_id)
        db.session.add(user)
    user.access_token = access_token  # update access token
    db.session.commit()
    flash('Login success.')

    user_info_request_url = "https://api.github.com/user"
    headers = {"Authorization": f"token {access_token}"}
    user_response = requests.get(user_info_request_url, headers=headers)
    user_data = user_response.json()
    # Get user ID from user data
    github_user_id = user_data["id"]
    session['user_id'] = github_user_id

    print(github_user_id)

    user = dbutil.get_user_by_github_username(db_file, username)
    if user is None:
        dbutil.add_user(db_file=db_file, github_username=username, github_user_id=github_user_id)
        print("Successfully added")
    else:
        print("No need to add")
    return redirect(url_for('main_page'))


@app.route('/login')
def login():
    if session.get('user_id', None) is None:
        return github.authorize(scope='repo')
    flash('Already logged in.')

    return redirect(url_for('main_page'))


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Goodbye.')
    return redirect(url_for('index'))


@app.route('/user')
def get_user():
    return jsonify(github.get('user'))


@app.route('/main')
def main_page():
    return render_template('main.html')


# Get all movies
@app.route("/api/movies", methods=["GET"])
def get_movies():
    movies = dbutil.get_all_movies("example.db")
    # print(movies)
    return jsonify(movies)


# Add favorite movie
@app.route("/api/movies/<int:movie_id>/favorite", methods=["POST"])
def favorite_movie(movie_id):
    # Get user ID, assuming the user is logged in, get the user ID from the frontend request
    github_user_id = session['user_id']
    print(dbutil.get_favorite_movies_by_user("example.db", github_user_id))
    # Check if the user has already favorited the movie
    if dbutil.get_favorite_movies_by_user("example.db", github_user_id):
        return jsonify({"message": "You have already favorited this movie!"}), 400  # Return 400 status code for bad request

    # Add favorite
    dbutil.add_favorite_movie("example.db", github_user_id, movie_id)

    return jsonify({"message": "Favorite added successfully!"})


# # Add route to get details of a single movie
# @app.route('/api/movies/<int:movie_id>', methods=['GET'])
# def get_movie_detail(movie_id):
#     movie_detail = dbutil.get_movie_detail("example.db", movie_id)
#     if movie_detail:
#         return jsonify(movie_detail), 200
#     else:
#         return jsonify({'message': 'Movie not found'}), 404

# Add route to get movie comments
@app.route('/api/movies/<int:movie_id>/comments', methods=['GET'])
def get_movie_comments(movie_id):
    comments = dbutil.get_movie_comments("example.db", movie_id)
    return jsonify(comments)


@app.route('/movie_detail/<int:movie_id>')
def movie_detail(movie_id):
    movie = dbutil.get_movie_detail(db_file, movie_id)
    if movie:
        comments = dbutil.get_movie_comments(db_file, movie_id)

        # Store movie details and comments in the session
        print(movie)
        session['movie'] = movie
        session['comments'] = comments

        return render_template('movie_detail.html')
    else:
        return "Movie not found", 404

# Add route to add movie comments
@app.route('/api/movies/<int:movie_id>/comments', methods=['POST'])
def add_movie_comment(movie_id):
    # Check if the user is logged in
    g.user = User.query.filter_by(user_id=session['user_id']).first()
    print(User.query.filter_by(user_id=session['user_id']).first())

    print(g.user)
    if g.user is None:
        return jsonify({"error": "Please log in first"}), 401

    # Get the comment content
    comment_text = request.json.get('comment', '').strip()

    # Ensure the comment content is not empty
    if not comment_text:
        return jsonify({"error": "Comment content cannot be empty"}), 400

    # Get GitHub user ID from the current user
    github_user_id = session['user_id']

    # Save the comment to the database
    dbutil.add_movie_comment(db_file, github_user_id, movie_id, comment_text)

    return jsonify({"message": "Comment successfully added"}), 201

# Add route in app.py to display favorite movies page
@app.route('/favorite_movies')
def favorite_movies():
    # Get current user information
    username = session.get('username')
    user_id = session.get('user_id')

    # Render the template and pass current user information to the template
    return render_template('favorite_movies.html', username=username, user_id=user_id)



# Get the list of movies favorited by the user
@app.route("/api/favorite_movies", methods=["GET"])
def get_favorite_movies():
    # Get GitHub user ID of the current user
    github_user_id = session['user_id']

    # Query the list of favorite movies using this user ID
    favorite_movies = dbutil.get_favorite_movies_by_user("example.db", github_user_id)
    # Return the list of favorite movies
    return jsonify(favorite_movies)


# Unfavorite a movie
@app.route("/api/favorite_movies/<int:movie_id>", methods=["DELETE"])
def unfavorite_movie(movie_id):
    # Get GitHub user ID of the current user
    github_user_id = session['user_id']

    # Check if the user has favorited the movie
    if dbutil.check_favorite_movie("example.db", github_user_id,movie_id):
        # Unfavorite the movie
        dbutil.remove_favorite_movie("example.db", github_user_id, movie_id)
        return jsonify({"message": "Unfavorited successfully!"}), 200
    else:
        return jsonify({"error": "Favorite movie not found!"}), 404


# Route to get movies by category
@app.route('/api/movies/category/<category>', methods=['GET'])
def get_movies_by_category(category):
    movies = dbutil.get_movies_by_category(db_file='example.db', category=category)
    return jsonify(movies)


# Route to handle keyword search
@app.route('/api/movies/search/<keyword>')
def search_by_keyword(keyword):
    movies = dbutil.get_movies_by_keyword('example.db',keyword.lower())
    return jsonify(movies)


if __name__ == '__main__':
    app.run(debug=True)
