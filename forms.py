from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField,RadioField,SelectField,TextAreaField,TextField
from wtforms.validators import DataRequired, Length, Email, EqualTo,ValidationError
from wtforms.fields.html5 import DateField
from wtforms import validators
from flask import Flask, render_template,request,flash,session,url_for,redirect,session

class RegistrationForm(FlaskForm):
    name = StringField("Fullname",validators=[validators.DataRequired("Please enter your Full name."),validators.Regexp(regex="[a-zA-Z]",message="Fullname Should Only Contain Letters")])
    email = StringField('Email',validators=[DataRequired("Please enter your Email."), Email()])
    password = PasswordField('Password', validators=[DataRequired("Please enter your Password.")])
    confirm_password = PasswordField('Confirm Password',validators=[DataRequired("Please enter your Confirm Password."), EqualTo('password',message='Password and Confirm Password must match')])
    Enrollment = StringField('Enrollment No',validators=[DataRequired("Please enter your Enrollment Number."),validators.Regexp(regex='[0-9]{11}',message="Enrollment Should Only Contain Eleven Numbers")])
    Gender = RadioField('Gender', choices = [('M','Male'),('F','Female')])
    birth = DateField("Date Of Birth", format='%Y-%m-%d', validators=[DataRequired(message="Please Select the Date Of Birth")],)
    contact = StringField('Mobile Number',validators=[DataRequired("Please enter your Mobile Number."),validators.Regexp(regex='(((\+){1}91){1})? ?-?[0-9]{10}',message="Please Enter Valid Mobile Number")])
    semester=SelectField('Your Semester:', coerce=int,choices=[(0, 'Please Select...'), (1, '1'),(2, '2'),(3, '3'),(4, '4'),(5, '5'),(6, '6'),(7, '7'),(8, '8')],validators=[DataRequired("Please enter your Semester.")])
    city=SelectField('Your City:', choices=[('0', 'Please Select...'), ('Ahmedabad','Ahmedabad')],validators=[DataRequired("Please enter your City.")])
    state=SelectField('Your State:', choices=[('0', 'Please Select...'), ('Gujarat','Gujarat')],validators=[DataRequired()])
    Address = TextAreaField('Address:',validators=[DataRequired("Please enter your Address.")])
    pincode = StringField('Pincode',validators=[DataRequired("Please enter your Pincode."),validators.Regexp(regex='[0-9]{6}',message="Pincode Should Only Contain Six Numbers") ])
    authorization = SelectField('Authorization', choices=[('0','0')])
    submit = SubmitField('Sign Up')

class EditProfileForm(FlaskForm):
    name = StringField("Fullname",validators=[validators.DataRequired("Please enter your Full name."),validators.Regexp(regex="[a-zA-Z]",message="Fullname Should Only Contain Letters")])
    email = StringField('Email',validators=[DataRequired("Please enter your Email."), Email()])
    password = PasswordField('Password', validators=[DataRequired("Please enter your Password.")])
    confirm_password = PasswordField('Confirm Password',validators=[DataRequired("Please enter your Confirm Password."), EqualTo('password',message='Password and Confirm Password must match')])
    Enrollment = StringField('Enrollment No',validators=[DataRequired("Please enter your Enrollment Number."),validators.Regexp(regex='[0-9]{11}',message="Enrollment Should Only Contain Eleven Numbers")])
    Gender = RadioField('Gender', choices = [('M','Male'),('F','Female')])
    birth = DateField("Date Of Birth", format='%a, %d %b %Y %H:%M:%S GMT', validators=[DataRequired(message="Please Select the Date Of Birth")],)
    contact = StringField('Mobile Number',validators=[DataRequired("Please enter your Mobile Number."),validators.Regexp(regex='(((\+){1}91){1})? ?-?[0-9]{10}',message="Please Enter Valid Mobile Number")])
    semester=SelectField('Your Semester:', coerce=int,choices=[(0, 'Please Select...'), (1, '1'),(2, '2'),(3, '3'),(4, '4'),(5, '5'),(6, '6'),(7, '7'),(8, '8')],validators=[DataRequired("Please enter your Semester.")])
    city=SelectField('Your City:',choices=[('0', 'Please Select...'), ('Ahmedabad','Ahmedabad')],validators=[DataRequired("Please enter your City.")])
    state=SelectField('Your State:', choices=[('0', 'Please Select...'), ('Gujarat','Gujarat')],validators=[DataRequired()])
    Address = TextAreaField('Address:',validators=[DataRequired("Please enter your Address.")])
    pincode = StringField('Pincode',validators=[DataRequired("Please enter your Pincode."),validators.Regexp(regex='[0-9]{6}',message="Pincode Should Only Contain Six Numbers") ])
    submit = SubmitField('Update Profile')
    submit1 = SubmitField('Change Password')

class TeacherRegistrationForm(FlaskForm):
    name = StringField("Fullname",validators=[validators.DataRequired("Please enter your Full name."),validators.Regexp(regex="[a-zA-Z]",message="Fullname Should Only Contain Letters")])
    email = StringField('Email',validators=[DataRequired("Please enter your Email."), Email()])
    password = PasswordField('Password', validators=[DataRequired("Please enter your Password.")])
    confirm_password = PasswordField('Confirm Password',validators=[DataRequired("Please enter your Confirm Password."), EqualTo('password',message='Password and Confirm Password must match')])
    Tid = StringField('Teacher Id',validators=[DataRequired("Please enter your Enrollment Number."),validators.Regexp(regex='[0-9]{11}',message="Enrollment Should Only Contain Eleven Numbers")])
    Gender = RadioField('Gender', choices = [('M','Male'),('F','Female')])
    birth = DateField("Date Of Birth", format='%Y-%m-%d', validators=[DataRequired(message="Please Select the Date Of Birth")],)
    contact = StringField('Mobile Number',validators=[DataRequired("Please enter your Mobile Number."),validators.Regexp(regex='(((\+){1}91){1})? ?-?[0-9]{10}',message="Please Enter Valid Mobile Number")])
    department=SelectField('Your Department:', choices=[(0, 'Please Select...'), ('B.Tech CSE(Computer Science and Engineering)', 'B.Tech CSE(Computer Science and Engineering)'),('B.Tech ICT(Information Communication Technology)', 'B.Tech ICT(Information Communication Technology)')],validators=[DataRequired("Please enter your Semester.")])
    qualifications=SelectField('Your Qualifications:', choices=[('0', 'Please Select...'), ('B.TECH','B.TECH'),('M.TECH','M.TECH')],validators=[DataRequired("Please enter your City.")])
    designation=SelectField('Your Designation:', choices=[('0', 'Please Select...'), ('Head Of Department(HOD)','Head Of Department(HOD)'),('Professor','Professor'),('Assistant Professor','Assistant Professor')],validators=[DataRequired()])
    Address = TextAreaField('Address:',validators=[DataRequired("Please enter your Address.")])
    pincode = StringField('Pincode',validators=[DataRequired("Please enter your Pincode."),validators.Regexp(regex='[0-9]{6}',message="Pincode Should Only Contain Six Numbers") ])
    authorization = SelectField('Authorization', choices=[('0','0')])
    submit = SubmitField('Sign Up')

class EditTeacherProfile(FlaskForm):
    name = StringField("Fullname",validators=[validators.DataRequired("Please enter your Full name."),validators.Regexp(regex="[a-zA-Z]",message="Fullname Should Only Contain Letters")])
    email = StringField('Email',validators=[DataRequired("Please enter your Email."), Email()])
    password = PasswordField('Password', validators=[DataRequired("Please enter your Password.")])
    confirm_password = PasswordField('Confirm Password',validators=[DataRequired("Please enter your Confirm Password."), EqualTo('password',message='Password and Confirm Password must match')])
    Tid = StringField('Teacher Id',validators=[DataRequired("Please enter your Enrollment Number."),validators.Regexp(regex='[0-9]{11}',message="Enrollment Should Only Contain Eleven Numbers")])
    Gender = RadioField('Gender', choices = [('M','Male'),('F','Female')])
    birth = DateField("Date Of Birth", format='%Y-%m-%d', validators=[DataRequired(message="Please Select the Date Of Birth")],)
    contact = StringField('Mobile Number',validators=[DataRequired("Please enter your Mobile Number."),validators.Regexp(regex='(((\+){1}91){1})? ?-?[0-9]{10}',message="Please Enter Valid Mobile Number")])
    department=SelectField('Your Department:', choices=[(0, 'Please Select...'), ('B.Tech CSE(Computer Science and Engineering)', 'B.Tech CSE(Computer Science and Engineering)'),('B.Tech ICT(Information Communication Technology)', 'B.Tech ICT(Information Communication Technology)')],validators=[DataRequired("Please enter your Semester.")])
    qualifications=SelectField('Your Qualifications:', choices=[('0', 'Please Select...'), ('B.TECH','B.TECH'),('M.TECH','M.TECH')],validators=[DataRequired("Please enter your City.")])
    designation=SelectField('Your Designation:', choices=[('0', 'Please Select...'), ('Head Of Department(HOD)','Head Of Department(HOD)'),('Professor','Professor'),('Assistant Professor','Assistant Professor')],validators=[DataRequired()])
    Address = TextAreaField('Address:',validators=[DataRequired("Please enter your Address.")])
    pincode = StringField('Pincode',validators=[DataRequired("Please enter your Pincode."),validators.Regexp(regex='[0-9]{6}',message="Pincode Should Only Contain Six Numbers") ])
    submit = SubmitField('Update Profile')

class LoginForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class RequestResetForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')

class ChangePasswordForm(FlaskForm):
    olpassword = PasswordField('Old Password', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Change Password')


class StudentRegistrationForm(FlaskForm):
    name = StringField("Fullname",validators=[validators.DataRequired("Please enter your Full name."),validators.Regexp(regex="[a-zA-Z]",message="Fullname Should Only Contain Letters")])
    email = StringField('Email',validators=[DataRequired("Please enter your Email."), Email()])
    password = PasswordField('Password', validators=[DataRequired("Please enter your Password.")])
    confirm_password = PasswordField('Confirm Password',validators=[DataRequired("Please enter your Confirm Password."), EqualTo('password',message='Password and Confirm Password must match')])
    Enrollment = StringField('Enrollment No',validators=[DataRequired("Please enter your Enrollment Number."),validators.Regexp(regex='[0-9]{11}',message="Enrollment Should Only Contain Eleven Numbers")])
    Gender = RadioField('Gender', choices = [('M','Male'),('F','Female')])
    birth = DateField("Date Of Birth", format='%Y-%m-%d', validators=[DataRequired(message="Please Select the Date Of Birth")],)
    contact = StringField('Mobile Number',validators=[DataRequired("Please enter your Mobile Number."),validators.Regexp(regex='(((\+){1}91){1})? ?-?[0-9]{10}',message="Please Enter Valid Mobile Number")])
    semester=SelectField('Your Semester:', coerce=int,choices=[(0, 'Please Select...'), (1, '1'),(2, '2'),(3, '3'),(4, '4'),(5, '5'),(6, '6'),(7, '7'),(8, '8')],validators=[DataRequired("Please enter your Semester.")])
    city=SelectField('Your City:', choices=[('0', 'Please Select...'), ('Ahmedabad','Ahmedabad')],validators=[DataRequired("Please enter your City.")])
    state=SelectField('Your State:', choices=[('0', 'Please Select...'), ('Gujarat','Gujarat')],validators=[DataRequired()])
    Address = TextAreaField('Address:',validators=[DataRequired("Please enter your Address.")])
    pincode = StringField('Pincode',validators=[DataRequired("Please enter your Pincode."),validators.Regexp(regex='[0-9]{6}',message="Pincode Should Only Contain Six Numbers") ])
    submit = SubmitField('Add New Student')

class AdminTeacherRegistrationForm(FlaskForm):
    name = StringField("Fullname",validators=[validators.DataRequired("Please enter your Full name."),validators.Regexp(regex="[a-zA-Z]",message="Fullname Should Only Contain Letters")])
    email = StringField('Email',validators=[DataRequired("Please enter your Email."), Email()])
    password = PasswordField('Password', validators=[DataRequired("Please enter your Password.")])
    confirm_password = PasswordField('Confirm Password',validators=[DataRequired("Please enter your Confirm Password."), EqualTo('password',message='Password and Confirm Password must match')])
    Tid = StringField('Teacher Id',validators=[DataRequired("Please enter your Enrollment Number."),validators.Regexp(regex='[0-9]{11}',message="Enrollment Should Only Contain Eleven Numbers")])
    Gender = RadioField('Gender', choices = [('M','Male'),('F','Female')])
    birth = DateField("Date Of Birth", format='%Y-%m-%d', validators=[DataRequired(message="Please Select the Date Of Birth")],)
    contact = StringField('Mobile Number',validators=[DataRequired("Please enter your Mobile Number."),validators.Regexp(regex='(((\+){1}91){1})? ?-?[0-9]{10}',message="Please Enter Valid Mobile Number")])
    department=SelectField('Your Department:', choices=[(0, 'Please Select...'), ('B.Tech CSE(Computer Science and Engineering)', 'B.Tech CSE(Computer Science and Engineering)'),('B.Tech ICT(Information Communication Technology)', 'B.Tech ICT(Information Communication Technology)')],validators=[DataRequired("Please enter your Semester.")])
    qualifications=SelectField('Your Qualifications:', choices=[('0', 'Please Select...'), ('B.TECH','B.TECH'),('M.TECH','M.TECH')],validators=[DataRequired("Please enter your City.")])
    designation=SelectField('Your Designation:', choices=[('0', 'Please Select...'), ('Head Of Department(HOD)','Head Of Department(HOD)'),('Professor','Professor'),('Assistant Professor','Assistant Professor')],validators=[DataRequired()])
    Address = TextAreaField('Address:',validators=[DataRequired("Please enter your Address.")])
    pincode = StringField('Pincode',validators=[DataRequired("Please enter your Pincode."),validators.Regexp(regex='[0-9]{6}',message="Pincode Should Only Contain Six Numbers") ])
    submit = SubmitField('Add New Professor')