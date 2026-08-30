/*Q36: Write a program to find the HCF (GCD) of two numbers.
*/
#include <stdio.h>

int main() {
    int a, b, i, hcf;

    scanf("%d %d", &a, &b);

    hcf = 1;

    for (i = 1; i <= a && i <= b; i++) {
        if (a % i == 0 && b % i == 0) {
            hcf = i;
        }
    }

    printf("%d", hcf);

    return 0;
}