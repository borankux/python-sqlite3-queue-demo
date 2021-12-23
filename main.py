from flask import Flask, request as req, render_template as rt
import json
import sqlite3

conn = sqlite3.connect('tasks.db')

def exe(sql, data=[], callback=None):
    conn = sqlite3.connect('tasks.db')
    cur  = conn.cursor()
    res  = cur.execute(sql, data)

    callbackResult = "nothing"
    if callback != None:
        callbackResult = callback(res)

    conn.commit()
    cur.close()
    conn.close()
    return callbackResult

def initDB():    
    sql  = "create table if not exists tasks(id integer primary key autoincrement, message varchar, status integer)"
    return exe(sql)

def insertTask(msg):
    sql = "insert into tasks(message, status) values(?, ?)"
    return exe(sql, [msg, 1])

def getCount(res):
    for value in res:
        return (value[0])

def taskExists(msg):
    sql = "select count(*) c from tasks where message = ?"
    res = exe(sql, [msg], getCount)
    return res > 0

def scanTasksFromCursor(res):
    tasks = []
    for task in res:
        tasks.append({
            "id":task[0],
            "message":task[1],
            "status":task[2]
        })
    return tasks

def getTasks():
    sql = "select * from tasks"
    tasks = exe(sql=sql, callback=scanTasksFromCursor)
    return tasks

app = Flask(__name__)

@app.route("/")
def index():
    return rt('./index.html')


@app.route("/tasks", methods=['POST'])
def addTask():
    message = req.form.get("message")
    print(message)
    if(taskExists(message)):
        return json.dumps({
            "status":"400",
            "message":"tasks exists with message" + message
        })

    insertTask(message)
    return json.dumps({
        "status":"200",
        "message":"success"
    })

@app.route("/tasks", methods=['GET'])
def getTasksList():
    tasks = getTasks()
    return json.dumps({
        "status":200,
        "data":tasks,
        "message":"success"
    })

if __name__ == '__main__':
    initDB()
    app.run(debug=True)
