## EBNF da Linguagem

```ebnf
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
```