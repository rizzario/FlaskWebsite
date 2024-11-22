import os
from flask import Blueprint, render_template, json
from flask_login import login_required, current_user
from .config import Config
from .models import *
# from config import Config
# from models import *

#from . import db

main = Blueprint('main',__name__)

@main.route('/')
def index():
    if current_user.is_authenticated:
        return render_template('index.html', name=current_user.username)
    else:
        return render_template('index.html')

@main.route('/menu')
@login_required
def menu():
    return render_template('menu.html', name=current_user.username)