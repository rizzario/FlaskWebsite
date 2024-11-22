from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, login_required, logout_user, current_user, LoginManager
from werkzeug.security import generate_password_hash
from .models import db, User
from urllib.parse import urlparse
from .ssh import RemoteConnect
from .config import Config
# from models import db, User
# from ssh import RemoteConnect
# from config import Config

auth = Blueprint('auth', __name__)
login_manager = LoginManager()
ssh = RemoteConnect("","","",None)

def redirect_destination(fallback):
    destination = request.args.get('next')
    try:
        dest_url = url_for(destination)
    except:
        return redirect(fallback)
    return redirect(dest_url)

@login_manager.unauthorized_handler
def unauthorized():
    return render_template('login.html')

@auth.errorhandler(404)
def page_not_found(e):
    if current_user.is_authenticated:
        return render_template('404.html', name=current_user.username), 404
    else:
        return render_template('404.html'), 404

@auth.route('/login', methods=['GET','POST'])
def login():

    if current_user.is_authenticated:
        return redirect(url_for('main.menu'))
    if request.method == "GET":
        return render_template('login.html')

    hostname = request.form.get('hostname')
    print("host is: ", hostname)
    name = request.form.get('username')
    password = request.form.get('password')
    next_url = request.form.get('next')
    
    user = User.query.filter_by(username=name).first()

    #update temporary user/password data for usage
    if user:
        user.password = generate_password_hash(password, method='scrypt')
        # user.password = password
        user.hostname = hostname
        db.session.commit()
    else:
        add_user_temp = User(username=name, password=generate_password_hash(password, method='scrypt'),hostname=hostname)
        # add_user_temp = User(username=name, password=password,hostname=hostname)
        db.session.add(add_user_temp)
        db.session.commit()
        user = User.query.filter_by(username=name).first()

    #connect via ssh Linux
    global ssh
    ssh = RemoteConnect(hostname,name,password,None)
    login_session = ssh.connect()

    print(login_session)

    #if connect failed index 3 from tuple is message
    if login_session["message"] is not None:
        flash('ชื่อผู้ใช้งาน/รหัสผ่านไม่ถูกต้อง กรุณาตรวจสอบข้อมูลใหม่อีกครั้ง')
        return redirect(url_for('auth.login'))
  
    login_user(user, remember=False)

    # next_url = request.args.get('next')

    if not next_url or urlparse(next_url).netloc != '':
        next_url = url_for('main.menu')

    #pass session user
    # session['username'] = name
    Config.SSH_SESSIONS[name] = ssh

    return redirect(next_url)
        

@auth.route('/logout')
@login_required
def logout():
    ssh = Config.SSH_SESSIONS.pop(current_user.username, None)
    if ssh:
        ssh.close()
    logout_user()
    return redirect(url_for('main.index'))