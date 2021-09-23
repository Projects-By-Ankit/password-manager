from flask import Flask, jsonify, request, make_response
from flask_restful import Api, Resource
import mysql.connector

app = Flask(__name__)
api = Api(app)
conn = mysql.connector.connect(
    host="sql5.freesqldatabase.com",
    user="sql5438699",
    password="Ektwg1xgFv",
    database="sql5438699"
)


def register_user(name, phno, mailid, userid, Password, cpassword):
    try:
        conn = mysql.connector.connect(
            host="sql5.freesqldatabase.com",
            user="sql5438699",
            password="Ektwg1xgFv",
            database="sql5438699"
        )
        mycursor = conn.cursor()
        mycursor.execute(
            "INSERT INTO login_data (name,ph_no,mail_id,user_name,password,c_password) VALUES (%s, %s, %s, %s, %s, %s)",
            (name, phno, mailid, userid, Password, cpassword,))
        conn.commit()
        return [True, "...User Created Successfully..."]

    except Exception as e:
        print(e)


def logindata(uname, upass):
    try:
        flag = False
        mycursor = conn.cursor()
        mycursor.execute("SELECT * FROM login_data")
        data = mycursor.fetchall()

        for row in range(len(data)):
            temp = data.__getitem__(row)

            if temp[3] == uname and temp[4] == upass:
                print("...Login Successful...")
                return [True, temp[3]]
                flag = True
                break
            else:
                flag = False

        if not flag:
            print("...Login Failed...")
            return [False]
    except Exception as e:
        print(e)


def get_data(uname):
    try:

        dict1 = {}

        mycursor = conn.cursor()
        mycursor.execute("SELECT * FROM data_table WHERE user_name=%s", (uname,))
        data = mycursor.fetchall()

        for row in range(len(data)):
            temp = data.__getitem__(row)
            dict1[row] = {"user_name": temp[0],
                          "site_name": temp[1],
                          "site_id_name": temp[2],
                          "site_password": temp[3],
                          "id_number": temp[4],
                          }
        # print(dict1)
        return dict1
    except Exception as e:
        print(e)


def update_data(siteuname, upass, uname, sitename, idnum):
    try:
        mycursor = conn.cursor()
        print(
            mycursor.execute(
                """UPDATE data_table SET site_user_name=%s,site_password=%s WHERE user_name=%s AND site_name=%s AND 
                id_number=%s""",
                (siteuname, upass, uname, sitename, idnum)))
        conn.commit()

        return [True, "...Data Updated Successfully..."]

    except Exception as e:
        print(e)


def delete_data(uname, sitename, idnum):
    try:
        mycursor = conn.cursor()
        print(
            mycursor.execute(
                """DELETE FROM data_table WHERE user_name=%s AND site_name=%s AND 
                id_number=%s""",
                (uname, sitename, idnum,)))
        conn.commit()

        return [True, "...Data Deleted Successfully..."]

    except Exception as e:
        print(e)


class Registerdata(Resource):
    def get(self):
        result = register_user(request.args.get("name"), request.args.get("ph_no"), request.args.get("mail_id"),
                               request.args.get("user_id"), request.args.get("password"),
                               request.args.get("c_password"))

        return make_response(jsonify(result, 200))


class Login(Resource):
    def get(self):
        status = logindata(request.args.get("user_id"), request.args.get("password"))
        if status[0]:
            return make_response(jsonify(status, 200))
        else:
            return make_response(jsonify(status, 401))


class Getdata(Resource):
    def get(self):
        result = get_data(request.args.get("uname"))
        return make_response(jsonify(result, 200))


class Updatedata(Resource):
    def get(self):
        result = update_data(request.args.get("site_u_name"), request.args.get("u_pass"), request.args.get("u_name"),
                             request.args.get("site_name"),
                             request.args.get("id_num"))
        return make_response(jsonify(result, 200))


class Deletedata(Resource):
    def get(self):
        result = delete_data(request.args.get("u_name"),
                             request.args.get("site_name"),
                             request.args.get("id_num"))
        return make_response(jsonify(result, 200))


class Help(Resource):
    def get(self):
        msghelp = {"Available End Points are: ": ["/ping",
                                                  "",
                                                  """/register-user?name=<Enter Your Name>&ph_no=<Enter Your Phone 
                                                  Number> &mail_id=<Enter Your Mail_Id>&user_id=<Enter the user id 
                                                  you want> &password=<Your Password>&c_password=<Confirm Password>""",
                                                  "",
                                                  "/login?user_id=<Your User Id>&password=<Your Password>",
                                                  "",
                                                  "/getdata?uname=<Your User Name>",
                                                  "",
                                                  """/updatedata?site_u_name=<Your Website User Name>&u_pass=<Your 
                                                  Site Password>&u_name=<Your MRG User Name>&site_name=<Which 
                                                  Web-Site You Want To Update>&id_num=<Website Id Number> """,
                                                  "",
                                                  """/deletedata?u_name=<Your MRG User Name>&site_name=<Which 
                                                  Web-Site You Want To Delete>&id_num=<Website Id Number> """
                                                  ]}
        # return make_response(jsonify(msghelp, 200))
        return jsonify(msghelp)

    def post(self):
        msghelp = {"Available End Points are: ": ["/ping",
                                                  "",
                                                  """/register-user?name=<Enter Your Name>&ph_no=<Enter Your Phone 
                                                  Number> &mail_id=<Enter Your Mail_Id>&user_id=<Enter the user id 
                                                  you want> &password=<Your Password>&c_password=<Confirm Password>""",
                                                  "",
                                                  "/login?user_id=<Your User Id>&password=<Your Password>",
                                                  "",
                                                  "/getdata?uname=<Your User Name>",
                                                  "",
                                                  """/updatedata?site_u_name=<Your Website User Name>&u_pass=<Your 
                                                  Site Password>&u_name=<Your MRG User Name>&site_name=<Which 
                                                  Web-Site You Want To Update>&id_num=<Website Id Number> """,
                                                  "",
                                                  """/deletedata?u_name=<Your MRG User Name>&site_name=<Which 
                                                  Web-Site You Want To Delete>&id_num=<Website Id Number> """
                                                  ]}
        # return make_response(jsonify(msghelp, 200))
        return jsonify(msghelp)


class Ping(Resource):
    def get(self):
        msgping = {"Status": "Alive"}
        return make_response(jsonify(msgping, 200))


api.add_resource(Help, "/")
api.add_resource(Ping, "/ping")
api.add_resource(Registerdata, "/register-user")
api.add_resource(Login, "/login")
api.add_resource(Getdata, "/getdata")
api.add_resource(Updatedata, "/updatedata")
api.add_resource(Deletedata, "/deletedata")

app.run(debug=False, host="0.0.0.0")
