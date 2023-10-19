from flask import Blueprint,render_template,request

from app import db,app
from .models import Student

student_bp=Blueprint('student',__name__)

@student_bp.route('/')
def index():
    students = db.session.query(Student).all()
    #print(students)
    return render_template("student/index.html", students=students)
    



@student_bp.route("/submit", methods=["POST"])
def submit():
    name = request.form["name"]
    year = request.form["year"]

    student_exists = db.session.query(Student).filter(Student.name == name).first()
    print(student_exists)
    # check if student already exists in db
    if not student_exists:
        student = Student(name=name,year=year)
        db.session.add(student)
        db.session.commit()

        response = f"""
        <tr>
            <td>{name}</td>
            <td>{year}</td>
            <td>
                <button class="btn btn-primary"
                    hx-get="/student/get-edit-form/{student.student_id}">
                    修改
                </button>
            </td>
            <td>
                <button hx-delete="/student/delete/{student.student_id}"
                    class="btn btn-primary">
                    删除
                </button>
            </td>
        </tr>
        """
        return response
    else:
        return ''


@student_bp.route("/delete/<int:id>", methods=["DELETE"])
def delete_student(id):
    student = Student.query.get(id)
    db.session.delete(student)
    db.session.commit()

    return ""

@student_bp.route("/get-edit-form/<int:id>", methods=["GET"])
def get_edit_form(id):
    student = Student.query.get(id)
    #author = Author.query.get(book.author_id)

    response = f"""
    <tr hx-trigger='cancel' class='editing' hx-get="/student/get-student-row/{id}">
  <td><input name="name" value="{student.name}"/></td>
  <td><input name="year" value="{student.year}"/></td>
  <td>
    <button class="btn btn-primary" hx-get="/student/get-student-row/{id}">
      取消
    </button>
    <button class="btn btn-primary" hx-put="/student/update/{id}" hx-include="closest tr">
      保存
    </button>
  </td>
    </tr>
    """
    return response

@student_bp.route("/get-student-row/<int:id>", methods=["GET"])
def get_student_row(id):
    student = Student.query.get(id)
    #author = Author.query.get(student.author_id)

    response = f"""
    <tr>
        <td>{student.name}</td>
        <td>{student.year}</td>
        <td>
            <button class="btn btn-primary"
                hx-get="/student/get-edit-form/{id}">
                编辑
            </button>
        </td>
        <td>
            <button hx-delete="/student/delete/{id}"
                class="btn btn-primary">
                删除
            </button>
        </td>
    </tr>
    """
    return response

@student_bp.route("/update/<int:id>", methods=["PUT"])
def update_student(id):
    db.session.query(Student).filter(Student.student_id == id).update({"name": request.form["name"],"year": request.form["year"]})
    db.session.commit()

    name = request.form["name"]
    student = Student.query.get(id)
    #author = Author.query.get(book.author_id)

    response = f"""
    <tr>
        <td>{student.name}</td>
        <td>{student.year}</td>
        <td>
            <button class="btn btn-primary"
                hx-get="/student/get-edit-form/{id}">
                编辑
            </button>
        </td>
        <td>
            <button hx-delete="/student/delete/{id}"
                class="btn btn-primary">
                删除
            </button>
        </td>
    </tr>
    """
    return response

