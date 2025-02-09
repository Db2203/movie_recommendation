import os
import requests
from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

###############################################################################
# Configuration & Setup
###############################################################################
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(BASE_DIR, 'app.db')

app = Flask(__name__)

# IMPORTANT: Replace with a secure random key in production!
app.config['SECRET_KEY'] = 'CHANGE_THIS_TO_SOMETHING_RANDOM'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Replace with your actual TMDb API key or use an environment variable
TMDB_API_KEY = os.getenv("TMDB_API_KEY")
if not TMDB_API_KEY:
    raise ValueError("TMDB_API_KEY is not set in .env or environment variables")
TMDB_BASE_URL = "https://api.themoviedb.org/3"
IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500"

# Jikan (MyAnimeList) base URL
JIKAN_BASE_URL = "https://api.jikan.moe/v4"

# Global dicts to store genres
movie_genres = {}  # {genre_id: genre_name}
tv_genres = {}     # {genre_id: genre_name}
anime_genres = {}  # {mal_id: genre_name}

###############################################################################
# Database Models
###############################################################################
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    # Relationship backref
    watchlist_items = db.relationship('WatchlistItem', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class WatchlistItem(db.Model):
    __tablename__ = 'watchlist_items'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    media_type = db.Column(db.String(20), nullable=False)  # "movie", "tv", or "anime"
    item_id = db.Column(db.Integer, nullable=False)         # TMDb or MAL ID
    title = db.Column(db.String(200), nullable=False)
    poster_url = db.Column(db.String(300))                  # optional poster image

###############################################################################
# Fetch Genres from TMDb & Jikan
###############################################################################
def fetch_genres():
    """
    Fetch movie & TV genres from TMDb, and anime genres from Jikan.
    Store them in global dictionaries.
    """
    global movie_genres, tv_genres, anime_genres

    # ------ TMDb: Movie Genres ------
    movie_url = f"{TMDB_BASE_URL}/genre/movie/list"
    m_params = {"api_key": TMDB_API_KEY, "language": "en-US"}
    m_res = requests.get(movie_url, params=m_params)
    m_data = m_res.json()
    if "genres" in m_data:
        movie_genres = {g["id"]: g["name"] for g in m_data["genres"]}

    # ------ TMDb: TV Genres ------
    tv_url = f"{TMDB_BASE_URL}/genre/tv/list"
    t_params = {"api_key": TMDB_API_KEY, "language": "en-US"}
    t_res = requests.get(tv_url, params=t_params)
    t_data = t_res.json()
    if "genres" in t_data:
        tv_genres = {g["id"]: g["name"] for g in t_data["genres"]}

    # ------ Jikan: Anime Genres ------
    anime_genre_url = f"{JIKAN_BASE_URL}/genres/anime"
    a_res = requests.get(anime_genre_url)
    a_data = a_res.json()
    if "data" in a_data:
        anime_genres = {
            genre["mal_id"]: genre["name"] for genre in a_data["data"]
        }

###############################################################################
# User Registration & Login Routes
###############################################################################
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        # Check if user/email already exists
        existing_user = User.query.filter(
            (User.username==username)|(User.email==email)
        ).first()
        if existing_user:
            return "Username or email already in use!"

        # Create new user
        new_user = User(username=username, email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            session['user_id'] = user.id
            session['username'] = user.username
            return redirect(url_for('home'))
        else:
            return "Invalid credentials!"

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    return redirect(url_for('home'))


###############################################################################
# Watchlist Routes
###############################################################################
@app.route('/add_to_watchlist', methods=['POST'])
def add_to_watchlist():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    media_type = request.form.get('media_type')
    item_id = request.form.get('item_id')
    title = request.form.get('title')
    poster_url = request.form.get('poster_url', '')

    # Check if already in watchlist
    existing = WatchlistItem.query.filter_by(
        user_id=user_id,
        media_type=media_type,
        item_id=item_id
    ).first()
    if existing:
        return "Item already in watchlist!"

    new_item = WatchlistItem(
        user_id=user_id,
        media_type=media_type,
        item_id=item_id,
        title=title,
        poster_url=poster_url
    )
    db.session.add(new_item)
    db.session.commit()
    return "Item added to watchlist!"


@app.route('/my_watchlist')
def my_watchlist():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    items = WatchlistItem.query.filter_by(user_id=user_id).all()
    return render_template('watchlist.html', items=items)


###############################################################################
# Movie/TV Routes (TMDb)
###############################################################################
@app.route('/')
def home():
    """
    Displays the home page with a form to search for movies/TV.
    """
    return render_template('index.html')


@app.route('/search', methods=['GET', 'POST'])
def search():
    """
    Searches for movies/TV shows via TMDb's /search/multi endpoint.
    """
    if request.method == 'POST':
        query = request.form.get('query', '').strip()
    else:
        query = request.args.get('query', '').strip()

    if not query:
        return render_template('results.html', results=[], query="")

    search_url = f"{TMDB_BASE_URL}/search/multi"
    params = {
        "api_key": TMDB_API_KEY,
        "query": query,
        "language": "en-US",
        "page": 1,
        "include_adult": "false"
    }
    response = requests.get(search_url, params=params)
    data = response.json()
    results = data.get('results', [])

    return render_template(
        'results.html',
        results=results,
        query=query,
        image_base_url=IMAGE_BASE_URL
    )


@app.route('/recommendations/<media_type>/<int:item_id>')
def recommendations(media_type, item_id):
    """
    Fetch recommended movies/TV from TMDb for the given item ID.
    """
    rec_url = f"{TMDB_BASE_URL}/{media_type}/{item_id}/recommendations"
    params = {
        "api_key": TMDB_API_KEY,
        "language": "en-US"
    }
    response = requests.get(rec_url, params=params)
    data = response.json()
    recommended_items = data.get('results', [])

    return render_template(
        'results.html',
        results=recommended_items,
        query="Recommendations",
        image_base_url=IMAGE_BASE_URL
    )


@app.route('/genres')
def genres_page():
    """
    Displays a page for picking a movie or TV genre (TMDb).
    """
    return render_template(
        'genre_select.html',
        movie_genres=movie_genres,
        tv_genres=tv_genres
    )


@app.route('/browse_by_genre')
def browse_by_genre():
    """
    Uses TMDb's /discover to list movies/TV by genre.
    """
    media_type = request.args.get('media_type', 'movie')
    genre_id = request.args.get('genre_id', '')

    if not genre_id:
        return "No genre selected!"

    discover_url = f"{TMDB_BASE_URL}/discover/{media_type}"
    params = {
        "api_key": TMDB_API_KEY,
        "language": "en-US",
        "sort_by": "popularity.desc",
        "with_genres": genre_id,
        "page": 1
    }
    response = requests.get(discover_url, params=params)
    data = response.json()
    results = data.get('results', [])

    chosen_genre_name = ""
    if media_type == 'movie' and int(genre_id) in movie_genres:
        chosen_genre_name = movie_genres[int(genre_id)]
    elif media_type == 'tv' and int(genre_id) in tv_genres:
        chosen_genre_name = tv_genres[int(genre_id)]

    return render_template(
        'results.html',
        results=results,
        query=f"Browsing {media_type.upper()} Genre: {chosen_genre_name}",
        image_base_url=IMAGE_BASE_URL
    )


###############################################################################
# Anime Routes (Jikan)
###############################################################################
@app.route('/anime/search', methods=['GET', 'POST'])
def search_anime():
    """
    Search for anime by keyword (e.g., "Naruto").
    """
    if request.method == 'POST':
        query = request.form.get('query', '').strip()
    else:
        query = request.args.get('query', '').strip()

    if not query:
        return render_template('anime_results.html', results=[], query="")

    anime_search_url = f"{JIKAN_BASE_URL}/anime"
    params = {
        "q": query,
        "order_by": "popularity",
        "sort": "desc",
        "limit": 20
    }
    response = requests.get(anime_search_url, params=params)
    data = response.json()
    results = data.get('data', [])

    return render_template(
        'anime_results.html',
        results=results,
        query=query
    )


@app.route('/anime/genres')
def anime_genres_page():
    """
    Show a page to pick an anime genre (Jikan).
    """
    return render_template(
        'anime_genre_select.html',
        anime_genres=anime_genres
    )


@app.route('/anime/browse_by_genre')
def browse_anime_by_genre():
    """
    Browse anime by chosen genre ID using Jikan's /anime endpoint.
    """
    genre_id = request.args.get('genre_id', '')
    if not genre_id:
        return "No anime genre selected!"

    anime_browse_url = f"{JIKAN_BASE_URL}/anime"
    params = {
        "genres": genre_id,
        "order_by": "popularity",
        "sort": "desc",
        "limit": 20
    }
    response = requests.get(anime_browse_url, params=params)
    data = response.json()
    results = data.get('data', [])

    chosen_genre_name = anime_genres.get(int(genre_id), "")

    return render_template(
        'anime_results.html',
        results=results,
        query=f"Browsing Anime Genre: {chosen_genre_name}"
    )


@app.route('/anime/recommendations/<int:mal_id>')
def anime_recommendations(mal_id):
    """
    Show recommended anime for a given MAL ID.
    """
    rec_url = f"{JIKAN_BASE_URL}/anime/{mal_id}/recommendations"
    response = requests.get(rec_url)
    data = response.json()
    recommended_items = data.get('data', [])

    return render_template(
        'anime_results.html',
        results=recommended_items,
        query="Anime Recommendations"
    )


###############################################################################
# Run the Flask App
###############################################################################
if __name__ == '__main__':
    # Fetch genres if you like (not strictly requiring app context)
    fetch_genres()

    # Create an application context before creating tables
    with app.app_context():
        db.create_all()  # Create tables if they don't exist

    # Finally, run your Flask app
    app.run(debug=True)
