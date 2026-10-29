/*Q88: Replace spaces with hyphens in a string.

/*
Sample Test Cases:
Input 1:
hello world
Output 1:
hello-world

*/
#include <stdio.h>
#include <string.h>

int main()
{
    char str[100];
    int i, len;

    fgets(str, sizeof(str), stdin);
    len = strlen(str);
    if (len > 0 && str[len - 1] == '\n')
    {
        str[len - 1] = '\0';
        len--;
    }

    for (i = 0; i < len; i++)
    {
        if (str[i] == ' ')
        {
            str[i] = '-';
        }
    }

    printf("%s", str);

    return 0;
}
