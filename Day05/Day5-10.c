//Write a program to input time in seconds and convert it to hours:minutes:seconds format.
#include <stdio.h>

int main() {
    int seconds, hours, minutes, remainingSeconds;

    scanf("%d", &seconds);

    hours = seconds / 3600;
    minutes = (seconds % 3600) / 60;
    remainingSeconds = seconds % 60;

    printf("%d:%d:%d", hours, minutes, remainingSeconds);

    return 0;
}