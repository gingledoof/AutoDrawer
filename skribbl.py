import numpy as np
import cv2
import pyautogui
import time
from pynput import keyboard


def getContours(path, mult):

    img = cv2.imread(path)

    #width = int(img.shape[1] * mult)
    #height = int(img.shape[0] * mult)

    #img = cv2.resize(img, (width, height))

    imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    ret, thresh = cv2.threshold(imgray, 140, 255, 0)

    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    resizeCont(contours, mult)

    #print("Number of contours = " + str(len(contours)))
    #print(contours[0])

    #cv2.drawContours(img, contours, -1, (0, 255, 0), 3)
    #cv2.drawContours(imgray, contours, -1, (0, 255, 0), 3)

    #cv2.imshow('Image', img)
    #cv2.imshow('Image GRAY', imgray)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()

    return contours


def resizeCont(contours, mult):

    for contour in contours:
        contour[:, :, 0] = contour[:, :, 0] * mult
        contour[:, :, 1] = contour[:, :, 1] * mult

def on_press(key):
    print(str(key))
    if (key == keyboard.Key.alt_r):
        print('Drawing...')
        executeDraw(.5)


def executeDraw(mult):
    initpos = pyautogui.position()

    contours = getContours('bred.jpg', mult)
    transCont(contours, ( initpos[0] - contours[0][0][0][0],  initpos[1] - contours[0][0][0][1]) )
    #relcon = convContour(contours)

    for contour in contours:
        pyautogui.moveTo(contour[0][0][0], contour[0][0][1], _pause=False)
        for point in contour:
            pyautogui.dragTo(point[0][0], point[0][1], _pause=False)

    #for i, contour in enumerate(relcon):
    #    # Moving to first point on next contour
    #    if i != 0:
    #        prev_cont_len = len(contours[i-1][0])
    #        pyautogui.moveRel( contours[i][0][0][0] - contours[i-1][0][prev_cont_len - 1][0], contours[i][0][0][1] - contours[i-1][0][prev_cont_len - 1][1], _pause=False)
#
    #    for point in contour:
 #           pyautogui.dragRel(point[0], point[1], _pause=False)


def transCont(contours, translate):
    for contour in contours:
        contour[:, :, 0] = contour[:, :, 0] + translate[0]
        contour[:, :, 1] = contour[:, :, 1] + translate[1]

def convContour(contours):
    curves = []

    for i in range(len(contours)):
        curve = []

        #if i == 0:
        #    # setting initpos
        #    curve.append([initpos[0], initpos[1]])
        #else:
        #    len_prev_cont = len(contours[i - 1])
        #    last_point_prev_cont = contours[i - 1][len_prev_cont - 1][0]
        #    curve.append([ contours[i][0][0][0] - last_point_prev_cont[0], contours[i][0][0][1] - last_point_prev_cont[1] ])

        for j in range(len(contours[i]) - 1):
            if j % 3 == 0:
                next_point = [contours[i][j+1][0][0], contours[i][j+1][0][1]]
                this_point = [contours[i][j][0][0], contours[i][j][0][1]]
                x = next_point[0] - this_point[0]
                y = next_point[1] - this_point[1]

                curve.append([x, y])
        curves.append(curve)

    return curves


listener = keyboard.Listener(
    on_press=on_press)
listener.start()

getContours('simp.jpg', .5)