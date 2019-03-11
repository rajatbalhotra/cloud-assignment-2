'''
Created on 28-Feb-2019

@author: seerat
'''
import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import dbtable
from sqlalchemy import Date
from _datetime import datetime
 
engine = create_engine('sqlite:///cloudtable.db', echo=True)
# login_id = 2
# result = engine.execute('SELECT * FROM "VIM"')
# print(result)
# for _r in result:
#     print(_r)
# for _row in result.all():
#     print(_row.cc_id)
    
#create a Session
Session = sessionmaker(bind=engine)
session = Session()
 
user = dbtable.User("admin","password")
session.add(user)
  
user = dbtable.User("seerat","sohal")
session.add(user)
  
user = dbtable.User("shivani","solanki")
session.add(user)
 
vm = dbtable.VIM(2,2,"Basic",datetime(2012, 3, 3, 10, 10, 10),datetime(2012, 3, 3, 11, 10, 10),20)
session.add(vm)
# # commit the record the database
session.commit()
  
# session.commit()