# ⚡ TaskFlow — Team Task Manager

A beautiful, full-stack team task management application with role-based access control, real-time performance tracking, and stunning animated UI.

## 🌐 Live Demo

🔗 **[https://web-production-6bd45.up.railway.app](https://web-production-6bd45.up.railway.app)**

### Test Credentials
- **Admin:** Sign up with role "Admin" to access all features
- **Member:** Sign up with role "Member" to see restricted view

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
- Due-soon reminders
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

\`\`\`bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/team-task-manager.git
cd team-task-manager

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file with your secrets
echo "SECRET_KEY=your-secret-key-here" > .env
echo "JWT_SECRET_KEY=your-jwt-secret-here" >> .env
echo "DATABASE_URL=sqlite:///taskmanager.db" >> .env

# Run the app
python run.py
\`\`\`

Visit **http://localhost:8000**

---

## 📡 API Endpoints

### Authentication
- `POST /api/auth/signup` — Create account
- `POST /api/auth/login` — Login
- `GET /api/auth/me` — Current user info

### Projects
- `GET /api/projects/` — List projects
- `POST /api/projects/` — Create project (Admin)
- `GET /api/projects/<id>` — Project details
- `PATCH /api/projects/<id>` — Update project
- `DELETE /api/projects/<id>` — Delete project (Admin)
- `POST /api/projects/<id>/members` — Add member
- `DELETE /api/projects/<id>/members/<uid>` — Remove member
- `GET /api/projects/<id>/reports` — List progress reports
- `POST /api/projects/<id>/reports` — Add progress report
- `GET /api/projects/alerts` — Get notifications

### Tasks
- `GET /api/tasks/` — List tasks
- `POST /api/tasks/` — Create task
- `PATCH /api/tasks/<id>` — Update task
- `DELETE /api/tasks/<id>` — Delete task

### Users (Admin)
- `GET /api/users/` — List all users
- `POST /api/users/` — Create user
- `PATCH /api/users/<id>` — Update user
- `DELETE /api/users/<id>` — Delete user (Members only)
- `GET /api/users/leaderboard` — Performance leaderboard

---

## 📂 Project Structure

\`\`\`
team-task-manager/
├── app/
│   ├── __init__.py          # Flask app factory
│   ├── models.py            # Database models
│   ├── decorators.py        # Auth decorators
│   ├── routes/
│   │   ├── auth.py
│   │   ├── projects.py
│   │   ├── tasks.py
│   │   ├── users.py
│   │   └── dashboard.py
│   ├── static/
│   │   ├── css/style.css
│   │   └── js/
│   │       ├── animations.js
│   │       └── app.js
│   └── templates/
│       ├── base.html
│       ├── login.html
│       ├── signup.html
│       └── dashboard.html
├── config.py
├── run.py
├── requirements.txt
├── Procfile
├── railway.json
└── README.md
\`\`\`

---

## 👨‍💻 Author

**VIVEK KUMAR SINGH**
- GitHub: [@kalilinux013](https://github.com/kalilinux013)

---

## 📜 License

MIT License — feel free to use this project!
