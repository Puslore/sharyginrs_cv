import cv2
import numpy as np

cv2.namedWindow('Camera', cv2.WINDOW_NORMAL)

capture = cv2.VideoCapture(0)
capture.set(cv2.CAP_PROP_AUTO_EXPOSURE, 3)
capture.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)
capture.set(cv2.CAP_PROP_EXPOSURE, 180)


def censore(image, size=(5, 5)):
    result = np.zeros_like(image)
    stepy = result.shape[0] // size[0]
    stepx = result.shape[1] // size[1]
    
    for y in range(0, image.shape[0], stepy):
        for x in range(0, image.shape[1], stepy):
            for c in range(0, image.shape[2]):
                result[y:y+stepy, x:x+stepx] = np.mean(image[y:y+stepy, x:x+stepx, c])
    
    return result


def remove_checkered_background(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower_white = np.array([0, 0, 180])
    upper_white = np.array([180, 30, 255])
    lower_gray = np.array([0, 0, 150])
    upper_gray = np.array([180, 30, 190])
    
    white_mask = cv2.inRange(hsv, lower_white, upper_white)
    gray_mask = cv2.inRange(hsv, lower_gray, upper_gray)
    
    background_mask = cv2.bitwise_or(white_mask, gray_mask)

    object_mask = cv2.bitwise_not(background_mask)

    img[:, :, 3] = object_mask
    
    return img


face_cascade = cv2.CascadeClassifier('./haarcascade-frontalface-default.xml')
eye_cascade = cv2.CascadeClassifier('./haarcascade-eye-tree-eyeglasses.xml')
glasses_img = cv2.imread('./deal-with-it.png', cv2.IMREAD_UNCHANGED)
glasses_img = remove_checkered_background(glasses_img)

while capture.isOpened():
    ret, frame = capture.read()
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    gray = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.4, minNeighbors=2)

    # cnt = []
    for x, y, w, h in faces[:2]:
        roi = gray[y:y+h, x:x+w]
        # cnt.append((x, x+w))
        eyes = eye_cascade.detectMultiScale(roi)
        
        if len(eyes) >= 2: # >= 2 потому что все таки может появиться случайный глаз)
            glasses_x = x
            glasses_y = y + h//4
            glasses_w = w
            glasses_h = int(glasses_w * glasses_img.shape[0] / glasses_img.shape[1])
            glasses_resized = cv2.resize(glasses_img, (glasses_w, glasses_h))
            
            glasses_alpha = glasses_resized[:, :, 3] // 255.0
            alpha_colored = cv2.merge([glasses_alpha, glasses_alpha, glasses_alpha])
            
            y_end = min(frame.shape[0], glasses_y + glasses_h)
            x_end = min(frame.shape[1], glasses_x + glasses_w)
                
            h_part = y_end - glasses_y
            w_part = x_end - glasses_x

            glasses_region = frame[glasses_y:y_end, glasses_x:x_end]

            glasses_part = glasses_resized[:h_part, :w_part, :3]
            alpha_part = alpha_colored[:h_part, :w_part]

            frame[glasses_y:y_end, glasses_x:x_end] = glasses_region * (1 - alpha_part) + glasses_part * alpha_part

        # cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        # new_w = int(w * 1.5)
        # new_h = int(h * 1.5)
        # x -= w //4
        # y -= h //4
        # try:
        #     roi = frame[y:y+new_h, x:x+new_w]
        #     censored = censore(roi, (5, 5))
        #     frame[y:y+new_h, x:x+new_w] = censored
        
        # except ValueError:
        #     pass

    key = chr(cv2.waitKey(1) & 0xFF)
    if key == 'q':
        break

    cv2.imshow('Camera', frame)

capture.release()
cv2.destroyAllWindows()
