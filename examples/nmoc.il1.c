int main() {
    a = 1;
    b = 2;
    open(x);
    open(y);
    open(z);
    if(a == b) {
        close(x);
    } else
    {
        close(y);
    }
    
    while(a < b) {
        close(c);
    }
    
}