/*Q54: Write a program to print the following pattern:

   *
  ***
 *****
*******
 *****
  ***
   *


/*
Sample Test Cases:
Input 1:
*/  
#include <stdio.h>

int main() {
    int n = 4;
    int size = 2 * n - 1;

    for (int i = 0; i < size; i++) {
        for (int j = 0; j < size; j++) {
            int top = i;
            int left = j;
            int bottom = size - 1 - i;
            int right = size - 1 - j;

            int min = top;

            if (left < min)
                min = left;
            if (bottom < min)
                min = bottom;
            if (right < min)
                min = right;

            if (min % 2 == 0)
                printf("*");
            else
                printf(" ");
        }
        printf("\n");
    }

    return 0;
}


