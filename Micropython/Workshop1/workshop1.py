from picounicorn import PicoUnicorn
import time
import random
from math import floor, ceil
picounicorn = PicoUnicorn()
buttonpress = False
button = None

h = picounicorn.get_width()
w = picounicorn.get_height()

red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
black = (0,0,0)
white = (255,255,255)


m = [[0,0,0,0,0,0,0],[0,0,0,1,0,0,0],[0,0,0,1,0,0,0],[0,0,1,1,1,0,0],[0,1,1,1,1,1,0],[1,1,1,1,0,1,0],[1,0,1,1,0,1,0],[1,0,1,1,0,1,1],[1,0,1,1,0,0,0],[0,0,1,1,0,0,0],[0,0,1,1,0,0,0],[0,1,1,0,1,0,0],[0,1,0,0,1,1,0],[1,1,0,0,1,1,0],[1,0,0,0,0,1,1],[0,1,0,0,0,1,0]]
pause = 3
def clear():
    picounicorn.clear()
    
    
def draw_rectangle(x1,y1,x2,y2,colour):
    (r,g,b) = colour
    for i in range(x1,x2+1):
        for j in range(y1,y2+1):
            picounicorn.set_pixel(i,j,r,g,b)
    
def draw_square(x1,y1,size,colour):
    draw_rectangle(x1,y1,x1+size-1,y1+size-1,colour)
    
def draw_circle(x,y,radius,colour):
    (r,g,b) = colour
    for i in range(floor(-radius), ceil(radius+1)):
        for j in range(floor(-radius), ceil(radius+1)):
            if i**2 + j**2 <= (radius*1.5)**2:
                f = ((radius*1.5)**2 - i**2 - j**2)/((radius*1.5)**2)
                f=f**1.5
                picounicorn.set_pixel(x+i,y+j,floor(r*f),floor(g*f),floor(b*f))
            if i**2 + j**2 <= (radius*0.75)**2:
                picounicorn.set_pixel(x+i,y+j,r,g,b)
    
def wait_button():
    while True:
        if picounicorn.is_pressed(picounicorn.BUTTON_A):
            return True
        if picounicorn.is_pressed(picounicorn.BUTTON_B):
            return True
        if picounicorn.is_pressed(picounicorn.BUTTON_X):
            return True
        if picounicorn.is_pressed(picounicorn.BUTTON_Y):
            return True

def wait_time(t):
    time.sleep(t)
    
def wait_time_button(t):
    future = time.time()+t
    while time.time()<future:
        if picounicorn.is_pressed(picounicorn.BUTTON_A):
            return True
        if picounicorn.is_pressed(picounicorn.BUTTON_B):
            return True
        if picounicorn.is_pressed(picounicorn.BUTTON_X):
            return True
        if picounicorn.is_pressed(picounicorn.BUTTON_Y):
            return True
    return False




