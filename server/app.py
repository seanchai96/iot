from flask import Flask, render_template, request, session, redirect, url_for , flash
import mysql
import time
from mysql.connector import errorcode
from datetime import datetime 
import json
from get_data import get_data, real_time, get_hourly, get_pic
from googleapiclient.discovery import build
from get_mr_data import authenticate, get_list_of_events

app = Flask(__name__)             

app.config['SECRET_KEY'] = "mysecretkey"



@app.route("/")                  
def hello():         
    #session['admin'] = False             
    return render_template("user.html")    

# @app.route("/user")
# def user():
#     return render_template("user.html")

@app.route("/process_login" , methods=['POST'])
def process_login():
    #session['admin'] = True
    return redirect("/home")

@app.route("/home")
def home(): 
    # if session['admin'] != True:
    #     return redirect("/")
    return render_template("overview.html")

@app.route("/hotdesk")
def hotdesk(): 
    # if session['admin'] != True:
    #     return redirect("/")
    return render_template("hotdesk.html")


@app.route("/meetingroom")
def test(): 
    # if session['admin'] != True:
    #     return redirect("/")
    return render_template("meeting_room.html")


@app.route("/about")
def about(): 
    # if session['admin'] != True:
    #     return redirect("/")
    return render_template("about.html")

import base64

@app.route("/get_utilization_stats", methods=["GET"])
def get_seat_utilization_img():

    current = real_time()
    status = get_pic()
    mb2, mb7 = status[0], status[1]

    if mb2[0] == "EMPTY": 
        a = "G"
    elif mb2[0] == "HOGGING":
        a = "O"
    elif mb2[0] == "OCCUPIED":
        a = "R"
    
    if mb7[0] == "EMPTY":
        b = "G"
    elif mb7[0] == "HOGGING":
        b = "O"
    elif mb7[0] == "OCCUPIED":
        b = "R"
    
    filename = "http://77robinson.xyz/static/img/a" + a +  "_b" + b  + "_Zoom.png"
    obj = {}
    obj['img'] = filename
    obj['empty'] = current[0]
    obj['occupied'] = current[2]
    obj['hogging'] = current[1]
    return obj

@app.route("/secret_sauce", methods=["GET"])
def secret_sauce():
    obj = {"sean": "http://77robinson.xyz/static/img/profile2.png", "sean1" : "http://77robinson.xyz/static/img/profile1.jpg"}
    return obj


@app.route("/get_seats", methods=['POST','GET'])
def get_seats():
    current = real_time()
    status = get_pic()
    mb2, mb7 = status[0], status[1]

    if mb2[0] == "EMPTY": 
        a = "G"
    elif mb2[0] == "HOGGING":
        a = "O"
    elif mb2[0] == "OCCUPIED":
        a = "R"
    
    if mb7[0] == "EMPTY":
        b = "G"
    elif mb7[0] == "HOGGING":
        b = "O"
    elif mb7[0] == "OCCUPIED":
        b = "R"
    
    return json.dumps([current[2], current[0], current[1], a, b])
    # empty color = "Green", hog color = "Orange", occ color = "Red"
        #return json.dumps([occupied_counter,empty_counter,hogging_counter, color])

@app.route("/get_doughnut", methods=['POST','GET'])
def get_doughnut():
    doughnut = real_time()
    print(doughnut)
    return json.dumps(doughnut)

@app.route("/get_stacked", methods=['POST', 'GET'])
def get_stacked():
    mon = get_data(0, "ALL")
    tue = get_data(1, "ALL")
    wed = get_data(2, "ALL")
    thur = get_data(3, "ALL")
    fri = get_data(4, "ALL")
    return json.dumps([mon, tue, wed, thur, fri])

@app.route("/get_stacked_cur", methods=['POST', 'GET'])
def get_stacked_cur():
    mon = get_data(0, "DAY")
    tue = get_data(1, "DAY")
    wed = get_data(2, "DAY")
    thur = get_data(3, "DAY")
    fri = get_data(4, "DAY")
    return json.dumps([mon, tue, wed, thur, fri])

@app.route("/get_line", methods=['POST', 'GET'])
def get_line():
    stacked_line = get_hourly()
    return json.dumps(stacked_line)

@app.route("/get_line_weekly", methods=['POST', 'GET'])
def get_line_weekly():
    stacked_line_weekly = get_hourly("WEEKLY")
    return json.dumps(stacked_line_weekly)

@app.route("/get_line_all", methods=['POST', 'GET'])
def get_line_all():
    #stacked_line_all = get_hourly("ALL")
    final_occ = [0,0,0,1,1,1,0,0,0,1,1,0,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0]
    final_emp = [2,2,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,2,2]
    final_hog = [0,0,0,0,0,0,1,1,1,0,0,1,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

    return json.dumps([final_emp, final_occ, final_hog])

@app.route("/get_schedule", methods=['GET'])
def get_schedule():
    creds = authenticate()
    service = build('calendar', 'v3', credentials=creds)

    # Meeting room H's ID
    meetingroom_id = 'ntucenterprise.sg_3234373130333231363934@resource.calendar.google.com' 

    events = get_list_of_events(service, meetingroom_id, '2020-04-02')
    return json.dumps(events)

@app.errorhandler(404)
def page_not_found(e):
    # your processing here
    return redirect("/")

if __name__ == "__main__":        
    # app.run(host="0.0.0.0")
    app.run(debug=True)


