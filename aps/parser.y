%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void yyerror(const char *s);
int yylex(void);
void free(void *);

typedef struct symbol {
    char *name;
    int value;
} symbol;

#define MAX_SYMBOLS 256
symbol symtab[MAX_SYMBOLS];
int sym_count = 0;

int sym_lookup(char *name) {
    for (int i = 0; i < sym_count; ++i) {
        if (strcmp(symtab[i].name, name) == 0) {
            return i;
        }
    }
    return -1;
}

int sym_add(char *name, int value) {
    if (sym_count < MAX_SYMBOLS) {
        symtab[sym_count].name = strdup(name);
        symtab[sym_count].value = value;
        return sym_count++;
    }
    return -1;
}

%}

%union {
    int num;
    char* str;
}

%token <str> IDENTIFIER
%token <str> STRING
%token <num> NUMBER
%token PRINT IF ELSE WHILE LPAREN RPAREN LBRACE RBRACE
%token TRUE FALSE
%token ASSIGN EQUAL NOTEQUAL GREATER LESS GREATEREQUAL LESSEQUAL NEWLINE  ENDSTATEMENT
%right NOT
%left PLUS MINUS OR AND
%left TIMES DIVIDE
%nonassoc UMINUS UPLUS // Higher precedence for unary minus and unary plus


%type <num> boolExp boolTerm relExp parseExp parseTerm factor
%type <num> statement
%type <num> program

%%

program
    : /* empty */
    | program statement
    ;

statement
    : boolExp ENDSTATEMENT NEWLINE                { printf("= %d\n", $1); }
    | PRINT boolExp ENDSTATEMENT NEWLINE          { printf("%d\n", $2); }
    | boolExp ENDSTATEMENT                   { printf("= %d\n", $1); }
    | PRINT boolExp ENDSTATEMENT             { printf("%d\n", $2); }
    | PRINT LPAREN boolExp RPAREN ENDSTATEMENT             { printf("%d\n", $3); }
    | IDENTIFIER ASSIGN boolExp ENDSTATEMENT NEWLINE {
        int idx = sym_lookup($1);
        if (idx == -1) idx = sym_add($1, $3);
        else symtab[idx].value = $3;
        free($1);
    }
    | IF LPAREN boolExp RPAREN LBRACE statement RBRACE ELSE LBRACE statement RBRACE  { 
        printf("if/else\n");
    }
    | WHILE LPAREN boolExp RPAREN LBRACE program RBRACE    { printf("WHILE\n"); }
    | NEWLINE   { $$ = 0; } // Provide a default value for empty statement
    ;

boolExp
    : boolTerm                  { $$ = $1; }
    | boolTerm OR boolTerm      { $$ = $1 || $3; }

boolTerm
    : relExp                    { $$ = $1; }
    | relExp AND relExp         { $$ = $1 && $3; }

relExp
    : parseExp                      { $$ = $1; }
    | parseExp EQUAL parseExp       { $$ = $1 == $3; }
    | parseExp NOTEQUAL parseExp    { $$ = $1 != $3; }
    | parseExp GREATER parseExp     { $$ = $1 > $3; }
    | parseExp LESS parseExp        { $$ = $1 < $3; }
    | parseExp GREATEREQUAL parseExp { $$ = $1 >= $3; }
    | parseExp LESSEQUAL parseExp   { $$ = $1 <= $3; }
    ;

parseExp
    : parseExp PLUS parseExp { $$ = $1 + $3; }
    | parseExp MINUS parseExp { $$ = $1 - $3; }
    | parseTerm { $$ = $1; }
    ;

parseTerm
    : parseTerm TIMES parseTerm { $$ = $1 * $3; }
    | parseTerm DIVIDE parseTerm { $$ = $1 / $3; }
    | factor { $$ = $1; }
    ;

factor
    : NUMBER { $$ = $1; }
    | IDENTIFIER                        { int idx = sym_lookup($1); if (idx != -1) $$ = symtab[idx].value; else yyerror("undefined variable"); free($1); }
    | TRUE                              { $$ = 1; }           // Represent True as 1
    | FALSE                             { $$ = 0; }  
    | NOT factor                        { $$ = !$2; }
    | LPAREN relExp RPAREN              { $$ = $2; }  // Ensure correct evaluation within parentheses
    | MINUS factor %prec UMINUS         { $$ = -$2; }
    | PLUS factor %prec UPLUS           { $$ = $2; }
    ;

%%
void yyerror(const char *s) {
    fprintf(stderr, "Error: %s\n", s);
}

int main(void) {
    printf("Enter your program, followed by EOF (Ctrl-D):\n");
    return yyparse();
}

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

