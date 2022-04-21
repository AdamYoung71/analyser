int main() {
    x = 1;
    *y = &x;
    x = 2;
    *z = y;
    z = 1;
}