/*Q50: Write a program to print the following pattern:
*****
 ****
  ***
   **
    *

/*
Sample Test Cases:
Input 1:

Output 1:
*****
 ****
  ***
   **
    *

Input 2:

Output 2:
Note: Spaces indicate indentation.

*/
#include <stdio.h>

int main() {
    int n = 5;
    for (int i = 1; i <= n; i++) {
        for (int j = 1; j < i; j++) {
            printf(" ");
        }
        for (int k = 1; k <= n - i + 1; k++) {
            printf("*");
        }
        printf("\n");
    }
    return 0;
}