/*
 * Q59: Count even and odd numbers in an array.
 */
#include <stdio.h>

int main() {
    int arr[] = {1, 5, 9, 14, 200};
    int size = sizeof(arr) / sizeof(arr[0]);
    int even_count = 0;
    int odd_count = 0;

    // Iterate over the array
    for(int i = 0; i < size; i++) {
        // Check for even number
        if(arr[i] % 2 == 0) {
            even_count++;
        } else {
            odd_count++;
        }
    }

    printf("Even elements = %d\n", even_count);
    printf("Odd elements = %d\n", odd_count);

    return 0;
}