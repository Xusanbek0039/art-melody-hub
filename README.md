# 🎵 Art Melody Hub

🇺🇿 O'zbek milliy musiqa va san'at merosini zamonaviy raqamli platformasi

## 📖 Loyiha haqida

**Art Melody Hub** - O'zbekistonning milliy cholg'u asboblari, musiqiy merosi va san'atini o'rganish, rivojlantirish va targ'ib qilish uchun yaratilgan zamonaviy raqamli platforma. Platforma musiqachilar, ustozlar, talabalar va san'at ixlosmandlari uchun to'liq funktsional imkoniyatlarni taqdim etadi.

### 🎯 Asosiy vazifalar

- **Ta'lim**: Musiqa nazariyasi, notalar, mashqlar va testlar
- **Ijro**: Cholg'u asboblari bo'yicha ustozlar va ustaxonalar
- **Tanlovlar**: Respublika va xalqaro miqyosdagi musiqiy tanlovlar
- **Bozor**: Milliy cholg'u asboblari va aksessuarlar do'koni
- **Jamiyat**: Musiqachilar uchun ijtimoiy platforma va statistika

## 🏗️ Texnologik arxitektura

### 🖥️ Frontend (React + TypeScript)
- **Framework**: React 18.3.1 + TypeScript
- **UI Kit**: Radix UI + Tailwind CSS
- **Routing**: React Router DOM
- **State Management**: TanStack Query
- **Form Handling**: React Hook Form + Zod
- **Styling**: Tailwind CSS + shadcn/ui
- **Icons**: Lucide React
- **Charts**: Recharts
- **Build Tool**: Vite

### 🗄️ Backend (Django REST API)
- **Framework**: Django 4.2.7 + Django REST Framework 3.14.0
- **Database**: SQLite (development), PostgreSQL (production)
- **Authentication**: Token-based authentication
- **File Storage**: AWS S3 (production)
- **Payment**: Click, Payme integration
- **Task Queue**: Celery + Redis
- **API Documentation**: Django REST Framework

## 📁 Proyekt tuzilishi

```
art-melody-hub/
├── frontend/                 # React frontend ilovasi
│   ├── src/
│   │   ├── components/       # UI komponentlar
│   │   ├── pages/           # Sahifalar
│   │   ├── hooks/           # Custom hooklar
│   │   ├── lib/             # Kutubxonalar
│   │   └── assets/          # Statik fayllar
│   ├── public/              # Publik fayllar
│   ├── package.json
│   └── vite.config.ts
├── backend/                 # Django REST API
│   ├── art_melody_hub/      # Asosiy sozlamalar
│   ├── accounts/            # Foydalanuvchilar
│   ├── notes/               # Notalar kutubxonasi
│   ├── instruments/         # Cholg'u ustalari
│   ├── competitions/        # Musiqiy tanlovlar
│   ├── market/              # Do'kon
│   ├── theory/              # Musiqa nazariyasi
│   ├── statistics/          # Statistika
│   └── requirements.txt
└── README.md
```

## 🚀 Boshlash

### 📋 Talablar

- Node.js 18+
- Python 3.9+
- Git

### 🔧 Frontend sozlamalari

```bash
# Frontend papkasiga o'tish
cd frontend

# Dependency'larni o'rnatish
npm install

# Development serverni ishga tushirish
npm run dev

# Build qilish
npm run build
```

### 🐍 Backend sozlamalari

```bash
# Backend papkasiga o'tish
cd backend

# Virtual environment yaratish
python -m venv venv

# Virtual environmentni faollashtirish
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Dependency'larni o'rnatish
pip install -r requirements.txt

# Ma'lumotlar bazasini sozlash
python manage.py makemigrations
python manage.py migrate

# Superuser yaratish
python manage.py createsuperuser

# Serverni ishga tushirish
python manage.py runserver
```

## 🌐 API Endpoint'lari

### 🔐 Autentifikatsiya
- `POST /api/auth/register/` - Ro'yxatdan o'tish
- `POST /api/auth/login/` - Tizimga kirish
- `POST /api/auth/logout/` - Chiqish
- `GET /api/auth/profile/` - Profil ma'lumotlari

### 🎼 Notalar
- `GET /api/notes/` - Notalar ro'yxati
- `GET /api/notes/{id}/` - Nota tafsilotlari
- `POST /api/notes/{id}/rate/` - Notani baholash
- `POST /api/notes/{id}/download/` - Notani yuklab olish

### 🎻 Cholg'u ustalari
- `GET /api/instruments/masters/` - Ustalar ro'yxati
- `GET /api/instruments/masters/{id}/` - Usta profili
- `POST /api/instruments/masters/{id}/review/` - Ustani baholash

### 🏆 Tanlovlar
- `GET /api/competitions/` - Tanlovlar ro'yxati
- `POST /api/competitions/register/{id}/` - Tanlovga ro'yxatdan o'tish
- `GET /api/competitions/my-registrations/` - Mening ro'yxatlarim

### 🛒 Do'kon
- `GET /api/market/` - Mahsulotlar ro'yxati
- `POST /api/market/cart/add/` - Savatga qo'shish
- `POST /api/market/orders/create/` - Buyurtma berish

### 📚 Musiqa nazariyasi
- `GET /api/theory/topics/` - Nazariy mavzular
- `GET /api/theory/tests/` - Testlar
- `POST /api/theory/tests/{id}/submit/` - Testni topshirish

### 📊 Statistika
- `GET /api/statistics/user/` - Foydalanuvchi statistikasi
- `GET /api/statistics/dashboard/` - Admin dashboard

## 🎨 Asosiy funktsiyalar

### 👤 Foydalanuvchi profili
- Shaxsiy ma'lumotlar
- Yutuqlar va medallar
- Amaliyot statistikasi
- Tanlovdagi ishtirok

### 📖 Notalar kutubxonasi
- PDF va audio fayllar
- Kategoriyalar bo'yicha filtrlash
- Baholash tizimi
- Yuklab olish statistikasi

### 🎯 Musiqa nazariyasi
- Interaktiv testlar
- Darajalarga bo'linish
- Progress tracking
- Video va audio resurslar

### 🏪 Onlayn do'kon
- Cholg'u asboblari
- To'lov tizimlari (Click, Payme)
- Yetkazib berish xizmati
- Mahsulot baholash

### 🎪 Musiqiy tanlovlar
- Onlayn ro'yxatdan o'tish
- Natijalarni e'lon qilish
- Sertifikatlar
- Jadval va yangiliklar

## 🔧 Konfiguratsiya

### Environment o'zgaruvchilar

Frontend (`.env.local`):
```env
VITE_API_BASE_URL=http://localhost:8000/api
VITE_APP_NAME=Art Melody Hub
```

Backend (`.env`):
```env
SECRET_KEY=your-secret-key
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3
CORS_ALLOWED_ORIGINS=http://localhost:3000
```

## 🚀 Deployment

### Frontend (Vercel/Netlify)
```bash
npm run build
# Build qilingan fayllarni hosting platformasiga yuklang
```

### Backend (Heroku/DigitalOcean)
```bash
# Production environment sozlamalari
pip install -r requirements.txt
python manage.py collectstatic
python manage.py migrate
gunicorn art_melody_hub.wsgi:application
```

## 🤝 Hamkorlik

Loyihaga hissa qo'shish istagida bo'lsangiz:

1. Repozitoriyani fork qiling
2. Feature branch yarating: `git checkout -b feature/amazing-feature`
3. O'zgarishlarni qo'shing: `git commit -m 'Add amazing feature'`
4. Push qiling: `git push origin feature/amazing-feature`
5. Pull request yarating

## 📄 Litsenziya

Bu loyiha MIT litsenziyasi ostida tarqatiladi.

## 📞 Aloqa

Loyiha haqida savollaringiz bo'lsa yoki hamkorlik uchun:

- 📧 Email: info@artmelodyhub.uz
- 🌐 Web: www.artmelodyhub.uz
- 📱 Telegram: @artmelodyhub

---

**Art Melody Hub** - O'zbek milliy san'atining raqamli maskani 🎵
