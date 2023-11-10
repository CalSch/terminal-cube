import math
import time
import random
import os

termsize=os.get_terminal_size()

# width =termsize.columns - 5
# height=termsize.lines*2 - 5
width =64
height=64

running = True
t = 0
rx=0
ry=0
rz=0
fps = 60

mesh_lines = [
    [ [-1,-1,-1], [1,-1,-1] ],
    [ [-1,-1,1], [1,-1,1] ],
    [ [-1,1,-1], [1,1,-1] ],
    [ [-1,1,1], [1,1,1] ],

    [ [-1,-1,-1], [-1,1,-1] ],
    [ [1,-1,-1], [1,1,-1] ],
    [ [-1,-1,1], [-1,1,1] ],
    [ [1,-1,1], [1,1,1] ],

    [ [-1,-1,-1], [-1,-1,1] ],
    [ [1,-1,-1], [1,-1,1] ],
    [ [-1,1,-1], [-1,1,1] ],
    [ [1,1,-1], [1,1,1] ],
]
# mesh_lines = [
#     [ [0,0,0], [1,0,0] ],
#     [ [0,0,0], [0,1,0] ],
#     [ [0,0,0], [0,0,1] ],
# ]

screen=[]

def clear():
    global screen
    screen=[]
    for y in range(height):
        row=[]
        for x in range(width):
            row.append(False)
        screen.append(row)

def draw_point(x:float,y:float,c:bool):
    if x<0 or y<0 or x>=width or y>=height:
        return
    screen[int(y)][int(x)]=c

def draw_line(x0:float,y0:float,x1:float,y1:float,c:bool):
    x0=int(x0)
    y0=int(y0)
    x1=int(x1)
    y1=int(y1)
    dx = x1 - x0 if x1 >= x0 else x0 - x1
    dy = y0 - y1 if y1 >= y0 else y1 - y0
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx + dy
    x = x0
    y = y0
    while True:
        draw_point(x,y,c)
        if((x == x1) and(y == y1)):
            break
        e2 = 2 * err;

        if e2 >= dy: # step x
            err += dy
            x += sx
        
        if e2 <= dx: # step y
            err += dx
            y += sy

def add(p1:list[float],p2:list[float]):
    for i in range(len(p1)):
        p1[i]+=p2[i]
    return p1
def scale(p:list[float],scalar:float):
    for i in range(len(p)):
        p[i]*=scalar
    return p
def sub(p1:list[float],p2:list[float]):
    return add(p1,scale(p2,-1))

def rotate(point:list[float],rx:float,ry:float,rz:float,origin:list[float]=[0,0,0]) -> list[float]:
    point=sub(point,origin)
    cosa = math.cos(ry);
    sina = math.sin(ry);

    cosb = math.cos(rx);
    sinb = math.sin(rx);

    cosc = math.cos(rz);
    sinc = math.sin(rz);

    Axx = cosa*cosb;
    Axy = cosa*sinb*sinc - sina*cosc;
    Axz = cosa*sinb*cosc + sina*sinc;

    Ayx = sina*cosb;
    Ayy = sina*sinb*sinc + cosa*cosc;
    Ayz = sina*sinb*cosc - cosa*sinc;

    Azx = -sinb;
    Azy = cosb*sinc;
    Azz = cosb*cosc;

    px=point[0]
    py=point[1]
    pz=point[2]

    point[0] = Axx*px + Axy*py + Axz*pz;
    point[1] = Ayx*px + Ayy*py + Ayz*pz;
    point[2] = Azx*px + Azy*py + Azz*pz;

    return add(point,origin)

def project(p:list[float]) -> list[float]:
    # p[1]=1-p[1]
    return add([
        p[0]* width/4,
        p[1]*height/4
    ],[width/2,height/2])

def draw_screen():
    s=""
    for line in range(int(height/2)):
        y=line*2
        y2=y+1
        for x in range(width):
            if screen[y][x]:
                if screen[y2][x]:
                    s += "█"
                else:
                    s += "▀"
            else:
                if screen[y2][x]:
                    s += "▄"
                else:
                    s += " "
        s += " |\n"
    s += "-"*width+"-+"
    print(s)

def update():
    global rx,ry,rz
    rx += 1 / fps
    ry += 2 / fps
    rz += 3 / fps


def draw():
    # origin = [0,0,0]
    # origin2d = project(origin)
    # p = [10,10,0]
    # p=rotate(p,rx,ry,rz)
    # p2d=project(p)
    # line(origin2d[0],origin2d[1],p2d[0],p2d[1],True)
    # print(p[2])
    for line in mesh_lines:
        p0=line[0].copy()
        p1=line[1].copy()
        p0=rotate(p0,rx,ry,rz)
        p1=rotate(p1,rx,ry,rz)
        p02d=project(p0)
        p12d=project(p1)
        draw_line(
            p02d[0],
            p02d[1],
            p12d[0],
            p12d[1],
            True
        )


clear()

if __name__=="__main__":
    print("\x1b[2J")
    while running:
        termsize=os.get_terminal_size()
        width = height = min(termsize.columns,termsize.lines*2) - 5
        print("\x1b[H",end="")
        clear()
        update()
        draw()
        draw_screen()
        time.sleep(1/fps)
        t += 1/fps