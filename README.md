# GitHub-Login
Example application for login with GitHub by GitHub-Flask

## Online Demo
https://helloflask.pythonanywhere.com

## Installation

```
$ git clone https://github.com/helloflask/github-login
$ cd github-login
```

## Register Your OAuth Application on GitHub

Go to https://github.com/settings/applications/new

Fill the form, then you will get your Client ID and Client Secret, write them into
app.py:

```python
app.config['GITHUB_CLIENT_ID'] = 'your_client_id'
app.config['GITHUB_CLIENT_SECRET'] = 'your_clent_secret'

```
*Warning: You normally need to save this values as enviroment variable in production.*

## Run

Just excute:
```
$ flask run
```
Then go to http://localhost:5000


# For Readers of Hello, Flask!

Online Demo
https://youtu.be/JfAtAOXURyQ

Overview The Movie Explorer Website is a web-based platform designed to assist users in finding, reviewing, and engaging with movies across various genres. Users can search for movies by category, leave comments, and add films to a personalized favorites list.

Objectives User Engagement: Enhance the browsing experience by providing an interactive and user-friendly interface. Database Integration: Use a database to manage movie data, user profiles, comments, and favorites. Social Interaction: Allow users to comment on movies and share their opinions within the community. Personalization: Enable users to curate their favorite movies in a personalized list for easy access.

Features Search Functionality Users can search for movies based on categories such as Action, Comedy, Drama, etc. Advanced search options to filter by year, rating, or director. User Comments and Ratings Registered users can post comments on movie pages. Users can rate movies, influencing the overall movie rating displayed. Favorites List Users can add movies to their favorites list. Easy management of the list with options to add or remove movies.

Technical Specifications Database (SQLite) Stores data about movies, user accounts, comments, and favorites. Facilitates quick retrieval and updates of movie information and user data. Back-End Development (Flask Framework & Python) Flask will serve as the web framework to handle requests and serve responses. Python used for server-side logic and interaction with the SQLite database. Front-End Development (HTML, CSS, JavaScript) HTML and CSS for structuring and styling the web pages. JavaScript for interactive elements and asynchronous data fetching. API Integration Integrate with external movie databases (like IMDb API) to fetch detailed descriptions, reviews, and ratings. Third-Party Authentication (Flask-OAuth) Implement OAuth for secure login processes. Allow users to sign in using Google or Facebook for a simplified login experience. Responsive Design Ensure the website is functional and aesthetically pleasing on both desktop and mobile devices.

Project Structure app.py: Main application file where Flask routes are defined. dbutil.py: Contains utility functions for database operations. data.db: Primary database file. example.db: Example or template database. templates/: Folder containing HTML files for the website. static/: Directory for CSS, JavaScript, and image files. LICENSE: Project license file. README.md: Markdown file with project details, setup instructions, and usage. Pipfile: Lists project dependencies and Python packages.
