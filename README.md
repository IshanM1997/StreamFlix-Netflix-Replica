# 🎬 StreamFlix — Netflix Replica

A full-stack Netflix clone built with **Django REST Framework** (Python backend) and **Angular 17 + Angular Material** (frontend).

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Django 4.2, Django REST Framework, SimpleJWT |
| Database | SQLite (dev) — swappable to PostgreSQL |
| Frontend | Angular 17, Angular Material, RxJS |
| Auth | JWT (access token 7d, refresh 30d) |
| Styling | SCSS + Angular Material dark theme |

---

## Features

| Feature | Details |
|---|---|
| **Auth** | Register / Login with JWT, persistent sessions |
| **Hero banner** | Featured movie with play + info actions |
| **Movie rows** | Horizontal scroll rails — Trending, Top 10, New Releases, by genre |
| **Movie cards** | Hover-expand with play, add-to-list, rate actions |
| **Movie modal** | Full detail dialog — cast, genres, rating, director, IMDb |
| **Video player** | Custom controls — play/pause, seek, volume, skip ±10s, fullscreen, progress saving |
| **Search** | Debounced search (350ms) across title, cast, genres, director |
| **My List** | Add/remove movies, persisted per user |
| **Continue Watching** | Resumes from last saved position |
| **Top 10** | Numbered rank badges on cards |
| **Responsive** | Works on mobile, tablet, desktop |

---

## Project Structure

```
streamflix/
├── backend/
│   ├── manage.py
│   ├── requirements.txt
│   ├── streamflix/          ← Django project (settings, urls, wsgi)
│   ├── movies/              ← Movie model, views, serializers, seed command
│   ├── users/               ← Custom User, WatchProgress, MyList
│   └── api/                 ← Central URL router
│
└── frontend/
    ├── angular.json
    ├── package.json
    ├── proxy.conf.json       ← Dev proxy → Django :8000
    └── src/app/
        ├── core/
        │   ├── guards/       ← authGuard, guestGuard
        │   ├── interceptors/ ← authInterceptor (JWT header)
        │   └── services/     ← AuthService, MovieService
        ├── features/
        │   ├── auth/         ← Login, Signup
        │   ├── browse/       ← Home page
        │   ├── player/       ← Video player
        │   ├── search/       ← Search page
        │   └── my-list/      ← My List page
        └── shared/
            ├── components/   ← Navbar, Hero, MovieRow, MovieCard, MovieModal
            └── models/       ← TypeScript interfaces
```

---

## Setup

### 1. Backend

```bash
cd streamflix/backend

# Create virtual environment
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Seed the database (40+ movies + demo user)
python manage.py seed_data

# Start Django server
python manage.py runserver
# → http://localhost:8000
```

**Demo credentials:**
- Email: `demo@streamflix.com`
- Password: `demo1234`

### 2. Frontend

```bash
cd streamflix/frontend

# Install dependencies
npm install

# Start Angular dev server (with Django proxy)
npm start
# → http://localhost:4200
```

The Angular dev server automatically proxies `/api/*` requests to `http://localhost:8000`.

---

## API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| POST | `/api/auth/register/` | — | Register new user |
| POST | `/api/auth/login/` | — | Login, get JWT |
| POST | `/api/auth/refresh/` | — | Refresh access token |
| GET | `/api/auth/me/` | ✓ | Current user profile |
| GET | `/api/movies/featured/` | ✓ | Hero banner movie |
| GET | `/api/movies/home-rows/` | ✓ | All home page rows |
| GET | `/api/movies/trending/` | ✓ | Trending movies |
| GET | `/api/movies/top-10/` | ✓ | Top 10 ranked |
| GET | `/api/movies/new-releases/` | ✓ | New releases |
| GET | `/api/movies/genre/<name>/` | ✓ | Movies by genre |
| GET | `/api/movies/search/?q=...` | ✓ | Full-text search |
| GET | `/api/movies/<id>/` | ✓ | Movie detail |
| GET | `/api/my-list/` | ✓ | User's list |
| POST | `/api/my-list/<id>/` | ✓ | Add to list |
| DELETE | `/api/my-list/<id>/` | ✓ | Remove from list |
| GET | `/api/continue-watching/` | ✓ | In-progress movies |
| POST | `/api/watch-progress/<id>/` | ✓ | Save position |

---

## Django Admin

```bash
python manage.py createsuperuser
# Visit http://localhost:8000/admin
```

---

## Production notes

- Set `SECRET_KEY` and `DEBUG=False` in environment
- Replace SQLite with PostgreSQL via `DATABASE_URL`
- Serve Angular build via nginx or whitenoise
- Use proper video CDN (S3, Cloudflare Stream, Mux) instead of sample MP4
