//Write a program to check if a number is a palindrome.
#include <stdio.h>

int main() {
    int num, original, reverse = 0, remainder;

    scanf("%d", &num);

    original = num;

    while (num != 0) {
        remainder = num % 10;
        reverse = reverse * 10 + remainder;
        num = num / 10;
    }

    if (original == reverse)
        printf("Palindrome");
    else
        printf("Not palindrome");

    return 0;
}