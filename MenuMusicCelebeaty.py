import pygame, sys
from pygame.locals import *
from MusicNotesTrumpet import MusicNotesTrumpet
from MusicNotesStars import MusicNotesStar
def menu():
    pygame.init()
    playX=50
    playY=430
    quitx=390
    quity=430
    pygame.display.set_caption("Celebeaty")
    screen = pygame.display.set_mode((640, 640))
    Logo=pygame.image.load("LogoMusicCelebeaty.png")
    def show_text (msg, x, y, color):
        fontobj=pygame.font.SysFont("freesans", 22)
        msgobj=fontobj.render(msg,False,color)
        screen.blit(msgobj, (x, y))
    def show_text1 (msg, x, y, color):
        fontobj=pygame.font.SysFont("freesans", 60)
        msgobj=fontobj.render(msg,False,color)
        screen.blit(msgobj, (x, y))
    while True:
        pygame.display.update()
        PLAY=pygame.draw.rect(screen, (255, 255, 255), (playX, playY, 200, 45), 5)
        QUIT=pygame.draw.rect(screen, (255, 255, 255), (quitx, quity, 200, 45), 5)
        for event in pygame.event.get():
            if event.type==QUIT:
                    pygame.quit()
                    exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if playX <= event.pos[0] <= playX+200 and playY <= event.pos[1] <= playY+45:
                    MusicNotesStar()
                if quitx <= event.pos[0] <= quitx+200 and quity<= event.pos[0] <=quity+45:
                    MusicNotesTrumpet()
                    #exit()=quit()?
                #make an if so that when the person holds the mouse at the play box it=play
        show_text((str("START PIANO")), 90, 440, (200, 183, 182))
        show_text((str("START TRUMPET")), 400, 440, (200, 183, 142))
        show_text1((str("Celebeaty")), 50, 200, (0, 135, 60))
        show_text1((str("Music")), 100, 300, (100, 75, 170))
menu() 

