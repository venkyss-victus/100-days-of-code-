/*
Question 91:
Remove all vowels from a string.
*/

#include <stdio.h>

int main()
{
    char str[1000];
    char result[1000];
    int j = 0;

    if (fgets(str, sizeof(str), stdin) != NULL)
    {
        for (int i = 0; str[i] != '\0'; i++)
        {
            char ch = str[i];
            if (ch != 'a' && ch != 'e' && ch != 'i' && ch != 'o' && ch != 'u' &&
                ch != 'A' && ch != 'E' && ch != 'I' && ch != 'O' && ch != 'U')
            {
                result[j] = ch;
                j++;
            }
        }
        result[j] = '\0';

        printf("%s", result);
    }

    return 0;
}
