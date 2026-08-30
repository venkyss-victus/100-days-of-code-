//Write a program to find the product of odd digits of a number.
#include <stdio.h>

int main() {
    int n, digit;
    int product = 1;
    int foundOdd = 0;

    scanf("%d", &n);

    while (n != 0) {
        digit = n % 10;

        if (digit % 2 != 0) {
            product *= digit;
            foundOdd = 1;
        }

        n /= 10;
    }

    if (foundOdd)
        printf("%d", product);
    else
        printf("0");

    return 0;
}