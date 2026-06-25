# 🏏 IPL 2026 — Django Web Application

A full-featured Indian Premier League web application built with Django, featuring match listings, team profiles, player statistics, fan comments, and email sharing.

---

## 📁 Project Structure

```
ipl_project/
├── manage.py
├── requirements.txt
├── setup.sh                        ← One-click setup script
│
├── ipl_project/                    ← Django project config
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
└── ipl/                            ← Main application
    ├── models.py                   ← Team, Player, Match, Comment
    ├── views.py                    ← All view logic
    ├── urls.py                     ← SEO-friendly URL patterns
    ├── forms.py                    ← CommentForm, ShareMatchForm
    ├── admin.py                    ← Admin panel config
    ├── management/
    │   └── commands/
    │       └── populate_ipl_data.py ← Sample data seeder
    └── templates/ipl/
        ├── base.html               ← Common layout & styles
        ├── match_list.html         ← Paginated match list
        ├── match_detail.html       ← Match + comments + squads
        ├── share_match.html        ← Email share form
        ├── team_list.html          ← All franchises
        ├── team_detail.html        ← Team + players by role
        └── player_list.html        ← Filtered/paginated players
```

---

## ⚡ Quick Start

### Option A — Automated Setup (recommended)
```bash
git clone <repo>
cd ipl_project
chmod +x setup.sh
./setup.sh
```

### Option B — Manual Setup
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Database
python manage.py makemigrations ipl
python manage.py migrate

# Seed sample data (10 teams, 100+ players, 70 matches)
python manage.py populate_ipl_data

# Create admin user
python manage.py createsuperuser

# Run server
python manage.py runserver
```

---

## 🌐 URLs

| URL | View | Description |
|-----|------|-------------|
| `/` | match_list | All IPL matches (paginated, 5/page) |
| `/matches/` | match_list | Same as above |
| `/matches/<slug>/` | match_detail | Single match + comments |
| `/matches/<slug>/comment/` | add_comment | POST — add fan comment |
| `/matches/<slug>/share/` | share_match | Email sharing form |
| `/teams/` | team_list | All 10 franchises |
| `/teams/<slug>/` | team_detail | Team + squad by role |
| `/players/` | player_list | All players (filter by team/role) |
| `/admin/` | Django Admin | Full CMS |

---

## 🗄️ Models

### Team
| Field | Type | Notes |
|-------|------|-------|
| name | CharField | Unique |
| slug | SlugField | Auto-generated, SEO URL |
| logo | ImageField | Optional upload |
| description | TextField | About the team |
| city | CharField | Home city |
| home_ground | CharField | Stadium name |
| color | CharField | Hex color (#RRGGBB) |

### Player
| Field | Type | Notes |
|-------|------|-------|
| name | CharField | |
| team | ForeignKey → Team | |
| role | CharField | Batsman / Bowler / All-rounder / Wicketkeeper |
| runs | IntegerField | Career IPL runs |
| wickets | IntegerField | Career IPL wickets |
| matches_played | IntegerField | |
| nationality | CharField | Default: Indian |
| photo | ImageField | Optional |

### Match
| Field | Type | Notes |
|-------|------|-------|
| title | CharField | e.g. "MI vs CSK — Match 1" |
| slug | SlugField | Auto, unique, SEO URL |
| team1 | ForeignKey → Team | Home team |
| team2 | ForeignKey → Team | Away team |
| match_date | DateTimeField | |
| venue | CharField | Stadium, City |
| result | TextField | e.g. "MI won by 6 wickets" |
| status | CharField | Upcoming / Live / Completed |
| match_number | IntegerField | |

### Comment
| Field | Type | Notes |
|-------|------|-------|
| match | ForeignKey → Match | |
| name | CharField | Commenter name |
| email | EmailField | |
| comment | TextField | |
| created_date | DateTimeField | Auto |
| active | BooleanField | Admin moderation |

---

## ✨ Features

### ✅ Implemented
- **Match List** — paginated 5/page, filter by Upcoming/Live/Completed
- **Match Detail** — full info, both team squads in sidebar
- **Comments** — post + display fan comments with moderation
- **Share via Email** — send match details to friend's email
- **Team List** — all 10 franchises with stats
- **Team Detail** — squad grouped by role (Batsman/Bowler/All-rounder/WK)
- **Player List** — filter by team & role, paginated 10/page
- **SEO URLs** — all routes use human-readable slugs
- **Admin Panel** — full CRUD with approve/reject comments
- **Sample Data** — 10 teams, 120+ players, 70 matches pre-seeded

### 🎨 Design
- Dark navy/gold cricket theme with `Bebas Neue` + `Rajdhani` fonts
- Animated live match badges, pulsing logo, staggered page animations
- Fully responsive layout
- Status badges: Upcoming (gold), Live (red pulse), Completed (green)

---

## 📧 Email Configuration

By default, emails print to the **console** (no SMTP needed for development).

For production, update `settings.py`:
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
```

---

## 🔧 Admin Panel

- URL: `http://127.0.0.1:8000/admin/`
- Default credentials: `admin` / `admin123`
- Features: Add/edit teams, players, matches; approve/reject comments

---

## 📦 Dependencies

```
Django>=4.2,<5.0
Pillow>=10.0        # For ImageField (logo/photo uploads)
```
