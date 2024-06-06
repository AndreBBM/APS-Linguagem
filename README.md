## EBNF da Linguagem

```ebnf

BLOCK = { STATEMENT };

STATEMENT = ( 
    IDENTIFIER, ( "=", BOOL_EXP | "(" , ( | BOOL_EXP, { ( "," ) , BOOL_EXP } ), ")" )
    | "local", IDENTIFIER, ["=", BOOL_EXP] 
    | "exibir", "(", BOOL_EXP, ")" 
    | "enquanto", BOOL_EXP, "{", "\n", { ( BLOCK )}, "}" 
    | "se", BOOL_EXP, "{", "\n", { ( BLOCK ) }, [ "senão", "\n", { ( BLOCK )}], "}"
    | "função", IDENTIFIER, "(", ( | IDENTIFIER, { ( "," ), IDENTIFIER } ), ")","{", "\n", { ( BLOCK ) }, "}"
    | "retorna", BOOL_EXP
    ), "\n" ;

BOOL_EXP = BOOL_TERM, { ("ou"), BOOL_TERM } ;

BOOL_TERM = REL_EXP, { ("e"), REL_EXP } ;

REL_EXP = EXPRESSION, ( ("==" | "<" | ">" ), EXPRESSION ) ;

EXPRESSION = TERM, { ("+" | "-" |".."), TERM } ;

TERM = FACTOR, { ("*" | "/"), FACTOR } ;

FACTOR = NUMBER 
    | STRING 
    | IDENTIFIER, ( | "(" , ( | BOOL_EXP, { ( "," ) , BOOL_EXP } ), ")" ) 
    | ("+" | "-" | "não"), FACTOR 
    | "(", BOOL_EXP, ")" 
    | "ler", "(", ")" ;

IDENTIFIER = LETTER, { LETTER | DIGIT | "_" } ;

NUMBER = DIGIT, { DIGIT } ;

LETTER = ( "a" | "..." | "z" | "A" | "..." | "Z" ) ;

DIGIT = ( "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9" | "0" ) ;

STRING = '"', ({LETTER | DIGIT | "_"}), '"';

```
![EBNF](EBNF.png)