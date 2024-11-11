function f=lerp(x,y,i)
x1=double(x(1));
x2=double(x(2));
y1=double(y(1));
y2=double(y(2));
i=double(i);

f=y1+(((y2-y1)/(x2-x1))*(i-x1));

end