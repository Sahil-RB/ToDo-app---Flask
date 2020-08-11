from app import app
from flask import render_template, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from wtforms.fields.html5 import DateField

class EntryForm(FlaskForm):
    task = StringField('Task', validators = [DataRequired()])
    deadline = DateField('Deadline', validators = [DataRequired()])
    submit = SubmitField('Create Task')

@app.route('/', methods = ['GET', 'POST'])
@app.route('/index', methods = ['GET', 'POST'])
def home():
    form = EntryForm()
    if form.validate_on_submit():
        flash('Task:'+str(form.task.data))
        flash('Deadline:'+str(form.deadline.data))
        return redirect(url_for('home'))
    return render_template('base.html', form=form)
