# Pearl Online Store

Pearl Online Store is a Django-based e-commerce web application with user authentication, a modern responsive design, and essential e-commerce features.

## Features
- User authentication: Sign Up, Login, Logout, Password Reset
- Responsive Navbar with Logo, Search, Cart, Account dropdown (Profile, Orders, Wishlist)
- Responsive Footer with About, Help, Social Media
- Modern UI: floating labels, password visibility toggle, mobile-friendly

## Technologies
- Django, Python 3.11+
- HTML, CSS, Bootstrap 5, Bootstrap Icons
- SQLite (development)

## Installation
```bash
git clone https://github.com/yourusername/pearl-online-store.git
cd pearl-online-store
python -m venv venv
# Activate venv
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
