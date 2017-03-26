from pygame.locals import *
import pygame,sys
from threading import Timer, Event, Thread

import os
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (50,50)

black = (0, 0, 0)
red = (255, 0, 0)
cyan = (0, 255, 255)
white = (255, 255, 255)

screen = time = cm = None

def init_setup(filename):
    global screen, time
    screen = pygame.display.set_mode((590, 700))
    pygame.display.set_caption("Trumpets (Instrumental) - Celebeaty")
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load(filename)
    Timer(0.8, pygame.mixer.music.play).start()
    time = pygame.time.Clock()

def drawBoundaries():
    global screen, time, black, red
    screen.fill(white)
    for rectX in range(200, 600, 200):
        pygame.draw.rect(screen, black,(rectX-10, 0, 10, 700), 10)
    pygame.draw.rect(screen, red,(0, 600, 590, 100), 10)

class Circle():
    global cyan
    
    def __init__(self, lineNum, diameter):
        self.cx = 95 + (200 * (lineNum - 1))
        self.cy = 0
        self.diameter = diameter

    def drawAndUpdate(self, dy):
        pygame.draw.circle(screen, cyan, (self.cx, self.cy), self.diameter)
        self.cy += dy

class CircleManager():
    def __init__(self):
        self.circles = []

    def addCircle(self, circle):
        self.circles.append(circle)

    def drawAndUpdate(self, dy):
        deleted = False
        for i in range(len(self.circles)):
            circle = self.circles[i]
            circle.drawAndUpdate(dy)
            if circle.cy > 800:
                deleted = True
                del self.circles[i]
                break
        if deleted:
            self.drawAndUpdate(dy)

def call_repeatedly(interval, func, *args):
    stopped = Event()
    def loop():
        while not stopped.wait(interval): # the first call is in `interval` secs
            func(*args)
    Thread(target=loop).start()    
    return stopped.set

def createCircle(lineNum):
    global cm
    cm.addCircle(Circle(lineNum, 40))
    
def gen_main_beat(offsetMain):
    mult = 5.7
    lineNums = [2,2,1,1,2,2,1,1,2,2,1,1,3,3,2,2]
    
    for offset in range(0, 16):
        Timer(offset / 2.8 + mult * offsetMain, createCircle, [lineNums[offset]]).start()
        

def MusicNotesTrumpet():
    global screen, time, cm
    init_setup('trumpets.mp3')
    cm = CircleManager()

    for moffset in range(4):
        gen_main_beat(moffset)
    
    while True:
        time.tick(50)
        pygame.display.update()
        drawBoundaries()

        cm.drawAndUpdate(10)
        
        for event in pygame.event.get():
            if event.type==QUIT:
                    pygame.quit()
                    exit()
