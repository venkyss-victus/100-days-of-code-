/*
 * Q79: Perform diagonal traversal of a matrix.
 */
#include <stdio.h>
int main() {
    int a[10][10];
    int r, c, i, j;
    printf("Enter the number of rows and columns of the matrix: ");
    scanf("%d %d", &r, &c);
    printf("Enter elements of the matrix:\n");
    for (i = 0; i < r; i++) {
        for (j = 0; j < c; j++) {
            scanf("%d", &a[i][j]);
        }
    }
    printf("Diagonal traversal of the matrix:\n");
    // Traverse the matrix diagonally
    for (int d = 0; d < r + c - 1; d++) {
        for (i = 0; i < r; i++) {
            j = d - i;
            if (j >= 0 && j < c) {
                printf("%d ", a[i][j]);
            }
        }
    }  // Print a new line after the traversal
    printf("\n");
    return 0;
}   
