%{
    #include <stdio.h>
    #include <string.h>
    int total = 0;
%}

%option noyywrap

%%

SELECT          { total++; fprintf(yyout, "db.collection.find("); printf("Matched SELECT rule\n"); }
FROM            { total++; fprintf(yyout, ".find("); printf("Matched FROM rule\n"); }
WHERE           { total++; fprintf(yyout, ".filter("); printf("Matched WHERE rule\n"); }
AND             { total++; fprintf(yyout, " && "); printf("Matched AND rule\n"); }
OR              { total++; fprintf(yyout, " || "); printf("Matched OR rule\n"); }
NOT             { total++; fprintf(yyout, "!"); printf("Matched NOT rule\n"); }
IN              { total++; fprintf(yyout, ".in("); printf("Matched IN rule\n"); }
EXISTS          { total++; fprintf(yyout, ".exists("); printf("Matched EXISTS rule\n"); }
LIKE            { total++; fprintf(yyout, ".regex("); printf("Matched LIKE rule\n"); }
IS              { total++; fprintf(yyout, ".eq("); printf("Matched IS rule\n"); }
NULL            { total++; fprintf(yyout, "null"); printf("Matched NULL rule\n"); }
NOTNULL         { total++; fprintf(yyout, "!null"); printf("Matched NOT NULL rule\n"); }
EQ              { total++; fprintf(yyout, ".eq("); printf("Matched EQ rule\n"); }
NEQ             { total++; fprintf(yyout, ".ne("); printf("Matched NEQ rule\n"); }
GT              { total++; fprintf(yyout, ".gt("); printf("Matched GT rule\n"); }
LT              { total++; fprintf(yyout, ".lt("); printf("Matched LT rule\n"); }
GTE             { total++; fprintf(yyout, ".gte("); printf("Matched GTE rule\n"); }
LTE             { total++; fprintf(yyout, ".lte("); printf("Matched LTE rule\n"); }
'*'             { total++; fprintf(yyout, ".*"); printf("Matched asterisk\n"); }
'>'             { total++; fprintf(yyout, ".gt("); printf("Matched greater than\n"); }
'<'             { total++; fprintf(yyout, ".lt("); printf("Matched less than\n"); }
'='             { total++; fprintf(yyout, ".eq("); printf("Matched equals\n"); }
','             { total++; fprintf(yyout, ", "); printf("Matched comma\n"); }
[a-zA-Z_][a-zA-Z0-9_]*  { total++; fprintf(yyout, "\"%s\"", yytext); printf("Matched identifier: %s\n", yytext); }
[0-9]+          { total++; fprintf(yyout, "%s", yytext); printf("Matched number: %s\n", yytext); }
\"[^"]*\"       { total++; fprintf(yyout, "\"%s\"", yytext); printf("Matched string: %s\n", yytext); }
\'[^']*\'      { total++; fprintf(yyout, "\"%s\"", yytext); printf("Matched string: %s\n", yytext); }
[ \t\n]+        { ; }
.               { fprintf(yyout, "Unrecognized character: %s\n\n", yytext); }

%%

int main()
{
    extern FILE *yyin, *yyout; 
    yyin = fopen("D:\\Projects\\Programs\\C,C++,Java\\lex\\sql.txt", "r"); 
    if (yyin == NULL) {
        fprintf(stderr, "Error opening input file sql.txt\n");
        return 1;
    }
    yyout = fopen("D:\\Projects\\Programs\\C,C++,Java\\lex\\mongo.txt", "w"); 
    if (yyout == NULL) {
        fprintf(stderr, "Error opening output file mongo.txt\n");
        fclose(yyin);
        return 1;
    }
    printf("Converting SQL query to MongoDB query...\n");
    yylex();
    fprintf(yyout, ");\n");
    if (ferror(yyout)) {
    fprintf(stderr, "Error writing to output file mongo.txt\n");
}
    fclose(yyin);
    fclose(yyout);
    printf("Conversion complete. Output written to mongo.txt\n");
    return 0;
}