from flask import Flask
import pymongo
app = Flask(__name__)


class Location:
    def __init__(self, host, user, db, pwd):
        self.connection = pymongo.MongoClient('mongodb://%s:%s@%s' % (user, pwd, host))
        print("dd")
        #self.db = exec("self.connection."+db)
        self.db = self.connection.locations
        #print(self.db)

    def user_profile(self):
        # 유저정보 & 가입여부 체크 메서드
        pass

    def useradd(self):
        # 회원가입
        pass

    def change_profile(self):
        # 회원정보 변경
        pass

    def exit_profile(self):
        #회원 탈퇴
        pass



@app.route('/')
def hello_flask():
    f = open("./pwd.txt", 'r')
    l = Location(host="127.0.0.1", user="location", pwd=f.readline(), db="locations")
    f.close()

    return 'Hello Flask!'

if __name__ == '__main__':

    app.debug = True
    app.run(host="0.0.0.0", port="5000")