/*
 * Q66: Insert an element in a sorted array at the appropriate position.
 */
#include <stdio.h>

int main() {
    int n, i, element, pos = 0;

    // Read the size of the array
    if (scanf("%d", &n) != 1) return 1;

    int arr[n + 1];

    // Read the sorted array
    for (i = 0; i < n; i++) {
        scanf("%d", &arr[i]);
    }

    // Read the element to be inserted
    scanf("%d", &element);

    // Find the correct position for the new element
    while (pos < n && arr[pos] < element) {
        pos++;
    }

    // Shift elements to the right to make space
    for (i = n; i > pos; i--) {
        arr[i] = arr[i - 1];
    }

    // Insert the new element
    arr[pos] = element;

    // Print the updated array
    for (i = 0; i <= n; i++) {
        printf("%d ", arr[i]);
    }
    printf("\n");

    return 0;
}
