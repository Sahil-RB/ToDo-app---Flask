from app import app, db
from flask import render_template, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from wtforms.fields.html5 import DateField
import datetime

class EntryForm(FlaskForm):
    task = StringField('Task', validators = [DataRequired()])
    deadline = DateField('Deadline', validators = [DataRequired()])
    submit = SubmitField('Create Task')

class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(120))
    date = db.Column(db.DateTime)
    completed = db.Column(db.Boolean)


    def __repr__(self):
        return 'Task:'+self.task+'\nDeadline:'+str(self.date)+'\ncompleted:'+str(self.completed)

@app.route('/', methods = ['GET', 'POST'])
@app.route('/index', methods = ['GET', 'POST'])
def home():
    form = EntryForm()
    if form.validate_on_submit():
        e = Entry(task = form.task.data, date = form.deadline.data, completed = False)
        db.session.add(e)
        db.session.commit()
        return redirect(url_for('home'))
    overdue = list(Entry.query.filter(Entry.date < datetime.date.today()).filter(Entry.completed == False))
    upcoming = list(Entry.query.filter(Entry.date >= datetime.date.today()).filter(Entry.completed == False))
    return render_template('home.html', form=form, overdue=overdue, upcoming=upcoming)

@app.route('/completed')
def completed():
    done = list(Entry.query.filter(Entry.completed == True))
    return render_template('completed.html', done=done)

@app.route('/mark_completed/<entryID>')
def mark_completed(entryID):
    e = Entry.query.filter(Entry.id == entryID).first()
    e.completed = True
    db.session.commit()
    return redirect(url_for('home'))
