import os
import csv
from datetime import datetime
import string
import random
from flask import request, jsonify, send_file
from flask_login import current_user
from werkzeug.utils import secure_filename
from .config import Config
from .models import *
from .ssh import RemoteConnect
# from config import Config
# from models import *
# from ssh import RemoteConnect

upload_folder = Config.UPLOAD_FOLDER
CSV_EXTENSIONS = Config.CSV_EXTENSIONS
TXT_EXTENSIONS = Config.TXT_EXTENSIONS

os.makedirs(upload_folder, exist_ok=True)

def cim_sales_order_head(cim_str,so_data):
    cim_str = cim_str + '@@batchload k7sosomt.p\n' #Initial batch load
    cim_str = cim_str + '"' + so_data["sonbr"] + '"' + '\n' #Sales order number
    cim_str = cim_str + '"' + so_data["sold"] + '"' + ' - ' + '"' + so_data["ship"] + '"' + '\n' #Customer
    cim_str = cim_str + '\n' #F1 as new line
    cim_str = cim_str + '\n' #F1 as new line
    cim_str = cim_str + so_data["ord_date"] + ' ' + so_data["req_date"] + ' '
    cim_str = cim_str + so_data["pro_date"] + ' ' + so_data["due_date"] + ' '
    cim_str = cim_str + so_data["pfm_date"] + ' ' + so_data["pri_date"] + ' '
    cim_str = cim_str + '"' + so_data["po_no"] + '" ' + so_data["rmk"] + ' '
    cim_str = cim_str + '"yes" "' + so_data["pri_table"] + '" "AR-SET" - - - - - '
    cim_str = cim_str + '"' + so_data["tax"] + '" "' + so_data["taxclass"] + '" - - - "' + so_data["site"] + '"\n'
    cim_str = cim_str + '- - "' + so_data["taxclass"] + '" - -\n'
    if so_data["so_cmmt"] == "yes":
        cim_str = cim_str + '- - - - - - - - - - - "yes"\n'
    else:
        cim_str = cim_str + '- - - - - - - - - - - "no"\n'
    return cim_str

def cim_sales_order_line(cim_str,so_data):
    cim_str = cim_str + str(so_data["line"]) + '\n'
    cim_str = cim_str + '"' + so_data["part_no"] + '"\n'
    cim_str = cim_str + '"' + so_data["site"] + '"\n'
    cim_str = cim_str + "{:.2f}".format(so_data["ord_qty"]) + '\n'
    cim_str = cim_str + '\n'  #F1 as new line
    cim_str = cim_str + '\n'  #F1 as new line
    cim_str = cim_str + '\n'  #F1 as new line
    cim_str = cim_str + '- - - - - - - - - - - - - - '
    cim_str = cim_str + so_data["due_date"] + ' - - - - - - '
    cim_str = cim_str + '"' + so_data["tax"] + '" "' + so_data["taxclass"] + '" - - '
    if so_data["sod_cmmt"] == "yes":
        cim_str = cim_str + '"yes"\n'
        cim_str = cim_str + '"' + so_data["po_no"] + '"\n'
        cim_str = cim_str + '\n' #F1 as new line
        cim_str = cim_str + '\n' #F1 as new line
        cim_str = cim_str + '"' + so_data["sod_cmmtval"] + '"\n'
        cim_str = cim_str + '\n' #F1 as new line
        cim_str = cim_str + '.\n' #F4 as .
    else:
        cim_str = cim_str + '"no"\n'
        cim_str = cim_str + '"' + so_data["po_no"] + '"\n'
        cim_str = cim_str + '\n' #F1 as new line
    return cim_str

def cim_sales_order_end(cim_str,so_data):
    cim_str = cim_str + '.\n' #F4 as .
    cim_str = cim_str + '.\n' #F4 as .
    cim_str = cim_str + '\n'  #F1 as new line
    cim_str = cim_str + '- - - - - ' #CR Init, Credit Card, Action Stat, Rev, EDI PO
    cim_str = cim_str + '- - - - - ' #Print SO, Print Pck, Print Inv, EDI Inv, Partial
    cim_str = cim_str + '- ' + so_data["fob"] + ' ' + so_data["shipvia"] + ' ' + so_data["bol"] + '\n'
    cim_str = cim_str + '.\n' #F4 as .
    cim_str = cim_str + '@@end\n'
    return cim_str

####################### FCC ##############################
class Customer_FCC:
    #Check file type (FCC)
    def fcc_allowed_file(self,filename):
        for ext in CSV_EXTENSIONS:
            if '.' in filename:
                for quote in filename.lower().rsplit('.',1):
                    if quote in ext:
                        return True
        return False

    #Get data from (FCC)
    def fcc_fetch_header(self):
        header_data = [column.name for column in FCC.__table__.columns]
        return header_data
    def fcc_fetch_data():
        row_data = db.session.query(FCC).all()
        menu_data = []
        for item in row_data:
            menu_data.append({column.name: getattr(item, column.name) for column in item.__table__.columns})
        return menu_data

    #Read csv data (FCC) and first upload to database
    def fcc_order_get(self,csvfile,soldto,shipto,site,taxclass,pri_table):
        with open(csvfile, 'r', encoding='utf-8-sig') as file:
            csv_file = csv.reader(file)
            next(csv_file)
            try:
                for row in csv_file:
                    #Packing Data
                    part_no = row[0]
                    po_no = row[5]
                    mfg_no = row[3]
                    model = row[4]
                    ord_qty = float(row[2])
                    deldate = datetime.strptime(row[1], "%d/%m/%Y")
                    sdeldate = str(deldate.year) + str('{:02d}'.format(deldate.month)) + str(deldate.day) 
                    pkindex = ''.join(random.choices(string.ascii_letters + string.digits, k=20))
                    #Insert Packing Data
                    Packing_data = FCC(
                                sold_to=soldto,
                                ship_to=shipto,
                                site=site,
                                tax=True,
                                taxclass=taxclass,
                                pri_table=pri_table,
                                part_no=part_no,
                                po_no=po_no,
                                ord_qty=ord_qty,
                                mfg_no=mfg_no,
                                model=model,
                                del_date=sdeldate,
                                pkindex=pkindex)
                    db.session.add(Packing_data)
                    db.session.commit()
            except :
                return False #Error because of inserting data
                
            return True

        return False

    #Clear sales order
    def fcc_clear_so(self):
        db.session.query(FCC).update(dict(sonbr=''))
        db.session.commit()
        return jsonify({"success": True, "message": "Clear all sales order success!"})
    
    #Clear data
    def fcc_clear_data(self):
        soempty = ""
        db.session.query(FCC).filter(FCC.pkindex != soempty).delete()
        db.session.commit()
        return jsonify({"success": True, "message": "Clear all data success!"})

    #Create CIM data
    def fcc_cim_crate(self,filepath,cimfilename,filesuffix):
        try:
            cimdata = db.session.query(FCC).order_by(FCC.sonbr.asc(), FCC.line.asc()).all()
            strcim = ""
            cim_dict = {}
            for index, order in enumerate(cimdata, start=1):
                #So_mstr header
                cim_dict["sonbr"] = str(order.sonbr).upper()
                cim_dict["sold"] = str(order.sold_to).upper()
                cim_dict["ship"] = str(order.ship_to).upper()
                cim_dict["ord_date"] = '-'
                cim_dict["req_date"] = '-'
                cim_dict["pro_date"] = '-'
                deldate = datetime.strptime(order.del_date, "%Y%m%d")
                sdeldate = deldate.strftime("%d/%m/%y")
                cim_dict["due_date"] = '"' + sdeldate + '"'
                cim_dict["pfm_date"] = '-'
                cim_dict["pri_date"] = '-'
                cim_dict["pri_table"] = str(order.pri_table).upper()
                cim_dict["po_no"] = order.po_no
                cim_dict["rmk"] = '-'
                if order.tax == True or order.tax == "true":
                    cim_dict["tax"] = 'yes'
                    cim_dict["taxclass"] = order.taxclass
                else:
                    cim_dict["tax"] = 'no'
                    cim_dict["taxclass"] = '-'
                cim_dict["site"] = order.site
                cim_dict["so_cmmt"] = "no" #Default for FCC
                #Sod_det detail
                cim_dict["line"] = order.line
                cim_dict["part_no"] = order.part_no
                cim_dict["ord_qty"] = order.ord_qty
                cim_dict["sod_cmmt"] = "yes" #Default for FCC
                cim_dict["sod_cmmtval"] = order.mfg_no #Default for FCC
                cim_dict["fob"] = '"' + order.model + '"'
                cim_dict["shipvia"] = '-'
                cim_dict["bol"] = '"' + order.model + '"'
                #Create CIM file
                if order.line == 1:
                    if index == 1:
                        strcim = '\n'
                        strcim = cim_sales_order_head(strcim,cim_dict)
                    else:
                        strcim = cim_sales_order_end(strcim,cim_dict)
                        strcim = cim_sales_order_head(strcim,cim_dict)
                strcim = cim_sales_order_line(strcim,cim_dict)
                if index == len(cimdata):
                    strcim = cim_sales_order_end(strcim,cim_dict)
            with open(os.path.join(upload_folder,cimfilename + filesuffix), "w", newline="\n") as file:
                #Write text into CIM file
                file.write(strcim)
            return True
        except Exception as e:
            print(f"Error while try to created cim file: {e}")
            return False
    
    def get_user_session(self):
        user = db.session.query(User).filter_by(username=current_user.username).first()
        return user
    
    def fcc_export(self):
        # Check if the input text from the client-side request is empty
        input_text = request.form.get('outputfile_fcc', '').strip()  # Retrieve input text from form data
        if not input_text:
            return jsonify({"success": False, "message": f"Error occurred during file download"})
        
        cimfilename = "fcc_export"
        filepath = ""
        filesuffix = ".cim"
        cimpath = os.path.join(os.path.abspath(upload_folder), cimfilename + filesuffix)
        if self.fcc_cim_crate(filepath,cimfilename,filesuffix):
            try:
                return send_file(cimpath, as_attachment=True, download_name=cimfilename + filesuffix)
            except Exception as e:
                return jsonify({"success": False, "message": f"Error occurred during file download: {str(e)}"})

    def fcc_submit(self):
        cimfilename = request.form.get("outputfile_fcc")
        filepath = ""
        filesuffix = ".cim"
        cimpath = os.path.join(upload_folder, cimfilename + filesuffix)
        user = self.get_user_session()
        print(user.username)
        if self.fcc_cim_crate(filepath,cimfilename,filesuffix):
            
            client = Config.SSH_SESSIONS.get(user.username)
            print("client session for:", current_user.username, client)
            if client:
                session = client.get_session()
                if session:
                    client.upload(cimpath) #Upload to FTP
                    os.remove(cimpath) #Delete file from temporary folder
                    return jsonify({"success": True, "message": "Create CIM file and FTP success!, Filename is: " + cimfilename + filesuffix})
                else:
                    return jsonify({"success": False, "message": "Inactive session; unable to upload CIM file."})
            else:
                return jsonify({"success": False, "message": "No SSH session found for user."})
            

    #Sales order running
    def fcc_order_running(self):
        sorunning = request.form.get("running_fcc")
        soempty = "" #Declare empty value
        so_found = db.session.query(FCC).filter_by(sonbr=sorunning).all()
        if so_found:
            return jsonify({"success": False, "message": "Sales Order duplicate! Please re-input sales order number again!"})
        so_not_emp = db.session.query(FCC).filter_by(sonbr=soempty).all()
        so_none = db.session.query(FCC).filter_by(sonbr=None).all()
        if (not so_not_emp) and (not so_none):
            return jsonify({"success": False, "message": "No data to process! Sales Order Number is not empty!"})
        
        so_data = db.session.query(FCC).order_by(FCC.model.asc()).all()

        def update_salesorder(value,num):
            salesorder_update = ""
            if num < 10:
                salesorder_update = value[:-3] + "00" + str(num)
            elif rightorder >= 10 and rightorder < 100:
                salesorder_update = value[:-3] + "0" + str(num)
            elif rightorder >= 100:
                salesorder_update = value[:-3] + str(num)
            
            return salesorder_update

        #Declare for first records before update
        temp_model = ""
        cline = 1
        update_sorunning = sorunning
        for index, order in enumerate(so_data, start=1):
            #Update at first record
            if index == 1:
                temp_model = order.model
            if temp_model == order.model and cline <= 6:
                if order.sonbr == '' or order.sonbr == None:
                    order.sonbr = update_sorunning
                    order.line = cline
            if temp_model != order.model or cline > 6:
                cline = 1
                order.line = cline
                rightorder = int(update_sorunning[-3:]) + 1
                update_sorunning = update_salesorder(update_sorunning, rightorder)
                order.sonbr = update_sorunning
            cline += 1
            temp_model = order.model

        db.session.commit()

        #Get next sales order number
        update_sorunning = update_salesorder(update_sorunning, rightorder + 1)
        return jsonify({"success": True, "message": "Running Number Complete, Next Start Sales Order Number: " + update_sorunning})
        

    #Upload file to server (this server)
    def fcc_upload_file(self):
        if 'file' not in request.files:
            return jsonify({"success": False, "message": "No file selected!"})

        file = request.files['file']

        soldto = request.form.get("soldto_fcc").strip()
        shipto = request.form.get("shipto_fcc").strip()
        site = request.form.get("site_fcc").strip()
        taxclass = request.form.get("taxclass_fcc").strip()
        pri_table = request.form.get("PriceTbl_fcc").strip()

        if soldto == "" or shipto == "" or site == "" or taxclass == "" or pri_table == "":
            return jsonify({"success": False, "message": "Form fields must not be blank!"})

        if file.filename == '':
            return jsonify({"success": False, "message": "No selected file!"})
        
        print(request.form.get("transfer_submit_fcc"))
        
        if file and self.fcc_allowed_file(file.filename):
            filename = secure_filename(file.filename)
            local_filepath = os.path.join(upload_folder, filename)
            file.save(local_filepath)
            print(local_filepath)
            if self.fcc_order_get(local_filepath,soldto,shipto,site,taxclass,pri_table):
                print("we are here")
                return jsonify({"success": True, "message": "File uploaded sucess!"})

            else:
                print("we are going to the wrong way!")
                return jsonify({"success": False, "message": "Incorrect format file for upload!"})
        
####################### FCC ##############################

####################### Siam Aisin ##############################
class Customer_SiamAisin:
    #Check file type (Siam Aisin)
    def siam_aisin_allowed_file(self,filename):
        for ext in CSV_EXTENSIONS:
            if '.' in filename:
                for quote in filename.lower().rsplit('.',1):
                    if quote in ext:
                        return True
        return False

    #Get data from (Siam Aisin)
    def siam_aisin_fetch_header(self):
        header_data = [column.name for column in Siam_Aisin.__table__.columns]
        return header_data
    def siam_aisin_fetch_data():
        row_data = db.session.query(Siam_Aisin).all()
        menu_data = []
        for item in row_data:
            menu_data.append({column.name: getattr(item, column.name) for column in item.__table__.columns})
        return menu_data

    #Read csv data (Siam Aisin) and first upload to database
    def siam_aisin_order_get(self,csvfile,soldto,shipto,site,taxclass,pri_table):
        with open(csvfile, 'r', encoding='utf-8-sig') as file:
            csv_file = csv.reader(file)
            next(csv_file)
            try:
                for row in csv_file:
                    #Packing Data
                    part_no = row[0]
                    po_no = row[5]
                    mfg_no = row[3]
                    model = row[4]
                    ord_qty = float(row[2])
                    deldate = datetime.strptime(row[1], "%d/%m/%Y")
                    sdeldate = str(deldate.year) + str('{:02d}'.format(deldate.month)) + str(deldate.day) 
                    pkindex = ''.join(random.choices(string.ascii_letters + string.digits, k=20))
                    #Insert Packing Data
                    Packing_data = Siam_Aisin(
                                sold_to=soldto,
                                ship_to=shipto,
                                site=site,
                                tax=True,
                                taxclass=taxclass,
                                pri_table=pri_table,
                                part_no=part_no,
                                po_no=po_no,
                                ord_qty=ord_qty,
                                mfg_no=mfg_no,
                                model=model,
                                del_date=sdeldate,
                                pkindex=pkindex)
                    db.session.add(Packing_data)
                    db.session.commit()
            except :
                return False #Error because of inserting data
                
            return True

        return False

    #Clear sales order
    def siam_aisin_clear_so(self):
        db.session.query(Siam_Aisin).update(dict(sonbr=''))
        db.session.commit()
        return jsonify({"success": True, "message": "Clear all sales order success!"})
    
    #Clear data
    def siam_aisin_clear_data(self):
        soempty = ""
        db.session.query(Siam_Aisin).filter(Siam_Aisin.pkindex != soempty).delete()
        db.session.commit()
        return jsonify({"success": True, "message": "Clear all data success!"})

    #Create CIM data
    def siam_aisin_cim_crate(self,filepath,cimfilename,filesuffix):
        try:
            cimdata = db.session.query(Siam_Aisin).order_by(Siam_Aisin.sonbr.asc(), Siam_Aisin.line.asc()).all()
            strcim = ""
            cim_dict = {}
            for index, order in enumerate(cimdata, start=1):
                #So_mstr header
                cim_dict["sonbr"] = str(order.sonbr).upper()
                cim_dict["sold"] = str(order.sold_to).upper()
                cim_dict["ship"] = str(order.ship_to).upper()
                cim_dict["ord_date"] = '-'
                cim_dict["req_date"] = '-'
                cim_dict["pro_date"] = '-'
                deldate = datetime.strptime(order.del_date, "%Y%m%d")
                sdeldate = deldate.strftime("%d/%m/%y")
                cim_dict["due_date"] = '"' + sdeldate + '"'
                cim_dict["pfm_date"] = '-'
                cim_dict["pri_date"] = '-'
                cim_dict["pri_table"] = str(order.pri_table).upper()
                cim_dict["po_no"] = order.po_no
                cim_dict["rmk"] = '-'
                if order.tax == True or order.tax == "true":
                    cim_dict["tax"] = 'yes'
                    cim_dict["taxclass"] = order.taxclass
                else:
                    cim_dict["tax"] = 'no'
                    cim_dict["taxclass"] = '-'
                cim_dict["site"] = order.site
                cim_dict["so_cmmt"] = "no" #Default for Siam Aisin
                #Sod_det detail
                cim_dict["line"] = order.line
                cim_dict["part_no"] = order.part_no
                cim_dict["ord_qty"] = order.ord_qty
                cim_dict["sod_cmmt"] = "yes" #Default for Siam Aisin
                cim_dict["sod_cmmtval"] = order.mfg_no #Default for Siam Aisin
                cim_dict["fob"] = '"' + order.model + '"'
                cim_dict["shipvia"] = '-'
                cim_dict["bol"] = '"' + order.model + '"'
                #Create CIM file
                if order.line == 1:
                    if index == 1:
                        strcim = '\n'
                        strcim = cim_sales_order_head(strcim,cim_dict)
                    else:
                        strcim = cim_sales_order_end(strcim,cim_dict)
                        strcim = cim_sales_order_head(strcim,cim_dict)
                strcim = cim_sales_order_line(strcim,cim_dict)
                if index == len(cimdata):
                    strcim = cim_sales_order_end(strcim,cim_dict)
            with open(os.path.join(upload_folder,cimfilename + filesuffix), "w", newline="\n") as file:
                #Write text into CIM file
                file.write(strcim)
            return True
        except Exception as e:
            print(f"Error while try to created cim file: {e}")
            return False
    
    def get_user_session(self):
        user = db.session.query(User).filter_by(username=current_user.username).first()
        return user
    
    def siam_aisin_export(self):
        # Check if the input text from the client-side request is empty
        input_text = request.form.get('outputfile_siam_aisin', '').strip()  # Retrieve input text from form data
        if not input_text:
            return jsonify({"success": False, "message": f"Error occurred during file download"})
        
        cimfilename = "siam_aisin_export"
        filepath = ""
        filesuffix = ".cim"
        cimpath = os.path.join(os.path.abspath(upload_folder), cimfilename + filesuffix)
        if self.siam_aisin_cim_crate(filepath,cimfilename,filesuffix):
            try:
                return send_file(cimpath, as_attachment=True, download_name=cimfilename + filesuffix)
            except Exception as e:
                return jsonify({"success": False, "message": f"Error occurred during file download: {str(e)}"})

    def siam_aisin_submit(self):
        cimfilename = request.form.get("outputfile_siam_aisin")
        filepath = ""
        filesuffix = ".cim"
        cimpath = os.path.join(upload_folder, cimfilename + filesuffix)
        user = self.get_user_session()
        print(user.username)
        if self.siam_aisin_cim_crate(filepath,cimfilename,filesuffix):
            
            client = Config.SSH_SESSIONS.get(user.username)
            print("client session for:", current_user.username, client)
            if client:
                session = client.get_session()
                if session:
                    client.upload(cimpath) #Upload to FTP
                    os.remove(cimpath) #Delete file from temporary folder
                    return jsonify({"success": True, "message": "Create CIM file and FTP success!, Filename is: " + cimfilename + filesuffix})
                else:
                    return jsonify({"success": False, "message": "Inactive session; unable to upload CIM file."})
            else:
                return jsonify({"success": False, "message": "No SSH session found for user."})
            

    #Sales order running
    def siam_aisin_order_running(self):
        sorunning = request.form.get("running_siam_aisin")
        soempty = "" #Declare empty value
        so_found = db.session.query(Siam_Aisin).filter_by(sonbr=sorunning).all()
        if so_found:
            return jsonify({"success": False, "message": "Sales Order duplicate! Please re-input sales order number again!"})
        so_not_emp = db.session.query(Siam_Aisin).filter_by(sonbr=soempty).all()
        so_none = db.session.query(Siam_Aisin).filter_by(sonbr=None).all()
        if (not so_not_emp) and (not so_none):
            return jsonify({"success": False, "message": "No data to process! Sales Order Number is not empty!"})
        
        so_data = db.session.query(Siam_Aisin).order_by(Siam_Aisin.model.asc()).all()

        def update_salesorder(value,num):
            salesorder_update = ""
            if num < 10:
                salesorder_update = value[:-3] + "00" + str(num)
            elif rightorder >= 10 and rightorder < 100:
                salesorder_update = value[:-3] + "0" + str(num)
            elif rightorder >= 100:
                salesorder_update = value[:-3] + str(num)
            
            return salesorder_update

        #Declare for first records before update
        temp_model = ""
        cline = 1
        update_sorunning = sorunning
        for index, order in enumerate(so_data, start=1):
            #Update at first record
            if index == 1:
                temp_model = order.model
            if temp_model == order.model and cline <= 6:
                if order.sonbr == '' or order.sonbr == None:
                    order.sonbr = update_sorunning
                    order.line = cline
            if temp_model != order.model or cline > 6:
                cline = 1
                order.line = cline
                rightorder = int(update_sorunning[-3:]) + 1
                update_sorunning = update_salesorder(update_sorunning, rightorder)
                order.sonbr = update_sorunning
            cline += 1
            temp_model = order.model

        db.session.commit()

        #Get next sales order number
        update_sorunning = update_salesorder(update_sorunning, rightorder + 1)
        return jsonify({"success": True, "message": "Running Number Complete, Next Start Sales Order Number: " + update_sorunning})
        

    #Upload file to server (this server)
    def siam_aisin_upload_file(self):
        if 'file' not in request.files:
            return jsonify({"success": False, "message": "No file selected!"})

        file = request.files['file']

        soldto = request.form.get("soldto_siam_aisin").strip()
        shipto = request.form.get("shipto_siam_aisin").strip()
        site = request.form.get("site_siam_aisin").strip()
        taxclass = request.form.get("taxclass_siam_aisin").strip()
        pri_table = request.form.get("PriceTbl_siam_aisin").strip()

        if soldto == "" or shipto == "" or site == "" or taxclass == "" or pri_table == "":
            return jsonify({"success": False, "message": "Form fields must not be blank!"})

        if file.filename == '':
            return jsonify({"success": False, "message": "No selected file!"})
        
        print(request.form.get("transfer_submit_siam_aisin"))
        
        if file and self.siam_aisin_allowed_file(file.filename):
            filename = secure_filename(file.filename)
            local_filepath = os.path.join(upload_folder, filename)
            file.save(local_filepath)
            print(local_filepath)
            if self.siam_aisin_order_get(local_filepath,soldto,shipto,site,taxclass,pri_table):
                print("we are here")
                return jsonify({"success": True, "message": "File uploaded sucess!"})

            else:
                print("we are going to the wrong way!")
                return jsonify({"success": False, "message": "Incorrect format file for upload!"})
        
####################### Siam Aisin ##############################