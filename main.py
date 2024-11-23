import tkinter as tk
import math
import cv2
import numpy as np
import easygui
from interp import interpolate,bilineal,nearest

def center_window(z,t):
    import tkinter as tk
    root = tk.Tk()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.destroy()

    x = (screen_width - z) // 2
    y = (screen_height - t) // 2
    print(x,y)
    return (x,y)



def file_selector()->str:
    '''
    Open file selector and return the path of the file.
    '''
    file_path = str(easygui.fileopenbox(title="Select an Image", filetypes=["*.jpg", "*.jpeg", "*.png", "*.bmp", "*.tiff"]))
    if file_path:
        return file_path
    return ""


def open_image()->np.ndarray|None:
    path=file_selector()
    tmp =cv2.imread(path)
    if tmp is None:
        print("error loading",path)
        return None
        
    img=cv2.cvtColor(tmp, cv2.COLOR_BGR2GRAY)
    if img.max() > 255:
        img = cv2.convertScaleAbs(img, alpha=(255.0 / img.max()))
    return img

def is_open_btn(x,y):
    return 0 < x < 100 and 0 < y < 20
def is_select_btn(x,y):
    return 100 < x < 200 and 0 < y < 20

def default_img():
    img= np.ones((400, 400, 3), dtype="uint8") * 230
    cv2.putText(img, 'No image selected', (130, 180), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0 ,0 ), 1, cv2.LINE_AA)
    return img
def draw_menu(img):
    if img is not None:
        cv2.rectangle(img, (0, 0), (100, 20), (255, 255, 255), -1)   
        cv2.rectangle(img, (0, 0), (100, 20), (0, 0, 0), 1)   
        cv2.putText(img, 'Open', (30, 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0 ,0 ), 1, cv2.LINE_AA)

        cv2.rectangle(img, (100, 0), (200, 20), (255, 255, 255), -1)   
        cv2.rectangle(img, (100, 0), (200, 20), (0, 0, 0), 1)   
        cv2.putText(img, 'Select', (130, 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0 ,0 ), 1, cv2.LINE_AA)


def click_event(event, x, y, flags, param):
    global img
    global first
    global second
    global selecting
    if event == cv2.EVENT_LBUTTONDOWN:
            if is_open_btn(x,y):
                img=open_image()
                return
            elif is_select_btn(x,y):
                selecting=True
                return

    if selecting:
        if event == cv2.EVENT_LBUTTONDOWN:
            if is_open_btn(x,y):
                img=open_image()
                return
            
            first=(x,y)
        elif event == cv2.EVENT_MOUSEMOVE: 
            second=(x,y)
        elif event ==cv2.EVENT_LBUTTONUP:
                resized=img[first[1]:second[1],first[0]:second[0]]
                w,h=img.shape
        
                factor=math.floor(w/(second[0]-first[0]))
                upsc=interpolate(resized,factor,bilineal)
                first=None
                second=None
                selecting=False
                cv2.imshow("b",upsc)



        
img:np.ndarray|None
img=default_img()
first=None
second=None
selecting= False    
cv2.namedWindow("a")
cv2.setMouseCallback("a", click_event)
cv2.imshow("a",img)

while True:
    if img is None:
        img=default_img()
    tmp=img.copy()
    draw_menu(tmp)
    if first and second:
        cv2.rectangle(tmp,first,second,(0,255,0),2)
    cv2.imshow("a",tmp)
    
    keyCode = cv2.waitKey(1)

    if cv2.getWindowProperty("a", cv2.WND_PROP_VISIBLE) <1:
        break

cv2.destroyAllWindows()

