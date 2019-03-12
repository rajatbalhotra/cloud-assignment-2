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
from flask import make_response

from dbtable import *
from _datetime import timedelta
engine = create_engine('sqlite:///cloudtable.db', echo=True)
 
app = Flask(__name__)


@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return 'Hello User! <a href="logout">Logout</a>'

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
        session['username']= POST_USERNAME
        session['login_id']=result.login_id

        return render_template('nextpage.html',login_id = result.login_id, username= result.username)
         
    else:
        flash('wrong password!')
        return home()
 
@app.route("/logout")
def logout():
    session['logged_in'] = False
    return home()

@app.route("/next", methods=['POST'])
def next_page():
    vm_config = str(request.form['VS Instance']).split(',')
    print(vm_config)
    items=[]
#     plan = vm_config[0]
    username= vm_config[1]
    login_id = vm_config[2]
    session['plan']=vm_config[0]
    plan = session.get('plan')
    time = session.get('stime')
    Session = sessionmaker(bind=engine)
    s = Session()
    q = s.query(VIM).filter(VIM.cc_id.in_(login_id))
    p = q.all()
    return render_template('page3.html',result=p,login_id=login_id,plan=plan,time=time)

@app.route("/page", methods=['GET','POST'])
def page():
#     plan = session.get('plan')
    login_id = session.get('login_id')
#     print(user_id,plan,login_id)
    Session = sessionmaker(bind=engine)
    s = Session()
    start = (request.form['time'])
    vm_id= (request.form['vm_id'])
    pl = (request.form['plan'])
    print(vm_id)
    if start:
        time = datetime.now()
        print(time)
        session['stime']=time
        vm = s.query(VIM).filter_by(vm_id=vm_id,cc_id=login_id).first()
        print("hello1")
        if vm:
            print("hello")
            if(vm.vm_type != pl):
                vm.vm_type = pl
                vm.start = time
                vm.stop = None
                s.commit()
                return render_template('page3.html')
            else:
                return render_template('page3.html')
        else:    
            vm = VIM(vm_id = vm_id,cc_id = login_id,vm_type= pl,start =time, stop=None,charges=None) 
            s.add(vm)
            s.commit()
            return render_template('page3.html')

@app.route("/pagestop", methods=['GET','POST'])
def pageStop():
    user_id = session.get('username')
    plan = session.get('plan')
    login_id = session.get('login_id')
    stop = (request.form['time'])
    vm_id= (request.form['vm_id'])
    if stop:
        time = datetime.now()
        Session = sessionmaker(bind=engine)
        s = Session()
        vm = s.query(VIM).filter_by(vm_id=vm_id,cc_id=login_id).first()
        start= vm.start
        ch = vm.charges
        vmplan = vm.vm_type
        vm.stop = time
        diff = timediff(start, time)
        charge = charges(diff,vmplan,ch)
        vm.stop = time
        vm.charges = charge
        s.commit()
        return render_template('page3.html',time=time)
    
@app.route("/upgrade", methods=['GET','POST'])
def upgrade():
    up = (request.form['up'])
    currentP = (request.form['cplan'])
    if up:
        if currentP == "Basic":
            session['plan']="Large"
        elif currentP =="Large":
            session['plan']="Ultra-Large"
    print(session.get("plan"))
    return render_template('page3.html',plan = session.get("plan"))

@app.route("/delete", methods=['GET','POST'])
def delete():
    vm = request.form['vm_id']
#     user_id = session.get('username')
    print(vm)
    Session = sessionmaker(bind=engine)
    s = Session()
    record = s.query(VIM).filter_by(vm_id=vm).all()
    for o in record:
        s.delete(o)
        s.commit()
    return render_template('page3.html')
        

def timediff(start,stop):
    diff = ((stop-start)// timedelta(minutes=1))
    return(diff)

def charges(diff,vmplan,ch):
    if(ch != None):
        if vmplan == "Basic":
            charge = ch+(diff*5)
        elif vmplan == "Large":
            charge = ch+(diff*10)
        elif vmplan == "Ultra-Large":
            charge = ch+(diff*15)
    else:
        if vmplan == "Basic":
            charge = diff*5
        elif vmplan == "Large":
            charge = diff*10
        elif vmplan == "Ultra-Large":
            charge = diff*15
    return(charge)

if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True,host='0.0.0.0', port=4000)
