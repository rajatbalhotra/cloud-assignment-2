'''
Created on 25-Feb-2019

@author: seerat
'''
from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort
#import flask
import os
 
app = Flask(__name__)
 
@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('Login.html')
    else:
        return "start session"
 
@app.route('/login', methods=['POST'])
def do_admin_login():
    if request.form['password'] == 'password' and request.form['username'] == 'admin':
        session['logged_in'] = True
 #       vim()
    else:
        #error ='invalid credentials'
        flash('invalid credentials')
        return home()
 
#def vim():
    
     
if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True,host='0.0.0.0', port=4000)
    
