/*
 * Q64: Find the digit that occurs the most times in an integer number.
 */

#include <stdio.h>

int main() {
    int num = 1223334444;
    int digit_count[10] = {0};

    while (num > 0) {
        int digit = num % 10;
        digit_count[digit]++;
        num /= 10;
    }

    int max_count = 0;
    int most_frequent_digit = 0;

    for (int i = 0; i < 10; i++) {
        if (digit_count[i] > max_count) {
            max_count = digit_count[i];
            most_frequent_digit = i;
        }
    }

    printf("The digit that occurs the most times is %d with %d occurrences.\n", most_frequent_digit, max_count);

    return 0;
}
