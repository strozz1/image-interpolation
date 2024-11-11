function new=interpbilineal(r,c,d,f,old,new)
[n,~,~]=size(old);
[m,~,~]=size(new);

y1=old(r(1),c(1));
y2=old(r(1),c(2));
y3=old(r(2),c(1));
y4=old(r(2),c(2));
new(pos(m,n,r(1)),pos(m,n,c(1)))=y1;
new(pos(m,n,r(1)),pos(m,n,c(2)))=y2;
new(pos(m,n,r(2)),pos(m,n,c(1)))=y3;
new(pos(m,n,r(2)),pos(m,n,c(2)))=y4;

row_range=pos(m,n,r(1)):pos(m,n,r(2));
col_range=pos(m,n,c(1)):pos(m,n,c(2));
for row =row_range
    range=pos(m,n,c(1)):pos(m,n,c(2));
    
    for col = range
        l1=lerp([col_range(1),col_range(end)],[y1,y2],col);
        l2=lerp([col_range(1),col_range(end)],[y3,y4],col);
        l3=lerp([row_range(1),row_range(end)],[l1,l2],row);
        
        new(row,col)=l3;
    end
end

end

function p=pos(m,n,q)
 p=floor(1+((m-1)/(n-1)*(q-1)));
end




