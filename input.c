int soma(int x, int y){
    int mult(int k, int j){
        return(k * j);
    };
    return(x + mult(y,2));
}
void main(){
    int a;
    int b;
    int c;
    int d;
    {
        int a;
        a = 2;
        printf(a);
    };
    a = 3;
    printf(a);
    c = soma(a,4);
    d = a;
    printf(c);
    printf(d);
    b = soma(a,3);
    printf(b);
}