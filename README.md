# EduTrack

EduTrack is a lightweight course management system built with Django and Django REST Framework. It allows teachers to manage courses and assignments, and students to enroll, view content, and submit assignments.

---

## 📂 Features

* Custom user roles: Teacher and Student
* Course creation and enrollment
* Assignment creation, submission, and grading
* Custom permissions for secure access
* RESTful API with Swagger documentation
* Admin interface customization
* Dockerized setup with environment-based configuration
* CI pipeline via GitHub Actions

---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/ALASHI1/edutrack.git
cd edutrack
```

### 2. Create a Virtual Environment

```bash
python -m venv env
source env/bin/activate  # or env\Scripts\activate on Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the Environment

Create two separate `.env` files:

#### .env (dev)

```env
DEBUG=True
SECRET_KEY=your-dev-secret-key
ALLOWED_HOSTS=localhost,127.0.0.1
DB_NAME=edutrack
DB_USER=edutrack
DB_PASSWORD=edutrack
DB_HOST=localhost
DB_PORT=5432
```

#### .env (prod)

```env
DEBUG=False
SECRET_KEY=your-prod-secret-key
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DB_NAME=edutrack
DB_USER=edutrack
DB_PASSWORD=your-secure-password
DB_HOST=db
DB_PORT=5432
```

### 5. Apply Migrations

```bash
python manage.py migrate
```

### 6. Run Server

```bash
python manage.py runserver
```

---

## 🚀 Docker Support

### Development

```bash
docker-compose up --build  -d #with default .env
```

### Production

```bash
docker-compose up --build -d  #with .env.prod
```

---

## 🔧 CI Integration

* GitHub Actions configured in `.github/workflows/ci.yml`
* Runs tests against PostgreSQL container on each push/PR

---

## 🔐 API Documentation

Visit `/swagger/` for interactive API docs.

---

## 🌐 Admin Panel

* Go to `/admin`
* Use superuser account (create with `python manage.py createsuperuser`)
* Customized for Teachers, Students, Courses, Assignments, and Submissions

---

## 🪖 Assumptions Made

* Teachers and Students are separate profiles linked to a single user model
* One assignment submission per student per assignment
* Only course owners (teachers) can create assignments
* Only enrolled students can access course content
* Custom permissions enforced via permissions classes

---

## 🧠 Design Decisions

* Used Django's built-in `User` model with separate `TeacherProfile` and `StudentProfile` models for clarity and scalability.

* Permissions are enforced via custom decorators and DRF mixins to restrict access to only authorized users.

* Chose `drf-yasg` for Swagger documentation due to its clarity and developer-friendliness.

* Separated dev and prod environments using .env files and python-decouple for clean environment management.

* Dockerized the application with separate compose files for development and production to mirror deployment environments.

* CI is configured to mirror the local .env.dev environment to prevent production exposure during tests.


## 🚧 Maintenance Guidelines

* Follow best practices for updating dependencies
* Always test changes using `python manage.py test` or GitHub Actions
* Back up `.env.prod` and production DB regularly
* Use `collectstatic` before deploying with Gunicorn or Whitenoise
* Rotate `SECRET_KEY` and DB credentials periodically

---

## 🚜 Contributing

Pull requests are welcome. For major changes, open an issue first to discuss what you'd like to change.

---

## 🚀 License

MIT License

---

*Developed as part of a Django Senior Backend Engineer Take-Home Project.*
