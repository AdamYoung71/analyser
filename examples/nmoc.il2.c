int main() {
    open(*x);
    open(*y);
    open(*z);
    open(&a1);
    open(*a2);
    close(*a3);
    if(*x) {
        close(*x);
        close(&a1);
    } else {
        close(*z);
    }

}