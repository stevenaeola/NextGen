from Workshop1.workshop1 import *

french_blue = (0,85,164)
french_white = (255,255,255)
french_red = (239,65,53)

german_black = (0,0,0)
german_red = (255,0,0)
german_gold = (255,204,0)

england_red = (200,16,46)
england_white = (255,255,255)

clear()

#draw french flag)
draw_rectangle(0,0,5,6,french_blue)
draw_rectangle(5,0,10,6,french_white)
draw_rectangle(10,0,15,6,french_red)


wait_button()

clear()

#draw german flag
draw_rectangle(0,0,15,1,german_black)
draw_rectangle(0,2,15,4,german_red)
draw_rectangle(0,5,15,6,german_gold)


wait_time(1)

clear()
draw_rectangle(0,0,15,6,england_white)
draw_rectangle(7,0,9,6,england_red)