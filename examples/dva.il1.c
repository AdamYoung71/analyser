int main {
    a = 1;
    b = 2;
    c = 1;
    if(a < b) {
        b = b + 1;
        call(a);
        c = 2;
    } else {
        b = b + 2;
        call(c);
    }
    call(b);
}