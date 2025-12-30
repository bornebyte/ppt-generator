# 🎯 Analytics & Tracking System - Quick Start

## What's New?

Your PPT Generator now includes **silent analytics tracking** to help you understand:
- 📊 How many people use your website
- 👥 Who they are (students, colleges)
- 📈 Usage trends and patterns
- ✅ Success rates and errors

**Important:** This is completely transparent to users - no changes to the frontend!

## Quick Setup

### 1. Install Dependencies

```bash
# Run the setup script
./setup_analytics.sh
```

Or manually:

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install packages
pip install -r requirements.txt
```

### 2. Configure Admin Access

Edit `.env` file:

```env
ADMIN_USERNAME=your_username
ADMIN_PASSWORD=your_secure_password
DATABASE_URL=sqlite:///pptgen.db
```

**⚠️ IMPORTANT:** Change the default credentials!

### 3. Run the Application

```bash
source venv/bin/activate  # If not already activated
python3 main.py
```

### 4. Access Admin Dashboard

Open browser: `http://localhost:5000/admin`

Login with your credentials to see:
- Total generations
- Success rates
- Student information
- College statistics
- Trend charts

## What Data is Tracked?

### Automatically Collected:
- ✅ Timestamp
- ✅ IP address
- ✅ Browser/device info
- ✅ File name
- ✅ Presentation title
- ✅ Number of slides
- ✅ Generation time
- ✅ Success/failure status

### From User Input (if provided):
- ✅ College/university name
- ✅ Student names and USN
- ✅ Course and semester
- ✅ Professor name
- ✅ Single vs group project

## Production Deployment

### Environment Variables

Set these on your hosting platform (Vercel, Heroku, etc.):

```env
DATABASE_URL=postgresql://user:pass@host:port/database
ADMIN_USERNAME=admin
ADMIN_PASSWORD=strong-password-here
SECRET_KEY=random-secret-key-for-sessions
```

### Database Options

**Local/Development:**
- SQLite (default) - automatic setup

**Production:**
- PostgreSQL (recommended)
- Vercel Postgres
- Supabase
- Neon
- Railway Postgres

### Vercel Setup

1. Add Vercel Postgres addon
2. Set environment variables in Vercel dashboard
3. Deploy normally

Database will auto-initialize on first request.

## Files Added

```
models.py                      # Database models
templates/admin_login.html     # Admin login page
templates/admin_dashboard.html # Analytics dashboard
ANALYTICS.md                   # Full documentation
setup_analytics.sh            # Setup script
.env.example                  # Updated with DB config
```

## Files Modified

```
main.py          # Added tracking + admin routes
requirements.txt # Added Flask-SQLAlchemy, psycopg2
.gitignore      # Added *.db files
```

## Admin Dashboard Features

### 📊 Overview Cards
- Total generations
- Success rate percentage
- Students tracked
- Average slides per PPT

### 📈 Trend Chart
- Daily generation counts (last 30 days)
- Visual timeline of usage

### 🏫 Top Colleges
- Most active institutions
- Generation counts per college

### 🕒 Recent Activity
- Latest 10 generations
- Full details including students
- Status and timing info

## Security Notes

1. **Change default credentials immediately**
2. **Use strong passwords** (12+ characters)
3. **Enable HTTPS** in production
4. **Keep SECRET_KEY secret**
5. **Regular database backups**

## Privacy & GDPR

The system tracks:
- IP addresses (for unique visitor count)
- Student information (when voluntarily provided)

For GDPR compliance:
- Add privacy policy
- Consider IP anonymization
- Implement data deletion on request

See [ANALYTICS.md](ANALYTICS.md) for full details.

## Troubleshooting

### "ModuleNotFoundError: No module named 'flask_sqlalchemy'"
```bash
pip install Flask-SQLAlchemy
```

### "Database is locked"
Use PostgreSQL in production, not SQLite.

### Can't access admin dashboard
1. Check credentials in `.env`
2. Verify SECRET_KEY is set
3. Check browser console for errors

### No data showing
1. Generate a test PPT first
2. Check database file exists: `ls -la pptgen.db`
3. Check application logs

## Need Help?

- 📖 Full documentation: [ANALYTICS.md](ANALYTICS.md)
- 🐛 Report issues: GitHub Issues
- 📧 Contact: shahshubham1888@gmail.com

---

**That's it!** Your analytics system is ready. The frontend remains unchanged, but you now have powerful insights into how people use your PPT generator.
