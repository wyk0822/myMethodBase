
from flask import Flask, request, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
# pymysql伪装成MysqlDB
import pymysql

pymysql.install_as_MySQLdb()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:mysql123321@192.168.9.102:33306/bookManager'
# 连接多个数据库
# app.config['SQLALCHEMY_BINDS'] = {
#    # 'database1': 'mysql+pymysql://root:@127.0.0.1/database1?charset=utf8mb4'
#     'database2': 'mysql+pymysql://root:@127.0.0.1/database2?charset=utf8mb4'
# }
# 执行操作后自动提交
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
db = SQLAlchemy(app)


# class Course(db.Model):
#     __tablename__ = 'course'
#     id = db.Column(db.Integer, primary_key=True)
#     cname = db.Column(db.String(30))
#     # 增加关联属性和反向引用关系
#     # 关联属性：在course对象中通过那个属性能够得到相应的所有的teacher
#     # 反向引用关系：在teacher对象中通过那个属性能找到对应的course
#     teachers = db.relationship('Teacher', backref='course', lazy='dynamic')  # 不会直接存在于teacher表中 运行时增加course属性
#
#     students = db.relationship('Student', secondary='student_course',
#                                lazy='dynamic',
#                                backref=db.backref('course', lazy='dynamic'))
#
#     def __repr__(self):
#         return '<Course>:%r' % self.cname
#
#     def __init__(self, cname):
#         self.cname = cname
#
#
# class Teacher(db.Model):
#     __tablename__ = 'teacher'
#     id = db.Column(db.Integer, primary_key=True)
#     tname = db.Column(db.String(30))
#     tage = db.Column(db.Integer)
#     # 增加一列：course_id 外键列，引用自主键表（course）的主键列（id）
#     course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
#
#
#     def __repr__(self):
#         return '<Teacher>:%r' % self.cname
#
#
# class Wife(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     wname = db.Column(db.String(30))
#     wage = db.Column(db.Integer)
#     # 增加一个列（外键）：表示引用自Teacher表的主键
#     teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'))
#
#     def __init__(self, wname, wage):
#         self.wage = wage
#         self.wname = wname
#
#     def __repr__(self):
#         return "<Wife:%r>" % self.wname
#
#
# class Student(db.Model):
#     __tablename__ = "student"
#     id = db.Column(db.Integer, primary_key=True)
#     sname = db.Column(db.String(30))
#     sage = db.Column(db.Integer)
#     # 增加关联属性，以及反向引用
#     courses = db.relationship('Course', secondary='student_course',
#                               lazy='dynamic',
#                               backref=db.backref('student', lazy='dynamic'))
#
#     teachers = db.relationship('Teacher', secondary='student_teacher',
#                                lazy='dynamic',
#                                backref=db.backref('students', lazy='dynamic'))
#
#     def __repr__(self):
#         return "Student:%r>" % self.sname
#
#
# # 使用db.tables创建第三张关联表，不需要对应的实体类
# Student_course = db.Table(
#     # 指定关联表的表名
#     'student_course',
#     # 指定关联表的主键
#     db.Column('id', db.Integer, primary_key=True),
#     # 指定外键，关联Student表的主键
#     db.Column('student_id', db.Integer, db.ForeignKey('student.id')),
#     # 指定外键，关联course表的主键
#     db.Column('course_id', db.Integer, db.ForeignKey('course.id'))
# )
#
# student_teacher = db.Table(
#     'student_teacher',
#     db.Column('id', db.Integer, primary_key=True),
#     db.Column('student_id', db.Integer, db.ForeignKey('student.id')),
#     db.Column('teacher_id', db.Integer, db.ForeignKey('teacher.id')),
# )
import datetime
class Lib_user(db.Model):
    __tablename__ = "lib_user"
    userid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    userpassword = db.Column(db.String(50))
    username = db.Column(db.String(50))
    userredp = db.Column(db.String(50))  # 院系

    book = db.relationship('Lib_book', secondary='bookbag',
                              lazy='dynamic',
                              backref=db.backref('lib_user', lazy='dynamic'))

class Lib_book(db.Model):
    __tablename__ = "lib_book"
    bookid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    bookname = db.Column(db.String(50))
    bookisbn = db.Column(db.String(50))

    book = db.relationship('Lib_user', secondary='bookbag',
                           lazy='dynamic',
                           backref=db.backref('lib_book', lazy='dynamic'))

class Lib_book_borrow(db.Model):
    borid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    bookid = db.Column(db.Integer, db.ForeignKey('lib_book.bookid'))
    userid = db.Column(db.Integer, db.ForeignKey('lib_user.userid'))
    bordate = db.Column(db.DateTime, default=datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S"))
    retdate = db.Column(db.DateTime, default=datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S"))
    borstate = db.Column(db.String(50))


student_teacher = db.Table(
    'bookbag',
    db.Column('bookid', db.Integer, db.ForeignKey('lib_book.bookid')),
    db.Column('userid', db.Integer, db.ForeignKey('lib_user.userid')),
)

# 同步数据库
db.create_all()


@app.route("/")
def fun():
    return "ok"

# def book():
#     from faker import Faker
#     fak = Faker(locale='zh_CN')
#     book = Lib_book(
#         bookname=fak.word(),
#         bookisbn=fak.isbn10(separator="-")
#     )
#     db.session.add(book)
#     import random
#     redps = ['计算机', '土木', '化工', '物流', '电子竞技', '挖掘机', '市场营销', '会计', '英语']
#     user = Lib_user(
#         username=fak.name(),
#         userpassword="123456",
#         userredp=redps[random.randint(0, 8)]
#     )
#     db.session.add(user)
#     return "ok"


if __name__ == '__main__':
    app.run(debug=True)
    # from faker import Faker
    # fak = Faker(locale='zh_CN')
    # # book = Lib_book(
    # #     bookname = fak.name()
    # # )
    # # # db.session.add(book)
    # print(fak.pyint(min_value=100000, max_value=999999, step=1))
