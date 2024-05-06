%{
#include "parser.tab.h"
%}

%%

[ \t]+                    { /* ignore white space */ }
"#"[^\n]*                 { /* Ignore comments starting with # */ }
"[^"\n]*\" {
    yylval.str = strdup(yytext + 1);  // Allocate memory and skip the initial quote
    yylval.str[strlen(yylval.str) - 1] = '\0';  // Remove the ending quote
    return STRING;
}
\n                        { return NEWLINE; }
"exibir"                  { return PRINT; }
"se"                      { return IF; }
"senão"                   { return ELSE; }
"enquanto"                { return WHILE; }
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
[a-zA-Z_][a-zA-Z0-9_]*    { yylval.str = strdup(yytext); return IDENTIFIER; }
[0-9]+                    { yylval.num = atoi(yytext); return NUMBER; }
"{"                       { return LBRACE; }
"}"                       { return RBRACE; }
";"                       { return ENDSTATEMENT; }
.                         { return *yytext; }

%%

/*
BLOCO = { DECLARAÇÃO };
DECLARAÇÃO = ( "λ" | ATRIBUIÇÃO | EXIBIR | ENQUANTO | SE | ATRIBUIÇÃO_LOCAL), "\n" ;
ATRIBUIÇÃO_LOCAL = "local", IDENTIFICADOR, (("=", EXPRESSÃO) | "λ");
ATRIBUIÇÃO = IDENTIFICADOR, "=", EXPRESSÃO ;
EXIBIR = "exibir", "(", EXPRESSÃO, ")" ;
ENQUANTO = "enquanto", EXP_BOOL, "faça", "\n", "λ", { ( DECLARAÇÃO ), "λ" }, "fim";
SE = "se", EXP_BOOL, "então", "\n", "λ", { ( DECLARAÇÃO ), "λ" }, ( "λ" | ( "senão", "\n", "λ", { ( DECLARAÇÃO ), "λ" })), "fim" ;
EXP_BOOL = BOOL_TERM, { ("ou"), BOOL_TERM } ;
BOOL_TERM = REL_EXP, { ("e"), REL_EXP } ;
REL_EXP = EXPRESSÃO, { ("==" | ">" | "<"), EXPRESSÃO } ;
EXPRESSÃO = TERMO, { ("+" | "-" | ".."), TERMO } ;
TERMO = FATOR, { ("*" | "/"), FATOR } ;
FATOR = NÚMERO | CARACTERES | IDENTIFICADOR | (("+" | "-" | "não"), FATOR ) | "(", EXPRESSÃO, ")" | "ler", "(", ")" ;
IDENTIFICADOR = LETRA, { LETRA | DÍGITO | "_" } ;
NÚMERO = DÍGITO, { DÍGITO } ;
LETRA = ( "a" | "..." | "z" | "A" | "..." | "Z" ) ;
DÍGITO = ( "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9" | "0" ) ;
BOOLEANO = ( "Verdadeiro" | "Falso" ) ;
*/