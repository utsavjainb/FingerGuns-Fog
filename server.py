# first of all import the socket library
import json
import socket

# next create a socket object
s = socket.socket()
print("Starting Fog Server")
listening = True

# reserve a port on your computer in our
# case it is 12345 but it can be anything
port = 12345

# Next bind to the port
# we have not typed any ip in the ip field
# instead we have inputted an empty string
# this makes the server listen to requests
# coming from other computers on the network
s.bind(('', port))
print("socket binded to %s" % (port))

# put the socket into listening mode
s.listen(5)
print("socket is listening")
c = None

rmoves = {"0": "READY", "1": "RELOAD", "2": "SHIELD", "3": "SHOOT", "False": ''}

# a forever loop until we interrupt it or
# an error occurs
while listening:
    # Establish connection with client.
    if c is None:
        c, addr = s.accept()
        print('Got connection from', addr)

    # send message to Game Server with Client ID
    # get game status from game server
    # {status: "Waiting Opponent"}
    game_input = input("Game Server Response: ")
    data = {"status": game_input, "Round": 1, "Bullet Count": 1, "Player Move": "SHOOT", "Opp Move": "RELOAD"}
    end_data = {
        "status": "Make Move",
        "Round": 1,
        "Bullet Count": 2,
        "Player Move": "Shield",
        "Opp Move": "Shoot",
        "PStats": {"SHOOT": 3, "SHIELD": 5, "RELOAD": 2},
        "OppStats": {"SHOOT": 2, "SHIELD": 7, "RELOAD": 1}
    }


    if data["status"] == "Waiting for Opponent":
        output = json.dumps(data)
        c.send(output.encode('utf-8'))
    elif data["status"] == "Make Move":
        output = json.dumps(data)
        c.send(output.encode('utf-8'))
        data = c.recv(1024).decode('utf-8')

        data = {"action": data}
        print("From Pi: {}".format(data))
    elif data["status"] == "Winner":
        data["PStats"] = end_data["PStats"]
        data["OppStats"] = end_data["OppStats"]
        output = json.dumps(data)
        c.send(output.encode('utf-8'))
    elif data["status"] == "Loser":
        output = json.dumps(data)
        c.send(output.encode('utf-8'))
    # else:
    #     output = data["status"]
    #     c.send(output.encode('utf-8'))

    # if data is None:
    #     continue
    # elif "action" in data.keys():
    #     if data["action"] == "disconnect":
    #         c.close()

