import jwt,datetime,os
from flask import Flask, request
from flask_mysqldb import MySQL

server=Flask(__name__)
mysql= MySQL(server)
server.config["MYSQL_HOST"] = "localhost"
server.config["MYSQL_USER"] = "user"
server.config["MYSQL_PASSWORD"] = "admin"
server.config["MYSQL_DB"] = "auth"
server.config["MYSQL_PORT"] = "3306"

@server.route("/login",methods=["POST"])
def login():
    auth=request.authorization
    if not auth:
        return "missing credentials", 401

    cur=mysql.connection.cursor()
    res=cur.execute(
        "SELECT email,password FROM user WHERE email=%s",(auth.username,)
    )
    if res>0:
        user_row=cur.fetchone()
        email=user_row[0]
        password=user_row[1]

        if auth.username != email  or auth.password != password:
            return "invalid credentials",401
        else:
            return createJWT(auth.username,os.environ.get("JWT_SECRET"),True)

    else:
        return "invalid credentials",401

def createJWT(username,secret,authz):
    return jwt.encode(
        {
            "username": username,
            "exp": datetime.datetime.utcnow() 
             + datetime.timedelta(days=1),
            "iat": datetime.datetime.utcnow(),
            "admin": authz,

        },
        secret,
        algorithm= "HS256",
    )
# @server.route("/validate",methods=["POST"])



if __name__=="__main__":
    server.run(host="0.0.0.0",port=5000)