import jwt, datetime, os
from flask import Flask, request
from flask_mysqldb import MySQL
from datetime import datetime, timezone

server = Flask(__name__) # our app
mysql = MySQL(server)

# 1. config
server.config["MYSQL_HOST"] = os.environ.get("MYSQL_HOST")
server.config["MYSQL_USER"] = os.environ.get("MYSQL_USER")
server.config["MYSQL_PASSWORD"] = os.environ.get("MYSQL_PASSWORD")
server.config["MYSQL_DB"] = os.environ.get("MYSQL_DB")
server.config["MYSQL_PORT"] = os.environ.get("MYSQL_PORT")

# 2. login route - take email and password and return JWT from create JWT function
@server.route("/login", methods=["POST"])
def login():
    auth = request.authorization
    if not auth:
        return "missing credential", 401
    
    # check db for username & password
    cur = mysql.connection.cursor()
    res = cur.execute(
        "SELECT email, password FROM user WHERE email=%s", (auth.username, )
    )

    # if res > 0, then user exists within db
    if res > 0:
        user_row = cur.fetchone()
        email = user_row[0]
        password = user_row[1]
        
        if auth.username != email or auth.password != password:
            return "invalid credentials", 401
        else:
            return createJWT(auth.username, os.environ.get("JWT_SECRET"), True)
    else:
        return "invalid credentials", 401

# 4. route to validate JWTs - API Gateway will use route to validate JWTs sent within clieent requests
@server.route("/validate", methods=["POST"])
def validate():
    encoded_jwt = request.headers["Authorization"]
    
    if not encoded_jwt:
        return "missing credentials", 401

    encoded_jwt = encoded_jwt.split(" ")[1] # token to be formatted as Bearer authentication (Bearer <token>)
    
    try:
        decoded = jwt.decode(
            encoded_jwt, os.environ.get("JWT_SECRET"), algorithm=["HS256"]
        )
    except:
        return decoded, 200
    

# 3. create JWTs
def createJWT(username, secret, authz):
    return jwt.encode(
        {
            "username": username,
            "exp": datetime.datetime.now(tz=datetime.timezone.utc)
            + datetime.timedelta(days=1), # expire token after 24 hrs
            "iat": datetime.datetime.utcnow(),  # when token is issued
            "admin": authz, #whether user is admin or not (T/F) . . .determine endpoints user. has access to
        },
        secret,
        algorithm="HS256",
    )

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=5000)