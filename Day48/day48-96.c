/*
Question 96:
Reverse each word in a sentence without changing the word order.
*/

#include <stdio.h>
#include <string.h>

int main()
{
    char str[1000];

    if (fgets(str, sizeof(str), stdin) == NULL)
    {
        return 0;
    }

    int len = strlen(str);
    if (len > 0 && str[len - 1] == '\n')
    {
        str[len - 1] = '\0';
        len--;
    }

    int start = 0;
    for (int i = 0; i <= len; i++)
    {
        if (str[i] == ' ' || str[i] == '\0')
        {
            int end = i - 1;
            while (start < end)
            {
                char temp = str[start];
                str[start] = str[end];
                str[end] = temp;
                start++;
                end--;
            }
            start = i + 1;
        }
    }

    printf("%s\n", str);

    return 0;
}
