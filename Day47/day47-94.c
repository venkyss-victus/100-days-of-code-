/*
Question 94:
Find the longest word in a sentence.
*/

#include <stdio.h>
#include <string.h>

int main()
{
    char sentence[1000];
    char longest[1000] = "";
    char current[1000] = "";
    int max_len = 0;
    int cur_len = 0;

    if (fgets(sentence, sizeof(sentence), stdin) == NULL)
    {
        return 0;
    }

    for (int i = 0; sentence[i] != '\0'; i++)
    {
        if (sentence[i] != ' ' && sentence[i] != '\n' && sentence[i] != '\t')
        {
            current[cur_len] = sentence[i];
            cur_len++;
        }
        else
        {
            if (cur_len > 0)
            {
                current[cur_len] = '\0';
                if (cur_len > max_len)
                {
                    max_len = cur_len;
                    strcpy(longest, current);
                }
                cur_len = 0;
            }
        }
    }

    if (cur_len > max_len)
    {
        current[cur_len] = '\0';
        strcpy(longest, current);
    }

    printf("%s\n", longest);

    return 0;
}
