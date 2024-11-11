function g = interplineal(pos,x1,y1,x2,y2)
    f1=y1;
    f12=int16((y2-y1)/(x2-x1));
    g= uint8(f1 + f12(pos-x1));
end