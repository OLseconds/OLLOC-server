from flask import Flask
import db, urllib.parse


class User:
    def __init__(self, database):
        self.database = database

    def user_profile(self):
        # 유저정보 & 가입여부 체크 메서드
        pass

    def useradd(self, username, password, name, mail):
        # 회원가입
        '''
        :param username: join user id
        :param password: join user password
        :param name: join user name
        :param mail: join user e-mail ex) test@test.com
        :return:
        '''
        """
        DB  예시
        { "_id" : ObjectId("5e2852ea6bc726b9ad8d52c0"), 
        "username" : "paperlee", "name" : "leejonghwi", 
        "password" : "", "mail" : "",
         "intro" : "peekaboo" }
        """
        self.database.user_coll.insert({
            "username": username,
            "password": password,
            "name": name,
            "mail": mail
        })

    def change_profile(self):
        # 회원정보 변경
        pass

    def exit_profile(self):
        # 회원 탈퇴
        pass


app = Flask(__name__)


@app.route('/user')
def userApi():
    # user 에 대한 api
    return 'Hello Flask!'

@app.route('/location')
def locationApi():
    # location 에 대한 api
    return "location api"



if __name__ == '__main__':
    f = open("./pwd.txt", 'r')
    database = db.Db(host="127.0.0.1", user="location", pwd=urllib.parse.quote(f.readline()), db="locations")
    f.close()
    usermod = User(database)
    usermod.useradd("test", "testpwd", "TEST", "test@test.com")

    app.debug = True
    app.run(host="0.0.0.0", port="5000")