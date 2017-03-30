from pygame.locals import *
import pygame,sys
from threading import Timer, Event, Thread

#Setup Leap Motion
import os, inspect, thread, time

src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
lib_dir = os.path.abspath(os.path.join(src_dir, './lib'))
sys.path.insert(0, lib_dir)

src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
arch_dir = './lib/x64' if sys.maxsize > 2**32 else './lib/x86'
sys.path.insert(0, os.path.abspath(os.path.join(src_dir, arch_dir)))

import Leap


os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (50,50)

black = (0, 0, 0)
red = (255, 0, 0)
cyan = (0, 255, 255)
white = (255, 255, 255)

screen = time = cm = None

class LeapMotionListener(Leap.Listener):
    finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
    bone_names = ['Metacarpal', 'Proximal', 'Intermediate', 'Distal']

    def on_init(self, controller):
        print("Initialized Leap Motion controller!")

    def on_connect(self, controller):
        print("Connected to Leap Motion controller!")

    def on_disconnect(self, controller):
        # Note: not dispatched when running in a debugger.
        print("Disconnected from Leap Motion controller!")

    def on_exit(self, controller):
        print("Exited App!")

    def on_frame(self, controller):
        # Get the most recent frame and report some basic information
        frame = controller.frame()

        print("Hands: %d, fingers: %d") % (len(frame.hands), len(frame.fingers))

        # Get hands
        for hand in frame.hands:
            if hand.is_left:
                print("Left hand")
            else:
                print("Right hand")
            
            # Get fingers
            for finger in hand.fingers:
                bone = finger.bone(Leap.Bone.TYPE_DISTAL)
                print(self.finger_names[finger.type] + " => " + str(bone.direction))

        if not frame.hands.is_empty:
            print()

def init_setup(filename):
    global screen, time
    screen = pygame.display.set_mode((700, 700))
    pygame.display.set_caption("Shooting Stars (Piano Instrumental) - Celebeaty")
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()
    time = pygame.time.Clock()

def drawBoundaries():
    global screen, time, black, red
    screen.fill(white)
    for rectX in range(100, 700, 100):
        pygame.draw.rect(screen, black,(rectX, 0, 10, 700), 10)
    pygame.draw.rect(screen, red,(0, 600, 700, 100), 10)

class Circle():
    global cyan
    
    def __init__(self, lineNum, diameter):
        self.cx = 55 + (100 * (lineNum - 1))
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
    
def gen_main_beat(offsetMain, offsetSide):
    mult = 1.85
    Timer(0.00 + mult * offsetMain, createCircle, [1 + offsetSide]).start()
    Timer(0.00 + mult * offsetMain, createCircle, [2 + offsetSide]).start()
    
    Timer(0.00 + mult * offsetMain, createCircle, [6]).start()
    Timer(0.60 + mult * offsetMain, createCircle, [6]).start()
    Timer(0.80 + mult * offsetMain, createCircle, [7]).start()
    Timer(1.20 + mult * offsetMain, createCircle, [6]).start()
    Timer(1.40 + mult * offsetMain, createCircle, [5]).start()

def MusicNotesStars():
    global screen, time, cm
    init_setup('shoot_stars.mp3')
    cm = CircleManager()

    listener = LeapMotionListener()
    controller = Leap.Controller()
    controller.add_listener(listener)
    
    for moffset in range(64):
        soffset = int(moffset / 16)
        gen_main_beat(moffset, soffset)

    try:
        while True:
            time.tick(50)
            pygame.display.update()
            drawBoundaries()
            
            cm.drawAndUpdate(10)
            
            for event in pygame.event.get():
                if event.type==QUIT:
                    pygame.quit()
                    exit()
    except KeyboardInterrupt:
        controller.remove_listener(listener)
    finally:
        # Remove the sample listener when done
        controller.remove_listener(listener)
