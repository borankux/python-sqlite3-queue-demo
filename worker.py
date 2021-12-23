import sqlite3
import time

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

def scanTasksFromCursor(res):
    for task in res:
        return {
            "id":task[0],
            "message":task[1],
            "status":task[2]
        }

def doOneTask():
    sql   = "select * from tasks where status = 1 or status = 2 limit 1"
    task  = exe(sql, callback=scanTasksFromCursor)
    if task == None:
        print("No Task to be done")
        return False

    print("working on task:#" + str(task['id']) +  task['message'])

    sqlUpdate   = "update tasks set status = 2 where id = ? "
    exe(sqlUpdate, [task['id']])
    print("started doing task:#" + str(task['id']))

    time.sleep(5)

    sqlDone   = "update tasks set status = 3 where id = ? "
    exe(sqlDone, [task['id']])
    print("Done doing task:#" + str(task['id']))
    time.sleep(5)
    return True


alive = True
while(alive):
    alive = doOneTask()
