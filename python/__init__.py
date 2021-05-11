from flask import Flask, request, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
# pymysql伪装成MysqlDB
import pymysql

pymysql.install_as_MySQLdb()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:mysql123321@192.168.9.102:23306/test'
# 连接多个数据库
# app.config['SQLALCHEMY_BINDS'] = {
#    # 'database1': 'mysql+pymysql://root:@127.0.0.1/database1?charset=utf8mb4'
#     'database2': 'mysql+pymysql://root:@127.0.0.1/database2?charset=utf8mb4'
# }
# 执行操作后自动提交
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
db = SQLAlchemy(app)


class Course(db.Model):
    __tablename__ = 'course'
    id = db.Column(db.Integer, primary_key=True)
    cname = db.Column(db.String(30))
    # 增加关联属性和反向引用关系
    # 关联属性：在course对象中通过那个属性能够得到相应的所有的teacher
    # 反向引用关系：在teacher对象中通过那个属性能找到对应的course
    teachers = db.relationship('Teacher', backref='course', lazy='dynamic')  # 不会直接存在于teacher表中 运行时增加course属性

    students = db.relationship('Student', secondary='student_course',
                               lazy='dynamic',
                               backref=db.backref('course', lazy='dynamic'))

    def __repr__(self):
        return '<Course>:%r' % self.cname

    def __init__(self, cname):
        self.cname = cname


class Teacher(db.Model):
    __tablename__ = 'teacher'
    id = db.Column(db.Integer, primary_key=True)
    tname = db.Column(db.String(30))
    tage = db.Column(db.Integer)
    # 增加一列：course_id 外键列，引用自主键表（course）的主键列（id）
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
    # 增加关联关系以及反向引用
    wife = db.relationship('Wife', backref='teacher', uselist=False)

    def __repr__(self):
        return '<Teacher>:%r' % self.cname


class Wife(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    wname = db.Column(db.String(30))
    wage = db.Column(db.Integer)
    # 增加一个列（外键）：表示引用自Teacher表的主键
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'))

    def __init__(self, wname, wage):
        self.wage = wage
        self.wname = wname

    def __repr__(self):
        return "<Wife:%r>" % self.wname


class Student(db.Model):
    __tablename__ = "student"
    id = db.Column(db.Integer, primary_key=True)
    sname = db.Column(db.String(30))
    sage = db.Column(db.Integer)
    # 增加关联属性，以及反向引用
    courses = db.relationship('Course', secondary='student_course',
                              lazy='dynamic',
                              backref=db.backref('student', lazy='dynamic'))

    teachers = db.relationship('Teacher', secondary='student_teacher',
                               lazy='dynamic',
                               backref=db.backref('students', lazy='dynamic'))

    def __repr__(self):
        return "Student:%r>" % self.sname


# 使用db.tables创建第三张关联表，不需要对应的实体类
Student_course = db.Table(
    # 指定关联表的表名
    'student_course',
    # 指定关联表的主键
    db.Column('id', db.Integer, primary_key=True),
    # 指定外键，关联Student表的主键
    db.Column('student_id', db.Integer, db.ForeignKey('student.id')),
    # 指定外键，关联course表的主键
    db.Column('course_id', db.Integer, db.ForeignKey('course.id'))
)

student_teacher = db.Table(
    'student_teacher',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('student_id', db.Integer, db.ForeignKey('student.id')),
    db.Column('teacher_id', db.Integer, db.ForeignKey('teacher.id')),
)

# 同步数据库
db.create_all()


@app.route('/01-addcourse')
def add_course():
    course1 = Course('python基础')
    course2 = Course('python高级')
    course3 = Course('数据库基础')
    db.session.add(course1)
    db.session.add(course2)
    db.session.add(course3)
    return 'Hello World!'


@app.route('/02-register-teacher')
def register_teacher():
    teacher = Teacher()
    teacher.tname = '刘老师'
    teacher.tage = 45
    # 先获取一个course对象
    # course = Course.query.filter_by(id=3).first()

    # 再将course对象赋值给teacher
    # teacher.course = course
    # 最后将teacher保存回数据库

    teacher.course_id = 2

    db.session.add(teacher)
    return 'Register Teacher Success !!!'


@app.route('/03-query-teacher')
def query_teacher():
    # 通过course查找对应的所有的老师们
    # 查找course_id为1的course对象
    # course = Course.query.filter_by(id=2).first()
    # print("课程名称："+course.cname)
    # 查找course对应的所有teacher
    # teachers = course.teachers.all()
    # for tea in teachers:
    #     print('教师名称：'+tea.tname)

    # -----------------------------------------------------------------

    # 通过teacher查询对应的course
    teacher = Teacher.query.filter_by(id=1).first()
    print("教师姓名：" + teacher.tname)
    # 通过teacher的course属性查找对应的course
    course = teacher.course
    print("教授课程" + course.cname)
    return "Query OK"


@app.route('/04-regTeacher', methods=['GET', 'POST'])
def regTeacher():
    if request.method == 'GET':
        # 查询所有课程
        courses = Course.query.all()
        # 将课程列表发送到04-rehTeacher.html上
        return render_template('04-regTeacher.html', courses=courses)
    else:
        # 接收前段传递来的数据
        tname = request.form.get('tname')
        tage = request.form.get('tage')
        course_id = request.form.get('course')
        # 将三个数据构建成Teacher对象，在保存回数据库
        teacher = Teacher()
        teacher.tname = tname
        teacher.tage = tage
        teacher.course_id = course_id
        db.session.add(teacher)
        return redirect('/05-showTea')


@app.route('/05-showTea')
def showTea():
    teachers = Teacher.query.all()
    return render_template('05-showTea.html', teachers=teachers)


@app.route('/06-regWife')
def regWife():
    # 通过id赋值
    # wife = Wife('王夫人',18)
    # wife.teacher_id = 2
    # db.session.add(wife)

    # 通过对象赋值
    wife = Wife('魏夫人', 15)
    teacher = Teacher.query.filter_by(tname='刘老师').first()
    wife.teacher = teacher
    db.session.add(wife)
    return 'Register OK'


@app.route('/07-querywife')
def querywife():
    # 通过teacher找wife
    # teacher = Teacher.query.filter_by(id=2).first()
    # wife = teacher.wife

    # 通过wife找teacher
    wife = Wife.query.filter_by(id=5).first()
    teacher = wife.teacher
    return '老师：{}，夫人{}'.format(teacher.tname, wife.wname)


@app.route('/08-asc')
def add_student_course():
    # 获取id为1的学员的信息
    student = Student.query.filter_by(id=1).first()
    # 获取id为1的课程的信息
    course = Course.query.filter_by(id=2).first()
    student.courses.append(course)
    db.session.add(student)
    return "Ok"


@app.route('/09-getM2M')
def getM2M():
    student = Student.query.filter_by(id=1).first()
    courses = student.courses.all()
    print(courses)
    return "Query OK"


@app.route('/10-getM2M')
def get_M2M():
    course = Course.query.filter_by(id=1).first()
    student = course.students.all()
    print(student)
    return "is OK"


@app.route('/010-register-student', methods=['GET', 'POST'])
def register_student():
    if request.method=='GET':
        students = Student.query.all()
        teachers = Teacher.query.all()

        return render_template('10-register-student.html', params=locals())
    else:
        sid = request.form.get('sid')
        tids = request.form.getlist('tids')
        student = Student.query.filter_by(id=sid).first()
        teachers = Teacher.query.filter(Teacher.id.in_(tids)).all()
        for tea in teachers:
            student.teachers.append(tea)
        db.session.add(student)
        return 'Register OK'


@app.route('/011-query')
def query11():
    students = Student.query.all()
    return render_template('011-query.html', students=students)


if __name__ == '__main__':
    app.run(debug=True)
