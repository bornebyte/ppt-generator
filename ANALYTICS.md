# Analytics & Tracking System

## Overview

The PPT Generator now includes a comprehensive analytics and tracking system that silently monitors all generation activity without any user-facing changes.

## Features

### 📊 What's Being Tracked

1. **Generation Metadata**
   - Timestamp of generation
   - File name
   - Presentation title and subtitle
   - Number of slides
   - File size
   - Generation time (performance)
   - Success/failure status

2. **User Information** (when provided)
   - College/University name
   - Student type (single/group)
   - Student names and USN numbers
   - Course and semester
   - Professor name

3. **Technical Data**
   - IP address (for unique visitor tracking)
   - User agent (browser/device info)
   - Content features used (tables, images, charts)

4. **Error Tracking**
   - Failed generations with error messages
   - Helps identify issues and improve reliability

## Admin Dashboard

### Access
- URL: `http://your-domain.com/admin`
- Default credentials:
  - Username: `admin`
  - Password: `changeme123`

**⚠️ IMPORTANT: Change the default password in production!**

### Dashboard Features

1. **Overview Statistics**
   - Total generations
   - Success rate
   - Total students tracked
   - Average slides per presentation

2. **Trend Analysis**
   - Daily generation chart (last 30 days)
   - Peak usage identification

3. **Top Colleges**
   - Most active institutions
   - Generation count per college

4. **Recent Activity**
   - Latest 10 generations
   - Detailed information per generation
   - Student names and details

## Database Schema

### Tables

#### `generations`
Main tracking table for each PPT generation:
- `id` - Primary key
- `timestamp` - When generated
- `file_name` - Output filename
- `title`, `subtitle` - Presentation info
- `num_slides` - Slide count
- `file_size` - File size in bytes
- `college_name` - College/university
- `presentation_title` - Academic title
- `student_type` - 'single' or 'group'
- `course`, `semester` - Academic info
- `professor_name` - Submitted to
- `ip_address` - User IP
- `user_agent` - Browser/device
- `generation_time` - Time taken (seconds)
- `status` - 'success' or 'failed'
- `error_message` - Error details if failed
- `has_tables`, `has_images`, `has_charts` - Feature flags

#### `students`
Student information linked to generations:
- `id` - Primary key
- `generation_id` - Foreign key to generations
- `name` - Student name
- `usn` - University serial number

#### `daily_stats`
Aggregate statistics for quick analytics:
- `id` - Primary key
- `date` - Date
- `total_generations` - Count
- `successful_generations` - Success count
- `failed_generations` - Failure count
- `total_slides_generated` - Total slides
- `unique_ips` - Unique visitors

## Configuration

### Environment Variables

Add to `.env` file:

```env
# Database
DATABASE_URL=sqlite:///pptgen.db  # For local development
# DATABASE_URL=postgresql://user:pass@host:port/db  # For production

# Admin Credentials
ADMIN_USERNAME=your_username
ADMIN_PASSWORD=your_secure_password
```

### Security

1. **Change Default Credentials**
   ```bash
   export ADMIN_USERNAME=your_username
   export ADMIN_PASSWORD=strong_password_here
   ```

2. **Use Strong Passwords**
   - Minimum 12 characters
   - Mix of letters, numbers, symbols

3. **HTTPS in Production**
   - Always use SSL/TLS
   - Protect admin endpoints

4. **IP Whitelisting** (Optional)
   - Restrict admin access to specific IPs
   - Add middleware in `main.py`

## Usage

### Local Development

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the application:**
   ```bash
   python main.py
   ```

3. **Access admin dashboard:**
   - Open browser to `http://localhost:5000/admin`
   - Login with credentials

### Production Deployment

#### Vercel

1. **Set environment variables** in Vercel dashboard:
   ```
   DATABASE_URL=postgresql://...
   ADMIN_USERNAME=your_username
   ADMIN_PASSWORD=your_password
   SECRET_KEY=random-secret-key
   ```

2. **Add PostgreSQL database:**
   - Use Vercel Postgres
   - Or external service (Supabase, Neon, etc.)

3. **Deploy:**
   ```bash
   vercel --prod
   ```

#### Other Platforms

For Heroku, Railway, Render:
1. Add PostgreSQL addon
2. Set environment variables
3. Deploy via Git push

## API Endpoints

### Public
- `GET /` - Main application
- `POST /generate_ppt` - Generate presentation
- `GET /health` - Health check

### Admin (Protected)
- `GET /admin` - Redirect to login
- `GET /admin/login` - Login page
- `POST /admin/login` - Process login
- `GET /admin/dashboard` - Analytics dashboard
- `GET /admin/logout` - Logout

## Database Migrations

The database is automatically created on first run. For schema changes:

1. **Backup existing data:**
   ```bash
   sqlite3 pptgen.db .dump > backup.sql
   ```

2. **Update models in `models.py`**

3. **Restart application** to apply changes

## Analytics Queries

### Get total generations by college:
```python
from models import Generation, db
from sqlalchemy import func

results = db.session.query(
    Generation.college_name,
    func.count(Generation.id)
).group_by(Generation.college_name).all()
```

### Get generations in date range:
```python
from datetime import datetime
start_date = datetime(2025, 1, 1)
end_date = datetime(2025, 12, 31)

results = Generation.query.filter(
    Generation.timestamp.between(start_date, end_date)
).all()
```

### Export to CSV:
```python
import csv
generations = Generation.query.all()

with open('analytics.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(['Date', 'Title', 'College', 'Slides', 'Status'])
    for g in generations:
        writer.writerow([g.timestamp, g.title, g.college_name, 
                        g.num_slides, g.status])
```

## Privacy & Compliance

### Data Collection
- **Silent tracking**: No user notifications
- **No authentication required**: Free access maintained
- **IP anonymization**: Consider hashing IPs for GDPR

### GDPR Considerations
If targeting EU users:
1. Add privacy policy
2. Implement data deletion
3. Allow opt-out option
4. Anonymize IP addresses

### Data Retention
Configure automatic cleanup:
```python
# In main.py, add scheduled task
from datetime import datetime, timedelta

def cleanup_old_data():
    cutoff = datetime.utcnow() - timedelta(days=365)
    Generation.query.filter(Generation.timestamp < cutoff).delete()
    db.session.commit()
```

## Monitoring & Alerts

### Set up alerts for:
1. High failure rate
2. Unusual traffic spikes
3. Database errors
4. Slow generation times

### Example: Email alert on failure
```python
def send_alert(generation):
    if generation.status == 'failed':
        # Send email notification
        pass
```

## Troubleshooting

### Database locked
- Use PostgreSQL in production
- SQLite not recommended for high traffic

### Missing data
- Check database permissions
- Verify environment variables
- Check application logs

### Dashboard not loading
- Verify admin credentials
- Check session configuration
- Ensure SECRET_KEY is set

## Future Enhancements

Potential additions:
- [ ] Export analytics to CSV/Excel
- [ ] Email reports (daily/weekly)
- [ ] Real-time dashboard updates
- [ ] User cohort analysis
- [ ] Geographic heatmaps
- [ ] A/B testing features
- [ ] Rate limiting per IP
- [ ] API for external analytics tools

## Support

For issues or questions:
- GitHub: https://github.com/bornebyte
- Email: shahshubham1888@gmail.com

---

**Last Updated:** December 30, 2025
