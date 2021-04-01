"""
使用须知：
代码中数据表名 aces ，需要更改该数据表名称的注意更改
"""
import pymysql


class Database():
    # 设置本地数据库用户名和密码
    host = "localhost"
    user = "root"
    password = ""
    database = "test"
    port = 3306
    charset = "utf8"
    cursor = ''
    connet = ''

    def __init__(self):
        # 连接到数据库
        self.connet = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database,
                                      charset=self.charset)
        self.cursor = self.connet.cursor()

    # #删表
    def dropTables(self):
        self.cursor.execute('''drop table if exists aces''')
        print("删表")

    # 建表
    def createTables(self):
        self.cursor.execute('''create table if not exists aces
                        ( 
                            asin    varchar(11) primary key not null,
                            checked varchar(200));''')
        print("建表")

    # 保存数据
    def save(self, aceslist):
        self.cursor.execute("insert into aces ( asin, checked) values(%s,%s)", (aceslist[0], aceslist[1]))
        self.connet.commit()

    # 判断元素是否已经在数据库里，在就返回true ,不在就返回false
    def is_exists_asin(self, asin):
        self.cursor.execute('select * from aces where asin = %s', asin)
        if self.cursor.fetchone() is None:
            return False
        return True

