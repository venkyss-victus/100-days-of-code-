/*Count positive, negative, and zero elements in an array.*/
#include <stdio.h>

int main() {
    int arr[] = {1, -2, 0, 3, -4, 0, 5};
    int n = sizeof(arr) / sizeof(arr[0]);
    int positive = 0, negative = 0, zero = 0;

    for (int i = 0; i < n; i++) {
        if (arr[i] > 0) {
            positive++;
        } else if (arr[i] < 0) {
            negative++;
        } else {
            zero++;
        }
    }

    printf("Positive elements: %d\n", positive);
    printf("Negative elements: %d\n", negative);
    printf("Zero elements: %d\n", zero);
    return 0;
}
