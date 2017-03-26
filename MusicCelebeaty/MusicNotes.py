from pygame.locals import *
def MusicNotes():
    import pygame,sys
    screen = pygame.display.set_mode((700, 700))
    pygame.display.set_caption("MusicNoteSetup")
    rectangleX = 100
    rectangleY = 0
    rectangleX2 = 200
    rectangleX3 = 300
    rectangleX4 = 400
    rectangleX5 = 500
    rectangleX6 = 600
    circleX=100
    circleY=0
    black = (0, 0, 0)
    red= (255, 0, 0)
    pygame.init()
    pygame.mixer.init()
    file = 'C:\\Users\\Audrey Im\\Desktop\\MusicCelebeaty\\trumpets.mp3'
    pygame.mixer.music.load(file)
    pygame.mixer.music.play()
    time = pygame.time.Clock()
    while True:
        time.tick (25)
        pygame.display.update()
        screen.fill((255, 255, 255))
        pygame.draw.rect(screen, black,(rectangleX, rectangleY, 10, 700), 10)
        pygame.draw.rect(screen, black,(rectangleX2, rectangleY, 10, 700), 10)
        pygame.draw.rect(screen, black,(rectangleX3, rectangleY, 10, 700), 10)
        pygame.draw.rect(screen, black,(rectangleX4, rectangleY, 10, 700), 10)
        pygame.draw.rect(screen, black,(rectangleX5, rectangleY, 10, 700), 10)
        pygame.draw.rect(screen, black,(rectangleX6, rectangleY, 10, 700), 10)
        pygame.draw.rect(screen, red,(0, 600, 700, 100), 10)
        pygame.draw.circle(screen, (0, 255, 255), (circleX+60, circleY), 40)
        circleY=circleY+50
        for event in pygame.event.get():
            if event.type==QUIT:
                    pygame.quit()
                    exit()
MusicNotes()
