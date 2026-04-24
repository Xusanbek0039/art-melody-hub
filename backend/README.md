# Art Melody Hub Backend

Django REST API backend for the Art Melody Hub platform - a comprehensive music education and marketplace for Uzbek traditional instruments.

## Features

- **User Authentication & Profiles**: Custom user model with extended profiles, achievements, and competition participation tracking
- **Notes Library**: Musical notes with PDF/audio files, ratings, progress tracking, and practice sessions
- **Instrument Masters**: Directory of instrument craftsmen with portfolios, reviews, and consultation requests
- **Competitions**: Music competition management with registrations, results, and schedules
- **Marketplace**: E-commerce platform for instruments and accessories with cart, orders, and payment integration
- **Music Theory**: Educational content with tests, levels, and progress tracking
- **Statistics & Analytics**: Comprehensive analytics for users and administrators

## Tech Stack

- **Backend**: Django 4.2.7, Django REST Framework 3.14.0
- **Database**: SQLite (development), PostgreSQL (production)
- **Authentication**: Django's built-in auth with token-based API authentication
- **File Storage**: Local storage (development), AWS S3 (production)
- **Payment**: Click, Payme integration
- **Task Queue**: Celery with Redis

## Project Structure

```
backend/
├── manage.py
├── art_melody_hub/          # Main project settings
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── accounts/                # User management
│   ├── models.py           # User, Profile, Achievement models
│   ├── serializers.py      # API serializers
│   ├── views.py            # API views
│   ├── urls.py             # URL routing
│   └── admin.py            # Django admin
├── notes/                  # Musical notes library
│   ├── models.py           # Note, Category, Rating models
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── admin.py
├── instruments/            # Instrument masters
│   ├── models.py           # Master, Review, Work models
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── admin.py
├── competitions/           # Music competitions
│   ├── models.py           # Competition, Registration, Result models
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── admin.py
├── market/                 # E-commerce marketplace
│   ├── models.py           # Product, Order, Cart models
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── admin.py
├── theory/                 # Music theory education
│   ├── models.py           # TheoryTopic, Test, Question models
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── admin.py
├── statistics/             # Analytics and reporting
│   ├── models.py           # Activity, Stats, Analytics models
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── admin.py
├── requirements.txt
└── README.md
```

## API Endpoints

### Authentication
- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - User login
- `POST /api/auth/logout/` - User logout
- `GET /api/auth/profile/` - Get user profile
- `PUT /api/auth/profile/` - Update user profile

### Notes
- `GET /api/notes/` - List notes
- `POST /api/notes/` - Create note (admin)
- `GET /api/notes/{id}/` - Get note details
- `POST /api/notes/{id}/rate/` - Rate a note
- `POST /api/notes/{id}/download/` - Download note

### Instruments
- `GET /api/instruments/masters/` - List instrument masters
- `POST /api/instruments/masters/` - Create master profile
- `GET /api/instruments/masters/{id}/` - Get master details
- `POST /api/instruments/masters/{id}/review/` - Review a master

### Competitions
- `GET /api/competitions/` - List competitions
- `POST /api/competitions/` - Create competition (admin)
- `GET /api/competitions/{id}/` - Get competition details
- `POST /api/competitions/register/{id}/` - Register for competition

### Market
- `GET /api/market/` - List products
- `POST /api/market/` - Create product (master)
- `GET /api/market/{id}/` - Get product details
- `POST /api/market/cart/add/` - Add to cart
- `POST /api/market/orders/create/` - Create order

### Theory
- `GET /api/theory/topics/` - List theory topics
- `GET /api/theory/tests/` - List theory tests
- `POST /api/theory/tests/{id}/submit/` - Submit test answers

### Statistics
- `GET /api/statistics/dashboard/` - Dashboard stats (admin)
- `GET /api/statistics/user/` - User statistics
- `POST /api/statistics/track/` - Track user activity

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd art-melody-hub/backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment setup**
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

5. **Database migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run development server**
   ```bash
   python manage.py runserver
   ```

## Environment Variables

Create a `.env` file in the root directory:

```env
# Django settings
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DATABASE_URL=sqlite:///db.sqlite3

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173

# File storage (AWS S3)
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_STORAGE_BUCKET_NAME=your-bucket-name
AWS_S3_REGION_NAME=your-region

# Redis (for Celery)
REDIS_URL=redis://localhost:6379/0

# Payment providers
CLICK_API_KEY=your-click-api-key
PAYME_API_KEY=your-payme-api-key
```

## Database Setup

### Development (SQLite)
The project uses SQLite by default for development. The database file will be created automatically.

### Production (PostgreSQL)
1. Install PostgreSQL
2. Create database:
   ```sql
   CREATE DATABASE art_melody_hub;
   CREATE USER art_melody_user WITH PASSWORD 'your-password';
   GRANT ALL PRIVILEGES ON DATABASE art_melody_hub TO art_melody_user;
   ```
3. Update `DATABASE_URL` in `.env`
4. Run migrations

## API Documentation

The API uses Django REST Framework with token authentication. Include the token in your requests:

```bash
curl -H "Authorization: Token your-token-here" http://localhost:8000/api/auth/profile/
```

## Testing

Run the test suite:

```bash
python manage.py test
```

Run tests for a specific app:

```bash
python manage.py test accounts
```

## Deployment

### Using Docker
```bash
docker build -t art-melody-hub-backend .
docker run -p 8000:8000 art-melody-hub-backend
```

### Using Gunicorn (Production)
```bash
pip install gunicorn
gunicorn art_melody_hub.wsgi:application --bind 0.0.0.0:8000
```

## Admin Panel

Access the Django admin panel at `http://localhost:8000/admin/` with your superuser credentials.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For support and questions, please contact the development team.
