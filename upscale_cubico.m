function new_fila = upscale_cubico(fila)
[m,n]=size(fila);
new_fila=uint8(zeros(m,n));


for i = 1:n

    new_fila((2*i)-1)=fila(i); % mantenemos el valor original
    i=double(i);
    y=[];
    if i==n
        y=[fila(i-1) fila(i) fila(i) fila(i)]';
    elseif i >(n-2)
        y=[fila(i-1) fila(i) fila(i+1) fila(i+1)]';
    elseif i==1
        y=[fila(i) fila(i) fila(i+1) fila(i+1)]';
    else
        y=[fila(i-1) fila(i) fila(i+1) fila(i+2)]';
    end

    ya=double(y);
    res=uint8(interpcubica(y,3));
    new_fila((2*i))=res;

end
end