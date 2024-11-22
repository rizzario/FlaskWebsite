from flask import Flask, render_template
from flask_login import LoginManager, current_user
import os
import socket
from .models import db, User
from .config import Config
# from models import db, User
# from config import Config
# from project.app.models import db, User
# from project.app.config import Config

# app = Flask(__name__,
#                 static_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)),'../static'),
#                 template_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)),'../templates'))

def create_app():
    app = Flask(__name__,
                static_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)),'../static'),
                template_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)),'../templates'))
    app.url_map.strict_slashes = False

    app.config.from_object(Config)

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    @app.errorhandler(404)
    def page_not_found(e):
        if current_user.is_authenticated:
            return render_template('404.html', name=current_user.username), 404
        else:
            return render_template('404.html'), 404

    # from auth import auth as auth_blueprint
    from .auth import auth as auth_blueprint
    # from app.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)
    # from main import main as main_blueprint
    from .main import main as main_blueprint
    # from app.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    with app.app_context():
        # from menu import menu as menu_blueprint
        from .menu import menu as menu_blueprint
        # from app.menu import menu as menu_blueprint
        app.register_blueprint(menu_blueprint)
        db.create_all() #using for deploy
    
    # print(list(app.url_map.iter_rules()))
    # print(list(app.url_map.iter_rules()))
    return app

if __name__ == "__main__":
    hostname = socket.gethostname()
    url = "https://" + hostname
    ipaddress = socket.gethostbyname(hostname)
    cert_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),'../certs')
    
    app = create_app()
    with app.app_context():
        db.create_all() #using for test
    app.run(host=hostname,
             #ssl_context=(os.path.join(cert_path,"cert.pem"), 
             #             os.path.join(cert_path,"key.pem")),
             debug=True) #for test
 