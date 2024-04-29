import sqlite3


# Connect to the database
def connect_to_database(db_file):
    conn = sqlite3.connect(db_file)
    return conn


# Close the database connection
def close_connection(conn):
    conn.close()


# Query all users from the database
def get_all_users(db_file):
    conn = connect_to_database(db_file)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM User")
    users = cursor.fetchall()
    close_connection(conn)
    return users


# Query user by GitHub username
def get_user_by_github_username(db_file, github_username):
    conn = connect_to_database(db_file)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM User WHERE github_username = ?", (github_username,))
    user = cursor.fetchone()
    close_connection(conn)
    return user


# Add a new user
def add_user(db_file, github_username, github_user_id):
    conn = connect_to_database(db_file)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO User (github_username, github_user_id) VALUES (?, ?)",
                   (github_username, github_user_id))
    conn.commit()
    close_connection(conn)


# Delete a user
def delete_user(db_file, user_id):
    conn = connect_to_database(db_file)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM User WHERE id = ?", (user_id,))
    conn.commit()
    close_connection(conn)


# Query all movies
def get_all_movies(db_file):
    conn = connect_to_database(db_file)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Movie")
    movies = cursor.fetchall()
    close_connection(conn)
    return movies


# Query categories of a specific movie
def get_movie_categories(db_file, movie_id):
    conn = connect_to_database(db_file)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT Category.name FROM Category INNER JOIN Movie_Category ON Category.id = Movie_Category.category_id WHERE Movie_Category.movie_id = ?",
        (movie_id,))
    categories = cursor.fetchall()
    close_connection(conn)
    return categories


# Add a new movie
def add_movie(db_file, title, director, actors, release_date):
    conn = connect_to_database(db_file)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Movie (title, director, actors, release_date) VALUES (?, ?, ?, ?)",
                   (title, director, actors, release_date))
    conn.commit()
    close_connection(conn)


# Delete a movie
def delete_movie(db_file, movie_id):
    conn = connect_to_database(db_file)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Movie WHERE id = ?", (movie_id,))
    conn.commit()
    close_connection(conn)


# Query all movie categories
def get_all_categories(db_file):
    conn = connect_to_database(db_file)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Category")
    categories = cursor.fetchall()
    close_connection(conn)
    return categories


# Add a new movie category
def add_category(db_file, category_name):
    conn = connect_to_database(db_file)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Category (name) VALUES (?)", (category_name,))
    conn.commit()
    close_connection(conn)


# Delete a movie category
def delete_category(db_file, category_id):
    conn = connect_to_database(db_file)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Category WHERE id = ?", (category_id,))
    conn.commit()
    close_connection(conn)


# Query comments by user and movie
def get_reviews_by_user_and_movie(db_file, user_id, movie_id):
    conn = connect_to_database(db_file)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Movie_Review WHERE user_id = ? AND movie_id = ?", (user_id, movie_id))
    reviews = cursor.fetchall()
    close_connection(conn)
    return reviews


# Add movie review
def add_review(db_file, user_id, movie_id, rating, comment):
    conn = connect_to_database(db_file)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Movie_Review (user_id, movie_id, rating, comment) VALUES (?, ?, ?, ?)",
                   (user_id, movie_id, rating, comment))
    conn.commit()
    close_connection(conn)


# Delete movie review
def delete_review(db_file, review_id):
    conn = connect_to_database(db_file)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Movie_Review WHERE id = ?", (review_id,))
    conn.commit()
    close_connection(conn)


# Query movies favorited by user
def get_favorite_movies_by_user(db_file, github_user_id):
    conn = connect_to_database(db_file)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT Movie.* FROM Movie INNER JOIN User_Favorite_Movie ON Movie.id = User_Favorite_Movie.movie_id WHERE User_Favorite_Movie.github_user_id = ?",
        (github_user_id,))
    favorite_movies = cursor.fetchall()
    close_connection(conn)
    return favorite_movies


# Add movie to user's favorites
def add_favorite_movie(db_file, github_user_id, movie_id):
    conn = connect_to_database(db_file)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO User_Favorite_Movie (github_user_id, movie_id) VALUES (?, ?)",
                   (github_user_id, movie_id))
    conn.commit()
    close_connection(conn)


# Delete movie from user's favorites
def delete_favorite_movie(db_file, github_user_id, movie_id):
    conn = connect_to_database(db_file)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM User_Favorite_Movie WHERE github_user_id = ? AND movie_id = ?",
                   (github_user_id, movie_id))
    conn.commit()
    close_connection(conn)


# Get details of a single movie
def get_movie_detail(db_file, movie_id):
    conn = connect_to_database(db_file)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Movie WHERE id = ?", (movie_id,))
    movie_detail = cursor.fetchone()
    conn.close()
    if movie_detail:
        return {
            "id": movie_detail[0],
            "title": movie_detail[1],
            "director": movie_detail[2],
            "actors": movie_detail[3],
            "release_date": movie_detail[4],
            "img": movie_detail[5],
            "description": movie_detail[6]
        }
    else:
        return None


# Get movie comments
def get_movie_comments(db_file, movie_id):
    conn = connect_to_database(db_file)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Movie_Review WHERE movie_id = ?", (movie_id,))
    comments = cursor.fetchall()
    conn.close()
    return [{
        "id": comment[0],
        "github_user_id": comment[1],
        "movie_id": comment[2],
        "rating": comment[3],
        "comment": comment[4]
    } for comment in comments]


def add_movie_comment(db_file, github_user_id, movie_id, comment_text):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    try:
        # Insert comment data into the database
        cursor.execute("""
            INSERT INTO Movie_Review (github_user_id, movie_id, comment)
            VALUES (?, ?, ?)
        """, (github_user_id, movie_id, comment_text))

        # Commit the transaction
        conn.commit()
    except sqlite3.Error as e:
        # If there's an error, roll back the transaction
        conn.rollback()
        print("Error occurred while adding a comment:", e)
    finally:
        # Close the database connection
        conn.close()


def get_user_by_github_userid(db_file, github_user_id):
    """
    Query user information by GitHub user ID.

    Args:
    - db_file: Path to the SQLite database file.
    - github_user_id: GitHub user ID.

    Returns:
    - User information if found, otherwise None.
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM User WHERE github_user_id = ?", (github_user_id,))
        user = cursor.fetchone()
        return user
    except sqlite3.Error as e:
        print(f"Error: {e}")
        return None
    finally:
        if conn:
            conn.close()


def add_access_token(db_file, github_user_id, access_token):
    """
    Add or update user's access_token in the user table.

    Args:
    - db_file: Path to the SQLite database file.
    - github_user_id: GitHub user ID.
    - access_token: Access token to add or update.

    Returns:
    - True if added or updated successfully, False otherwise.
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO User (github_user_id, access_token)
            VALUES (?, ?)
            ON CONFLICT(github_user_id) DO UPDATE SET access_token=?
            """, (github_user_id, access_token, access_token))
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"Error adding or updating access_token: {e}")
        return False
    finally:
        if conn:
            conn.close()


def get_access_token(db_file, github_user_id):
    """
    Get access_token by GitHub user ID.

    Args:
    - db_file: Path to the SQLite database file.
    - github_user_id: GitHub user ID.

    Returns:
    - Access token if found for the user, otherwise None.
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        cursor.execute("SELECT access_token FROM User WHERE github_user_id=?", (github_user_id,))
        result = cursor.fetchone()
        if result:
            return result[0]
        else:
            return None
    except sqlite3.Error as e:
        print(f"Error getting access_token: {e}")
        return None
    finally:
        if conn:
            conn.close()


def remove_favorite_movie(db_file, github_user_id, movie_id):
    """
    Remove a movie from user's favorites.

    Args:
    - db_file: Path to the SQLite database file.
    - github_user_id: GitHub user ID.
    - movie_id: Movie ID.
    """
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM User_Favorite_Movie WHERE github_user_id=? AND movie_id=?", (github_user_id, movie_id))
    conn.commit()
    conn.close()


def check_favorite_movie(db_file, github_user_id, movie_id):
    """
    Check if a user has favorited a specific movie.

    Args:
    - db_file: Path to the SQLite database file.
    - github_user_id: GitHub user ID.
    - movie_id: Movie ID.

    Returns:
    - True if the user has favorited the movie, False otherwise.
    """
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM User_Favorite_Movie WHERE github_user_id=? AND movie_id=?",
                   (github_user_id, movie_id))
    result = cursor.fetchone()
    conn.close()
    return result is not None


def get_movies_by_category(db_file, category):
    conn = connect_to_database(db_file)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Movie WHERE category = ?", (category,))
    movies = cursor.fetchall()
    close_connection(conn)
    return movies


def get_movies_by_keyword(db_file, keyword):
    """Get movies from the database by keyword."""
    conn = connect_to_database(db_file)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Movie WHERE lower(title) LIKE ?", ('%' + keyword + '%',))
    movies = cursor.fetchall()
    close_connection(conn)
    return movies
