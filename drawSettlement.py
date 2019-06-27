# Basic Animation Framework

from tkinter import *

####################################
# customize these functions
####################################

def init(data):
    # load data.xyz as appropriate
    data.cx = data.width/2
    data.cy = data.height/2
    data.cx2 = data.width/2-50
    data.cy2 = data.height/2-50

def mousePressed(event, data):
    # use event.x and event.y
    pass

def keyPressed(event, data):
    # use event.char and event.keysym
    pass

def redrawAll(canvas, data):
    # draw in canvas
    #canvas.create_polygon(data.cx, data.cy-15, data.cx-15, data.cy, data.cx-15, data.cy+15, data.cx+15, data.cy+15, data.cx+15, data.cy, fill='yellow3')
    #canvas.create_polygon(data.cx, data.cy-15, data.cx-15, data.cy, data.cx-35, data.cy-5, data.cx-15, data.cy-20, fill='yellow')
    #canvas.create_polygon(data.cx-15, data.cy, data.cx-35, data.cy-5, data.cx-35, data.cy+10, data.cx-15, data.cy+15, fill='yellow2')
    canvas.create_polygon(data.cx, data.cy-15, data.cx-10, data.cy, data.cx-10, data.cy+10, data.cx+10, data.cy+10, data.cx+10, data.cy, fill='magenta4')
    canvas.create_polygon(data.cx, data.cy-15, data.cx-10, data.cy, data.cx-25, data.cy-5, data.cx-15, data.cy-20, fill='magenta2')
    canvas.create_polygon(data.cx-10, data.cy, data.cx-25, data.cy-5, data.cx-25, data.cy+5, data.cx-10, data.cy+10, fill='magenta3')
    
    canvas.create_polygon(data.cx2, data.cy2-15, data.cx2-5, data.cy2-10, data.cx2-5, data.cy2, data.cx2-10, data.cy2, data.cx2-10, data.cy2+5, data.cx2+5, data.cy2+5, data.cx2+5, data.cy2-10, fill='medium blue')
    canvas.create_polygon(data.cx2, data.cy2-15, data.cx2-5, data.cy2-10, data.cx2-15, data.cy2-15, data.cx2-10, data.cy2-20, fill='royal blue')
    canvas.create_polygon(data.cx2-5, data.cy2-10, data.cx2-15, data.cy2-15, data.cx2-15, data.cy2-5, data.cx2-5, data.cy2, fill='RoyalBlue2')
    canvas.create_polygon(data.cx2-15, data.cy2-5, data.cx2-20, data.cy2-5, data.cx2-10, data.cy2, data.cx2-5, data.cy2, fill='royal blue')
    canvas.create_polygon(data.cx2-20, data.cy2-5, data.cx2-20, data.cy2, data.cx2-10, data.cy2+5, data.cx2-10, data.cy2, fill='RoyalBlue2')

    

####################################
# use the run function as-is
####################################

def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    root = Tk()
    root.resizable(width=False, height=False) # prevents resizing window
    init(data)
    # create the root and the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.configure(bd=0, highlightthickness=0)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    redrawAllWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run(600, 600)