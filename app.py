from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    sn = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime,default=datetime.utcnow())
    
    def __repr__(self) -> str:
        return f"{self.sn} - {self.title}"

@app.route("/add", methods = ['POST'])
def hello_world():
    if request.method=='POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()
    return redirect('/')

@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
    if request.method=='POST':
        title = request.form['title']
        desc = request.form['desc']
        todo =Todo.query.filter_by(sn=sno).first()
        todo.title = title
        todo.desc = desc  
        db.session.add(todo)
        db.session.commit()
        return redirect('/')   
    todo =Todo.query.filter_by(sn=sno).first()
    return render_template('update.html', todo = todo)
     

@app.route('/delete/<int:sno>')
def delete(sno):
    todo = Todo.query.filter_by(sn=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')

@app.route('/')
def index():
    alltodo =Todo.query.all()
    return render_template('index.html', alltodo = alltodo)

@app.route("/products")
def products():
    return "<h1>This is a test products</h1>"

if __name__== "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5001)