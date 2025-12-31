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

movie_recommendation/
├── app.py
├── app.db
├── requirements.txt
├── .gitignore
└── templates/
    ├── base.html
    ├── index.html
    ├── login.html
    ├── register.html
    ├── results.html
    ├── anime_results.html
    └── watchlist.html

---

## ⚙️ Setup & Installation

### 1️⃣ Prerequisites
- Python 3.x
- A TMDb API Key

---

### 2️⃣ Clone the Repository

git clone <your-repo-url>  
cd movie_recommendation

---

### 3️⃣ Install Dependencies

python -m venv venv  
source venv/bin/activate  
pip install -r requirements.txt

---

### 4️⃣ Configuration

export TMDB_API_KEY='your_api_key_here'

⚠️ Update the SECRET_KEY in app.py for production.

---

### 5️⃣ Run the Application

python app.py

App runs at: http://127.0.0.1:5000/

---

## 🖥️ Usage

- Search movies or TV shows from the home page
- Browse or search anime
- Register/login to save items to your watchlist
- View recommendations using "View Similar"

---

## 📜 License

This project is for educational and personal use.

---

Happy coding 🚀
