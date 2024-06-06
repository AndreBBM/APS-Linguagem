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

typedef struct function {
    char *name;
    char **params;
    int param_count;
    struct statement_node *body;
} function;

typedef struct statement_node {
    char *stmt;
    struct statement_node *next;
} statement_node;

#define MAX_FUNCTIONS 256
function functab[MAX_FUNCTIONS];
int func_count = 0;

int sym_lookup(const char *name);
int sym_add(const char *name, int value);
int func_lookup(const char *name);
int func_add(const char *name, char **params, int param_count, statement_node *body);
int func_call(const char *name, char **args, int arg_count);

%}

%union {
    int num;
    char* str;
    char** str_list;
}

%token <str> IDENTIFIER
%token <str> STRING
%token <num> NUMBER
%token PRINT IF ELSE WHILE LPAREN RPAREN LBRACE RBRACE LOCAL LER FUNCTION RETORNA CONCAT
%token TRUE FALSE
%token ASSIGN EQUAL NOTEQUAL GREATER LESS GREATEREQUAL LESSEQUAL NEWLINE
%right NOT
%left PLUS MINUS OR AND
%left TIMES DIVIDE
%nonassoc UMINUS UPLUS // Higher precedence for unary minus and unary

%type <num> boolExp boolTerm relExp parseExp parseTerm factor
%type <num> statement
%type <num> program block
%type <str_list> ident_list boolexp_list

%%

program:
    block
    ;

block:
    statement 
    | block statement 
    ;

statement:
    boolExp                                                 { /* Ação */ }
    | PRINT LPAREN boolExp RPAREN                           { /* Ação */ }
    | LOCAL IDENTIFIER                                      { /* Ação */ }
    | IDENTIFIER ASSIGN boolExp                               { /* Ação */ }
    | LOCAL IDENTIFIER ASSIGN boolExp                       { /* Ação */ }
    | IF boolExp LBRACE block RBRACE ELSE LBRACE block RBRACE { /* Ação */ }
    | IF boolExp LBRACE block RBRACE                        { /* Ação */ }
    | WHILE boolExp LBRACE block RBRACE                     { /* Ação */ }
    | FUNCTION IDENTIFIER LPAREN ident_list_opt RPAREN LBRACE block RBRACE { /* Ação */ }
    | RETORNA boolExp                                       { /* Ação */ }
    | NEWLINE                                               { /* Ação */ }
    ;

boolExp:
    boolTerm                  { $$ = $1; }
    | boolTerm OR boolTerm    { $$ = $1 || $3; }
    ;

boolTerm:
    relExp                    { $$ = $1; }
    | relExp AND relExp       { $$ = $1 && $3; }
    ;

relExp:
    parseExp                      { $$ = $1; }
    | parseExp EQUAL parseExp     { $$ = $1 == $3; }
    | parseExp NOTEQUAL parseExp  { $$ = $1 != $3; }
    | parseExp GREATER parseExp   { $$ = $1 > $3; }
    | parseExp LESS parseExp      { $$ = $1 < $3; }
    | parseExp GREATEREQUAL parseExp { $$ = $1 >= $3; }
    | parseExp LESSEQUAL parseExp { $$ = $1 <= $3; }
    ;

parseExp:
    parseExp PLUS parseExp        { $$ = $1 + $3; }
    | parseExp MINUS parseExp     { $$ = $1 - $3; }
    | parseExp CONCAT parseExp    { /* Ação */ }
    | parseTerm                   { $$ = $1; }
    ;

parseTerm:
    parseTerm TIMES parseTerm     { $$ = $1 * $3; }
    | parseTerm DIVIDE parseTerm  { $$ = $1 / $3; }
    | factor                      { $$ = $1; }
    ;

factor:
    NUMBER                                  { $$ = $1; }
    | STRING                                { /* Ação */ }
    | IDENTIFIER LPAREN boolexp_list_opt RPAREN {  /* Ação */ }
    | IDENTIFIER                            {/* Acao */}
    | LER                                   {/* Acao */}
    | TRUE                                  { $$ = 1; }           // Represent True as 1
    | FALSE                                 { $$ = 0; }  
    | NOT factor                            { $$ = !$2; }
    | LPAREN boolExp RPAREN                 { $$ = $2; }  // Ensure correct evaluation within parentheses
    | MINUS factor %prec UMINUS             { $$ = -$2; }
    | PLUS factor %prec UPLUS               { $$ = $2; }
    ;

ident_list:
    IDENTIFIER                    { /* Ação */ }
    | ident_list ',' IDENTIFIER   { /* Ação */ }
    ;

ident_list_opt:
    /* empty */                   { /* Ação */ }
    | ident_list                  { /* Ação */ }
    ;

boolexp_list:
    boolExp                       { /* Ação */ }
    | boolexp_list ',' boolExp    { /* Ação */ }
    ;

boolexp_list_opt:
    /* empty */                   { /* Ação */ }
    | boolexp_list                { /* Ação */ }
    ;

%%

void yyerror(const char *s) {
    fprintf(stderr, "Error: %s\n", s);
}

int main(void) {
    printf("\nEnter your program, followed by EOF (Ctrl-D):\n");
    return yyparse();
}

// Symbol table lookup function
int sym_lookup(const char *name) {
    for (int i = 0; i < sym_count; ++i) {
        if (strcmp(symtab[i].name, name) == 0) {
            return i;
        }
    }
    return -1;
}

// Symbol table add function
int sym_add(const char *name, int value) {
    if (sym_count < MAX_SYMBOLS) {
        symtab[sym_count].name = strdup(name);
        symtab[sym_count].value = value;
        return sym_count++;
    }
    return -1;
}

// Function table lookup function
int func_lookup(const char *name) {
    for (int i = 0; i < func_count; ++i) {
        if (strcmp(functab[i].name, name) == 0) {
            return i;
        }
    }
    return -1;
}

// Function table add function
int func_add(const char *name, char **params, int param_count, statement_node *body) {
    if (func_count < MAX_FUNCTIONS) {
        functab[func_count].name = strdup(name);
        functab[func_count].params = params;
        functab[func_count].param_count = param_count;
        functab[func_count].body = body;
        return func_count++;
    }
    return -1;
}

// Function call implementation (simplified for this example)
int func_call(const char *name, char **args, int arg_count) {
    // This function should look up the function by name and execute it with the provided arguments.
    // For simplification, we're just returning a fixed value here.
    // You can implement this function as needed to execute actual function logic.
    return 42; // Example return value
}
