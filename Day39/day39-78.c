/*
 * Q78: Find the sum of main diagonal elements for a square matrix.
 */
#include <stdio.h>
int main() {
    int a[10][10];
    int r, c, i, j, sum = 0;
    printf("Enter the number of rows and columns of the matrix: ");
    scanf("%d %d", &r, &c);
    if (r != c) {
        printf("The matrix is not square. Please enter a square matrix.\n");
        return 1;
    }
    printf("Enter elements of the matrix:\n");
    for (i = 0; i < r; i++) {
        for (j = 0; j < c; j++) {
            scanf("%d", &a[i][j]);
        }
    }
    // Calculate the sum of main diagonal elements
    for (i = 0; i < r; i++) {
        sum += a[i][i];
    }
    printf("The sum of main diagonal elements is: %d\n", sum);
    return 0;
}   
