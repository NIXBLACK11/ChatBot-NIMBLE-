import mysql.connector


mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="2004",
  database="chatbot"
)

mycursor = mydb.cursor()

def setRoutine(routine, time):
    sql = "INSERT INTO tasks (name, time) VALUES (%s, %s)"
    val = (routine, time)
    mycursor.execute(sql, val)
    mydb.commit()
    print(mycursor.rowcount, "record inserted.")


def getRoutines():
    sql = "SELECT * FROM tasks;"
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    return myresult


def deleteRoutine(name):
    sql = "DELETE FROM tasks WHERE name=\""+name+"\";"
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    print(myresult)