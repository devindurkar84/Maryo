#adding modules

import pygame,random,sys
from pygame.locals import*
pygame.init()

#some global variable

window_width=1200
window_height=600

black=(0,0,0)
white=(255,255,255)

font=pygame.font.SysFont(None,48)

fps=35

mainclock=pygame.time.Clock()


topscore=0
level=1

addnewflamerate=20


#initializing display

canvas=pygame.display.set_mode((window_width,window_height))
canvas.fill(black)
pygame.display.set_caption("maryo")


fire=pygame.image.load("fire_bricks.png")               #bottom fire
firerect=fire.get_rect()
firerect.top=550
firerect.left=0

cactus=pygame.image.load("cactus_bricks.png")           #top cactus
cactusrect=cactus.get_rect()
cactusrect.bottom=50
cactusrect.left=0

startimage=pygame.image.load('start.png')               #startimage
startimagerect=startimage.get_rect()
startimagerect.centerx=window_width/2
startimagerect.centery=window_height/2

endimage=pygame.image.load('end.png')                   #endimage
endimagerect=endimage.get_rect()
endimagerect.centerx=window_width/2
endimagerect.centery=window_height/2

#initialize sound

pygame.mixer.music.load('mario_theme.wav')
gameover = pygame.mixer.Sound('mario_dies.wav')

#useful function

def terminate():                                        #to end the program
    pygame.quit()
    sys.exit()

def waitforkey():                                       #to wait for user to start
    while True :                                        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:            #to terminate if the user presses the escape key
                if event.key == pygame.K_ESCAPE:
                    terminate()
                return


#defination and declaratio of class

class Dragon:                                           #class for dragon

    up=False
    down=True
    speed=10
    
    def __init__(self):
        self.image=pygame.image.load('dragon.png')
        self.imagerect=self.image.get_rect()
        self.imagerect.right=window_width
        self.imagerect.top=window_height/2

    def height(self):
        return self.imagerect.centery

    def postleft(self):
        return self.imagerect.left+60

    def update(self):
        if self.imagerect.top<=cactusrect.bottom:
            self.down=True
            self.up=False
        if self.imagerect.bottom>=firerect.top:
            self.down=False
            self.up=True
        if self.down==True:
            self.imagerect.bottom+=self.speed
        if self.up==True:
            self.imagerect.top-=self.speed

class Maryo:                                            #class for mario

    up=False
    down=False
    gravity=False
    downspeed=20
    upspeed=10
    gravityspeed=10
    
    
    def __init__(self):
        self.image=pygame.image.load('maryo.png')
        self.imagerect=self.image.get_rect()
        self.imagerect.left=50
        self.imagerect.top=window_height/2

    def update(self):
        if self.up and (self.imagerect.top>cactusrect.bottom):
            self.imagerect.top-=self.upspeed
            global score
            score+=1
        if self.down and (self.imagerect.bottom<firerect.top):
            self.imagerect.bottom+=self.downspeed
            global score
            score+=1
        if self.gravity and (self.imagerect.bottom<firerect.top):
            self.imagerect.bottom+=self.gravityspeed
        

class flame:                                            #class for flames

    flamespeed=20
    
    def __init__(self,Dragon):
        self.image=pygame.image.load('fireball.png')
        self.imagerect=self.image.get_rect()
        self.imagerect.top=Dragon.height()
        self.imagerect.right=Dragon.postleft()
        self.surface=pygame.transform.scale(self.image,(20,20))
       # self.imagerect=pygame.Rect(window_width-310,self.height,20,20)

    def update(self):
        self.imagerect.right-=self.flamespeed    

    def rm(self):
        if self.imagerect.left<=0:
            return True

#end of class def. and declarations
        
#main procedural coding goes here

canvas.blit(startimage,startimagerect)
canvas.blit(cactus,cactusrect)
canvas.blit(fire,firerect)
pygame.display.update()

waitforkey()

while True:                                             #game initializing loop

    gameover.stop()
    flame_list=[]
    score=0
    flameaddcounter=20
    dragon=Dragon()
    player=Maryo()
    pygame.mixer.music.play(-1,0)

    while True:                                         #main game loop

        flameaddcounter+=1
        
        for event in pygame.event.get():                #input detection start

            if event.type==QUIT:
                terminate()

            if event.type==KEYDOWN:
                if event.key==K_ESCAPE:
                    terminate()
                if event.key==K_UP:
                    player.up=True
                    player.down=False
                    player.gravity=False
                    #score+=1
                if event.key==K_DOWN:
                    player.down=True
                    player.up=False
                    player.gravity=False
                    #score+=1

            if event.type==KEYUP:
                player.down=False
                player.up=False
                player.gravity=True                     #input detection end

        if flameaddcounter>addnewflamerate:             #add new flames after fix interval of distance
            flameaddcounter=0
            newflame=flame(dragon)
            flame_list.append(newflame)

        for f in flame_list:                            #update the position of all the flames
            f.update()

        if flame_list[0].rm():                          #remove flames which are out of screen
            flame_list.remove(flame_list[0])
            

        if score in range(0,250):                        #checking the score to alter level and position of cactus and fire
            level=1
            firerect.top=550
            cactusrect.bottom=50
        elif score in range(250,500):
            level=2
            firerect.top=525
            cactusrect.bottom=75
        elif score in range(500,750):
            level=3
            firerect.top=500
            cactusrect.bottom=100
        elif score in range(750,1000):
            level=4
            firerect.top=475
            cactusrect.bottom=125                                   

                                                        #to check if player is collide with cactus or fire
        
        if (player.imagerect.top<=cactusrect.bottom) or (player.imagerect.bottom>=firerect.top):
            if score>topscore:
                topscore=score
            break
                                                        #to check if player is collide with flames
        
        if (player.imagerect.right>=flame_list[0].imagerect.left) and ((player.imagerect.top in range(flame_list[0].imagerect.top,flame_list[0].imagerect.bottom)) or (player.imagerect.bottom in range(flame_list[0].imagerect.top,flame_list[0].imagerect.bottom))):
            if score>topscore:
                topscore=score
            break


                                                        #updating dragon and player position
        dragon.update()
        player.update()

                                                        #this group statement is to display scoreboard
                                                        
        text="Score::{} | Topscore::{} | Level::{}".format(score,topscore,level)
        textobj=font.render(text,1,white)
        textrect=textobj.get_rect()
        textrect.top=cactusrect.bottom+10
        textrect.centerx=window_width/2
                                                        
        canvas.fill(black)                              #here all the visual object are set on the canvas
        canvas.blit(textobj,textrect)
        canvas.blit(fire,firerect)
        canvas.blit(cactus,cactusrect)
        canvas.blit(dragon.image,dragon.imagerect)
        canvas.blit(player.image,player.imagerect)
        for f in flame_list:
            canvas.blit(f.surface,f.imagerect)
            
        pygame.display.update()
        mainclock.tick(fps)

#main game loop ends

    pygame.mixer.music.stop()
    gameover.play()
    canvas.blit(endimage,endimagerect)
    pygame.display.update()
    waitforkey()

#program ends
