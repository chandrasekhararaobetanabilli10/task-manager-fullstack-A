import os
from flask import Flask, jsonify, request, send_from_directory
import mysql.connector
from mysql.connector import Error

app=Flask(__name__,static_folder="../frontend",static_url_path="")
def connect():
    return mysql.connector.connect(host=os.getenv("DB_HOST","localhost"),port=int(os.getenv("DB_PORT","3306")),user=os.getenv("DB_USER","taskuser"),password=os.getenv("DB_PASSWORD","taskpass"),database=os.getenv("DB_NAME","taskmanager"))
def item(r):
    return {"id":r[0],"title":r[1],"description":r[2] or "","due_date":r[3].isoformat() if r[3] else None,"status":r[4]}
@app.get("/")
def home(): return send_from_directory(app.static_folder,"index.html")
@app.get("/api/tasks")
def all_tasks():
    try:
        c=connect();q=c.cursor();q.execute("SELECT id,title,description,due_date,status FROM tasks ORDER BY id DESC");data=[item(r) for r in q.fetchall()];q.close();c.close();return jsonify(data)
    except Error: return jsonify(error="Database unavailable. Check MySQL is running."),503
@app.post("/api/tasks")
def add():
    d=request.get_json(silent=True) or {};title=(d.get("title") or "").strip();status=d.get("status","Pending")
    if not title:return jsonify(error="Task title is required."),400
    if status not in ("Pending","Completed"):return jsonify(error="Invalid status."),400
    try:
        c=connect();q=c.cursor();q.execute("INSERT INTO tasks(title,description,due_date,status) VALUES(%s,%s,%s,%s)",(title,d.get("description",""),d.get("due_date") or None,status));c.commit();new_id=q.lastrowid;q.close();c.close();return jsonify(id=new_id),201
    except Error:return jsonify(error="Could not save task. Check database settings and date."),500
@app.put("/api/tasks/<int:task_id>")
def update(task_id):
    d=request.get_json(silent=True) or {};title=(d.get("title") or "").strip();status=d.get("status","Pending")
    if not title or status not in ("Pending","Completed"):return jsonify(error="Enter a title and valid status."),400
    try:
        c=connect();q=c.cursor();q.execute("UPDATE tasks SET title=%s,description=%s,due_date=%s,status=%s WHERE id=%s",(title,d.get("description",""),d.get("due_date") or None,status,task_id));c.commit();n=q.rowcount;q.close();c.close()
        return (jsonify(message="Updated"),200) if n else (jsonify(error="Task not found."),404)
    except Error:return jsonify(error="Could not update task."),500
@app.delete("/api/tasks/<int:task_id>")
def remove(task_id):
    try:
        c=connect();q=c.cursor();q.execute("DELETE FROM tasks WHERE id=%s",(task_id,));c.commit();n=q.rowcount;q.close();c.close()
        return ("",204) if n else (jsonify(error="Task not found."),404)
    except Error:return jsonify(error="Could not delete task."),500
if __name__=="__main__":app.run(host="0.0.0.0",port=5000)
