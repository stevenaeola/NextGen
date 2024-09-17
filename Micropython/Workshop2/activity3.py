from Workshop2.workshop2 import *

red = (255,0,0)
clear()
button_x = 4
button_y = 4

def update_button(button):
    global button_x, button_y
    print(button)
    if button == "Left":
        button_x -= 1
    elif button == "Right":
        button_x += 1
    elif button == "Up":
        button_y -= 1
    elif button == "Down":
        button_y += 1
    
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
        
            
def run():
    global button_x, button_y
    button_x = 4
    button_y = 4
    draw_circle(button_x,button_y,1,red)
    while True:
        setup_server(update_button)




run()

