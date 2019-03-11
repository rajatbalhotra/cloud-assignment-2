'''
Created on 28-Feb-2019

@author: seerat
'''
from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort
import os
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import select

from dbtable import *
engine = create_engine('sqlite:///cloudtable.db', echo=True)
 
app = Flask(__name__)


@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return 'Hello User! <a href="logout">Log out</a>'
 
@app.route('/login', methods=['POST'])
def do_admin_login():
 
    POST_USERNAME = str(request.form['username'])
    POST_PASSWORD = str(request.form['password'])
    
    Session = sessionmaker(bind=engine)
    s = Session()
    query = s.query(User).filter(User.username.in_([POST_USERNAME]), User.password.in_([POST_PASSWORD]) )
    result = query.first()
    if result:
        print(result.login_id)
        session['logged_in'] = True
        return render_template('nextpage.html',login_id = result.login_id, username= result.username)
         
    else:
        flash('wrong password!')
        return home()
 
@app.route("/logout")
def logout():
    session['logged_in'] = False
    return home()

@app.route("/nextpage", methods=['GET','POST'])
def next_page():
    vm_config = str(request.form['VS Instance']).split(',')
    print(vm_config)
    items=[]
    plan = vm_config[0]
    username= vm_config[1]
    login_id = vm_config[2]
    Session = sessionmaker(bind=engine)
    s = Session()
#     query = s.execute('SELECT * FROM "VIM"')
    q = s.query(VIM).filter(VIM.cc_id.in_(login_id))
    p = q.all()
#     for d in p:
    return render_template('page3.html',result=p,login_id=login_id,plan=plan)

@app.route("/page3", methods=['GET','POST'])   
def calculate():
    start = request.getData('Start')
    if(start == 'Start'):
        print("hello")
        start = datetime.now()
        return render_template('page3.html',start=start)

#  
# @app.route('/results')
# def search_results(search):
#     results = []
#     search_string = search.data['search']
#  
#     if search.data['search'] == '':
#         qry = db_session.query(Album)
#         results = qry.all()
#  
#     if not results:
#         flash('No results found!')
#         return redirect('/')
#     else:
#         # display results
#         table = Results(results)
#         table.border = True
#         return render_template('results.html', table=table)
    
     
if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True,host='0.0.0.0', port=4000)
