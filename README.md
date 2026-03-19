fastapi-online-course-platform

# 🎓 LearnHub – Online Course Management API (FastAPI Project)

## 📌 Project Overview

**LearnHub** is a fully functional backend application built using **FastAPI** that simulates a real-world **online course platform**.
It allows users to browse courses, enroll with discounts, manage wishlists, and perform advanced operations like filtering, searching, sorting, and pagination.

This project demonstrates strong backend development skills and is ideal for showcasing on a resume.

---

## 🚀 Features

### 📚 Course Management

* View all courses
* Add new courses
* Update course details
* Delete courses (with validation)
* Course summary statistics

### 🎟️ Enrollment System

* Enroll in courses
* Automatic seat reduction
* Discount system:

  * ✅ 10% Early Bird Discount (if seats > 5)
  * ✅ Coupon Codes:

    * `STUDENT20` → 20% off
    * `FLAT500` → ₹500 off
* Gift enrollment feature

### ❤️ Wishlist System

* Add courses to wishlist
* Remove courses from wishlist
* View wishlist with total value
* Enroll all wishlist items at once

### 🔍 Advanced Functionalities

* Search courses & enrollments
* Filter courses (category, level, price, availability)
* Sort courses & enrollments
* Pagination support
* Combined browsing API

---

## 🛠️ Tech Stack

* **Backend Framework:** FastAPI
* **Programming Language:** Python
* **Validation:** Pydantic
* **Server:** Uvicorn

---

## ⚙️ Installation & Setup

### 1️⃣ Clone Repository

```bash
git clone https://github.com/your-username/learnhub-fastapi.git
cd learnhub-fastapi
```

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Run the Server

```bash
uvicorn main:app --reload
```

---

## 🌐 API Documentation

After running the server, open:

👉 http://127.0.0.1:8000/docs

This provides an interactive Swagger UI to test all APIs.

---

## 📌 API Endpoints

### 📚 Courses

* `GET /courses` → Get all courses
* `POST /courses` → Add new course
* `PUT /courses/{course_id}` → Update course
* `DELETE /courses/{course_id}` → Delete course
* `GET /courses/{course_id}` → Get single course

### 🎟️ Enrollments

* `POST /enrollments` → Enroll in a course
* `GET /enrollments` → View all enrollments
* `GET /enrollments/search` → Search enrollments
* `GET /enrollments/sort` → Sort enrollments
* `GET /enrollments/page` → Paginate enrollments

### ❤️ Wishlist

* `POST /wishlist/add` → Add to wishlist
* `GET /wishlist` → View wishlist
* `DELETE /wishlist/remove/{course_id}` → Remove item
* `POST /wishlist/enroll-all` → Enroll all wishlist items

### 🔍 Advanced APIs

* `GET /courses/filter` → Filter courses
* `GET /courses/search` → Search courses
* `GET /courses/sort` → Sort courses
* `GET /courses/page` → Pagination
* `GET /courses/browse` → Combined filtering + sorting + pagination

---

## 🧪 Sample Request (Enrollment)

```json
{
  "student_name": "Sravan",
  "course_id": 1,
  "email": "sravan@gmail.com",
  "coupon_code": "STUDENT20"
}
```

---

## 📊 Business Logic Highlights

* Seat availability is checked before enrollment
* Discounts are applied in sequence:

  1. Early bird discount
  2. Coupon discount
* Prevent duplicate wishlist entries
* Prevent deleting courses with enrollments

---

## 💡 Learning Outcomes

* Built RESTful APIs using FastAPI
* Implemented request validation using Pydantic
* Applied real-world business logic
* Designed modular backend architecture
* Practiced API testing using Swagger UI

---

## 🔮 Future Enhancements

* Integrate database (MySQL / PostgreSQL)
* Add authentication (JWT)
* Deploy on cloud (AWS / Render)
* Build frontend using React

---

## 👨‍💻 Author

**Sravan Kumar Janjirala**
B.Tech Student | Backend Developer

---

## ⭐ Support

If you like this project, give it a ⭐ on GitHub!
