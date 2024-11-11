function new_fila = upscale_linear(fila)
new_fila=uint8(zeros(1,8));
for i = 1:8
    new_fila((2*i)-1)=fila(i); % mantenemos el valor original
    i=int16(i);
    new_fila((2*i))=interplineal((2*i)+1,i*2,int16(fila(i)),(2*i)+2,int16(fila((i)+1)));
end
new_fila((2*9)-1)=fila(9); % el ultimo lo duplicamos
new_fila((2*9))=fila(9);
end