/*
 * Q77: Check if the elements on the diagonal of a matrix are distinct.
 */
#include <stdio.h>
int main() {
    int a[10][10];
    int r, c, i, j, isDistinct = 1;
    printf("Enter the number of rows and columns of the matrix: ");
    scanf("%d %d", &r, &c);
    printf("Enter elements of the matrix:\n");
    for (i = 0; i < r; i++) {
        for (j = 0; j < c; j++) {
            scanf("%d", &a[i][j]);
        }
    }
    // Check if the elements on the diagonal are distinct
    for (i = 0; i < r; i++) {
        for (j = 0; j < c; j++) {
            if (i == j) { // Check only diagonal elements
                for (int k = 0; k < i; k++) {
                    if (a[i][j] == a[k][k]) {
                        isDistinct = 0;
                        break;
                    }
                }
            }
            if (!isDistinct) {
                break;
            }
        }
        if (!isDistinct) {
            break;
        }
    }
    if (isDistinct) {
        printf("The elements on the diagonal are distinct.\n");
    } else {
        printf("The elements on the diagonal are not distinct.\n");
    }
    return 0;
}
