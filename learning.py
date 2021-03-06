from flask import Flask, make_response, request, jsonify
from flask_mongoengine import MongoEngine
from api_constants import mongodb_password, database_name

app = Flask(__name__)

DB_URI = "mongodb+srv://m001-student:{}@sandbox.j0jwd.mongodb.net/{}?retryWrites=true&w=majority".format(
    mongodb_password, database_name)
app.config["MONGODB_HOST"] = DB_URI

db = MongoEngine()
db.init_app(app)


# @app.route('/')
def hello_world():
    return 'Welcome to Learning Management System'


class Detail(db.Document):
    student_id = db.IntField()
    program = db.StringField()
    semester = db.IntField()
    course = db.StringField()
    section = db.StringField()
    instructor = db.StringField()

    def to_json(self):
        return {
            "student_id": self.program,
            "program": self.program,
            "semester": self.semester,
            "course": self.course,
            "section": self.section,
            "instructor": self.instructor
        }


# @app.route('/populate', methods=['POST'])
def db_populate():
    detail1 = Detail(student_id=1, program="BE", semester=1, course="Maths", section="A", instructor="Deepak")
    detail2 = Detail(student_id=2, program="BBA", semester=1, course="account", section="B", instructor="Gagan")
    detail3 = Detail(student_id=3, program="BIM", semester=1, course="tours", section="A", instructor="Pretna")
    detail1.save()
    detail2.save()
    detail3.save()
    return make_response("", 201)


# @app.route('/api/student', methods=['GET', 'POST'])
def api_student():
    if request.method == "GET":
        details = []
        for detail in Detail.objects:
            details.append(detail)
        return make_response(jsonify(details), 200)
    elif request.method == "POST":
        content = request.json
        detail = Detail(student_id=content['student_id'],
                        program=content['program'], semester=content['semester'], course=content['course'],
                        section=content['section'], instructor=content['instructor'])
        detail.save()
        return make_response("", 201)


# @app.route('/api/semester/<semester>', methods=['GET'])
def api_each_semester(semester):
    if request.method == "GET":
        result = Detail.objects(semester=semester).only('student_id', 'instructor')
        return result.to_json()


# @app.route('/api/program/<program>', methods=['GET'])
def api_each_program(program):
    if request.method == "GET":
        result1 = Detail.objects(program=program).only('student_id', 'instructor')
        return result1.to_json()


# @app.route('/api/section/<section>', methods=['GET'])
def api_each_section(section):
    if request.method == "GET":
        result2 = Detail.objects(section=section).only('student_id', 'instructor')
        return result2.to_json()


# @app.route('/api/semester/view/<semester>', methods=['GET'])
def api_each_sem_view(semester_no):
    if request.method == "GET":
        result3 = Detail.objects(semester=semester_no).only('course', 'section', 'instructor')
        return result3.to_json()


# @app.route('/api/course/<course>', methods=['GET'])
def api_each_subject(course):
    if request.method == "GET":
        result4 = Detail.objects(course=course).only('instructor')
        return result4.to_json()


app.add_url_rule("/", "/", hello_world)
app.add_url_rule("/populate", "populate", db_populate)
app.add_url_rule("/api/student", "student", api_student, methods=['GET', 'POST'])
app.add_url_rule("/api/semester/<semester>", "<semester>", api_each_semester)
app.add_url_rule("/api/program/<program>", "<program>", api_each_program)
app.add_url_rule("/api/section/<section>", "<section>", api_each_section)
app.add_url_rule("/api/semester/view/<semester_no>", "<semester_no>", api_each_sem_view)
app.add_url_rule("/api/course/<course>", "<course>", api_each_subject)

if __name__ == '__main__':
    app.run()
