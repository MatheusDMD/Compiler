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
    a = 3;
    b = soma(a, 4);
    printf(b);
    {
        int c;
        int a;
        a = 2;
        c = soma(b, 2); /* Não dá erro */
        printf(a); /* Imprime 2 */
    };
    printf(b);
    printf(a); /* Imprime 3 */
    printf(c); /* Dá erro */
}