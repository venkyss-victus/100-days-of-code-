/*
Question 92:
Find the first repeating lowercase alphabet in a string.
*/

#include <stdio.h>

int main()
{
    char str[1000];
    int visited[26] = {0};
    int found = 0;

    if (fgets(str, sizeof(str), stdin) != NULL)
    {
        for (int i = 0; str[i] != '\0'; i++)
        {
            if (str[i] >= 'a' && str[i] <= 'z')
            {
                int index = str[i] - 'a';
                if (visited[index] == 1)
                {
                    printf("%c\n", str[i]);
                    found = 1;
                    break;
                }
                visited[index] = 1;
            }
        }
    }

    if (!found)
    {
        printf("-1\n");
    }

    return 0;
}
