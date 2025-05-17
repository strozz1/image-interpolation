#include <math.h>

typedef unsigned char uint;

uint lerp(int x0, int x1, uint y0, uint y1, int p) {
    if (x1 == x0) return y0;
    
    float t = (float)(p - x0) / (float)(x1 - x0);
    if (t < 0.0f) t = 0.0f;
    if (t > 1.0f) t = 1.0f;
    
    return (uint)(y0 + t * (y1 - y0));
}

int pos(int new_size, int old_size, int point) {
    return (int)((float)point * (float)(new_size - 1) / (float)(old_size - 1));
}
void inter_bilineal_square(int row0,int row1,int col0,int col1, uint *old, int o_rows, int o_cols, uint *new,int n_rows, int n_cols){
    uint y1=old[col0+o_cols*row0];
    uint y2=old[col1+o_cols*row0];
    uint y3=old[col0+o_cols*row1];
    uint y4=old[col1+o_cols*row1];
    // Define the range of rows and cols
    
    int row_s=pos(n_rows,o_rows,row0);
    int row_e=pos(n_rows,o_rows,row1);
    int col_s=pos(n_cols,o_cols,col0);
    int col_e=pos(n_cols,o_cols,col1);


    int row=0;
    int col=0;

   unsigned int l1,l2,l3;
    for(row=row_s;row<=row_e;row++){
        for(col=col_s;col<=col_e;col++){
            l1=lerp(col_s,col_e,y1,y2,col);
            l2=lerp(col_s,col_e,y3,y4,col);
            l3=lerp(row_s,row_e,l1,l2,row);


            new[col+n_cols*row]=l3;

        }
    }
}
