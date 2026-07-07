import cv2
from cvzone.HandTrackingModule import HandDetector
import numpy as np
import os as oss
import traceback



capture = cv2.VideoCapture(0)
hd = HandDetector(maxHands=1)
hd2 = HandDetector(maxHands=1)

script_dir = oss.path.dirname(oss.path.abspath(__file__))
white_path = oss.path.join(script_dir, "white.jpg")
dataset_dir = oss.path.join(script_dir, "AtoZ_3.1")

def get_count_and_create_dir(dir_char):
    target_path = oss.path.join(dataset_dir, dir_char)
    oss.makedirs(target_path, exist_ok=True)
    return len(oss.listdir(target_path)), target_path

c_dir = 'A'
count, target_path = get_count_and_create_dir(c_dir)

offset = 15
step = 1
flag=False
suv=0

white=np.ones((400,400),np.uint8)*255
cv2.imwrite(white_path,white)


while True:
    try:
        _, frame = capture.read()
        frame = cv2.flip(frame, 1)
        hands_res = hd.findHands(frame, draw=False, flipType=True)
        hands = hands_res[0] if isinstance(hands_res, tuple) else hands_res
        white = cv2.imread(white_path)

        if hands:
            hand = hands[0]
            x, y, w, h = hand['bbox']
            
            img_h, img_w, _ = frame.shape
            y1, y2 = max(0, y - offset), min(img_h, y + h + offset)
            x1, x2 = max(0, x - offset), min(img_w, x + w + offset)
            image = np.array(frame[y1:y2, x1:x2])

            if image.size > 0:
                handz_res = hd2.findHands(image, draw=True, flipType=True)
                handz = handz_res[0] if isinstance(handz_res, tuple) else handz_res
                if handz:
                    hand = handz[0]
                    pts = hand['lmList']
                # x1,y1,w1,h1=hand['bbox']
                os=((400-w)//2)-15
                os1=((400-h)//2)-15
                for t in range(0,4,1):
                    cv2.line(white,(pts[t][0]+os,pts[t][1]+os1),(pts[t+1][0]+os,pts[t+1][1]+os1),(0,255,0),3)
                for t in range(5,8,1):
                    cv2.line(white,(pts[t][0]+os,pts[t][1]+os1),(pts[t+1][0]+os,pts[t+1][1]+os1),(0,255,0),3)
                for t in range(9,12,1):
                    cv2.line(white,(pts[t][0]+os,pts[t][1]+os1),(pts[t+1][0]+os,pts[t+1][1]+os1),(0,255,0),3)
                for t in range(13,16,1):
                    cv2.line(white,(pts[t][0]+os,pts[t][1]+os1),(pts[t+1][0]+os,pts[t+1][1]+os1),(0,255,0),3)
                for t in range(17,20,1):
                    cv2.line(white,(pts[t][0]+os,pts[t][1]+os1),(pts[t+1][0]+os,pts[t+1][1]+os1),(0,255,0),3)
                cv2.line(white, (pts[5][0]+os, pts[5][1]+os1), (pts[9][0]+os, pts[9][1]+os1), (0, 255, 0), 3)
                cv2.line(white, (pts[9][0]+os, pts[9][1]+os1), (pts[13][0]+os, pts[13][1]+os1), (0, 255, 0), 3)
                cv2.line(white, (pts[13][0]+os, pts[13][1]+os1), (pts[17][0]+os, pts[17][1]+os1), (0, 255, 0), 3)
                cv2.line(white, (pts[0][0]+os, pts[0][1]+os1), (pts[5][0]+os, pts[5][1]+os1), (0, 255, 0), 3)
                cv2.line(white, (pts[0][0]+os, pts[0][1]+os1), (pts[17][0]+os, pts[17][1]+os1), (0, 255, 0), 3)

                skeleton0=np.array(white)
                zz=np.array(white)
                for i in range(21):
                    cv2.circle(white,(pts[i][0]+os,pts[i][1]+os1),2,(0 , 0 , 255),1)

                skeleton1=np.array(white)

                cv2.imshow("1",skeleton1)

        frame = cv2.putText(frame, "dir=" + str(c_dir) + "  count=" + str(count), (50,50),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            1, (255, 0, 0), 1, cv2.LINE_AA)
        cv2.imshow("frame", frame)
        interrupt = cv2.waitKey(1)
        if interrupt & 0xFF == 27:
            # esc key
            break


        if interrupt & 0xFF == ord('n'):
            c_dir = chr(ord(c_dir)+1)
            if ord(c_dir)==ord('Z')+1:
                c_dir='A'
            flag = False
            count, target_path = get_count_and_create_dir(c_dir)

        if interrupt & 0xFF == ord('a'):
            if flag:
                flag=False
            else:
                suv=0
                flag=True

        print("=====",flag)
        if flag==True:

            if suv==180:
                flag=False
            if step%3==0:
                cv2.imwrite(oss.path.join(target_path, str(count) + ".jpg"),
                            skeleton1)

                count += 1
                suv += 1
            step+=1



    except Exception:
        print("==",traceback.format_exc() )

capture.release()
cv2.destroyAllWindows()