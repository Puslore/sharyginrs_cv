import cv2
import numpy as np
from time import sleep


def main():
    cnt = {}
    sup_cnt = 1
    sup_sup_cnt = 1
    video = cv2.VideoCapture('./output.avi')

    while True:
        # print(sup_cnt)
        ret, frame = video.read()
        if not ret:
            break
        
        cv2.putText(frame, f'Frame number - {sup_cnt}', (10, 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(gray, 10, 255, cv2.THRESH_BINARY)

        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL,
                                    cv2.CHAIN_APPROX_SIMPLE)
        
        # 182.76881269290107
        average_color = np.average(np.average(np.average(frame, axis=0), axis=0))
        
        # if sup_cnt == 59:
        #     print(average_color, type(average_color))
        #     break
        
        if average_color > 182.0 and average_color < 183.0:
            # print('да')
            cnt[sup_sup_cnt] = sup_cnt
            sup_sup_cnt += 1

        # 59
        if NEED_TO_FIND_MY_PIC_FLAG:
            cv2.imshow('Pics', frame)
            sleep(1)

        cv2.waitKey(1)
        sup_cnt += 1

    video.release()
    cv2.destroyAllWindows()
    
    for key, value in cnt.items():
        print(f'Моя картинка {key} на {value} кадре')
    
    print(f'Общее количество картинок: {len(cnt)}')


if __name__ == "__main__":
    NEED_TO_FIND_MY_PIC_FLAG = False
    main()
