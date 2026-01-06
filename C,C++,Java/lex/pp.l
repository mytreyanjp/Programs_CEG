%{
#include <stdio.h>

int is_prime(int num) {
    if (num <= 1) return 0;
    for (int i = 2; i * i <= num; i++) {
        if (num % i == 0) return 0;
    }
    return 1;
}

int yywrap() {
    return 1;  // Return 1 to indicate end of input
}
%}

%%
[0-9]+ {
    int num = atoi(yytext);
    if (is_prime(num)) {
        printf("%d is a prime number.\n", num);
    } else {
        printf("%d is not a prime number.\n", num);
    }
}

.|\n ;
%%

int main() {
    printf("Enter a number: ");
    yylex();
    return 0;
}
int yywrap() {
    return 1;
}
