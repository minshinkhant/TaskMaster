from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
# adding database to the app
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

# model for the Database table(model)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id


# to set the route for the app(view)
# create route for the task
@app.route("/", methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        # create object for the model with data from the form
        new_task = Todo(content=task_content)

        try:
            # saving the model object to the database
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return "There was an issue adding your task"

    else:
        # returning the list of all the task created order by date created
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)

# Delete route for the task
@app.route('/delete/<int:id>')
def delete(id):
    # create task object to delete with the ID
    task_to_delete = Todo.query.get_or_404(id)

    try:
        # deleting from the database
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')

    except:
        return 'There was a problem deleting that task'

# update route for the task
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)

    # to change the current content to the new content from Post request
    if request.method == 'POST':
        task.content = request.form['content']

        try:
            # just need to commit to the database
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating the task'

    else:
        return render_template('update.html', task=task)


if __name__ == "__main__":
    app.run(debug=True)
