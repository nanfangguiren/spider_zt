from PyQt5 import QtGui
import pymysql


class LoginDB():
    def __init__(self):
        self._createLoginTable_()

    def getConnection(self):
        return pymysql.connect(
            host='121.4.121.91',
            port=3306,
            user='root',
            password="Songzhe_123",
            db="Spider_ZT"
        )

    def _createLoginTable_(self):
        connection = self.getConnection()
        cursor = connection.cursor()
        cursor.execute(
            "CREATE table if not exists tb_login_user(username varchar(64) primary key, password varchar(64))")
        cursor.close()
        connection.close()

    # 登录 -> True:登录成功 or False:用户名密码格式无效或密码错误
    def login(self, username, password):
        if not self.checkValidUsername(username) or not self.checkValidPassword(password):
            return False

        sql = "SELECT username, password FROM tb_login_user WHERE username='{0}'"
        sql = sql.format(username)

        connection = self.getConnection()
        cursor = connection.cursor()
        cursor.execute(sql)
        data = cursor.fetchall()
        cursor.close()
        connection.close()

        return data[0][1] == password

    # 注册 -> True:注册成功 or False:用户名密码格式无效或已经存在用户名
    def register(self, username, password):
        if self.existUsername(username):
            return False

        if not self.checkValidUsername(username) or not self.checkValidPassword(password):
            return False

        sql = "INSERT into tb_login_user(username, password) values ('{0}', '{1}')"
        sql = sql.format(username, password)

        connection = self.getConnection()
        cursor = connection.cursor()
        cursor.execute(sql)
        connection.commit()                 # 修改数据库要commit

        cursor.close()
        connection.close()

        return True

    def existUsername(self, username):
        if not self.checkValidUsername(username):
            return False

        sql = "SELECT username FROM tb_login_user WHERE username='{0}'"
        sql = sql.format(username)

        connection = self.getConnection()
        cursor = connection.cursor()
        cursor.execute(sql)
        data = cursor.fetchall()

        cursor.close()
        connection.close()

        return len(data) > 0

    def checkValidUsername(self, username):
        return True

    def checkValidPassword(self, password):
        return True


if __name__ == '__main__':
    db = LoginDB()
    
    if db.register('abc', '123456'):
        print('注册成功！')
    else:
        print('注册失败！')

    if db.login('abc', 'xxxx'):
        print('登录成功')
    else:
        print('登录失败')

    if db.login('abc', '123456'):
        print('登录成功')
    else:
        print('登录失败')
