import math
import numpy as np

__all__=['interpolate','bilineal','nearest','none_interp']


def lerp(x0,x1,y0,y1,p):
    y0=float(y0)
    y1=float(y1)
    m=float(y1-y0)/float(x1-x0)
    f=math.floor(y0+(m*(p-x0)))

    return f

def interp_bilineal_square(row0,row1,col0,col1,old,new):
    old_rows,old_cols=old.shape
    new_rows,new_cols,z=new.shape

    y1=old[row0,col0]
    y2=old[row0,col1]
    y3=old[row1,col0]
    y4=old[row1,col1]

    #Define the range of rows and cols
    row_s=pos(new_rows,old_rows,row0)
    row_e=pos(new_rows,old_rows,row1)
    col_s=pos(new_cols,old_cols,col0) 
    col_e=pos(new_cols,old_cols,col1) 

    for row in range(row_s,row_e+1):
        for col in range(col_s,col_e+1):
            l1=lerp(col_s,col_e,y1,y2,col)
            l2=lerp(col_s,col_e,y3,y4,col)
            l3=lerp(row_s,row_e,l1,l2,row)

            new[row,col]=l3;
    return new


def pos(new_s, old_s, point):
    #because indecies starts with 0, we have to sub 1 to sizes
    scale=(new_s-1)/(old_s-1)
    new_position = int(point * scale)
    return new_position

def bilineal(image,factor):
    original_height, original_width = image.shape
    
    new_width = int(original_width * factor)
    new_height = int(original_height * factor)
    new_img = np.zeros((new_height, new_width, 3), dtype=np.uint8)
    for row in range(original_height-1):
        for col in range(original_width-1):
            new_img=interp_bilineal_square(row,row+1,col,col+1,image,new_img)
    return new_img

def nearest(image,factor):
    original_height, original_width = image.shape
    
    new_height = int(original_height * factor)
    new_width = int(original_width* factor)
    new_img = np.zeros((new_height, new_width, 3), dtype=np.uint8)
    for row in range(new_height):
        for col in range(new_width):
            orig_row = min(int(row / factor), original_height - 1)
            orig_col = min(int(col / factor), original_height - 1)
            new_img[row, col]=image[orig_row, orig_col]
    return new_img

def none_interp(image,factor):
    original_rows, original_cols = image.shape
    
    new_rows = int(original_rows * factor)
    new_cols = int(original_cols * factor)

    y_scale = new_cols / original_cols
    x_scale = new_rows / original_rows
    new_img = np.zeros((new_rows, new_cols, 3), dtype=np.uint8)

    for i in range(new_rows):
        for j in range(new_cols):
            orig_x = int(j // x_scale)
            orig_y = int(i // y_scale)
            
            new_img[i, j] = image[orig_y, orig_x]
    return new_img


def interpolate(image,factor,method):
    return method(image,factor)


