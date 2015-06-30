from flask import current_app, Blueprint, render_template, abort, request, flash, redirect, url_for, jsonify

core = Blueprint('core', __name__, template_folder='templates')


@core.route('/')
def notes():
    return render_template('home.html')
