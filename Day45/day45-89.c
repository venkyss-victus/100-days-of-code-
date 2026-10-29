/*Q89: Count frequency of a given character in a string.

/*
Sample Test Cases:
Input 1:
programming
g
Output 1:
2

*/
#include <stdio.h>
#include <string.h>

int main()
{
    char str[100];
    char ch;
    int i, len, count = 0;

    fgets(str, sizeof(str), stdin);
    len = strlen(str);
    if (len > 0 && str[len - 1] == '\n')
    {
        str[len - 1] = '\0';
        len--;
    }

    scanf(" %c", &ch);

    for (i = 0; i < len; i++)
    {
        if (str[i] == ch)
        {
            count++;
        }
    }

    printf("%d", count);

    return 0;
}
