from flask import Flask, request, jsonify
import json
import sqlite3

app = Flask(__name__)

#database connecting function

def db_connection():
    conn = None
    try:
        conn = sqlite3.connect("events.sqlite")
    except sqlite3.Error as e:
        print(e)

    return conn

#return sample data

events_list = [
   {
       "id":0,
       "event_type": "pull_request",
       "event_name": "change_event"
   },


   {
       "id":1,
       "event_type":"release",
       "event_name":"deployment_event"
   },
   {
       "id":2,
       "event_type":"push",
       "event_name":"workflow_event"
   },
   {
       "id":3,
       "event_type": "pull_request_merged",
       "event_name":"deployment_event"
   }
]

#define our own endpoints or routes 
@app.route('/events', methods=["GET","POST"])
def events():
    conn = db_connection()
    #creates a cursor object used to execute SQL queries against database
    cursor = conn.cursor()

    #once query is executed can be used to fetch results

    #use get method to serve request
    if request.method == "GET":
        if len(events_list) > 0:
            return jsonify(events_list)
        else:
            return 'No Event found', 404
        

    #check if method is post
    if request.method == "POST":
        new_event_type = request.json['event_type']
        new_event_name = request.json['event_name']

        sql = """INSERT INTO events (event_type, event_name)
             VALUES (?, ?)"""
        
        cursor.execute(sql, (new_event_type, new_event_name))
        conn.commit()

        #update the eventid
        new_event_id = cursor.lastrowid

        new_obj = {
            'id': new_event_id,
            'event_type': new_event_type,
            'event_name': new_event_name
        }

        events_list.append(new_obj)
        return jsonify(events_list), 201
    
    #single event endpoint

@app.route('/event/<int:id>',methods=['GET','PUTS'])
def single_event_workflow(id):
    conn = db_connection()
    cursor = conn.cursor()

    #GET Methods
    if request.method == "GET":
        for event in events_list:
            if event[id] == id:
                return jsonify(event)
            return "Event not found"
        
    #PUT Methods
    if request.method == "PUT":
        updated_event_type = request.json['event_type']
        updated_event_name = request.json['event_name']

        sql = """INSERT INTO events (event_type, event_name)
             VALUES (?, ?)"""
        
        cursor.execute(sql, (updated_event_type, updated_event_name))
        conn.commit

        for event in events_list:
            if events['id'] == id:
                event['event_type'] = updated_event_type
                event['event_name'] = updated_event_name

                return jsonify(event), 200
        return "Event not found", 404
    
    #patch method
    if request.method == "PATCH":

        #loop through elements
        for event in events_list:
            if event['id'] == id:
                #request the passed in json values
                new_event_type = request.json['event_type']
                new_event_name = request.json['event_name']

                #check if update is necessary
                if new_event_name is not event["event_name"] or new_event_type is not event["event_type"]:
                    event["event_name"] = new_event_name
                    event["event_type"] = new_event_type


    






