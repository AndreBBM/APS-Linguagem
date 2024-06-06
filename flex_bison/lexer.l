%{
#include "parser.tab.h"
%}

%%

[ \t]+                    { /* Ignore white space */ }
"#"[^\n]*                 { /* Ignore comments starting with # */ }
"--"[^\n]*                 { /* Ignore comments starting with # */ }
\"[^\"]*\"                  { yylval.str = strdup(yytext + 1); yylval.str[strlen(yylval.str) - 1] = '\0'; return STRING; }
"\n"                      { return NEWLINE; }
"ler()"                     { return LER; }
"local"                   { return LOCAL; }
"retorna"                 { return RETORNA; }
"exibir"                  { return PRINT; }
"se"                      { return IF; }
"senão"                   { return ELSE; }
"enquanto"                { return WHILE; }
"função"                  { return FUNCTION; }
"ou"                      { return OR;  }
"e"                       { return AND;  }
"não"                     { return NOT;  }
"Verdadeiro"              { return TRUE; }
"Falso"                   { return FALSE; }
"("                       { return LPAREN; }
")"                       { return RPAREN; }
"+"                       { return PLUS; }
"-"                       { return MINUS; }
"*"                       { return TIMES; }
"/"                       { return DIVIDE; }
"=="                      { return EQUAL; }
"!="                      { return NOTEQUAL; }
">"                       { return GREATER; }
"<"                       { return LESS; }
">="                      { return GREATEREQUAL; }
"<="                      { return LESSEQUAL; }
"="                       { return ASSIGN; }
".."                      { return CONCAT; }
[a-zA-Z_][a-zA-Z0-9_]*    { yylval.str = strdup(yytext); return IDENTIFIER; }
[0-9]+                    { yylval.num = atoi(yytext); return NUMBER; }
"{"                       { return LBRACE; }
"}"                       { return RBRACE; }

.                         { return *yytext; }

%%

// Required function for Flex
int yywrap() {
    return 1;
}

/*
bison -d -o parser.tab.c parser.y
flex -o lexer.c lexer.l
gcc -o parser parser.tab.c lexer.c -lfl
./parser < lua.txt
*/