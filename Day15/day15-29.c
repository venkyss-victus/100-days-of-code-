//Write a program to calculate the factorial of a number.
#include <stdio.h>

int main() {
    int n, i;
    long long factorial = 1;

    scanf("%d", &n);

    for(i = 1; i <= n; i++) {
        factorial = factorial * i;
    }

    printf("%lld", factorial);

    return 0;
}