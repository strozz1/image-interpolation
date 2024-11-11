clc;clear;
% fila=uint8([30,42,53,60, 62,190, 200, 220,232]);
% new_fila=upscale_cubico(fila);
% new_fila2=upscale_linear(fila);
%
% filaA=imresize(fila,[40,460],"nearest");
% imshow(filaA,[0,255]);
%
% figure;
% filaA=imresize(new_fila,[40,720],"nearest");
% imshow(filaA,[0,255]);
% title("Cubica")
% figure;
% filaB=imresize(new_fila2,[40,720],"nearest");
% imshow(filaB,[0,255]);
% title("Lineal")


%%Bilineal interpolation



factor=7;
old=uint8([ 56, 80,120; 125,146,180; 67,140,235;]);
old=imread("muestras/m1/x600-o.jpg");
old = rgb2gray(old);
new=upscale_bilineal(old,factor);
imshow(new);
figure
imshow(old);
figure
dd=imresize(old,size(new),"bilinear");
imshow(dd)
imwrite(new,"muestras/m1/x600-bil.jpg");
