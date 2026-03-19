from fastapi import FastAPI, Query, status
from pydantic import BaseModel, Field

app = FastAPI()

# ------------------ DATA ------------------

courses = [
    {"id": 1, "title": "Python Basics", "instructor": "Ravi", "category": "Web Dev", "level": "Beginner", "price": 0, "seats_left": 10},
    {"id": 2, "title": "FastAPI Mastery", "instructor": "Anil", "category": "Web Dev", "level": "Intermediate", "price": 1999, "seats_left": 5},
    {"id": 3, "title": "Data Science 101", "instructor": "Priya", "category": "Data Science", "level": "Beginner", "price": 1499, "seats_left": 8},
    {"id": 4, "title": "ML Advanced", "instructor": "Kiran", "category": "Data Science", "level": "Advanced", "price": 2999, "seats_left": 3},
    {"id": 5, "title": "UI UX Design", "instructor": "Neha", "category": "Design", "level": "Beginner", "price": 999, "seats_left": 6},
    {"id": 6, "title": "DevOps Basics", "instructor": "Arjun", "category": "DevOps", "level": "Beginner", "price": 1299, "seats_left": 4},
]

enrollments = []
wishlist = []
enrollment_counter = 1

# ------------------ HELPERS ------------------

def find_course(course_id):
    for c in courses:
        if c["id"] == course_id:
            return c
    return None


def calculate_enrollment_fee(price, seats_left, coupon):
    discount = 0

    if seats_left > 5:
        discount += price * 0.10

    if coupon == "STUDENT20":
        discount += price * 0.20
    elif coupon == "FLAT500":
        discount += 500

    final = price - discount
    return max(final, 0), discount

# ------------------ MODELS ------------------

class EnrollRequest(BaseModel):
    student_name: str = Field(..., min_length=2)
    course_id: int = Field(..., gt=0)
    email: str = Field(..., min_length=5)
    payment_method: str = "card"
    coupon_code: str = ""
    gift_enrollment: bool = False
    recipient_name: str = ""


class NewCourse(BaseModel):
    title: str = Field(..., min_length=2)
    instructor: str = Field(..., min_length=2)
    category: str = Field(..., min_length=2)
    level: str = Field(..., min_length=2)
    price: int = Field(..., ge=0)
    seats_left: int = Field(..., gt=0)

# ------------------ DAY 1 ------------------

@app.get("/")
def home():
    return {"message": "Welcome to LearnHub Online Courses"}


@app.get("/courses")
def get_courses():
    total_seats = sum(c["seats_left"] for c in courses)
    return {
        "total_courses": len(courses),
        "total_seats_available": total_seats,
        "courses": courses
    }


@app.get("/enrollments")
def get_enrollments():
    return {"total": len(enrollments), "enrollments": enrollments}


@app.get("/courses/summary")
def summary():
    free = [c for c in courses if c["price"] == 0]
    most_expensive = max(courses, key=lambda x: x["price"])
    total_seats = sum(c["seats_left"] for c in courses)

    category_count = {}
    for c in courses:
        category_count[c["category"]] = category_count.get(c["category"], 0) + 1

    return {
        "total_courses": len(courses),
        "free_courses": len(free),
        "most_expensive": most_expensive,
        "total_seats": total_seats,
        "category_count": category_count
    }

# ------------------ DAY 2 & 3 ------------------

@app.post("/enrollments")
def enroll(data: EnrollRequest):
    global enrollment_counter

    course = find_course(data.course_id)
    if not course:
        return {"error": "Course not found"}

    if course["seats_left"] <= 0:
        return {"error": "No seats available"}

    if data.gift_enrollment and not data.recipient_name:
        return {"error": "Recipient name required for gift"}

    final_fee, discount = calculate_enrollment_fee(
        course["price"], course["seats_left"], data.coupon_code
    )

    course["seats_left"] -= 1

    record = {
        "id": enrollment_counter,
        "student": data.student_name,
        "course": course["title"],
        "final_fee": final_fee,
        "discount": discount
    }

    if data.gift_enrollment:
        record["gift_for"] = data.recipient_name

    enrollments.append(record)
    enrollment_counter += 1

    return record


@app.get("/courses/filter")
def filter_courses(category: str = None, level: str = None, max_price: int = None, has_seats: bool = None):
    result = courses

    if category is not None:
        result = [c for c in result if c["category"] == category]

    if level is not None:
        result = [c for c in result if c["level"] == level]

    if max_price is not None:
        result = [c for c in result if c["price"] <= max_price]

    if has_seats is not None:
        result = [c for c in result if (c["seats_left"] > 0) == has_seats]

    return result

# ------------------ DAY 4 ------------------

@app.post("/courses", status_code=201)
def add_course(data: NewCourse):
    for c in courses:
        if c["title"].lower() == data.title.lower():
            return {"error": "Course already exists"}

    new_id = max(c["id"] for c in courses) + 1
    course = data.dict()
    course["id"] = new_id
    courses.append(course)
    return course


@app.put("/courses/{course_id}")
def update_course(course_id: int, price: int = None, seats_left: int = None):
    course = find_course(course_id)
    if not course:
        return {"error": "Course not found"}

    if price is not None:
        course["price"] = price

    if seats_left is not None:
        course["seats_left"] = seats_left

    return course


@app.delete("/courses/{course_id}")
def delete_course(course_id: int):
    course = find_course(course_id)
    if not course:
        return {"error": "Course not found"}

    for e in enrollments:
        if e["course"] == course["title"]:
            return {"error": "Cannot delete course with enrollments"}

    courses.remove(course)
    return {"message": "Course deleted"}

# ------------------ DAY 5 ------------------

@app.post("/wishlist/add")
def add_wishlist(student_name: str, course_id: int):
    course = find_course(course_id)
    if not course:
        return {"error": "Course not found"}

    for w in wishlist:
        if w["student"] == student_name and w["course_id"] == course_id:
            return {"error": "Already in wishlist"}

    wishlist.append({
        "student": student_name,
        "course_id": course_id,
        "price": course["price"]
    })

    return {"message": "Added to wishlist"}


@app.get("/wishlist")
def get_wishlist():
    total_value = sum(w["price"] for w in wishlist)
    return {"wishlist": wishlist, "total_value": total_value}


@app.delete("/wishlist/remove/{course_id}")
def remove_wishlist(course_id: int, student_name: str):
    for w in wishlist:
        if w["student"] == student_name and w["course_id"] == course_id:
            wishlist.remove(w)
            return {"message": "Removed"}
    return {"error": "Item not found"}


@app.post("/wishlist/enroll-all")
def enroll_all(student_name: str, payment_method: str):
    global enrollment_counter

    user_items = [w for w in wishlist if w["student"] == student_name]

    if not user_items:
        return {"error": "Wishlist empty"}

    results = []
    total_fee = 0

    for item in user_items:
        course = find_course(item["course_id"])

        if course and course["seats_left"] > 0:
            fee, _ = calculate_enrollment_fee(course["price"], course["seats_left"], "")

            course["seats_left"] -= 1

            record = {
                "id": enrollment_counter,
                "student": student_name,
                "course": course["title"],
                "final_fee": fee
            }

            enrollments.append(record)
            enrollment_counter += 1

            results.append(record)
            total_fee += fee

    wishlist[:] = [w for w in wishlist if w["student"] != student_name]

    return {"total_enrolled": len(results), "total_fee": total_fee, "details": results}

# ------------------ DAY 6 ------------------

@app.get("/courses/search")
def search_courses(keyword: str):
    result = [
        c for c in courses
        if keyword.lower() in c["title"].lower()
        or keyword.lower() in c["instructor"].lower()
        or keyword.lower() in c["category"].lower()
    ]

    return {"total_found": len(result), "results": result}


@app.get("/courses/sort")
def sort_courses(sort_by: str = "price", order: str = "asc"):
    if sort_by not in ["price", "title", "seats_left"]:
        return {"error": "Invalid sort_by"}

    reverse = order == "desc"
    return sorted(courses, key=lambda x: x[sort_by], reverse=reverse)


@app.get("/courses/page")
def paginate_courses(page: int = 1, limit: int = 3):
    start = (page - 1) * limit
    end = start + limit

    total = len(courses)
    total_pages = -(-total // limit)

    return {
        "page": page,
        "total_pages": total_pages,
        "data": courses[start:end]
    }


@app.get("/enrollments/search")
def search_enrollments(student_name: str):
    return [e for e in enrollments if student_name.lower() in e["student"].lower()]


@app.get("/enrollments/sort")
def sort_enrollments():
    return sorted(enrollments, key=lambda x: x["final_fee"])


@app.get("/enrollments/page")
def paginate_enrollments(page: int = 1, limit: int = 2):
    start = (page - 1) * limit
    end = start + limit
    return enrollments[start:end]


@app.get("/courses/browse")
def browse(
    keyword: str = None,
    category: str = None,
    level: str = None,
    max_price: int = None,
    sort_by: str = "price",
    order: str = "asc",
    page: int = 1,
    limit: int = 3
):
    result = courses

    if keyword:
        result = [c for c in result if keyword.lower() in c["title"].lower()]

    if category:
        result = [c for c in result if c["category"] == category]

    if level:
        result = [c for c in result if c["level"] == level]

    if max_price:
        result = [c for c in result if c["price"] <= max_price]

    reverse = order == "desc"
    result = sorted(result, key=lambda x: x[sort_by], reverse=reverse)

    start = (page - 1) * limit
    end = start + limit

    return {
        "total": len(result),
        "page": page,
        "data": result[start:end]
    }

# ------------------ LAST ROUTE ------------------

@app.get("/courses/{course_id}")
def get_course(course_id: int):
    course = find_course(course_id)
    if course:
        return course
    return {"error": "Course not found"}
