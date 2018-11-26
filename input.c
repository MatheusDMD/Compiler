int soma(int x, int y)
{
    int mult(int a)
    {
        return(2 * a);
    };
    return(x + mult(y));
}
void main()
{
    int a;
    int b;
    int var;
    a = 3;
    var = 0;
    b = soma(a, 4);
    if(a > b && b > 3){
        printf(b);
    }else{
        printf(a); /* Prints 3 */
    };
    while(var < a || var < 10){
        printf(var); /* Prints 0, 1, 2, 3, 4, 5, 6, 7, 8, 9 */
        var = var + 1;
    };
    printf(b - 1); /* Prints 10 */
    {
        int c;
        int a;
        a = 2;
        c = soma(b, 2); /* works fine */
        printf(a); /* Prints 2 */
    };
    printf(b); /* Prints 11 */
    printf(a); /* Prints 3 */
    printf(c); /* Error */
}