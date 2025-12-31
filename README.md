# 🎬 Movie, TV & Anime Recommender

A full-stack **Flask web application** that allows users to search, browse, and receive personalized recommendations for **movies, TV shows, and anime**. The app integrates real-time data from external APIs and includes a secure authentication system with a private watchlist for each user.

---

## ✨ Features

- 🔍 **Multi-Platform Search**
  - Movies & TV Shows via **TMDb API**
  - Anime via **Jikan (MyAnimeList) API**

- 🧭 **Genre Browsing**
  - Discover movies, TV shows, and anime by genre

- 🤖 **Smart Recommendations**
  - Get similar or recommended titles based on selected content

- 🔐 **User Authentication**
  - Secure registration & login
  - Password hashing using `werkzeug.security`

- ⭐ **Personal Watchlist**
  - Save favorite movies, shows, and anime
  - Watchlists are private and user-specific

- 🎨 **Responsive UI**
  - Clean and centralized interface using **Jinja2** and **CSS**

---

## 🛠️ Tech Stack

**Backend**
- Python
- Flask
- Flask-SQLAlchemy
- SQLite

**APIs**
- The Movie Database (TMDb)
- Jikan API (Unofficial MyAnimeList API)

**Frontend**
- HTML5
- CSS3
- Jinja2 Templates

---

## 📂 Project Structure

```text
movie_recommendation/
├── app.py                 # Main Flask application & routes
├── app.db                 # SQLite database (users & watchlists)
├── requirements.txt       # Project dependencies
├── .gitignore             # Git ignore rules
└── templates/
    ├── base.html          # Base layout template
    ├── index.html         # Home & search page
    ├── login.html         # User login page
    ├── register.html      # User registration page
    ├── results.html       # Movie & TV results
    ├── anime_results.html # Anime search results
    └── watchlist.html     # User watchlist page
```

---

## ⚙️ Setup & Installation

### 1️⃣ Prerequisites
- Python **3.x**
- A **TMDb API Key**

---

### 2️⃣ Clone the Repository

```bash
git clone <your-repo-url>
cd movie_recommendation
```

---

### 3️⃣ Install Dependencies

It is recommended to use a virtual environment:

```bash
python -m venv venv
source venv/bin/activate   # macOS / Linux
venv\Scripts\activate    # Windows
pip install -r requirements.txt
```

---

### 4️⃣ Configuration

Set your **TMDb API Key** as an environment variable:

**macOS / Linux**
```bash
export TMDB_API_KEY='your_api_key_here'
```

**Windows (Command Prompt)**
```bash
set TMDB_API_KEY=your_api_key_here
```

⚠️ **Note:** Update the `SECRET_KEY` in `app.py` for production environments.

---

### 5️⃣ Run the Application

```bash
python app.py
```

The app will be available at:  
👉 **http://127.0.0.1:5000/**

---

## 🖥️ Usage

- Search for movies or TV shows from the home page
- Browse or search anime using the Jikan API
- Register or log in to save items to your personal watchlist
- Click **"View Similar"** to get recommendations

---

## 📜 License

This project is intended for **educational and personal use**.  
All media data is provided by **TMDb** and **MyAnimeList (via Jikan API)**.

---

## 🙌 Acknowledgements

- TMDb API for movie and TV data
- Jikan API for anime data
- Flask & the open-source community

---
