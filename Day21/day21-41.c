//Write a program to swap the first and last digit of a number.
#include <stdio.h>

int main() {
    int n, first, last, digits = 0;
    int temp, pow10 = 1, middle, result;

    scanf("%d", &n);

    last = n % 10;

    temp = n;
    while (temp >= 10) {
        temp /= 10;
        digits++;
        pow10 *= 10;
    }

    first = temp;

    middle = (n % pow10) / 10;

    result = last * pow10 + middle * 10 + first;

    printf("%d", result);

    return 0;
}