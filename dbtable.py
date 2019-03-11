'''
Created on 28-Feb-2019

@author: seerat
'''
from sqlalchemy import *
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
import datetime
from datetime import datetime

 
engine = create_engine('sqlite:///cloudtable.db', echo=True)
Base = declarative_base()
# Base.metadata.drop_all(engine)

########################################################################
class User(Base):
  
    __tablename__ = "users"
   
    login_id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)
   
#----------------------------------------------------------------------
    def __init__(self, username, password):
  
        self.username = username
        self.password = password
  
# create tables
  
class VIM(Base):
    __tablename__ = "VIM"
      
    vm_id= Column(Integer,autoincrement=False, primary_key=True)
    cc_id=Column(Integer, ForeignKey("users.login_id"),primary_key=True)
    vm_type= Column(String)
    start = Column(TIMESTAMP)
    stop = Column(TIMESTAMP)
    charges = Column(Integer)
    cc= relationship("User", foreign_keys=[cc_id])
      
    def __init__(self,vm_id, cc_id, vm_type, start, stop, charges):
        self.vm_id =vm_id
        self.cc_id = cc_id
        self.vm_type = vm_type
        self.start = start
        self.stop = stop
        self.charges = charges
           
Base.metadata.create_all(engine)