import re

class Token:
    def __init__(self, tipo, valor):
        self.tipo = tipo
        self.valor = valor
        self.parenteses = 0

class Tokenizer:
    def __init__(self, expressao):
        self.source = expressao
        self.position = 0
        self.next = None
        self.parenteses = 0
        self.chaves = 0
        self.novalinha = 0
        
    def selectNext(self):
        if self.position == len(self.source):
            self.next = Token('EOF', None)

        elif self.source[self.position] == ' ':
            while self.position < len(self.source) and self.source[self.position] == ' ':
                self.position += 1
            if self.position == len(self.source):
                self.next = Token('EOF', None)
            #elif self.next.tipo == 'NUMERO' and self.source[self.position].isdigit():
            #    raise ValueError(f"Caractere inesperado: '{self.source[self.position]}'")
            else:
                self.selectNext()
 
        elif self.source[self.position] in ['+', '-', '*', '/']:
            self.next = Token('OPERADOR', self.source[self.position])
            self.position += 1

        elif self.source[self.position].isdigit():
            start = self.position
            while self.position < len(self.source) and self.source[self.position].isdigit():
                self.position += 1
            self.next = Token('NUMERO', int(self.source[start:self.position]))

        elif self.source[self.position] == '(':
            self.next = Token('ABRE PARENTESES', self.source[self.position])
            self.parenteses += 1
            self.position += 1

        elif self.source[self.position] == ')':
            self.next = Token('FECHA PARENTESES', self.source[self.position])
            self.parenteses -= 1
            self.position += 1

        elif self.source[self.position] == '{':
            self.next = Token('ABRE CHAVES', self.source[self.position])
            self.chaves += 1
            self.position += 1

        elif self.source[self.position] == '}':
            self.next = Token('FECHA CHAVES', self.source[self.position])
            self.chaves -= 1
            self.position += 1
            
        # Pode ser que quebre tudo e eu tenha que reverter
        elif self.source[self.position] == '\n':
            self.next = Token('NOVALINHA', self.source[self.position])
            self.position += 1
            #self.selectNext()

        elif self.source[self.position] == '\t':
            self.position += 1
            self.selectNext()
        
        elif self.source[self.position:self.position+6] == 'exibir':    #print
            self.next = Token('PRINT', self.source[self.position:self.position+6])
            self.position += 6

        elif self.source[self.position:self.position+2] == '==':
            self.next = Token('IGUAL A', self.source[self.position:self.position+2])
            self.position += 2

        elif self.source[self.position] == '=':
            self.next = Token('IGUAL', self.source[self.position])
            self.position += 1

        elif self.source[self.position] == ',':
            self.next = Token('VIRGULA', self.source[self.position])
            self.position += 1

        elif self.source[self.position:self.position+5] == 'então': #then
            self.next = Token('THEN', self.source[self.position:self.position+5])
            self.position += 5

        elif self.source[self.position:self.position+3] == 'não':   #not
            self.next = Token('NOT', self.source[self.position:self.position+3])
            self.position += 3

        elif self.source[self.position:self.position+2] == 'ou':    #or
            self.next = Token('OR', self.source[self.position:self.position+2])
            self.position += 2

        elif self.source[self.position] == '>' or self.source[self.position] == '<':
            self.next = Token('MAIOR OU MENOR', self.source[self.position])
            self.position += 1

        elif self.source[self.position:self.position+8] == 'enquanto':  #while
            self.next = Token('WHILE', self.source[self.position:self.position+8])
            self.position += 8
        
        elif self.source[self.position:self.position+5] == 'senão':   #else
            self.next = Token('ELSE', self.source[self.position:self.position+5])
            self.position += 5

        elif self.source[self.position:self.position+2] == 'se':    #if
            self.next = Token('IF', self.source[self.position:self.position+2])
            self.position += 2

        elif self.source[self.position:self.position+4] == 'faça':  #do
            self.next = Token('DO', self.source[self.position:self.position+4])
            self.position += 4

        elif self.source[self.position:self.position+3] == 'fim':   #end
            self.next = Token('END', self.source[self.position:self.position+3])
            self.position += 3

        elif self.source[self.position:self.position+1] == 'e':   #and
            self.next = Token('AND', self.source[self.position:self.position+1])
            self.position += 1
        
        elif self.source[self.position:self.position+5] == 'ler()':  #read
            self.next = Token('READ', self.source[self.position:self.position+5])
            self.position += 5
        
        elif self.source[self.position:self.position+7] == 'retorna':   #return
            self.next = Token('RETURN', self.source[self.position:self.position+7])
            self.position += 7

        elif self.source[self.position:self.position+5] == 'local':
            self.next = Token('LOCAL', self.source[self.position:self.position+5])
            self.position += 5

        elif self.source[self.position:self.position+2] == '..':
            self.next = Token('OPERADOR', self.source[self.position:self.position+2])
            self.position += 2

        elif self.position+8 < len(self.source) and self.source[self.position:self.position+6] == 'função': #function
            self.next = Token('FUNCTION', self.source[self.position:self.position+6])
            self.position += 6 

        elif self.source[self.position] == '"':
            start = self.position
            self.position += 1
            while self.source[self.position] != '"':
                self.position += 1
                if self.position == len(self.source) or self.source[self.position] == '\n':
                    raise ValueError(f"String não fechada")
            self.next = Token('STRING', self.source[start+1:self.position])
            self.position += 1

        elif re.match(r'^[a-zA-Z_$][\w$]*$', self.source[self.position]):
            start = self.position
            while self.position < len(self.source) and re.match(r'^[\w$]*$', self.source[self.position]) and self.source[self.position] != '\n':
                self.position += 1
            self.next = Token('VARIAVEL', self.source[start:self.position])
    
        else:
            raise ValueError(f"Caractere inesperado: '{self.source[self.position]}'")