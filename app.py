from flask import Flask , render_template ,url_for,request,redirect ,session ,flash

from flask_mysqldb import MySQL

import MySQLdb.cursors

import re



app=Flask(__name__)
app.secret_key = "Mdhiva911@"
#MYSQL CONNECTION
app.config["MYSQL_HOST"]="localhost"
app.config["MYSQL_USER"]="root"
app.config["MYSQL_PASSWORD"]="Mdhiva911@"
app.config["MYSQL_DB"]="sbi"
app.config["MYSQL_CURSORCLASS"]="DictCursor"
mysql=MySQL(app)


#Loading Home Page

@app.route("/")

def homepage():
      
   return render_template("home.html")



@app.route("/admin/", methods=['GET','POST'])
def admin():
    # Define a dictionary of validation conditions and corresponding request form values
    validation_conditions = {
        'Branch_code': request.form.get('Branch_code'),
        'Branch_manager': request.form.get('Branch_manager'),
        'Admin_Id_Number': request.form.get('Admin_Id_Number'),
        'Admin_password': request.form.get('Admin_password')
    }

    # Check if all validation conditions are met
    if all(validation_conditions.values()):
        Branch_code = validation_conditions['Branch_code']
        Branch_manager = validation_conditions['Branch_manager']
        Admin_Id_Number = validation_conditions['Admin_Id_Number']
        Admin_password = validation_conditions['Admin_password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM bank_details WHERE Branch_code = %s AND Branch_manager = %s AND Admin_Id_Number = %s AND Admin_password = %s", (Branch_code, Branch_manager, Admin_Id_Number, Admin_password,))
        res = cursor.fetchone()

        # Set session variables if validation conditions are met
        if res:
            session['admin-loggedin'] = True
            session['Branch_code'] = res['Branch_code']
            session['Branch_manager'] = res['Branch_manager']
            session['Admin_Id_Number'] = res['Admin_Id_Number']
            session['Admin_password'] = res['Admin_password']
            return redirect(url_for('ad_action'))
        else:
            return ('Invalid User')

    return render_template('admin.html')

@app.route("/ad-action")
def ad_action():
    return render_template("ad-action.html")
  
   
@app.route("/demo")
def user_details():
    con=mysql.connection.cursor()
    sql="SELECT * FROM customer_details"
    con.execute(sql)
    res=con.fetchall()
    return render_template("demo.html",datas=res)
    
    


#inserting a new user

@app.route("/ad-newuser/",methods=['GET','POST'])
def newuser():
    if request.method=='POST':
        branch=request.form['abranch']
        acc_number=request.form['anumber']
        cus_id=request.form['C_id']
        cus_name=request.form['C_name']
        contact=request.form['Mob_nu']
        add=request.form['aaddress']
        bal=request.form['balance']
        passw=request.form['psw']
        con=mysql.connection.cursor()
        sql="insert into customer_details(Branch_code,account_number,customer_id,customer_name,mobile_number,address,Balance,Password) value (%s,%s,%s,%s,%s,%s,%s,%s)"
        con.execute(sql,[branch,acc_number,cus_id,cus_name,contact,add,bal,passw])
        mysql.connection.commit()
        con.close()
        flash('User Details Added') 
        return redirect(url_for('ad_action'))

    return render_template('ad-newuser.html')


#editing the User details

@app.route("/edit/<string:id>",methods=['GET','POST'])

def edit(id):
    con=mysql.connection.cursor()
    if request.method=='POST':
        branch=request.form['abranch']
        cus_id=request.form['C_id']
        cus_name=request.form['C_name']
        contact=request.form['Mob_nu']
        add=request.form['aaddress']
        bal=request.form['balance']
        passw=request.form['psw']
        sql="UPDATE customer_details SET Branch_code = %s, customer_id = %s,customer_name = %s, mobile_number = %s,address = %s, Balance = %s,Password = %s WHERE account_number= %s" 
        con.execute(sql,[branch,cus_id,cus_name,contact,add,bal,passw,id])
        mysql.connection.commit()
        con.close()
        flash('User Detail Updated')
        return redirect(url_for("ad-action"))
        con=mysql.connection.cursor()
        
    sql="select * from customer_details WHERE account_number = %s"
    con.execute(sql,[id])
    res=con.fetchone()
    return render_template("edit.html", datas = res)  #, datas = res



# User login 

@app.route("/userlog/", methods=['GET', 'POST'])
def userlog():
    # Define a dictionary of validation conditions and corresponding request form values
    validation_conditions = {
        'account_number': request.form.get('account_number'),
        'customer_name': request.form.get('customer_name'),
        'customer_id': request.form.get('customer_id'),
        'Password': request.form.get('Password')
    }

    # Check if all validation conditions are met
    if all(validation_conditions.values()):
        account_number = validation_conditions['account_number']
        customer_name = validation_conditions['customer_name']
        customer_id = validation_conditions['customer_id']
        Password = validation_conditions['Password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM customer_details WHERE account_number = %s AND customer_name = %s AND customer_id = %s AND Password = %s", (account_number, customer_name, customer_id, Password,))
        res = cursor.fetchone()

        # Set session variables if validation conditions are met
        if res:
            session['user-loggedin'] = True
            session['account_number'] = res['account_number']
            session['customer_name'] = res['customer_name']
            session['customer_id'] = res['customer_id']
            session['Password'] = res['Password']
            return redirect(url_for('user_action'))
            
        if res:
            session['user-loggedin'] = True
            session['account_number'] = res['account_number']
            session['customer_name'] = res['customer_name']
            session['customer_id'] = res['customer_id']
            session['Password'] = res['Password']
            
            return redirect(url_for('transfer'))
        else:
            return ('Invalid User')

    return render_template('userlog.html')

@app.route("/user-action", methods=['GET', 'POST'])
def user_action():
    return render_template("user-action.html")


#Money Transfer
  
@app.route("/Transfer", methods=['GET', 'POST']) 
def transfer():
    return render_template("Transfer.html") 
  

    

#logout

@app.route('/logout') 
def logout():
    session.clear()
    return redirect(url_for('homepage'))

if __name__==('__main__'):
    app.run(debug=True) 
