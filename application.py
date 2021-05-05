from flask import Flask, render_template,request,flash,session,url_for,redirect,session,jsonify,g,send_file,send_from_directory
from flask_sqlalchemy import SQLAlchemy
from passlib.hash import sha256_crypt
from forms import RegistrationForm,LoginForm,TeacherRegistrationForm,EditProfileForm,EditTeacherProfile,RequestResetForm, ResetPasswordForm,ChangePasswordForm,StudentRegistrationForm,AdminTeacherRegistrationForm
from flask_mail import Mail,Message
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo
import json
from flask_mysqldb import MySQL
import MySQLdb.cursors 
from flask_bcrypt import Bcrypt
from flask_login import LoginManager,logout_user,login_user, current_user, logout_user, login_required
from datetime import datetime, date

from werkzeug.utils import secure_filename
import urllib.request
import os
from io import BytesIO

import uuid
import urllib.parse

with open('config.json', 'r') as c:
    params = json.load(c)["params"]

app = Flask(__name__)
app.config.update(
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = '465',
    MAIL_USE_SSL = True,
	MAIL_USE_TLS = False,
    MAIL_USERNAME = 'studentassignmentportal12@gmail.com',
    MAIL_PASSWORD=  '181267174'
)
mail = Mail(app)
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+mysqlconnector://root:@localhost/student'.format(user='root', password='', server='localhost', database='student')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'student'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app) 
db = SQLAlchemy(app)
bcrypt=Bcrypt(app)
login_manager=LoginManager(app)

@app.before_request
def before_request():
	g.email=None
	if 'email'  in session:
		g.email=session['email']

class Register(db.Model):
	name = db.Column(db.String(80),	unique=False,	nullable=False)
	email = db.Column(db.String(80),	unique=True,	primary_key=True,	nullable=False)
	Enrollment = db.Column(db.String(11), 	unique=True,	primary_key=True,	nullable=False)
	Gender = db.Column(db.String(120),	nullable=False)
	birth = db.Column(db.String(12),	nullable=False)
	contact = db.Column(db.String(20),	nullable=False)
	semester = db.Column(db.String(120),	nullable=False)
	city = db.Column(db.String(120),	nullable=False)
	state = db.Column(db.String(120),	nullable=False)
	Address = db.Column(db.String(120),	nullable=False)
	pincode = db.Column(db.String(120),	nullable=False)
	password = db.Column(db.String(120),	nullable=False)
	confirm_password = db.Column(db.String(120),nullable=False)
	authorization = db.Column(db.String(120),	nullable=False)

class Teacherregister(db.Model):
	name = db.Column(db.String(80),	unique=False,	nullable=False)
	email = db.Column(db.String(80),	unique=True,	primary_key=True,	nullable=False)
	Tid = db.Column(db.String(11), 	unique=True,	primary_key=True,	nullable=False)
	Gender = db.Column(db.String(120),	nullable=False)
	birth = db.Column(db.String(12),	nullable=False)
	contact = db.Column(db.String(20),	nullable=False)
	department = db.Column(db.String(120),	nullable=False)
	qualifications = db.Column(db.String(120),	nullable=False)
	designation = db.Column(db.String(120),	nullable=False)
	Address = db.Column(db.String(120),	nullable=False)
	pincode = db.Column(db.String(120),	nullable=False)
	password = db.Column(db.String(120),	nullable=False)
	confirm_password = db.Column(db.String(120),nullable=False)
	authorization = db.Column(db.String(120),	nullable=False)

class Subjectdetail(db.Model):
	sname = db.Column(db.String(80),	unique=False,	nullable=False)
	scode = db.Column(db.String(80),	unique=False,	nullable=False)
	sem = db.Column(db.String(80),	unique=False,	nullable=False)
	name = db.Column(db.String(80),	unique=False,	nullable=False)
	email = db.Column(db.String(80),	unique=True,	primary_key=True,	nullable=False)
	Tid = db.Column(db.String(11), 	unique=True,	primary_key=True,	nullable=False)

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/register", methods=['GET', 'POST'])
def register():
	form = RegistrationForm(request.form)
	if request.method=='POST' and form.validate_on_submit():
		name = request.form.get('name')
		email = request.form.get('email')
		Enrollment = request.form.get('Enrollment')
		Gender = request.form.get('Gender')
		birth = request.form.get('birth')
		contact = request.form.get('contact')
		semester = request.form.get('semester')
		city = request.form.get('city')
		authorization = request.form.get('authorization')
		state = request.form.get('state')
		Address = request.form.get('Address')
		pincode = request.form.get('pincode')
		password = request.form.get('password')
		confirm_password = request.form.get('confirm_password')
		secure_password = bcrypt.generate_password_hash(password).decode('utf-8')
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor) 
		result=cursor.execute('SELECT * FROM register WHERE email = % s ', [email])
		result1=cursor.execute('SELECT * FROM register WHERE Enrollment = % s ', [Enrollment])
		if result>0:
			flash('That Email is already Registered, please choose another','danger')
			return render_template('register.html', form=form)
		elif result1>0:
			flash('That Enrollment is already Registered, please choose another','danger')
			return render_template('register.html', form=form)
		else:
			entry = Register(name=name,email = email,Enrollment = Enrollment,Gender = Gender,birth= birth,contact=contact,semester = semester,city = city,state = state,Address = Address,pincode = pincode,password = secure_password,confirm_password=secure_password,authorization=authorization)
			db.session.add(entry)
			db.session.commit()
			msg=Message(subject="New message from Student Assignment Submission Portal",sender='studentassignmentportal12@gmail.com',recipients =[email])
			msg.html=render_template("email.html",name=name,Enrollment=Enrollment)
			mail.send(msg)
			flash(f'Account created for {form.email.data}!', 'success')
			return redirect(url_for('register'))
	return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
	form = LoginForm(request.form)
	if g.email:
		return redirect(url_for('stsignup'))
	if request.method=='POST' and form.validate_on_submit() and 'email' in request.form and 'password' in request.form:
		email=request.form.get('email')
		password1 = request.form.get('password')
		#secure_password = bcrypt.generate_password_hash('password').decode('utf-8')
		#secure_pass = sha256_crypt.verify("password",secure_password)
		#secure_pass=bcrypt.check_password_hash(secure_password,password)
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor) 
		result=cursor.execute('SELECT * FROM register WHERE email = % s ', [email])    
		if result>0:
			register = cursor.fetchone()
			password=register['password']
			if bcrypt.check_password_hash(password,password1):
				session['loggedin']=True
				session['email']=register['email'] 
				session['name']=register['name']
				session['Enrollment']=register['Enrollment']
				session['Gender']=register['Gender']
				session['birth']=register['birth']
				session['contact']=register['contact']
				session['semester']=register['semester']
				session['city']=register['city']
				session['state']=register['state']
				session['Address']=register['Address']
				session['pincode']=register['pincode']
				session['authorization']=register['authorization']
				flash('You have been logged in!', 'success')
				return redirect(url_for('stsignup'))
				cursor.close() 
			else:
				flash('Password is incorrect','danger')
		else: 
			flash('Login Unsuccessful. Please check email and password', 'danger')
	return render_template('login.html', title='Login', form=form)

@app.route("/stsignup")
def stsignup():
	if g.email:
		cursor = mysql.connection.cursor()
		cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cur.execute('SELECT * FROM announcement')
		data = cur.fetchall()
		cur.close()
		return render_template('/StudentLogin/index.html',email=session['email'],name=session['name'],Enrollment=session['Enrollment'],Gender=session['Gender'],birth=session['birth'],contact=session['contact'],semester=session['semester'],city=['city'],state=session['state'],Address=session['Address'],pincode=session['pincode'],authorization=session['authorization'],showannounce=data)
	return redirect(url_for('login'))

@app.route('/studentprofile/edit_profile', methods=['GET', 'POST'])
def edit_profile():
	if g.email:
		form = EditProfileForm(request.form)
		if form.validate_on_submit():
			session['email'] = form.email.data
			session['name'] = form.name.data
			session['Enrollment'] = form.Enrollment.data
			session['Gender'] = form.Gender.data
			session['birth'] = form.birth.data
			session['contact'] = form.contact.data
			session['semester'] = form.semester.data
			session['city'] = form.city.data
			session['state'] = form.state.data
			session['Address'] = form.Address.data
			session['pincode'] = form.pincode.data
		elif request.method == 'GET':
			form.email.data = session['email']
			form.name.data = session['name']
			form.Enrollment.data = session['Enrollment']
			form.Gender.data = session['Gender']
			birth = session['birth']
			birth = datetime.strptime(birth, '%a, %d %b %Y %H:%M:%S GMT')
			birth = birth.strftime("%d-%m-%Y")
			form.contact.data = session['contact']
			form.semester.data = session['semester']
			form.city.data = session['city']
			form.state.data = session['state']
			form.Address.data = session['Address']
			form.pincode.data = session['pincode']
		return render_template('/StudentLogin/edit_profile.html', title='Edit Profile',form=form)
	return redirect(url_for('login'))

@app.route('/teacherprofile/teacher_edit_profile', methods=['GET', 'POST'])
def teacher_edit_profile():
	if g.email:
		form = EditTeacherProfile(request.form)
		if form.validate_on_submit():
			g.email = form.email.data
			session['name'] = form.name.data
			session['Tid'] = form.Tid.data
			session['Gender'] = form.Gender.data
			session['birth'] = form.birth.data
			session['contact'] = form.contact.data
			session['department'] = form.department.data
			session['qualifications'] = form.qualifications.data
			session['designation'] = form.designation.data
			session['Address'] = form.Address.data
			session['pincode'] = form.pincode.data
		elif request.method == 'GET':
			form.email.data = g.email
			form.name.data = session['name']
			form.Tid.data = session['Tid']
			form.Gender.data = session['Gender']
			form.contact.data = session['contact']
			form.department.data = session['department']
			form.qualifications.data=session['qualifications']
			form.designation.data=session['designation']
			form.Address.data = session['Address']
			form.pincode.data = session['pincode']
		return render_template('/TeacherAdmin/tedit_profile.html', title='Edit Profile',form=form)
	return redirect(url_for('teacherlogin'))


@app.route("/logout3")
def logout3():
	session.pop('loggedin', None)
	session.pop('email', None)
	session.pop('Enrollment', None)
	session.pop('Gender', None)
	session.clear()
	return redirect(url_for('login'))



@app.route("/teacherlogin", methods=['GET', 'POST'])
def teacherlogin():
	form = LoginForm(request.form)
	if g.email:
		return redirect(url_for('teachersignup'))
	if request.method=='POST' and form.validate_on_submit() and 'email' in request.form and 'password' in request.form:
		email=request.form.get('email')
		password1 = request.form.get('password')
		#secure_password = bcrypt.generate_password_hash('password').decode('utf-8')
		#secure_pass = sha256_crypt.verify("password",secure_password)
		#secure_pass=bcrypt.check_password_hash(secure_password,password)
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor) 
		result=cursor.execute('SELECT * FROM teacherregister WHERE email = % s ', [email])    
		if result>0:
			register = cursor.fetchone()
			password=register['password']
			if bcrypt.check_password_hash(password,password1):
				session['loggedin']=True
				session['email']=register['email'] 
				session['name']=register['name'] 
				session['Tid']=register['Tid']
				session['Gender']=register['Gender']
				session['birth']=register['birth']
				session['contact']=register['contact']
				session['department']=register['department']
				session['qualifications']=register['qualifications']
				session['designation']=register['designation']
				session['Address']=register['Address']
				session['pincode']=register['pincode']
				session['authorization']=register['authorization']
				flash('You have been logged in!', 'success')
				return redirect(url_for('teachersignup'))
				cursor.close() 
			else:
				flash('Password is incorrect','danger')
		else: 
			flash('Login Unsuccessful. Please check email and password', 'danger')
	return render_template('teacherlogin.html', title='Login', form=form)
	
@app.route("/teachersignup")
def teachersignup():
	if g.email:
		cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		result = cur.execute("SELECT * FROM subjectdetail ORDER BY Tid")
		carbrands = cur.fetchall()
		return render_template('/TeacherAdmin/index.html',email=session['email'],name=session['name'],Tid=session['Tid'],Gender=session['Gender'],birth=session['birth'],contact=session['contact'],department=session['department'],qualifications=session['qualifications'],designation=session['designation'],Address=session['Address'],pincode=session['pincode'],carbrands=carbrands)
	return redirect(url_for('teacherlogin'))

@app.route("/logout2")
def logout2():
	session.pop('loggedin', None)
	session.pop('email', None)
	session.clear()
	return redirect(url_for('teacherlogin'))

@app.route('/logout')
def logout():
	logout_user()
	session.pop('loggedin', None)
	session.pop('id', None)
	session.pop('email', None)
	session.clear()
	return redirect(url_for('login'))


@app.route("/contact")
def contact():
    return render_template('contact.html')



@app.route("/adminlogin",methods =['GET', 'POST'])
def adminlogin():
	if g.email:
		return redirect(url_for('admindash'))
	form = LoginForm(request.form)
	if request.method=='POST' and form.validate_on_submit() and 'email' in request.form and 'password' in request.form:
		session.pop('email', None)
		email=request.form.get('email')
		password = request.form.get('password')
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor) 
		cursor.execute('SELECT * FROM admin WHERE email = % s AND password = % s', (email, password, )) 
		account = cursor.fetchone() 
		if account: 
			session['loggedin'] = True
			session['id'] = account['id'] 
			session['email'] = account['email'] 
			flash('You have been logged in!', 'success')
			return redirect(url_for('admindash'))
		else:
			flash('Login Unsuccessful. Please check username and password', 'danger')
	return render_template('adminlogin.html',title='Login', form=form)

@app.route("/admindash")
def admindash():
	if g.email:
		cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		result=cur.execute('select *  FROM register')
		result1=cur.execute('select * FROM teacherregister')
		result2=cur.execute('select *  FROM subjectdetail')
		result3=cur.execute('select *  FROM crassignment')
		return render_template('/ADMIN/index.html',email=session['email'],id=session['id'],data=result,data1=result1,data2=result2,data3=result3)
	return redirect(url_for('adminlogin'))




@app.route('/logout1')
def logout1():
	session.pop('loggedin', None)
	session.pop('email', None)
	session.clear()
	return redirect(url_for('adminlogin'))
	
@app.route("/teacheregister",methods =['GET', 'POST'])
def teacheregister():
	form = TeacherRegistrationForm(request.form)
	if request.method=='POST' and form.validate_on_submit():
		name = request.form.get('name')
		email = request.form.get('email')
		Tid = request.form.get('Tid')
		Gender = request.form.get('Gender')
		birth = request.form.get('birth')
		contact = request.form.get('contact')
		department = request.form.get('department')
		qualifications = request.form.get('qualifications')
		designation = request.form.get('designation')
		Address = request.form.get('Address')
		pincode = request.form.get('pincode')
		password = request.form.get('password')
		authorization = request.form.get('authorization')
		confirm_password = request.form.get('confirm_password')
		secure_password = bcrypt.generate_password_hash(password).decode('utf-8')
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor) 
		result=cursor.execute('SELECT * FROM teacherregister WHERE email = % s ', [email])
		result1=cursor.execute('SELECT * FROM teacherregister WHERE Tid = % s ', [Tid])
		if result>0:
			flash('That Email is already Registered, please choose another','danger')
			return render_template('teachergister.html', form=form)
		elif result1>0:
			flash('That Teacher Id is already Registered, please choose another','danger')
			return render_template('teachergister.html', form=form)
		else:
			entry = Teacherregister(name=name,email = email,Tid = Tid,Gender = Gender,birth= birth,contact=contact,department = department,qualifications = qualifications,designation = designation,Address = Address,pincode = pincode,password = secure_password,confirm_password=secure_password,authorization=authorization)
			db.session.add(entry)
			db.session.commit()
			msg=Message(subject="New message from Student Assignment Submission Portal",sender='studentassignmentportal12@gmail.com',recipients =[email])
			msg.html=render_template("temail.html",name=name,Tid=Tid)
			mail.send(msg)
			flash(f'Account created for {form.email.data}!', 'success')
			return redirect(url_for('teacheregister'))
	return render_template('teachergister.html',title='Teacherregister', form=form)



@app.route("/about")
def about():
    return render_template('about.html')


@app.route('/Addsubject',methods=["POST","GET"])
def Addsubject():
	if g.email:
		cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		result = cur.execute("SELECT * FROM teacherregister ORDER BY Tid")
		carbrands = cur.fetchall()
		if request.method=='POST' :
			sname = request.form.get('sname')
			scode = request.form.get('scode')
			sem = request.form.get('sem')
			Tid = request.form.get('Tid')
			name = request.form.get('name')
			email = request.form.get('email')
			Add = Subjectdetail(sname=sname,scode=scode,sem=sem,Tid=Tid,name=name,email=email)
			db.session.add(Add)
			db.session.commit()
			msg=Message(subject="Subject Details",sender='studentassignmentportal12@gmail.com',recipients =[email])
			msg.html=render_template("aemail.html",name=name,Tid=Tid,sname=sname,sem=sem)
			mail.send(msg)
			flash(f'Subject Details are Successfully Added !', 'success')
		return render_template('/ADMIN/blank.html',carbrands=carbrands)
	return redirect(url_for('adminlogin'))		
 
@app.route("/carbrand",methods=["POST","GET"])
def carbrand():  
    cursor = mysql.connection.cursor()
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if request.method == 'POST':
        category_id = request.form['category_id'] 
        print(category_id)
        result = cur.execute("SELECT * FROM teacherregister WHERE Tid = %s ORDER BY Tid ASC", [category_id] )
        carmodel = cur.fetchall()  
        OutputArray = []
        for row in carmodel:
            outputObj = {
                'Tid': row['Tid'],
                'name': row['name'],
                'email': row['email']}
            OutputArray.append(outputObj)
    return jsonify(OutputArray)

@app.route("/studentprofile", methods=['GET', 'POST'])
def studentprofile():
	if g.email:
		form = RegistrationForm(request.form)
		return render_template('/StudentLogin/profile.html', title='Register', form=form)
	return redirect(url_for('login'))

@app.route("/teacherprofile", methods=['GET', 'POST'])
def teacherprofile():
	if g.email:
		form = TeacherRegistrationForm(request.form)
		return render_template('/TeacherAdmin/tprofile.html', title='Register', form=form)
	return redirect(url_for('teacherlogin'))

@app.route('/createassignment',methods=["POST","GET"])
def createassignment():
	if g.email:
		cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		result = cur.execute("SELECT * FROM subjectdetail ORDER BY Tid")
		carbrands = cur.fetchall()
		return render_template('/TeacherAdmin/CreateAssignment.html',carbrands=carbrands)
	return redirect(url_for('teacherlogin'))

@app.route("/crassignment",methods=["POST","GET"])
def crassignment():  
    cursor = mysql.connection.cursor()
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if request.method == 'POST':
        category_id = request.form['category_id'] 
        print(category_id)
        result = cur.execute("SELECT * FROM subjectdetail WHERE Tid = %s ORDER BY Tid ASC", [category_id] )
        carmodel = cur.fetchall()  
        OutputArray = []
        for row in carmodel:
            outputObj = {
                'Tid': row['Tid'],
				'sname': row['sname'],
                'name': row['name'],
                'email': row['email'],
				'sem':row['sem']}
            OutputArray.append(outputObj)
    return jsonify(OutputArray)

@app.route("/crassignment1",methods=["POST","GET"])
def crassignments():  
    cursor = mysql.connection.cursor()
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if request.method == 'POST':
        category_id = request.form['category_id'] 
        print(category_id)
        result = cur.execute("SELECT * FROM subjectdetail WHERE sem = %s ORDER BY sem ASC", [category_id] )
        carmodel = cur.fetchall()  
        OutputArray = []
        for row in carmodel:
            outputObj = {
                'Tid': row['Tid'],
				'sname': row['sname'],
                'name': row['name'],
                'email': row['email'],
				'sem':row['sem']}
            OutputArray.append(outputObj)
    return jsonify(OutputArray)

@app.route('/showstudent')
def showstudent():
	if g.email:
		cursor = mysql.connection.cursor()
		cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cur.execute('SELECT * FROM register')
		data = cur.fetchall()
		cur.close()
		return render_template('/ADMIN/showstudent.html', employee = data)
	return redirect(url_for('adminlogin'))

@app.route('/edit/<id>', methods = ['POST', 'GET'])
def get_employee(id):
	form = EditProfileForm(request.form)
	cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
	cur.execute('SELECT * FROM register WHERE id = %s', (id,))
	data = cur.fetchall()
	cur.close()
	print(data[0])
	return render_template('/ADMIN/edit_student.html', employee = data[0],form=form)
 
@app.route('/update/<id>', methods=['POST'])
def update_employee(id):
	if request.method == 'POST':
		name = request.form['name']
		email = request.form['email']
		Enrollment = request.form['Enrollment']
		Gender = request.form['Gender']
		birth = request.form['birth']
		contact = request.form['contact']
		semester = request.form['semester']
		city = request.form['city']
		state = request.form['state']
		Address = request.form['Address']
		pincode = request.form['pincode']
		cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cur.execute("""
       UPDATE register
       SET name = %s,email = %s,Enrollment=%s,Gender=%s,birth=%s,contact = %s,semester=%s,city=%s,state=%s,Address=%s,pincode=%s
       WHERE id = %s
    """, (name, email,Enrollment,Gender,birth,contact,semester,city,state,Address,pincode, id))
		flash('Student Data Updated Successfully','success')
		
		return redirect(url_for('showstudent'))
 
@app.route('/delete/<string:id>', methods = ['POST','GET'])
def delete_employee(id):
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute('DELETE FROM register WHERE id = {0}'.format(id))
    flash('Student Data Removed Successfully','success')
    return redirect(url_for('showstudent'))

UPLOAD_FOLDER = './static/upassig/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'doc','docx'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

class Crassignment(db.Model):
	stitle = db.Column(db.String(80),	unique=False,	nullable=False)
	amark = db.Column(db.String(80),	unique=False,	nullable=False)
	name = db.Column(db.String(80),	unique=False,	nullable=False)
	sname = db.Column(db.String(80),	unique=False,	nullable=False)
	email = db.Column(db.String(80),	unique=True,	primary_key=True,	nullable=False)
	Tid = db.Column(db.String(11), 	unique=True,	primary_key=True,	nullable=False)
	pdpart = db.Column(db.String(1000),	unique=False,	nullable=False)
	ddate = db.Column(db.String(12),	nullable=False)
	sdate = db.Column(db.String(12),	nullable=False)
	sem = db.Column(db.String(120),	nullable=False)
	file = db.Column(db.String(150))
	adescription = db.Column(db.String(200), nullable=False)
	data=db.Column(db.LargeBinary)

@app.route('/crassign',methods=['POST'])
def crassign():
	if g.email:
		if request.method=='POST':
			file=request.files['inputFile']
			filename=secure_filename(file.filename)
			new_file = str(urllib.parse.quote(filename))
			name = request.form.get('name')
			sname = request.form.get('sname')
			stitle = request.form.get('stitle')
			email = request.form.get('email')
			Tid = request.form.get('Tid')
			pdpart = request.form.get('pdpart')
			ddate = request.form.get('ddate')
			sdate = request.form.get('sdate')
			amark = request.form.get('amark')
			sem = request.form.get('sem')
			adescription = request.form.get('adescription')
			if file and allowed_file(file.filename):
				file.save(os.path.join(app.config['UPLOAD_FOLDER'], new_file))
				newassign=Crassignment(stitle=stitle,Tid=Tid,pdpart=pdpart,sem=sem,sname=sname,name=name,email=email,file=new_file,sdate=sdate,ddate=ddate,adescription=adescription,amark=amark,data=file.read())
				db.session.add(newassign)
				db.session.commit()
				cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
				result=cur.execute('select * FROM register WHERE semester = %s',(sem,))
				data = cur.fetchall()
				print(data)
				for row in data:
					user=row['email']
					user1=row['name']
					print(user1)
					print(user)
					msg=Message(subject="New Assignment is Uploaded",sender='studentassignmentportal12@gmail.com',recipients =[user])
					msg.html=render_template("assignmetmail.html",name=name,sname=sname,sem=sem,stitle=stitle,sdate=sdate,amark=amark,ddate=ddate,data=data,user1=user1)
					mail.send(msg)
				flash('Assignment Successfully created','success') 
				return redirect(url_for('createassignment'))
			else:
				flash('Invalid Uplaod only txt, pdf, doc,docx','danger') 
		return redirect(url_for('createassignment'))
	return redirect(url_for('teacherlogin'))

@app.route("/showassignment", methods=['GET', 'POST'])
def showassignment():
	if g.email:
		cursor = mysql.connection.cursor()
		cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cur.execute('SELECT * FROM subjectdetail')
		data = cur.fetchall()
		cur.close()	
		return render_template('/StudentLogin/showassign.html',showst = data)
	return redirect(url_for('login'))



@app.route('/view/<string:sname>', methods = ['POST','GET'])
def viewassignment(sname):
	if g.email:
		cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cur.execute('select * FROM crassignment WHERE sname = %s',(sname,))
		data = cur.fetchall()
		cur.close()
		return render_template('/StudentLogin/showassignsubject.html',showstsb = data,datetime = date.today())
	return redirect(url_for('login'))

@app.route('/viewassignmentsb/<string:id>', methods = ['POST','GET'])
def viewassignmentsb(id):
	if g.email:
		cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cur.execute('select * FROM uploadassign WHERE asid = %s',(id,))
		result=cur.fetchall()
		print(result)
		cur.execute('select * FROM crassignment WHERE id = %s',(id,))
		data = cur.fetchall()
		print(data)
		cur.close()
		return render_template('/StudentLogin/viewfullassign.html',showstsb = data, showans=result,datetime = date.today())
	return redirect(url_for('login'))

@app.route('/down/<file>', methods = ['GET'])
def down(file):
	if g.email:
		cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		result=cur.execute('select * FROM crassignment WHERE file = %s',(file,))
		data = cur.fetchall()
		cur.close()
		file_path = UPLOAD_FOLDER + file
		return send_file(file_path, as_attachment=True, attachment_filename='')
		#return send_file(BytesIO(data.data),as_attachment=True,attachment_filename=data.file)
	return redirect(url_for('login'))

UPLOAD_FOLDERR = 'static/uploadanswer/'
app.config['UPLOAD_FOLDERR'] = UPLOAD_FOLDERR

class Uploadassign(db.Model):
	Enrollment = db.Column(db.String(11), 	unique=True,	primary_key=True,	nullable=False)
	sname = db.Column(db.String(80),	unique=False,	nullable=False)
	name = db.Column(db.String(200),	unique=False,	nullable=False)
	pname = db.Column(db.String(200),	unique=False,	nullable=False)
	semester = db.Column(db.String(120),	nullable=False)
	ddate = db.Column(db.String(12),	nullable=False)
	sdate = db.Column(db.String(12),	nullable=False)
	realmark = db.Column(db.String(80),	unique=False,	nullable=False)
	asmark = db.Column(db.String(80),	unique=False,	nullable=False)
	remark = db.Column(db.String(80),	unique=False,	nullable=False)
	stitle = db.Column(db.String(80),	unique=False,	nullable=False)
	asid= db.Column(db.String(80),	unique=False,	nullable=False)
	uploaddate = db.Column(db.String(12),	nullable=False)
	email = db.Column(db.String(80),	unique=True,	primary_key=True,	nullable=False)
	file = db.Column(db.String(150))

@app.route('/uploadans', methods=['GET','POST'])
def uploadans():
	if g.email:
		if request.method=='POST':
			semester=session['semester']
			pname=request.form.get('pname')
			sname = request.form.get('sname')
			id = request.form.get('id')
			asmark = request.form.get('asmark')
			remark = request.form.get('remark')
			from datetime import datetime
			now = datetime.now()
			formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
			stitle = request.form.get('stitle')
			realmark = request.form.get('realmark')
			ddate = request.form.get('ddate')
			sdate = request.form.get('sdate')
			Enrollment=session['Enrollment']
			name=session['name']
			email=session['email']
			file=request.files['inputFile']
			print(id)
			filename=secure_filename(file.filename)
			new_file = str(urllib.parse.quote(filename))
			if file and allowed_file(file.filename):
				file.save(os.path.join(app.config['UPLOAD_FOLDERR'], new_file))
				cursor = mysql.connection.cursor()
				cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
				result=cur.execute('SELECT * FROM uploadassign WHERE asid=%s AND Enrollment=%s',(id,Enrollment,))
				if result>0:
					data = cur.fetchone()
					assid=data['asid']
					enroll=data['Enrollment']
					print(assid)
					print(enroll)
					os.remove(os.path.join(app.config['UPLOAD_FOLDERR'], data['file']))
					if assid and enroll :
						file.save(os.path.join(app.config['UPLOAD_FOLDERR'], new_file))
						cur.execute("""UPDATE uploadassign SET file=%s,uploaddate=%s WHERE Enrollment=%s AND asid=%s""", (new_file, formatted_date, session['Enrollment'],id))
						flash('Assignment Successfully updated','success') 
						return redirect(url_for('viewassignmentsb',id=id))
				else:
					uploadassign=Uploadassign(Enrollment=session['Enrollment'],name=session['name'],semester=session['semester'],file=new_file,uploaddate=formatted_date,sname=sname,stitle=stitle,asmark='null',remark='null',asid=id,pname=pname,sdate=sdate,ddate=ddate,realmark=realmark,email=session['email'])
					db.session.add(uploadassign)
					db.session.commit()
					flash('Assignment Successfully uploaded','success') 
					return redirect(url_for('viewassignmentsb',id=id))
			else:
				flash('Invalid Uplaod only txt, pdf, doc,docx','danger') 
		return render_template('/StudentLogin/viewfullassign.html')
	return redirect(url_for('login'))

@app.route("/showallassignment/<string:sname>", methods=['GET', 'POST'])
def showallassignment(sname):
	if g.email:
		cursor = mysql.connection.cursor()
		cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cur.execute('SELECT * FROM crassignment')
		data = cur.fetchall()
		cur.close()	
		return render_template('/TeacherAdmin/showallassign.html',showst = data)
	return redirect(url_for('teacherlogin'))

@app.route('/editassign/<id>', methods = ['POST', 'GET'])
def editassign(id):
	cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
	cur.execute('SELECT * FROM crassignment WHERE id = %s', (id,))
	data = cur.fetchall()
	cur.close()
	print(data[0])	
	return render_template('/TeacherAdmin/editallassign.html', showst = data[0])

@app.route('/deleteassign/<string:id>', methods = ['POST','GET'])
def deleteassign(id):
	cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
	cur.execute('SELECT * FROM crassignment WHERE id = %s',(id,))
	result=cur.fetchone()
	data=result['sname']
	print(result)
	os.remove(os.path.join(app.config['UPLOAD_FOLDER'], result['file']))
	cur.execute('DELETE FROM crassignment WHERE id = %s',(id,))
	flash('Assignment Data Removed Successfully','success')
	return redirect(url_for('showallassignment',sname=data))

@app.route("/statusforstudent/<string:sname>", methods=['GET', 'POST'])
def statusforstudent(sname):
	if g.email:
		cursor = mysql.connection.cursor()
		cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cur.execute('SELECT * FROM uploadassign WHERE sname = %s',(sname,))
		data = cur.fetchall()
		cur.close()	
		return render_template('/StudentLogin/statusofassign.html',showstatus = data)
	return redirect(url_for('login'))

@app.route('/viewuploadans/<string:id>', methods = ['POST','GET'])
def viewuploadans(id):
	if g.email:
		cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cur.execute('select * FROM uploadassign WHERE id = %s',(id,))
		data = cur.fetchall()
		cur.close()
		return render_template('/StudentLogin/showuploadans.html',viewans = data)
	return redirect(url_for('login'))

@app.route('/downans/<file>', methods = ['GET'])
def downans(file):
	if g.email:
		cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		result=cur.execute('select * FROM uploadassign WHERE file = %s',(file,))
		data = cur.fetchall()
		cur.close()
		file_path = UPLOAD_FOLDERR + file
		return send_file(file_path, as_attachment=True, attachment_filename='')
		#return send_file(BytesIO(data.data),as_attachment=True,attachment_filename=data.file)
	return redirect(url_for('login'))

@app.route("/statusofstudent/<string:sname>", methods=['GET', 'POST'])
def statusofstudent(sname):
	if g.email:
		cursor = mysql.connection.cursor()
		cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cur.execute('SELECT * FROM uploadassign')
		data = cur.fetchall()
		cur.close()	
		return render_template('/TeacherAdmin/statusofassign.html',showstatus = data)
	return redirect(url_for('teacherlogin'))

@app.route('/viewuploadansst/<string:id>', methods = ['POST','GET'])
def viewuploadansst(id):
	if g.email:
		cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cur.execute('select * FROM uploadassign WHERE id = %s',(id,))
		data = cur.fetchall()
		cur.close()
		return render_template('/TeacherAdmin/showuploadans.html',viewans = data)
	return redirect(url_for('teacherlogin'))

@app.route('/uploadmark', methods=['GET','POST'])
def uploadmark():
	if g.email:
		if request.method=='POST':
			asmark=request.form.get('asmark')
			remark=request.form.get('remark')
			id=request.form.get('id')
			email=request.form.get('email')
			name=request.form.get('name')
			pname=request.form.get('pname')
			sname=request.form.get('sname')
			stitle=request.form.get('stitle')
			realmark=request.form.get('realmark')
			semester=request.form.get('semester')
			cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
			if int(asmark)<=int(realmark):
				print('inif')
				cur.execute("""UPDATE uploadassign SET asmark=%s, remark=%s WHERE id=%s""", (asmark, remark, id))
				msg=Message(subject="Assignment Graded",sender='studentassignmentportal12@gmail.com',recipients =[email])
				msg.html=render_template("markmail.html",name=name,pname=pname,sname=sname,semester=semester,stitle=stitle,asmark=asmark,realmark=realmark,remark=remark)
				mail.send(msg)
				cur.close()
				flash('Assignment mark uploaded','success') 
				return redirect(url_for('viewuploadansst',id=id))
			else:
				flash(f'total Assgnment Number is {realmark} Mark','danger')
				return redirect(url_for('viewuploadansst',id=id))
		return render_template('/TeacherAdmin/showuploadans.html')
	return redirect(url_for('teacherlogin'))

@app.route('/updateprofilestudent', methods=['GET','POST'])
def updateprofilestudent():
	if g.email:
		if request.method=='POST':
			name = request.form.get('name')
			email = request.form.get('email')
			Enrollment = request.form.get('Enrollment')
			Enrollment=session['Enrollment']
			Gender = request.form.get('Gender')
			birth = request.form.get('birth')
			contact = request.form.get('contact')
			semester = request.form.get('semester')
			city = request.form.get('city')
			state = request.form.get('state')
			Address = request.form.get('Address')
			pincode = request.form.get('pincode')
			cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
			cur.execute("""
       UPDATE register
       SET name = %s,Gender=%s,birth=%s,contact = %s,city=%s,state=%s,Address=%s,pincode=%s
       WHERE Enrollment = %s
    """, (name,Gender,birth,contact,city,state,Address,pincode, Enrollment))
			
			cur.close()
			flash('Your Profile is successfully updated','success') 
			return redirect(url_for('edit_profile'))
		return render_template('/StudentLogin/edit_profile.html', title='Edit Profile',form=form)
	return redirect(url_for('stsignup'))

@app.route('/updateprofileteacher', methods=['GET','POST'])
def updateprofileteacher():
	if g.email:
		if request.method=='POST':
			name = request.form.get('name')
			email = request.form.get('email')
			Tid = session['Tid']
			Gender = request.form.get('Gender')
			birth = request.form.get('birth')
			contact = request.form.get('contact')
			department = request.form.get('department')
			qualifications = request.form.get('qualifications')
			designation = request.form.get('designation')
			Address = request.form.get('Address')
			pincode = request.form.get('pincode')
			cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
			cur.execute("""
       UPDATE teacherregister
       SET name = %s,Gender=%s,birth=%s,contact = %s,department=%s,qualifications=%s,designation=%s,Address=%s,pincode=%s
       WHERE Tid = %s
    """, (name,Gender,birth,contact,department,qualifications,designation,Address,pincode, Tid))
			
			cur.close()
			flash('Your Profile is successfully updated','success') 
			return redirect(url_for('teacher_edit_profile'))
		return render_template('/TeacherAdmin/tedit_profile.html', title='Edit Profile',form=form)
	return redirect(url_for('stsignup'))

@app.route('/showprofessor')
def showprofessor():
	if g.email:
		cursor = mysql.connection.cursor()
		cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cur.execute('SELECT * FROM teacherregister')
		data = cur.fetchall()
		cur.close()
		return render_template('/ADMIN/showprofessor.html', showprofe = data)
	return redirect(url_for('adminlogin'))

@app.route('/editprof/<id>', methods = ['POST', 'GET'])
def editprof(id):
	form = EditTeacherProfile(request.form)
	cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
	cur.execute('SELECT * FROM teacherregister WHERE id = %s', (id,))
	data = cur.fetchall()
	cur.close()
	print(data[0])
	return render_template('/ADMIN/tedit_profile.html', showprofe = data[0],form=form)
 
@app.route('/updateprof/<id>', methods=['POST'])
def updateprof(id):
	if request.method == 'POST':
		name = request.form['name']
		email = request.form['email']
		Tid = request.form['Tid']
		Gender = request.form['Gender']
		birth = request.form['birth']
		contact = request.form['contact']
		department = request.form['department']
		qualifications = request.form['qualifications']
		designation = request.form['designation']
		Address = request.form['Address']
		pincode = request.form['pincode']
		cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cur.execute("""
       UPDATE teacherregister
       SET name = %s,email = %s,Tid=%s,Gender=%s,birth=%s,contact = %s,department=%s,qualifications=%s,designation=%s,Address=%s,pincode=%s
       WHERE id = %s
    """, (name, email,Tid,Gender,birth,contact,department,qualifications,designation,Address,pincode, id))
		flash('Professor Data Updated Successfully','success')
		
		return redirect(url_for('showprofessor'))
 
@app.route('/deleteprof/<string:id>', methods = ['POST','GET'])
def deleteprof(id):
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute('DELETE FROM teacherregister WHERE id = {0}'.format(id))
    flash('Professor Data Removed Successfully','success')
    return redirect(url_for('showprofessor'))

@app.route("/viewuploadans/logout3")
def logout4():
	session.pop('loggedin', None)
	session.pop('email', None)
	session.pop('Enrollment', None)
	session.pop('Gender', None)
	session.clear()
	return redirect(url_for('login'))

@app.route("/view/logout3")
def logout5():
	session.pop('loggedin', None)
	session.pop('email', None)
	session.pop('Enrollment', None)
	session.pop('Gender', None)
	session.clear()
	return redirect(url_for('login'))

@app.route("/viewassignmentsb/logout3")
def logout6():
	session.pop('loggedin', None)
	session.pop('email', None)
	session.pop('Enrollment', None)
	session.pop('Gender', None)
	session.clear()
	return redirect(url_for('login'))

@app.route("/editassign/logout2")
def logout7():
	session.pop('loggedin', None)
	session.pop('email', None)
	session.clear()
	return redirect(url_for('teacherlogin'))

@app.route("/viewuploadansst/logout2")
def logout8():
	session.pop('loggedin', None)
	session.pop('email', None)
	session.clear()
	return redirect(url_for('teacherlogin'))

@app.route('/edit/logout1')
def logout9():
	session.pop('loggedin', None)
	session.pop('email', None)
	session.clear()
	return redirect(url_for('adminlogin'))

@app.route('/editprof/logout1')
def logout10():
	session.pop('loggedin', None)
	session.pop('email', None)
	session.clear()
	return redirect(url_for('adminlogin'))

@app.route('/updateassign/<id>', methods=['POST'])
def updateassign(id):
	if request.method == 'POST':
		file=request.files['inputFile']
		filename=secure_filename(file.filename)
		name = request.form['name']
		sname = request.form['sname']
		stitle = request.form['stitle']
		email = request.form['email']
		Tid = request.form['Tid']
		pdpart = request.form['pdpart']
		ddate = request.form['ddate']
		sdate = request.form['sdate']
		amark = request.form['amark']
		sem = request.form['sem']
		adescription = request.form['adescription']	
		cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cur.execute('SELECT * FROM crassignment WHERE id = %s',(id,))
		result=cur.fetchone()
		print(result)
		os.remove(os.path.join(app.config['UPLOAD_FOLDER'], result['file']))
		if file and allowed_file(file.filename):
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			cur.execute("""UPDATE crassignment
       		SET stitle = %s,Tid = %s,pdpart=%s,sem=%s,sname=%s,name = %s,email=%s,file=%s,sdate=%s,ddate=%s,adescription=%s,amark=%s
       		WHERE id = %s
   			 """, (stitle, Tid,pdpart,sem,sname,name,email,file.filename,sdate,ddate,adescription,amark, id))
			flash('Assignment Data Successfully updated','success') 
			return redirect(url_for('editassign',id=id))
		else:
			flash('Invalid Uplaod only txt, pdf, doc,docx','danger') 
	return redirect(url_for('editassign',id=id))

@app.route("/showsubjectassignment", methods=['GET', 'POST'])
def showsubjectassignment():
	if g.email:
		cursor = mysql.connection.cursor()
		cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cur.execute('SELECT * FROM subjectdetail')
		data = cur.fetchall()
		cur.close()	
		return render_template('/StudentLogin/showstatussubject.html',showst = data)
	return redirect(url_for('login'))

@app.route("/statusforstudent/logout3")
def logout11():
	session.pop('loggedin', None)
	session.pop('email', None)
	session.pop('Enrollment', None)
	session.pop('Gender', None)
	session.clear()
	return redirect(url_for('login'))

@app.route("/statusofstudent/logout2")
def logout12():
	session.pop('loggedin', None)
	session.pop('email', None)
	session.pop('Enrollment', None)
	session.pop('Gender', None)
	session.clear()
	return redirect(url_for('teacherlogin'))

@app.route("/showsubjectassignmentbytecher", methods=['GET', 'POST'])
def showsubjectassignmentbytecher():
	if g.email:
		cursor = mysql.connection.cursor()
		cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cur.execute('SELECT * FROM subjectdetail')
		data = cur.fetchall()
		cur.close()	
		return render_template('/TeacherAdmin/showstatussubjectteacher.html',showst = data)
	return redirect(url_for('teacherlogin'))


class Announcement(db.Model):
	Tid = db.Column(db.String(11), 	unique=True,	primary_key=True,	nullable=False)
	atitle = db.Column(db.String(80),	unique=False,	nullable=False)
	name = db.Column(db.String(80),	unique=False,	nullable=False)
	pdpart = db.Column(db.String(1000),	unique=False,	nullable=False)
	adate = db.Column(db.String(12),	nullable=False)
	sem = db.Column(db.String(120),	nullable=False)
	adescription = db.Column(db.String(200), nullable=False)

@app.route('/announcement',methods=['POST'])
def announcement():
	if g.email:
		if request.method=='POST':
			name = request.form.get('name')
			atitle = request.form.get('atitle')
			pdpart = request.form.get('pdpart')
			from datetime import datetime
			now = datetime.now()
			formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
			sem = request.form.get('sem')
			adescription = request.form.get('adescription')	
			Tid = request.form.get('Tid')		
			newassign=Announcement(atitle=atitle,pdpart=pdpart,sem=sem,name=name,Tid=Tid,adescription=adescription,adate=formatted_date)
			db.session.add(newassign)
			db.session.commit()
			flash('Announcement Successfully created','success') 
		return redirect(url_for('teachersignup'))
	return redirect(url_for('teacherlogin'))


@app.route("/showsubjectdetail", methods=['GET', 'POST'])
def showsubjectdetail():
	if g.email:
		cursor = mysql.connection.cursor()
		cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cur.execute('SELECT * FROM subjectdetail')
		data = cur.fetchall()
		cur.close()	
		return render_template('/TeacherAdmin/subjectdetails.html',showst = data)
	return redirect(url_for('login'))


@app.route("/forgot", methods=['GET', 'POST'])
def forgot():
	form = RequestResetForm()
	if request.method=='POST' and form.validate_on_submit():
		email=request.form.get('email')
		token=str(uuid.uuid4())
		cursor = mysql.connection.cursor()
		cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		result=cur.execute('SELECT * FROM register where email=%s',(email,))
		if result>0:
			data=cur.fetchone()
			msg=Message(subject="Forgot Password Request",sender='studentassignmentportal12@gmail.com',recipients =[email])
			msg.html=render_template("sent.html",token=token,data=data)
			mail.send(msg)
			cursor = mysql.connection.cursor()
			cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
			cur.execute('UPDATE register SET token=%s where email=%s',(token,email,))
			mysql.connection.commit()
			cur.close()
			flash(f"Email Already Sent To Your Email {form.email.data}!",'success')
			return redirect('/forgot')
		else:
			flash("Email Do Not Match",'danger')
	return render_template('stforgot.html', title='Forgot Password', form=form)

@app.route("/reset/<token>", methods=['GET', 'POST'])
def reset(token):
	form = ResetPasswordForm()
	if request.method=='POST' and form.validate_on_submit():
		email=request.form.get('email')
		password=request.form.get('password')
		confirm_password=request.form.get('confirm_password')
		password=bcrypt.generate_password_hash(password)
		token1=str(uuid.uuid4())
		cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cur.execute('SELECT * FROM register where token=%s',(token,))
		user=cur.fetchone()
		if user:
			cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
			cur.execute('UPDATE register SET token=%s,password=%s where token=%s',(token1,password,token,))
			mysql.connection.commit()
			cur.close()
			flash("Your Password Successfully Updated",'success')
			return redirect('/login')
		else:
			flash("Your Link is Expired",'danger')
	return render_template('stforgotpass.html', title='Forgot Password', form=form)

@app.route("/tforgot", methods=['GET', 'POST'])
def tforgot():
	form = RequestResetForm()
	if request.method=='POST' and form.validate_on_submit():
		email=request.form.get('email')
		token=str(uuid.uuid4())
		cursor = mysql.connection.cursor()
		cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		result=cur.execute('SELECT * FROM teacherregister where email=%s',(email,))
		if result>0:
			data=cur.fetchone()
			msg=Message(subject="Forgot Password Request",sender='studentassignmentportal12@gmail.com',recipients =[email])
			msg.html=render_template("sent.html",token=token,data=data)
			mail.send(msg)
			cursor = mysql.connection.cursor()
			cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
			cur.execute('UPDATE teacherregister SET token=%s where email=%s',(token,email,))
			mysql.connection.commit()
			cur.close()
			flash(f"Email Already Sent To Your Email {form.email.data}!",'success')
			return redirect('/tforgot')
		else:
			flash("Email is Not Registered",'danger')
	return render_template('tforgot.html', title='Forgot Password', form=form)

@app.route("/treset/<token>", methods=['GET', 'POST'])
def treset(token):
	form = ResetPasswordForm()
	if request.method=='POST' and form.validate_on_submit():
		email=request.form.get('email')
		password=request.form.get('password')
		confirm_password=request.form.get('confirm_password')
		password=bcrypt.generate_password_hash(password)
		token1=str(uuid.uuid4())
		cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cur.execute('SELECT * FROM teacherregister where token=%s',(token,))
		user=cur.fetchone()
		if user:
			cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
			cur.execute('UPDATE teacherregister SET token=%s,password=%s where token=%s',(token1,password,token,))
			mysql.connection.commit()
			cur.close()
			flash("Your Password Successfully Updated",'success')
			return redirect('/teacherlogin')
		else:
			flash("Your Link is Expired",'danger')
	return render_template('tforgotpass.html', title='Forgot Password', form=form)

@app.route("/teacherprofile/logout2")
def logout13():
	session.pop('loggedin', None)
	session.pop('email', None)
	session.clear()
	return redirect(url_for('teacherlogin'))

@app.route("/changepasswd/<Enrollment>",methods=['GET', 'POST'])
def changepasswd(Enrollment):
	if g.email:
		form = ChangePasswordForm()
		if request.method=='POST' and form.validate_on_submit():
			olpassword=request.form.get('olpassword')
			password=request.form.get('password')
			confirm_password=request.form.get('confirm_password')
			password=bcrypt.generate_password_hash(password)
			confirm_password=bcrypt.generate_password_hash(confirm_password)
			cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
			result=cur.execute('SELECT * FROM register WHERE Enrollment=%s',(Enrollment,))
			if result>0:
				user=cur.fetchone()
				passw=user['password']
				print(passw)
				if bcrypt.check_password_hash(passw,olpassword):
					cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
					cur.execute('UPDATE register SET password=%s,confirm_password=%s WHERE Enrollment=%s',(password,confirm_password,Enrollment,))
					mysql.connection.commit()
					cur.close()
					flash('Your Password has been successfully updated','success')
					return redirect(url_for('changepasswd',Enrollment=Enrollment))
				else:
					flash('Old Password is Incorrect','danger')
		return render_template('/StudentLogin/changepasswd.html',title='Change Password', form=form)
	return redirect(url_for('login'))

@app.route("/changepasswd/logout3")
def logout14():
	session.pop('loggedin', None)
	session.pop('email', None)
	session.pop('Enrollment', None)
	session.pop('Gender', None)
	session.clear()
	return redirect(url_for('login'))

@app.route("/changepasswdteacher/<Tid>",methods=['GET', 'POST'])
def changepasswdteacher(Tid):
	if g.email:
		form = ChangePasswordForm()
		if request.method=='POST' and form.validate_on_submit():
			olpassword=request.form.get('olpassword')
			password=request.form.get('password')
			confirm_password=request.form.get('confirm_password')
			password=bcrypt.generate_password_hash(password)
			confirm_password=bcrypt.generate_password_hash(confirm_password)
			print(olpassword)
			cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
			result=cur.execute('SELECT * FROM teacherregister WHERE Tid=%s',(Tid,))
			if result>0:
				user=cur.fetchone()
				passw=user['password']
				print(passw)
				if bcrypt.check_password_hash(passw,olpassword):
					cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
					cur.execute('UPDATE teacherregister SET password=%s,confirm_password=%s WHERE Tid=%s',(password,confirm_password,Tid,))
					mysql.connection.commit()
					cur.close()
					flash('Your Password has been successfully updated','success')
					return redirect(url_for('changepasswdteacher',Tid=Tid))
				else:
					flash('Old Password is Incorrect','danger')
					return redirect(url_for('changepasswdteacher',Tid=Tid))
		return render_template('/TeacherAdmin/changepasswdteacher.html',title='Change Password', form=form)
	return redirect(url_for('teacherlogin'))

@app.route("/changepasswdteacher/logout2")
def logout15():
	session.pop('loggedin', None)
	session.pop('email', None)
	session.clear()
	return redirect(url_for('teacherlogin'))

@app.errorhandler(413)
def too_large(e):
	flash('Maximum File Size is 10MB','danger')
	return redirect(url_for('createassignment'))

@app.route('/viewassignmentbyprofessor/<string:id>', methods = ['POST','GET'])
def viewassignmentbyprofessor(id):
	if g.email:
		cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cur.execute('select * FROM crassignment WHERE id = %s',(id,))
		data = cur.fetchall()
		cur.close()
		return render_template('/TeacherAdmin/showfullassignteacher.html',showstsb = data)
	return redirect(url_for('login'))

@app.route("/showsubjectwiseassignmentbytecher", methods=['GET', 'POST'])
def showsubjectwiseassignmentbytecher():
	if g.email:
		cursor = mysql.connection.cursor()
		cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cur.execute('SELECT * FROM subjectdetail')
		data = cur.fetchall()
		cur.close()	
		return render_template('/TeacherAdmin/statusfullassign.html',showst = data)
	return redirect(url_for('teacherlogin'))


@app.route("/showallassignment/logout2")
def logout16():
	session.pop('loggedin', None)
	session.pop('email', None)
	session.clear()
	return redirect(url_for('teacherlogin'))

@app.route("/viewassignmentbyprofessor/logout2")
def logout17():
	session.pop('loggedin', None)
	session.pop('email', None)
	session.clear()
	return redirect(url_for('teacherlogin'))


@app.route("/studentprofile/logout3")
def logout18():
	session.pop('loggedin', None)
	session.pop('email', None)
	session.pop('Enrollment', None)
	session.pop('Gender', None)
	session.clear()
	return redirect(url_for('login'))

@app.route("/addnewstudent", methods=['GET', 'POST'])
def addnewstudent():
	if g.email:
		form = StudentRegistrationForm(request.form)
		if request.method=='POST' and form.validate_on_submit():
			name = request.form.get('name')
			email = request.form.get('email')
			Enrollment = request.form.get('Enrollment')
			Gender = request.form.get('Gender')
			birth = request.form.get('birth')
			contact = request.form.get('contact')
			semester = request.form.get('semester')
			city = request.form.get('city')
			state = request.form.get('state')
			Address = request.form.get('Address')
			pincode = request.form.get('pincode')
			password = request.form.get('password')
			confirm_password = request.form.get('confirm_password')
			secure_password = bcrypt.generate_password_hash(password).decode('utf-8')
			cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor) 
			result=cursor.execute('SELECT * FROM register WHERE email = % s ', [email])
			result1=cursor.execute('SELECT * FROM register WHERE Enrollment = % s ', [Enrollment])
			if result>0:
				flash('That Email is already Registered, please choose another','danger')
				return render_template('/ADMIN/addnewstudent.html', form=form)
			elif result1>0:
				flash('That Enrollment is already Registered, please choose another','danger')
				return render_template('/ADMIN/addnewstudent.html', form=form)
			else:
				entry = Register(name=name,email = email,Enrollment = Enrollment,Gender = Gender,birth= birth,contact=contact,semester = semester,city = city,state = state,Address = Address,pincode = pincode,password = secure_password,confirm_password=secure_password)
				db.session.add(entry)
				db.session.commit()
				msg=Message(subject="New message from Student Assignment Submission Portal",sender='studentassignmentportal12@gmail.com',recipients =[email])
				msg.html=render_template("email.html",name=name,Enrollment=Enrollment)
				mail.send(msg)
				flash(f'Account created for {form.email.data}!', 'success')
				return redirect(url_for('addnewstudent'))
		return render_template('/ADMIN/addnewstudent.html', title='Register', form=form)
	return redirect(url_for('adminlogin'))

@app.route("/addnewprofessor",methods =['GET', 'POST'])
def addnewprofessor():
	if g.email:
		form = AdminTeacherRegistrationForm(request.form)
		if request.method=='POST' and form.validate_on_submit():
			name = request.form.get('name')
			email = request.form.get('email')
			Tid = request.form.get('Tid')
			Gender = request.form.get('Gender')
			birth = request.form.get('birth')
			contact = request.form.get('contact')
			department = request.form.get('department')
			qualifications = request.form.get('qualifications')
			designation = request.form.get('designation')
			Address = request.form.get('Address')
			pincode = request.form.get('pincode')
			password = request.form.get('password')
			confirm_password = request.form.get('confirm_password')
			secure_password = bcrypt.generate_password_hash(password).decode('utf-8')
			cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor) 
			result=cursor.execute('SELECT * FROM teacherregister WHERE email = % s ', [email])
			result1=cursor.execute('SELECT * FROM teacherregister WHERE Tid = % s ', [Tid])
			if result>0:
				flash('That Email is already Registered, please choose another','danger')
				return render_template('/ADMIN/addnewprofessor.html', form=form)
			elif result1>0:
				flash('That Teacher Id is already Registered, please choose another','danger')
				return render_template('/ADMIN/addnewprofessor.html', form=form)
			else:
				entry = Teacherregister(name=name,email = email,Tid = Tid,Gender = Gender,birth= birth,contact=contact,department = department,qualifications = qualifications,designation = designation,Address = Address,pincode = pincode,password = secure_password,confirm_password=secure_password)
				db.session.add(entry)
				db.session.commit()
				msg=Message(subject="New message from Student Assignment Submission Portal",sender='studentassignmentportal12@gmail.com',recipients =[email])
				msg.html=render_template("temail.html",name=name,Tid=Tid)
				mail.send(msg)
				flash(f'Account created for {form.email.data}!', 'success')
				return redirect(url_for('addnewprofessor'))
		return render_template('/ADMIN/addnewprofessor.html',title='Teacherregister', form=form)
	return redirect(url_for('adminlogin'))


@app.route('/authorizestudent')
def authorizestudent():
	if g.email:
		cursor = mysql.connection.cursor()
		cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cur.execute('SELECT * FROM register')
		data = cur.fetchall()
		cur.close()
		return render_template('/ADMIN/authorizeadmin.html', employee = data)
	return redirect(url_for('adminlogin'))

@app.route('/authorizationstudent/<id>', methods = ['POST', 'GET'])
def authorizationstudent(id):
	if g.email:
		cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cur.execute('SELECT * FROM register WHERE id = %s', (id,))
		data = cur.fetchone()
		result=data['authorization']
		print(result)
		if result== 0:
			cur.execute("""UPDATE register SET authorization=%s WHERE id = %s""", (1, id))
			return redirect(url_for('authorizestudent'))
		else:
			cur.execute("""UPDATE register SET authorization=%s WHERE id = %s""", (0, id))
			return redirect(url_for('authorizestudent'))
	return redirect(url_for('adminlogin'))

@app.route('/authorizeteacher')
def authorizeteacher():
	if g.email:
		cursor = mysql.connection.cursor()
		cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cur.execute('SELECT * FROM teacherregister')
		data = cur.fetchall()
		cur.close()
		return render_template('/ADMIN/authorizeprofessor.html', employee = data)
	return redirect(url_for('adminlogin'))

@app.route('/authorizationforprofessor/<id>', methods = ['POST', 'GET'])
def authorizationforprofessor(id):
	if g.email:
		cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cur.execute('SELECT * FROM teacherregister WHERE id = %s', (id,))
		data = cur.fetchone()
		result=data['authorization']
		print(result)
		if result== 0:
			cur.execute("""UPDATE teacherregister SET authorization=%s WHERE id = %s""", (1, id))
			return redirect(url_for('authorizeteacher'))
		else:
			cur.execute("""UPDATE teacherregister SET authorization=%s WHERE id = %s""", (0, id))
			return redirect(url_for('authorizeteacher'))
	return redirect(url_for('adminlogin'))


@app.errorhandler(Exception)
def exception_handler(error):
	return render_template('index.html')  + repr(error)


app.secret_key="12345678"
app.run(debug=True)

if __name__ == '__main__':
    app.run(debug=True)

