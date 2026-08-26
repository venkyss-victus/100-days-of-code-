/* Q33 (Loops without Arrays/Strings)
Write a program to check if a number is an Armstrong number.*/
#include <stdio.h>

int main() {
    int n, original, remainder, digits = 0, sum = 0;
    int temp, i, power;

    printf("Enter a number: ");
    scanf("%d", &n);

    original = n;
    temp = n;

    // Count number of digits
    while (temp != 0) {
        digits++;
        temp /= 10;
    }

    temp = n;

    // Calculate Armstrong sum
    while (temp != 0) {
        remainder = temp % 10;

        power = 1;
        for (i = 0; i < digits; i++) {
            power *= remainder;
        }

        sum += power;
        temp /= 10;
    }

    if (sum == original)
        printf("%d is an Armstrong number.\n", original);
    else
        printf("%d is not an Armstrong number.\n", original);

    return 0;
}