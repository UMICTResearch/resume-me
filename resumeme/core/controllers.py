from flask import Blueprint, render_template

core = Blueprint('core', __name__, template_folder='templates')


@core.route('/')
def home():
    return render_template('home.html')


@core.route('/job_preparation')
def job_preparation():
    return render_template('core/job_preparation.html')


@core.route('/networking')
def networking():
    return render_template('core/networking.html')


@core.route('/aboutus')
def aboutus():
    return render_template('core/aboutus.html')


@core.route('/contactus')
def contactus():
    return render_template('core/contactus.html')
