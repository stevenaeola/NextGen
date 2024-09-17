from Workshop2.workshop2 import *

red = (255,0,0)
clear()

def run():
    button_x = 4
    button_y = 4
    while True:
        draw_circle(button_x,button_y,1,red)
        button = get_button_server()
        
        if button == "X":
            button_y -= 1
        elif button == "Y":
            button_y += 1
        elif button == "A":
            button_x -= 1
        elif button == "B":
            button_x += 1
        
        if button_y < 0:
            button_y = 0
        if button_y > 6:
            button_y = 6
        if button_x < 0:
            button_x = 0
        if button_x > 15:
            button_x = 15
            
        clear()
        draw_circle(button_x,button_y,1,red)




run()

