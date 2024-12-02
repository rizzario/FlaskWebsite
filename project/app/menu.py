import os
import sys
from flask import Blueprint, render_template,redirect,url_for,request,json
from flask_login import current_user
from .models import *
from .customer import *
# from models import *
# from customer import *

menu = Blueprint('menu',__name__)

@menu.before_request
def require_login():
    if not current_user.is_authenticated and request.endpoint != 'login':
        # Redirect to the login page with 'next' parameter
        return redirect(url_for('auth.login', next=request.path))

#Loading Json customer data
def load_data():
    def resource_path(relative_path):
        base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
        return os.path.join(base_path, relative_path)
    data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),'../static/json')
    json_url = os.path.join(data_path,"customer.json")
    # json_url = resource_path('static/json/customer.json')

    with open(json_url) as json_data:
        data = json.load(json_data)
    return data

json_data = load_data()

#Convert String name to model class for getting Table header
def get_model_class(model_name):
    model_class = globals().get(model_name)
    if model_class and issubclass(model_class, db.Model):
        return model_class
    else:
        return None
    
# #Get Row data via Model
def get_row_data(model):
    row_data = db.session.query(FCC).all()
    return row_data

def listfromData(val):
    menu_data = []
    row_data = get_row_data(val)
    for item in row_data:
        menu_data.append({column.name: getattr(item, column.name) for column in item.__table__.columns})
    return menu_data

@menu.route('/menu/automotive')
# @login_required
def automotive_index():
    return render_template('automotive/index.html', customer_list=json_data, name=current_user.username)

@menu.route('/menu/spring')
# @login_required
def spring_index():
    return render_template('spring/index.html', customer_list=json_data, name=current_user.username)

#Managing url route from json data

# def register_route():
#     json_data = load_data()
#     #Loading all route
#     for main_route in json_data:
#         for route in json_data[main_route]:
#             name = route['name']
#             path = route['path']
#             template = route['group'] + "/" + route['template']
#             model_class = get_model_class(name)
#             if model_class is not None:
#                 header_data = [column.name for column in model_class.__table__.columns]
#                 #Get row data
#                 table_data = listfromData(model_class)
#             else:
#                 header_data = None
#                 table_data = None

#             def view_function(template=template, header=header_data,row=table_data):
#                 response = make_response(render_template(template, header=header,row=row))
#                 # response = make_response(render_template(template))
#                 response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
#                 response.headers['Pragma'] = 'no-cache'
#                 response.headers['Expires'] = '0'
#                 return response

#             menu.add_url_rule(path,endpoint=name.lower(), view_func=login_required(view_function))

# register_route()

####################### FCC ##############################
classFCC = Customer_FCC()

@menu.route('/menu/spring/fcc',methods=['GET'])
def fcc():
    model_class = get_model_class("FCC")
    header_data = [column.name for column in model_class.__table__.columns]
    #Get row data
    table_data = listfromData(model_class)
    print(current_user.username)
    return render_template('spring/fcc.html',header=header_data, row=table_data, name=current_user.username)

@menu.route('/menu/spring/fcc/upload', methods=['POST'])
def fcc_upload_file():
    return classFCC.fcc_upload_file() #Process upload file and response json

@menu.route('/menu/spring/fcc/clear', methods=['POST'])
def fcc_clear_so():
    return classFCC.fcc_clear_so() #Running to clear sales order

@menu.route('/menu/spring/fcc/remove', methods=['POST'])
def fcc_clear_data():
    return classFCC.fcc_clear_data()

@menu.route('/menu/spring/fcc/cimcreate', methods=['POST'])
def fcc_cim_create():
    if 'export' in request.form:
        # Handle the export action
        print("export")
        return classFCC.fcc_export()
    elif 'ok' in request.form:
        print("ok")
        # Handle the ok action
        return classFCC.fcc_submit()

# @menu.route('/menu/spring/fcc/cimdownload', methods=['GET'])
# def fcc_download():
#     return classFCC.fcc_export()

@menu.route('/menu/spring/fcc/running', methods=['POST'])
def fcc_order_running():
    return classFCC.fcc_order_running()
####################### FCC ##############################

####################### Siam Aisin ##############################
classSiamAisin = Customer_SiamAisin()

@menu.route('/menu/spring/siam_aisin',methods=['GET'])
def siam_aisin():
    model_class = get_model_class("Siam_Aisin")
    header_data = [column.name for column in model_class.__table__.columns]
    #Get row data
    table_data = listfromData(model_class)
    print(current_user.username)
    return render_template('spring/siam_aisin.html',header=header_data, row=table_data, name=current_user.username)

@menu.route('/menu/spring/siam_aisin/upload', methods=['POST'])
def siam_aisin_upload_file():
    return classSiamAisin.siam_aisin_upload_file() #Process upload file and response json

@menu.route('/menu/spring/siam_aisin/clear', methods=['POST'])
def siam_aisin_clear_so():
    return classSiamAisin.siam_aisin_clear_so() #Running to clear sales order

@menu.route('/menu/spring/siam_aisin/remove', methods=['POST'])
def siam_aisin_clear_data():
    return classSiamAisin.siam_aisin_clear_data()

@menu.route('/menu/spring/siam_aisin/cimcreate', methods=['POST'])
def siam_aisin_cim_create():
    if 'export' in request.form:
        # Handle the export action
        print("export")
        return classSiamAisin.siam_aisin_export()
    elif 'ok' in request.form:
        print("ok")
        # Handle the ok action
        return classSiamAisin.siam_aisin_submit()

@menu.route('/menu/spring/siam_aisin/running', methods=['POST'])
def siam_aisin_order_running():
    return classSiamAisin.siam_aisin_order_running()
####################### Siam Aisin ##############################