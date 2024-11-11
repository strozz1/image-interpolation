function yy = interpcubica(yi,pos)
yi=double(yi);
if numel(yi) ~= 4
    error('El array debe tener exactamente %d elementos.', 4);
end
xi=double([0:2:6]');


H=double([xi.^0 xi xi.^2 xi.^3]);
c=H\yi;

xx=pos;
yy=c(1) + c(2)*xx + c(3)*xx^2 + c(4)*xx^3;
end