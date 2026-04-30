# ⚡ TaskFlow — Team Task Manager

A beautiful, full-stack team task management application with role-based access control, real-time performance tracking, and stunning animated UI.

## 🌐 Live Demo

🔗 **[https://your-app.up.railway.app](https://your-app.up.railway.app)**

> Replace with your actual Railway URL

### Test Credentials
- **Admin:** `admin@taskflow.com` / `admin123`
- **Member:** `member@taskflow.com` / `member123`

---

## ✨ Key Features

### 🔐 Authentication & Authorization
- JWT-based authentication
- Role-based access control (Admin / Member)
- Secure password hashing with bcrypt

### 📁 Project Management
- Create, edit, delete projects
- Assign start & due dates with countdown
- Project phase tracking (Planning → Development → Testing → Deployment → Completed)
- Real-time progress bar
- Team member management per project

### ✅ Task Management  
- Create tasks with priority (Low/Medium/High)
- Status tracking (Todo / In Progress / Done)
- Assign tasks to team members
- Due date tracking with overdue alerts
- Filterable task views (All / Completed / Overdue)

### 👥 User Management (Admin Only)
- Create, edit, delete users
- Role assignment (Admin/Member)
- Custom designations (e.g., "Senior Developer")
- Admin protection (Admins cannot be deleted)

### 📊 Performance Monitoring (Admin Only)
- Real-time leaderboard with badges (🏆 🥈 🥉)
- Live completion rate tracking
- Auto-updates every 10 seconds
- Per-user task breakdown

### 🔔 Smart Notifications
- Overdue project alerts
- Due-soon reminders (within 3-7 days)
- Auto-toast notifications
- Notification bell with badge counter

### 📝 Progress Reports
- Team members can submit progress updates
- Timeline view of all reports per project
- Auto-updates project progress percentage

### 🎨 Beautiful UI
- Glassmorphism design
- Animated particle background
- Smooth GSAP animations
- Dark theme with gradient accents
- Fully responsive

---

## 🛠️ Tech Stack

**Backend:**
- Python 3.11
- Flask 3.0
- SQLAlchemy (ORM)
- Flask-JWT-Extended (Auth)
- Flask-Bcrypt (Password hashing)
- Flask-CORS

**Database:**
- PostgreSQL (Production - Railway)
- SQLite (Development)

**Frontend:**
- Vanilla JavaScript
- GSAP (Animations)
- Custom Glassmorphism CSS
- Font Awesome icons

**Deployment:**
- Railway (Hosting)
- Gunicorn (WSGI server)

---

## 🚀 Run Locally

### Prerequisites
- Python 3.10+
- pip

### Setup

```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/team-task-manager.git
cd team-task-manager

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cat > .env << EOF
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-here
DATABASE_URL=sqlite:///taskmanager.db
EOF

# Run the app
python run.py
