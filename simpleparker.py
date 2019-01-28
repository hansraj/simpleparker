from flask import Flask
from flask import request
from flask import Response 
import json
app = Flask(__name__)

#Assume a grid of parking slots on the map with indexes representing the co-ordinates(lat, long)
#Open slots are marked by 0, filled slots marked by numbers > 0 (user ids)
slot = [[2,1,1,1,0,0,0,0],
        [2,1,1,1,0,0,0,4],
        [1,1,1,0,0,0,0,0],
        [8,0,0,1,0,0,0,0],
        [0,0,0,0,0,0,0,7],
        [0,0,0,2,0,0,0,0],
        [9,1,0,0,0,0,6,0],
        [1,0,0,4,0,0,0,0],
        [6,3,0,0,0,0,3,0]]


@app.route("/")
def welcome():
    return '''WELCOME TO PARKER.. Your parking helper -- 
            (1) To list open parkings within a radius:
                e.g:  /list/lat=2&lon=2&r=2
            (2) To list your total bookings:
                e.g: /mybookings/user=1
            (3) To book a new parking slot:
                e.g. /book/lat=3&lon=4/user=1
            (4) To Cancel booking:
                e.g. /book/lat=3&lon=4/user=1'''

@app.route("/user/<username>", methods=['GET'])
def show_user(username):
    return 'Hello %s ' % username 


@app.route("/list/", methods=['GET'])
def get_open_list():
    open_slots = []
    count = 0
    lat = int(request.args.get('lat'))
    lon = int(request.args.get('lon'))
    r = int(request.args.get('r')) + 1
    if(lat > 7 or lon > 9 or r > 3):
        return "Invalid or out of range parameters. Please try again with correct values"
    open_slots_count = str(slot).count('0')
    for i in range((lat - r), (lat + r)):
        for j in range((lon - r), (lon + r)):
            if(slot[i][j]==0 and i>=0 and j>=0):
                count+=1
                open_slots.insert(0, ("[lat:%d, lon:%d] " % (i,j)))

    open_slots.insert(0, "TOTAL SLOTS AVAILABLE: [%d]" % count)
    response_json = json.dumps(open_slots)
    return Response(response_json, 'application/json')

@app.route("/mybookings/<user>", methods=['GET'])
def my_bookings(user):
#    user = request.args.get('user')
    return "You have total: %d bookings" % (str(slot).count(user))


@app.route("/book/", methods=['GET', 'POST'])
def book():
    lat = int(request.args.get('lat'))
    lon = int(request.args.get('lon'))
    user = int(request.args.get('user'))
    if(lat > 7 or lon > 9 or user < 0):
        return "Invalid or out of range parameters. Please try again with correct values"
    if(slot[lat][lon] == 0):
        slot[lat][lon] = user
        open_slots = str(slot).count('0')
        return "Booked successful. [OPEN SLOTS: %d ] " % open_slots
    else:
        open_slots = str(slot).count('0')
        return "Parking slot taken, Please try another. [OPEN SLOTS: %d ]" %open_slots


@app.route("/cancel/", methods=['GET', 'POST'])
def cancel_booking():
    lat = int(request.args.get('lat'))
    lon = int(request.args.get('lon'))
    user = int(request.args.get('user'))
    if(lat > 7 or lon > 9 or user < 0):
        return "Invalid parameters. Please try again with correct values"
    if(slot[lat][lon] == user):
        slot[lat][lon] = 0
        open_slots = str(slot).count('0')
        return "Booking cancellation successfull. [OPEN SLOTS: %d ] " % open_slots
    else:
        open_slots = str(slot).count('0')
        return "Booking Cancellation Unsuccessful, try another.[OPEN SLOTS: %d ] " % open_slots

if __name__ == "__main__":
    app.run()

