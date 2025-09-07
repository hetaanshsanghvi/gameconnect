# GameHub Connect

GameHub Connect is an online game discovery and bookmarking platform. It aggregates game details from various sources, allowing users to browse, search, and save their favorite games. Users can view game details, bookmark games, and play them via external links.

## Features

- **Game Catalog:** Browse games with title, thumbnail, description, category, and tags.
- **Game Details:** View full game info, tags, and play via external link.
- **Favorites System:** Logged-in users can add/remove games from their favorites list.
- **Search & Filters:** Search by title, filter by category/tags, and sort by newest.
- **User Authentication:** Register, login, logout, and manage profile.
- **Admin Panel:** Add/edit/delete games, manage categories/tags.
- **Responsive Design:** Mobile-friendly layout using Bootstrap.

## Tech Stack

- **Backend:** Django (Python)
- **Frontend:** HTML, CSS (Bootstrap), JavaScript
- **Database:** SQLite (default, can be swapped for PostgreSQL/MySQL)
- **Authentication:** Django Auth

## Project Structure

```
manage.py
db.sqlite3
add_arcade_games.py
GameHub[1].txt
catalog/
    models.py
    views.py
    forms.py
    urls.py
    admin.py
    migrations/
    templatetags/
gamehub/
    settings.py
    urls.py
    wsgi.py
games/
    models.py
    views.py
media/
static/
    css/theme.css
    img/
templates/
    base.html
    catalog/
    registration/
```

## Setup Instructions

1. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

2. **Apply migrations:**
   ```sh
   python manage.py migrate
   ```

3. **Create a superuser (for admin access):**
   ```sh
   python manage.py createsuperuser
   ```

4. **Run the development server:**
   ```sh
   python manage.py runserver
   ```

5. **Access the app:**
   - Home: [http://localhost:8000/](http://localhost:8000/)
   - Admin: [http://localhost:8000/admin/](http://localhost:8000/admin/)

## Usage

- Browse games on the homepage.
- Register/login to save favorites.
- Use search and filters to find games.
- Admins can manage games and categories via the admin panel.

## License

This project is for educational/demo purposes.

---

For more details, see [GameHub[1].txt](GameHub[1].txt)