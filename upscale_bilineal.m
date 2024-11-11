
function new=upscale_bilineal(old,factor)
[o_rows,o_cols,dim]=size(old);
rows=o_rows*factor+1;
cols=o_cols*factor+1;
new=uint8(zeros(rows,cols,dim));

for row= 1:o_rows-1
    for col= 1:o_cols-1

        new=interpbilineal([row,row+1],[col,col+1],1,factor,old,new);
    end

end
end