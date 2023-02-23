import serial
ser = serial.Serial('/dev/ttyACM0',9600)

#import pygame
import pygame
import math

#Initialize pygame
pygame.init()

#Clock
clock=pygame.time.Clock()

#RGB colors
BLACK=(0,0,0)
TVOC=(255,0,0)
CO2=(255,0,0)

#set up window
wn_width = 800
wn_height=415
wn=pygame.display.set_mode((wn_width,wn_height))
#DISPLAYSURF = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Indoor Air Quality Monitor Interface")

#color changing variables
redCo2=255
greenCo2 = 0

redVoc=255
greenVoc = 0

#fonts
font = pygame.font.SysFont(None,72)
font_small = pygame.font.SysFont(None,56)

#text variables
def show_title(msg,color,x,y):
    screen_text = font.render(msg,True, color)
    wn.blit(screen_text, (x,y))
    
#text variables
def show_title_small(msg,color,x,y):
    screen_text = font_small.render(msg,True, color)
    wn.blit(screen_text, (x,y)) 
    
#while loop
state=True
while state:
    #arduino
    read_serial=ser.readline()
    s = str((ser.readline(),30))
    
    inp = s.split("_")
    
    #parse CO2
    inpCO2 = inp[0]
    inpCO2parsed = inpCO2.split("'")
    co2string = inpCO2parsed[1]
    co2 = float(co2string)

    #parse TVOC
    inpVoc = inp[1]
    inpVocParsed = inpVoc.split("\\")
    vocString = inpVocParsed[0]
    voc = float(vocString)
    
    print(co2,voc)
    
    #scaling inp to changing color
    sc_co2 = co2/8 - 50
    
    if sc_co2 > 100:
        sc_co2 = 100
    if sc_co2 < 0:
        sc_co2 = 0

    sc_voc = voc/1.5
    
    if sc_voc>100:
        sc_voc=100
    if sc_voc<0:
        sc_voc=0
    #color variables
    #red should be 255 from 0-50, then go to 0 from 51-100
    
    #co2
    if (sc_co2>50):
        redCo2=255
    else:
        redCo2 = (sc_co2)*5
    #green starts at 0, goes to 255 by 50, then stays 255
    if (sc_co2>50):
        greenCo2 = 255-((sc_co2-50)*5)
    else:
        greenCo2 = 255
        
    #voc
    if (sc_voc>51):
        redVoc=255
    else:
        redVoc = (sc_voc)*5
    #green starts at 0, goes to 255 by 50, then stays 255
    if (sc_voc>50):
        greenVoc = 255-((sc_voc-50)*5)
    else:
        greenVoc = 255

    
    #bg color
    wn.fill(BLACK)
    
    #redefine color
    TVOC=(int(redVoc),int(greenCo2),0)
    CO2=(int(redCo2),int(greenCo2),0)
    
    #TVOC CIRCLE
    X=200; Y=207; radius=150;
    pygame.draw.circle(wn,TVOC, (X,Y), radius)
    
    #eCO2 CIRCLE
    X=600; Y=207; radius=110;
    pygame.draw.circle(wn,CO2, (X,Y), radius)
    
    #show text
    show_title("TVOC", BLACK,125,150)
    show_title("CO2", BLACK,550,150)
    
    show_title_small("PPB: " + str(int(voc)), BLACK,100,200)
    show_title_small("PPM: " + str(int(co2)), BLACK,500,200)


        
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
                state=False
    pygame.display.update()
    clock.tick(30)


#pygame quit
pygame.quit()
quit()
