import curses
import cv2
import numpy as np
import time
import pygame
import re
import os
from tkinter import *

startText = '''
Winner Winner chicken dinner
'''

endText = '''
Made by
    Zhao Jiawei
    Li You
    Wei Xinlong
    Li Rongwei
'''

SCREEN = [1920, 1080]

def getOutline(path):
    img = cv2.imread(path)
    sp = img.shape
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    _, contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    print(len(contours))
    #return contours[0]
    return contours, sp[0], sp[1]

def initMusic():
    pygame.mixer.init()
    pygame.mixer.music.load('music/song.mp3')
    pygame.mixer.music.play(-1)

def initGame(width, height):
    pygame.init()
    screen=pygame.display.set_caption('hello world!')
    screen=pygame.display.set_mode([width, height])
    screen.fill([255,255,255])
    return screen

def drawOutline(screen, path, color, speed, size):
    conlist, height, width = getOutline(path)
    offsetX = (size[0] - width) / 2
    offsetY = (size[1] - height) / 2
    for contours in conlist:
        if len(contours) < 5:
            continue
        for i in range(0, len(contours) - 1):
            startPoint = contours[i][0]
            endPoint = contours[i + 1][0]
            #print startPoint, endPoint
            pygame.draw.line(screen, color, (offsetX + startPoint[0], offsetY + startPoint[1]), (offsetX + endPoint[0], offsetY + endPoint[1]), 3)
            #pygame.time.delay(speed)
            pygame.time.Clock().tick(speed)
            pygame.display.flip()

def drawTextByLine(screen, text):
    font = pygame.font.Font(None, 40)
    #lines = text.strip().splitlines()
    lines = text.split('\n')
    print(lines)

    height = len(lines) * font.get_linesize()

    center,top = screen.get_rect().center
    top -= height / 2

    antialias = 1
    black = 0, 0, 0

    for line in lines:
        left = center - height / 2
        for word in line:
            text = font.render(word, antialias, black)
            r = text.get_rect()
            r.left = left
            r.top = top
            screen.blit(text, r)
            pygame.display.flip()
            pygame.time.delay(100)
            left += r.width
        top += font.get_linesize()

    pygame.time.delay(1000)

def getPics(path):
    files = os.listdir(path)
    return sorted(files)

def test(path):
    img = cv2.imread(path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(img,contours,-1,(0,0,255),2)
    cv2.imshow("img", img)
    cv2.waitKey(0)

def test1(path):
    black = [0, 0, 0]
    white = [255, 255, 255]
    screen = initGame(SCREEN[0], SCREEN[1])

    drawOutline(screen, path, black, 3000, SCREEN)
    pygame.time.delay(1000)
    drawOutline(screen, path, white, 6000, SCREEN)
    pygame.time.delay(1000)

    screen.fill(white)

def test2(text):
    black = [0, 0, 0]
    white = [255, 255, 255]
    screen = initGame(SCREEN[0], SCREEN[1])
    drawTextByLine(screen, text)

def main():
    initMusic()
    black = [0, 0, 0]
    white = [255, 255, 255]
    screen = initGame(SCREEN[0], SCREEN[1])

    drawTextByLine(screen, startText)
    screen.fill(white)

    files = getPics('pic')
    print(files)
    for f in files:
        path = os.path.join('pic/', f)
        drawOutline(screen, path, black, 10000, SCREEN)
        pygame.time.delay(1000)
        drawOutline(screen, path, white, 20000, SCREEN)
        pygame.time.delay(1000)

    # drawOutline(screen, 'pic/p0.jpg', black, 5)
    # drawOutline(screen, 'pic/p0.jpg', white, 0)
    screen.fill(white)
    drawTextByLine(screen, endText)
    pygame.time.delay(10000)

if __name__ == '__main__':
    main()
