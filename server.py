# first of all import the socket library
import socket
import io

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
    data = {"status": game_input}

    if data["status"] == "Waiting for Opponent":
        output = 'Waiting for Opponent'
        c.send(output.encode('utf-8'))
    elif data["status"] == "Make Move":
        output = 'Make Move'
        c.send(output.encode('utf-8'))
        data = c.recv(1024).decode('utf-8')
        data = {"action": data}
        print("From Pi: {}".format(data))
    elif data["status"] == "Winner":
        output = 'Winner'
        c.send(output.encode('utf-8'))
    elif data["status"] == "Loser":
        output = 'Loser'
        c.send(output.encode('utf-8'))
    # else:
    #     output = data["status"]
    #     c.send(output.encode('utf-8'))

    # if data is None:
    #     continue
    # elif "action" in data.keys():
    #     if data["action"] == "disconnect":
    #         c.close()

