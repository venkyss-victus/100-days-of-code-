//Write a program to find the 1’s complement of a binary number and print it.
#include <stdio.h>

int main() {
    long long binary, complement = 0, place = 1;
    int digit;

    scanf("%lld", &binary);

    while (binary != 0) {
        digit = binary % 10;

        if (digit == 0)
            complement += 1 * place;
        else
            complement += 0 * place;

        place *= 10;
        binary /= 10;
    }

    printf("%lld", complement);

    return 0;
}