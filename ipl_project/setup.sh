#!/usr/bin/env bash
# ============================================================
#  IPL 2026 Django Project — One-shot Setup Script
#  Run this from inside the ipl_project/ folder:
#      chmod +x setup.sh && ./setup.sh
# ============================================================
set -e

echo ""
echo "🏏  IPL 2026 Django Project Setup"
echo "=================================="
echo ""

# 1. Create & activate virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# 2. Install dependencies
echo "📥 Installing dependencies..."
pip install --upgrade pip -q
pip install -r requirements.txt -q
echo "   ✓ Django & Pillow installed"

# 3. Run migrations
echo ""
echo "🗄️  Running database migrations..."
python manage.py makemigrations ipl
python manage.py migrate
echo "   ✓ Database ready (SQLite)"

# 4. Populate sample data
echo ""
echo "🌱 Seeding sample IPL 2026 data..."
python manage.py populate_ipl_data

# 5. Create superuser
echo ""
echo "👤 Creating admin superuser..."
echo "   Username: admin"
echo "   Password: admin123"
python manage.py shell -c "
from django.contrib.auth.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@ipl2026.com', 'admin123')
    print('   ✓ Superuser created')
else:
    print('   ✓ Superuser already exists')
"

# 6. Collect static files
echo ""
echo "📁 Setting up static files..."
mkdir -p staticfiles
python manage.py collectstatic --noinput -v 0 2>/dev/null || true
echo "   ✓ Done"

echo ""
echo "✅  Setup complete!"
echo ""
echo "🚀  Start the server:"
echo "    source venv/bin/activate"
echo "    python manage.py runserver"
echo ""
echo "🌐  Open in browser:"
echo "    http://127.0.0.1:8000/          ← Match List"
echo "    http://127.0.0.1:8000/teams/    ← Teams"
echo "    http://127.0.0.1:8000/players/  ← Players"
echo "    http://127.0.0.1:8000/admin/    ← Admin Panel (admin / admin123)"
echo ""
