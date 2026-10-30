/*
Question 93:
Check if two strings are anagrams of each other.
*/

#include <stdio.h>
#include <string.h>

int main()
{
    char str1[100];
    char str2[100];
    int count[256] = {0};
    int i, isAnagram = 1;

    if (scanf("%s %s", str1, str2) != 2) {
        return 0;
    }

    if (strlen(str1) != strlen(str2)) {
        printf("Not anagrams\n");
        return 0;
    }

    for (i = 0; str1[i] != '\0'; i++) {
        count[(unsigned char)str1[i]]++;
        count[(unsigned char)str2[i]]--;
    }

    for (i = 0; i < 256; i++) {
        if (count[i] != 0) {
            isAnagram = 0;
            break;
        }
    }

    if (isAnagram) {
        printf("Anagrams\n");
    } else {
        printf("Not anagrams\n");
    }

    return 0;
}
