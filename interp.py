import math
import numpy as np

__all__=['interpolate','bilineal','nearest']


def lerp(x0,x1,y0,y1,p):
    y0=float(y0)
    y1=float(y1)
    m=float(y1-y0)/float(x1-x0)
    f=math.floor(y0+(m*(p-x0)))

    return f

def interp_bilineal_square(w0,w1,h0,h1,old,new):
    old_w,old_h=old.shape
    new_w,new_h,z=new.shape

    y1=old[w0,h0]
    y2=old[w0,h1]
    y3=old[w1,h0]
    y4=old[w1,h1]
    new[_pos(new_w,old_w,w0),_pos(new_h,old_h,h0)]=y1
    new[_pos(new_w,old_w,w0),_pos(new_h,old_h,h1)]=y2
    new[_pos(new_w,old_w,w1),_pos(new_h,old_h,h0)]=y3
    new[_pos(new_w,old_w,w1),_pos(new_h,old_h,h1)]=y4
    row_r_s=_pos(new_w,old_w,w0)
    row_r_e=_pos(new_w,old_w,w1)

    col_r_s=_pos(new_w,old_w,h0) 
    col_r_e=_pos(new_w,old_w,h1) 
    for row in range(row_r_s,row_r_e):
    
        for col in range(_pos(new_w,old_w,h0),_pos(new_w,old_w,h1)):
            l1=lerp(col_r_s,col_r_e,y1,y2,col)
            l2=lerp(col_r_s,col_r_e,y3,y4,col)
            l3=lerp(row_r_s,row_r_e,l1,l2,row)
        
            new[row,col]=l3;
    return new


def _pos(new, old, point):
    scale = new / old
    new_position = int(point * scale)
    return new_position

def bilineal(image,factor):
    original_width, original_height = image.shape
    new_width = int(original_width * factor)+1
    new_height = int(original_height * factor)+1
    new_img = np.zeros((new_width, new_height, 3), dtype=np.uint8)
    for y in range(original_height-1):
        for x in range(original_width-1):
            new_img=interp_bilineal_square(x,x+1,y,y+1,image,new_img)
    return new_img

def nearest(image,factor):
    original_width, original_height = image.shape
    
    new_width = int(original_width * factor)
    new_height = int(original_height * factor)
    new_img = np.zeros((new_width, new_height, 3), dtype=np.uint8)
    for y in range(new_height):
        for x in range(new_width):
            orig_x = min(int(x / factor), original_width - 1)
            orig_y = min(int(y / factor), original_height - 1)
            new_img[x, y]=image[orig_x, orig_y]
    return new_img


def interpolate(image,factor,method):
    return method(image,factor)


