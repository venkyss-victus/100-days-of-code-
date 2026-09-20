/*
 * Q68: Delete an element from an array.
 */
#include <stdio.h>

int main() {
    int n, i, element, pos;

    // Read the size of the array
    if (scanf("%d", &n) != 1) return 1;

    int arr[n];

    // Read the array
    for (i = 0; i < n; i++) {
        scanf("%d", &arr[i]);
    }

    // Read the element to be deleted and its position
    scanf("%d %d", &element, &pos);

    // Shift elements to the left to fill the gap
    for (i = pos; i < n - 1; i++) {
        arr[i] = arr[i + 1];
    }

    // Print the updated array
    for (i = 0; i < n - 1; i++) {
        printf("%d ", arr[i]);
    }
    printf("\n");

    return 0;
}
