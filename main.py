import cv2 as cv
from time import time, sleep
from windowcapture import WindowCapture
from contact import AlbionBot, BotState


DEBUG = True

# initialize the WindowCapture class
wincap = WindowCapture('Gasparini - Dofus Retro v1.41.5')# 'Gasparini - Dofus Retro v1.41.3'

bot = AlbionBot((wincap.offset_x, wincap.offset_y), (wincap.w, wincap.h))
bot.start()
wincap.start()

while(True):
    sleep(0.3)
    # if we don't have a screenshot yet, don't run the code below this point yet
    if wincap.screenshot is None:
        continue
    
    # give detector the current screenshot to search for objects in
    bot.update_screenshot(wincap.screenshot)

    if bot.state == BotState.INITIALIZING:
        bot.update_screenshot(wincap.screenshot)
        # while bot is waiting to start, go ahead and start giving it some targets to work
        # on right away when it does start
        # update the bot with the data it needs right now
    elif bot.state == BotState.SEARCHING:
        # When searching for something to click on next, the bot needs to know what the click
        # points are for the current detection results. it also needs an update screenshot
        # to verify the hover tooltip once it has moved the mouse to that position
        bot.update_screenshot(wincap.screenshot)
    elif bot.state == BotState.MOVING:
        # when moving, we need fresh screenshots to determine when we've stopped moving
        bot.update_screenshot(wincap.screenshot)

    # elif bot.state == BotState.MINING:
    #     #nothing is need while we wait for the mining to finish
    #     pass

    if DEBUG: 
        #draw the detection results onto the original image
        detection_image = wincap.screenshot
        # cv.imshow('Matches', detection_image)

        # x, y, largura, altura = 730, 70, 110, 50
        # regiao_cortada = detection_image[y:y+altura, x:x+largura]
        # cv.imshow('Matches', regiao_cortada)
      
    # press 'q' with the output window focused to exit.
    # waits 1 ms every loop to process key presses
    if cv.waitKey(1) == ord('q'):
        bot.stop()
        wincap.stop()
        cv.destroyAllWindows()
        break
    

print('Done.')