# Smart Assessment and Question Generation System

A Django-based web application designed to provide a smart quiz and assessment platform with user authentication, profile management, category-based quizzes, and configurable quiz settings.

---

## 🚀 Features (Milestone 1)

- User Registration & Login
- Secure Authentication & Sessions
- User Profile with Image Upload
- Quiz Categories & Subcategories
- Quiz Configuration (Difficulty, Questions, Timer)
- Admin Panel for Management
- Clean & Responsive UI (Bootstrap 5)

---

## 🛠 Tech Stack

- Python 3.11
- Django 5.x
- SQLite (Development)
- Bootstrap 5
- HTML, CSS

---

## 📂 Project Structure

smart_assessment/
├── users/
├── quizzes/
├── dashboard/
├── templates/
├── static/
├── manage.py


---

## ⚙️ Installation & Setup

1. Clone the repository
```bash
    git clone https://github.com/deepakjha018/smart-assessment.git

2. Create virtual environment
```bash
    python -m venv venv
    venv\Scripts\activate

3. Install dependencies
```bash
    pip install -r requirements.txt

4. Apply migrations
```bash
    python manage.py migrate

5. Create superuser
```bash
    python manage.py createsuperuser

6. Run server
```bash
    python manage.py runserver

👨‍💻 Author

Deepak Kumar Jha
B.Tech – Artificial Intelligence & Data Science

GitHub: https://github.com/deepakjha018

📌 Future Scope

AI-based Question Generation

Timed Quizzes

Result Analysis & Dashboard

Difficulty-based Question Selection
