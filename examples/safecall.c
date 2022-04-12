

int main() {
    x = 3;
    if(x>1) {
        protect();
    } else {
        y = 2;
        protect();
    }
    untrust();
}