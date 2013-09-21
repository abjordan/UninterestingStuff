#!/bin/env python

import socket

gensToRun = 0
theUniverse = []
params = ""

def countSurrounding(universe, a, b):
    count = 0
    surrounding = ((a - 1, b - 1),
                   (a - 1, b    ),
                   (a - 1, b + 1),
                   (a    , b - 1),
                   (a    , b + 1),
                   (a + 1, b - 1),
                   (a + 1, b    ),
                   (a + 1, b + 1))
    for a, b in surrounding:
        #x = a
        #y = b
        #if (a is -1):
        #    x = len(universe)
        #elif (a is len(universe)):
        #    x = 0
        #if (b is -1):
        #    y = len(universe[0])
        #elif (b is len(universe[0])):
        #    y = 0
        #if not(x < 0 or y < 0 or x >= len(universe) or y >= len(universe[x])) and (universe[x][y] == "*"):
        #    count += 1
        if not(a < 0 or b < 0 or a >= len(universe) or b >= len(universe[a])) and (universe[a][b] == "*"):
            count += 1
        
    return count
    
#def printUniverse(universe):
#    for a in universe:
#        print(a)
#    print("\n")
#nextUniverse = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
#                [0, 0, 0, 0, 0, 0, 0, 0, 0],
#                [0, 0, 0, 1, 0, 0, 0, 0, 0],
#                [0, 0, 0, 1, 0, 0, 0, 0, 0],
#                [0, 0, 0, 1, 0, 0, 0, 0, 0],
#                [0, 0, 0, 1, 0, 0, 0, 0, 0],
#                [0, 0, 0, 1, 0, 0, 0, 0, 0],
#                [0, 0, 0, 0, 0, 0, 0, 0, 0],
#                [0, 0, 0, 0, 0, 0, 0, 0, 0]]
def runLife(nextUniverse, iterations):
    for gen in range(0, iterations):
        universe = [a[:] for a in nextUniverse]
        # printUniverse(universe)
        for a in range(0, len(universe)):
            for b in range(0, len(universe[a])):
                count = 0
                surrounding = ((a - 1, b - 1),
                       (a - 1, b    ),
                       (a - 1, b + 1),
                       (a    , b - 1),
                       (a    , b + 1),
                       (a + 1, b - 1),
                       (a + 1, b    ),
                       (a + 1, b + 1))
                for x, y in surrounding:
                    if not(x < 0 or y < 0 or x >= len(universe) or y >= len(universe[x])) and (universe[x][y] == "*"):
                        count += 1
                        
                if universe[a][b] == " " and count == 3:
                    nextUniverse[a][b] = "*"
                elif universe[a][b] == "*" and (count != 2) and (count != 3):
                    nextUniverse[a][b] = " "
                else:
                    nextUniverse[a][b] = universe[a][b]
    return nextUniverse

def formatBoard(uni):
    # [ [ " ", "*", " ", ... ]
    #   ...
    #   [        ...         ] ]
    height = len(uni)
    width = len(uni[0])
    out = ""
    # out += params + "\n"
    out += "#" * (width + 2) + "\n"
    for row in uni:
        out += "#" + "".join(row) + "#\n"
    out += "#" * (width + 2) + '\n'
    # out += '\n'
    return out
    
    
def lifeIt(in_data, time):
    global gensToRun
    global board
    global params
    lines = in_data.split("\n")
    #print time, "========"
    #i = 0
    #for line in lines:
    #    print "%02dLINE :" % i, line
    #    i += 1
    #print time, "========"
    
    if time == 0:
        # This is the setup
        params = lines[1]
        toks = params.split(":")
        gens = toks[1].strip().split(" ")[0]
        gensToRun = int(gens)
        return None
        
    elif time == 1:
        board = lines
        width = len(board[0])
        height = len(board) - 2
        real_board = [r.strip("#") for r in board[1:height]]
        theUniverse = []
        for b in real_board:
            cells = [x for x in b]
            theUniverse.append(cells)
        
        after = runLife(theUniverse, gensToRun)
        str = formatBoard(after)
        #i = 0
        #for line in str.split("\n"):
        #    print "%02dAFTER:" % i, line
        #    i += 1
        return str
    
def netcat(hostname, port, content=None):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((hostname, port))
    called = 0
    won = False
    while 1:
        data = s.recv(4096)
        if data == "":
            break
        # print "Received:", repr(data)
        if "#####" not in data:
            print "Received:", repr(data)
            
        if "Congratulations" in data:
            won = True
        
        if not won:
            retn = lifeIt(data,called)
            called += 1 
        
            if retn is not None:
                print "SENDING"
                # retn = "##### Round 2: 0 Generations #####\n" + retn
                s.sendall(retn)
                called = 0
        
    print "Connection closed."
    s.close()
    
# nc 128.238.66.216 45678
if __name__=="__main__":
    netcat("128.238.66.216", 45678)