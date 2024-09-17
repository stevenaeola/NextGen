from Workshop2.workshop2 import *

red = (255,0,0)
clear()

def run():
    button_x = 4
    button_y = 4
    while True:
        draw_circle(button_x,button_y,1,red)
        button = wait_button()
        
        if button == "X":
            button_y += 1
        elif button == "Y":
            button_y -= 1
        
        if button_y < 0:
            button_y = 0
        if button_y > 6:
            button_y = 6
            
        clear()
        draw_circle(button_x,button_y,1,red)




run()