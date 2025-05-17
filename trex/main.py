import cv2
import numpy as np
import pyscreenshot
from evdev import UInput, ecodes
from time import sleep, time
import asyncio
# import webbrowser


def take_screenshot():
    screenshot = pyscreenshot.grab()

    img_np = np.array(screenshot)
    img = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)
    return img


async def short_jump(sec=0.065):
    ui.write(ecodes.EV_KEY, ecodes.KEY_SPACE, 1)
    ui.syn()
    await asyncio.sleep(sec)
    ui.write(ecodes.EV_KEY, ecodes.KEY_SPACE, 0)
    ui.syn()


async def normal_jump(sec=0.125):
    ui.write(ecodes.EV_KEY, ecodes.KEY_SPACE, 1)
    ui.syn()
    await asyncio.sleep(sec)
    ui.write(ecodes.EV_KEY, ecodes.KEY_SPACE, 0)
    ui.syn()


async def long_jump(sec=0.225):
    ui.write(ecodes.EV_KEY, ecodes.KEY_SPACE, 1)
    ui.syn()
    await asyncio.sleep(sec)
    ui.write(ecodes.EV_KEY, ecodes.KEY_SPACE, 0)
    ui.syn()


async def jump_for_sec(sec):
    '''
    Attributes:
        sec (float): количество секунд зажатия пробела (1, 10, 0.01)
    '''
    ui.write(ecodes.EV_KEY, ecodes.KEY_SPACE, 1)
    ui.syn()
    await asyncio.sleep(sec)
    ui.write(ecodes.EV_KEY, ecodes.KEY_SPACE, 0)
    ui.syn()


async def down(sec):
    ui.write(ecodes.EV_KEY, ecodes.KEY_DOWN, 1)
    ui.syn()
    await asyncio.sleep(sec)
    ui.write(ecodes.EV_KEY, ecodes.KEY_DOWN, 0)
    ui.syn()


def crop_image(img, x, y, w, h):
    return img[y:y+h, x:x+w]


def get_game_field(img):
    field_x = 1176
    field_y = 270 
    field_width = 600
    field_height = 115
    game_field = crop_image(img, field_x, field_y, field_width, field_height)
    
    return game_field 


async def main():
    # webbrowser.open('https://chromedino.com/')
    # start_time = time()
    sleep(1)
    ui.write(ecodes.EV_KEY, ecodes.KEY_SPACE, 1) 
    ui.syn()
    ui.write(ecodes.EV_KEY, ecodes.KEY_SPACE, 0)
    ui.syn()
    
    # window = cv2.namedWindow('Dinosaur', cv2.WINDOW_AUTOSIZE)
    while True:
        key = chr(cv2.waitKey(1) & 0xFF) 
        if key == 'q':
            break 
         
        img = take_screenshot()
        game_field = get_game_field(img)
        
        gray = cv2.cvtColor(game_field, cv2.COLOR_BGR2GRAY) 
        blurred = cv2.GaussianBlur(gray, (5, 5), 2)   # Если убрать блюр, то динозаврик станет прыгать 
                                                                            #лучше, однако полностью перестанет признавать
                                                                            # существование тройных кактусов
        ret, thresh = cv2.threshold(blurred, 127, 255, cv2.THRESH_BINARY_INV)

        opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN,
                                   np.ones((3, 3), np.uint8), iterations=2)
        dilation = cv2.dilate(opening, np.ones((3, 3), np.uint8), iterations=1)
        

        contours, _ = cv2.findContours(dilation, cv2.RETR_EXTERNAL,
                                    cv2.CHAIN_APPROX_SIMPLE)
         
        max_area = 100
        
        for contour in contours:
            area = cv2.contourArea(contour)
            # if area < max_area: 
            x, y, w, h = cv2.boundingRect(contour)
                
            # cv2.drawContours(game_field, [contour], -1, (0, 255, 0), 2)
            # cv2.rectangle(game_field, (x, y), (x+w, y+h), (0, 255 , 0), 2)
            
            # if x <= 200: print(f'Расстояние до кактуса: {x}') 
            if x <= 120:
                # print(f'Ширина кактуса: {w}')
                if w <= 10:
                    # print('Короткий прыжок')
                    await short_jump()
                elif w <= 20:
                    # print('Обычный прыжок')
                    await normal_jump()
                else:
                    # print('Длинный прыжок')
                    await long_jump()
         
        # cv2.drawContours(game_field , contours, 0, (255, 0, 0), 3)
        
         
        # cv2.imshow('Dinosaur', game_field)


if __name__ == "__main__":
    try:
        ui = UInput()
        asyncio.run(main())

    finally:
        ui.close()
