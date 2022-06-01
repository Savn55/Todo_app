from flask import Flask, render_template,request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

# setting cofig vars
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///db.sqlite' #/// is indicating relative path and db.sqlite is just given name
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False #don't worry about this rn
db = SQLAlchemy(app)

#creating a database
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean())

@app.route('/')
def index(): #homepage
    #show all todos
    todo_list = Todo.query.all()
    print(todo_list)

    return render_template('base.html', todo_list=todo_list) #todo_list=todo_list to include in html

@app.route("/add", methods=["POST"])
def add():
    #add new item
    title = request.form.get("todo-title")
    new_todo = Todo(title=title, complete=False)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/update/<int:todo_id>")
def update(todo_id):
    #update the exisiting dbase
    todo = Todo.query.filter_by(id=todo_id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    #delete an item
    todo = Todo.query.filter_by(id=todo_id).first()
    todo.complete = not todo.complete
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("index"))


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)