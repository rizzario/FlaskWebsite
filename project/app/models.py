from flask_login import UserMixin
#from . import db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String)
    hostname = db.Column(db.String)

class FCC(db.Model):
    __tablename__ = 'FCC_ORD'
    sonbr = db.Column(db.String(8))
    sold_to = db.Column(db.String(8))
    ship_to = db.Column(db.String(8))
    po_no = db.Column(db.String(22))
    del_date = db.Column(db.String(8))
    site = db.Column(db.String(4))
    tax = db.Column(db.Boolean)
    taxclass = db.Column(db.String(3))
    pri_table = db.Column(db.String(4))
    ctype = db.Column(db.String(2))
    line = db.Column(db.Integer)
    part_no = db.Column(db.String(18))
    ord_qty = db.Column(db.Float)
    mfg_no = db.Column(db.String(20))
    model = db.Column(db.String(15))
    tflag = db.Column(db.String(1))
    pkindex = db.Column(db.String(20), primary_key=True)

class Siam_Aisin(db.Model):
    __tablename__ = 'SIAM_AISIN_ORD'
    sonbr = db.Column(db.String(8))
    sold_to = db.Column(db.String(8))
    ship_to = db.Column(db.String(8))
    po_no = db.Column(db.String(22))
    del_date = db.Column(db.String(8))
    site = db.Column(db.String(4))
    tax = db.Column(db.Boolean)
    taxclass = db.Column(db.String(3))
    pri_table = db.Column(db.String(4))
    ctype = db.Column(db.String(2))
    line = db.Column(db.Integer)
    part_no = db.Column(db.String(18))
    ord_qty = db.Column(db.Float)
    mfg_no = db.Column(db.String(20))
    model = db.Column(db.String(15))
    tflag = db.Column(db.String(1))
    pkindex = db.Column(db.String(20), primary_key=True)