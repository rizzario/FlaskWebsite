#import os
class Config:
    SECRET_KEY = 'ssh-temporary-db'
   #SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(basedir,'db.sqlite')}'
   #SQLALCHEMY_DATABASE_URI = f'DRIVER{{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://postgres:1234@localhost:5432/NHKDB'
    # SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://nhkadmin:e6Ls6sLjCAHRla3xnysOhvaKzXFasck8@dpg-csbfr65ds78s73b6qm70-a:5432/nhkdb' #Production
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # FLASK_APP = 'project/app'
    # FLASK_DEBUG = 1
    UPLOAD_FOLDER = 'project/uploads'
    CSV_EXTENSIONS = {'csv'}
    TXT_EXTENSIONS = {'txt'}
    ALL_EXTENSIONS = {'txt','csv'}
    APPLICATION_ROOT = 'project/app'
    SSH_SESSIONS = {}
    # PREFERRED_URL_SCHEME = 'http'  # Or 'http' if not using SSL