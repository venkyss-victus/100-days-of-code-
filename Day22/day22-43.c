/*Q43 (Loops without Arrays/Strings)
Write a program to check if a number is a strong number.d*/
#include <stdio.h>

int main() {
    int n, original, digit, factorial, sum = 0;
    printf("Enter a number: ");
    scanf("%d", &n);
    original = n;

    while (n > 0) {
        digit = n % 10;
        factorial = 1;
        for (int i = 1; i <= digit; i++) {
            factorial *= i;
        }
        sum += factorial;
        n /= 10;
    }

    if (sum == original) {
        printf("%d is a strong number.\n", original);
    } else {
        printf("%d is not a strong number.\n", original);
    }

    return 0;
}