# 🧠 Smart Assessment & AI Question Generation System

A full-stack Django web application that dynamically generates quizzes using AI (Groq + LLaMA 3), supports timed assessments, automatic evaluation, and detailed performance analytics.

Link:- https://smart-assessment.onrender.com/

---

## 🚀 Features

### 🔐 Authentication System
- User Registration & Login
- Secure Session Management
- User Profile with Image Upload
- Admin Panel Control

### 🧠 AI-Powered Quiz Engine
- Dynamic question generation using Groq API (LLaMA 3)
- Difficulty-based quiz generation (Easy / Medium / Hard)
- Configurable number of questions
- JSON-based structured question parsing

### ⏳ Smart Timer System
- User-selectable quiz duration
- Live countdown (MM:SS format)
- Auto-submit when time expires
- Tracks total time taken

### 📊 Automatic Evaluation
- Real-time answer storage
- Auto score calculation
- Percentage scoring
- Performance classification:
  - Excellent 🎯
  - Good 👍
  - Needs Improvement 💪

### 📋 Detailed Result View
- Question-by-question breakdown
- Correct/Incorrect highlighting
- Answer comparison
- Score & time analysis

### 🎨 UI & UX
- Bootstrap 5 responsive design
- Modern card-based layout
- Loading spinner during AI generation
- Clean user flow navigation

---

## 🛠 Tech Stack

- Python 3.11
- Django 5.x
- SQLite (Development)
- Bootstrap 5
- Groq API (LLaMA 3.1 8B Instant)
- HTML, CSS, JavaScript

---

## 📂 Project Structure

```
smart_assessment/
├── users/
├── quizzes/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── utils.py
├── dashboard/
├── templates/
│   ├── quizzes/
│   ├── users/
├── static/
├── .env (not included in repo)
├── manage.py
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone Repository

```bash
git clone https://github.com/deepakjha018/smart-assessment.git
cd smart-assessment
```

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Create `.env` File

Create a `.env` file in project root:

```
GROQ_API_KEY=your_groq_api_key_here
```

⚠ Do NOT commit this file.

---

### 5️⃣ Apply Migrations

```bash
python manage.py migrate
```

### 6️⃣ Create Superuser

```bash
python manage.py createsuperuser
```

### 7️⃣ Run Development Server

```bash
python manage.py runserver
```

Open:

```
http://127.0.0.1:8000/
```

---

## 🔐 Environment Variables

| Variable | Description |
|----------|------------|
| GROQ_API_KEY | API key for AI-based quiz generation |

---

## 🎯 Current Milestone Status

✅ Milestone 1 – Authentication & Base Quiz Structure  
✅ Milestone 2 – AI Integration & Smart Evaluation Engine  

---

## 📈 Future Enhancements

- Quiz history per user
- Leaderboard system
- Performance analytics dashboard
- Role-based access (Teacher / Student)
- PostgreSQL production deployment
- Docker support
- Cloud deployment (Render / Railway)

---

## 👨‍💻 Author

**Deepak Kumar Jha**  
B.Tech – Artificial Intelligence & Data Science  

GitHub: https://github.com/deepakjha018  

---

## ⭐ Why This Project Stands Out

- Real AI integration (not static questions)
- Dynamic difficulty-based generation
- Session-safe secure quiz flow
- Auto-evaluation logic
- Timer + analytics
- Resume-ready full-stack architecture
