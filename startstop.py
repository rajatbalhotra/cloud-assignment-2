'''
Created on Mar. 4, 2019

@author: khushali
'''


from datetime import datetime

def time_difference(time_start, time_end):
    

    start = datetime.strptime(time_start, "%H%M")
    end = datetime.strptime(time_end, "%H%M")
    difference = end - start
    minutes = difference.total_seconds() / 60
    return int(minutes)