/*
Question 95:
Check if one string is a rotation of another.
*/

#include <stdio.h>
#include <string.h>

int main()
{
    char str1[1000];
    char str2[1000];
    char combined[2000];

    if (scanf("%s", str1) != 1 || scanf("%s", str2) != 1)
    {
        return 0;
    }

    if (strlen(str1) != strlen(str2))
    {
        printf("No\n");
        return 0;
    }

    strcpy(combined, str1);
    strcat(combined, str1);

    if (strstr(combined, str2) != NULL)
    {
        printf("Yes\n");
    }
    else
    {
        printf("No\n");
    }

    return 0;
}
