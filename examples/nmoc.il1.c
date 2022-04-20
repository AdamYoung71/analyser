int main() {
    a = 1;
    b = 2;
    open(1);
    open(2);
    open(3);
    open(4);
    close(5);
    open(x);
    open(y);
    open(z);
    open(a1);
    close(a2);
    if(a == b) {
        close(x);
        close(1);
    } else
    {
        close(y);
        close(2);
    }

    while(a < b) {
        close(z);
        close(3);
    }

}