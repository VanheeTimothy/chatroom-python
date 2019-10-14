# importeren van
import pyodbc
import logging
import uuid
from classes.User import User
SERVR = "DESKTOP-4AQVELP\SQLEXPRESS"
DATABASE = "ChatroomDB"
USERNAME = "Timothy"
PASSWORD = "microsoft1.0"
DRIVER = "{ODBC Driver 13 for SQL Server}"



connectionstring = 'DRIVER=' + DRIVER + ';PORT=1433;SERVER=' + SERVR + ';PORT=1433;DATABASE=' + DATABASE + ';UID=' + USERNAME + ';PWD=' + PASSWORD

connection = pyodbc.connect(connectionstring)
cursor = connection.cursor()




def checkEmailAlreadyExists(Email): # return True if email exists else False
    sql = "select * from USERS WHERE Email = (?)"
    cursor.execute(sql,str(Email))
    result = cursor.fetchone()
    if result:
        logging.info("Email already exist")
        return True
    else:
        return False



def checkNicknameAlreadyExists(Nickname): # return True if nickname exists else False
    sql = "SELECT * from USERS WHERE Nickname = (?)"
    cursor.execute(sql,str(Nickname))
    result = cursor.fetchone()
    if result:
        logging.warning("Nickname already exist")
        return True
    else:
        return False


def checkLogin(nickname, userPassword):
    sql = "SELECT * FROM USERS WHERE Nickname = (?) AND Password = (?) "
    cursor.execute(sql,nickname, userPassword )
    result = cursor.fetchone()
    if result:
        logging.info("User credentials are corrected")
        return True
    else:
        logging.warning("user credentials are incorrect")
        return False

def addUser(User):

    sql = "INSERT INTO USERS VALUES (?,?,?,?,?)"
    try:
        cursor.execute(sql, User.uniqueId, User.Name, User.nickname, User.email, User.password)
        cursor.commit()
    except Exception as ex:
        logging.error("Failed to add user" + ex)


