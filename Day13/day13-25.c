/*Write a program to implement a basic calculator using switch-case for +, -, *, /, %.*/
#include <stdio.h>

int main() {
    int num1, num2;
    char op;

    printf("Enter first number: ");
    scanf("%d", &num1);

    printf("Enter operator (+, -, *, /, %%): ");
    scanf(" %c", &op);

    printf("Enter second number: ");
    scanf("%d", &num2);

    switch(op) {
        case '+':
            printf("Result = %d", num1 + num2);
            break;

        case '-':
            printf("Result = %d", num1 - num2);
            break;

        case '*':
            printf("Result = %d", num1 * num2);
            break;

        case '/':
            if(num2 != 0)
                printf("Result = %d", num1 / num2);
            else
                printf("Division by zero is not possible.");
            break;

        case '%':
            if(num2 != 0)
                printf("Result = %d", num1 % num2);
            else
                printf("Modulo by zero is not possible.");
            break;

        default:
            printf("Invalid operator.");
    }

    return 0;
}