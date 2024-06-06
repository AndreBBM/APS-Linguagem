import re 
from abc import abstractmethod
import sys
from FuncTable import *
from Tokenizer import *

class SymbolTable:
    def __init__(self):
        self.table = {}
        self.sp = 0

    def setter(self, key, value):
        #if value[1] != self.table[key][1]:
        #    raise SyntaxError("Tipo não combina") 
        self.table[key][0] = value[0]
        self.table[key][1] = value[1]
        
    def getter(self, key):
        return self.table[key]
    
    def create(self, key, value, tipo):
        if key in self.table.keys():
            print(self.table)
            raise SyntaxError("Essa variável já existe, {}".format(key))
        else:
            self.sp += 4
            self.table[key] = [value, tipo, self.sp]

class PrePro:
    def filter(self, expressao):
        return re.sub(r'--.*', '', expressao)
    
class Writer:
    
    text = ''
    
    @staticmethod
    def write_start():
        file = sys.argv[1]
        file = file.split(".")
        test = file[0]+".asm"
        with open(test, "w") as f:
            with open("header.asm", "r", encoding="utf-8") as start:
                f.write(start.read()) 
    
    @staticmethod
    def write_asm(code):
        code = code
        Writer.text+=code+'\n'
            
    @staticmethod
    def write_end():
        file = sys.argv[1]
        file = file.split(".")
        test = file[0]+".asm"
        with open(test, 'a') as file:
            with open("footer.asm", "r") as end:
                file.write(Writer.text+end.read())
        
class Node:
    i = 0
    def __init__(self, tipo, valor):
        self.tipo = tipo
        self.valor = valor
        self.children = []
        self.id = Node.newId()
        Writer.sp = 0
        
    def __repr__(self):
        return f'{self.tipo}({self.valor})'
    
    @abstractmethod
    def evaluate(self, ST):
        pass

    @staticmethod
    def newId():
        Node.i += 1
        return Node.i

class Block(Node):
    def __init__(self):
        super().__init__('Block', None)
        self.statements = []
        
    def addStatement(self, statement):
        self.statements.append(statement)
        
    def evaluate(self, ST):
        for statement in self.statements:
            if statement.tipo == 'Return':
                return statement.evaluate(ST)
            statement.evaluate(ST)

class If(Node):
    def __init__(self, exp, iftrue, iffalse=None):
        super().__init__('If', None)
        self.exp = exp          # Expressão condicional
        self.iftrue = iftrue    # Bloco de código a ser executado se a expressão for verdadeira
        self.iffalse = iffalse  # Bloco de código a ser executado se a expressão for falsa (else)

    def evaluate(self, ST):
        #Writer.write_asm("IF_{}:".format(self.id))
        #self.exp.evaluate(ST)
        #Writer.write_asm("CMP EAX, False")
        #if self.iffalse is not None:
        #    Writer.write_asm("ELSE_{}:".format(self.id))
        #    #self.iffalse.evaluate(ST)
        #    Writer.write_asm("JMP EXIT_{}".format(self.id))
        #    Writer.write_asm("EXIT_{}:".format(self.id))
        #    
        #else:
        #    Writer.write_asm("JE EXIT_{}".format(self.id))
        #    #self.iftrue.evaluate(ST)
        #    Writer.write_asm("JMP EXIT_{}".format(self.id))
        #    Writer.write_asm("EXIT_{}:".format(self.id))

        #############################
        if self.exp.evaluate(ST) == 1:
            self.iftrue.evaluate(ST)
        else:
            if self.iffalse is not None:
                self.iffalse.evaluate(ST)

class While(Node):
    def __init__(self, exp, block):
        super().__init__('While', None)
        self.exp = exp
        self.block = block
        
    def evaluate(self, ST):
        Writer.write_asm("WHILE_{}: ; Inicializacao do loop".format(self.id))
        self.exp.evaluate(ST)
        Writer.write_asm("CMP EAX, False ; Condicao do loop")
        Writer.write_asm("JE EXIT_{} ; pula para o fim do loop".format(self.id))
        self.block.evaluate(ST)
        Writer.write_asm("JMP WHILE_{} ; Volta ao comeco do loop".format(self.id))
        Writer.write_asm("EXIT_{}: ; sai do loop:".format(self.id))

        #############################
        while self.exp.evaluate(ST):
            self.block.evaluate(ST)

class Statement(Node):
    def __init__(self, exp):
        super().__init__('Statement', None)
        self.exp = exp
        
    def evaluate(self, ST):
        self.exp.evaluate(ST)
    
class Assign(Node): # Usado para declarar variáveis com ou sem valor: local var = exp/ local var
    def __init__(self, var, exp):
        super().__init__('Assign', var)
        self.var = var
        self.exp = exp

    def evaluate(self, ST):
        #Writer.write_asm("PUSH DWORD 0 ; local {} = {}".format(self.var, self.exp))

        #############################
        if self.exp is None:
            ST.create(self.var, None, 'int')
            return None
        exp_evaluate = self.exp.evaluate(ST)
        if isinstance(exp_evaluate, int):
            ST.create(self.var, exp_evaluate, 'int')
        elif isinstance(exp_evaluate, str):
            ST.create(self.var, exp_evaluate, 'str')
        else:
            raise ValueError(f"Tipo de variável não suportado: {type(exp_evaluate)}, {exp_evaluate}")
        
        ##############################
        #return symbolTable[self.valor]     # talvez descomentar
        return ST.getter(self.var)
        
class DefineDecalrado(Node):    # Usado para definir/redefinir variáveis já declaradas: var = exp
    def __init__(self, var, exp):
        super().__init__('defineLocal', var)
        self.exp = exp
        self.var = var

    def evaluate(self, ST):
        exp_evaluate = self.exp.evaluate(ST)
        variavel = ST.getter(self.var)
        sp = variavel[2]

        asm = "MOV [EBP-{}], EAX ; {} = {}".format(sp, self.var, self.exp)
        Writer.write_asm(asm)


        #############################
        #exp_evaluate = self.exp.evaluate(ST)
        if isinstance(exp_evaluate, int):
            ST.setter(self.var, (exp_evaluate, 'int'))
        elif isinstance(exp_evaluate, str):
            ST.setter(self.var, (exp_evaluate, 'str'))
        else:
            raise ValueError(f"Tipo de variável não suportado: {type(exp_evaluate)}")
        return ST.getter(self.var)

class Identifier(Node):
    def __init__(self, valor):
        super().__init__('Identifier', valor)
        self.valor = valor
        
    def evaluate(self, ST):
        if self.valor not in ST.table.keys():
            raise ValueError(f"Variável não declarada: {self.valor}")
        variavel = ST.getter(self.valor)
        sp = variavel[2]

        #asm = "MOV EAX, [EBP-{}] ; retorna identificador {}".format(sp, self.valor)
        #Writer.write_asm(asm)
        
        return variavel[0]
        #############################
    
class Scan(Node):
    def __init__(self, var):
        super().__init__('Read', var)
        self.var = var
        
    def evaluate(self, ST):
        Writer.write_asm("PUSH scanint ; começa o read")
        Writer.write_asm("PUSH formatin")
        Writer.write_asm("call scanf")
        Writer.write_asm("ADD ESP, 8")
        Writer.write_asm("MOV EAX, DWORD [scanint] ; termina o read e salva o valor em EAX")

        return int(input())

class Print(Node):
    def __init__(self, exp):
        super().__init__('Print', None)
        self.exp = exp
        
    def evaluate(self, ST):
        self.exp.evaluate(ST)
        Writer.write_asm("PUSH EAX ; começa o print")
        Writer.write_asm("PUSH formatout ; formato int de saida")
        Writer.write_asm("CALL printf ; print")
        Writer.write_asm("ADD ESP, 8 ; termina o print")

        #############################
        if isinstance(self.exp.evaluate(ST), tuple):
            print(self.exp.evaluate(ST)[0])
        else:
            print(self.exp.evaluate(ST))

class BinOp(Node):
    def __init__(self, valor, left, right):
        super().__init__('BinOp', valor)
        self.children = [left, right]

    def evaluate(self, ST):
        b = self.children[1].evaluate(ST)
        Writer.write_asm("PUSH EAX")
        a = self.children[0].evaluate(ST)
        Writer.write_asm("POP EBX")

        if type(a) == tuple:
            a = a[0]
            atype = type(a)
        else:
            atype = type(a)
        if type(b) == tuple:
            b = b[0]
            btype = type(b)
        else:
            btype = type(b)

        if self.valor == '..':
            return str(a) + str(b)

        if atype != btype:
            raise ValueError(f"Tipos incompatíveis: {atype} e {btype}, a: {a}, b: {b}, valor: {self.valor}")

        if self.valor == '+':
            Writer.write_asm("ADD EAX, EBX ; soma") 
            return a + b
        elif self.valor == '-':
            Writer.write_asm("SUB EAX, EBX ; subtracao")
            return a - b
        elif self.valor == '*':
            Writer.write_asm("IMUL EBX ; multiplicacao")
            return a * b
        elif self.valor == '/':
            Writer.write_asm("CDQ ; divisao")
            Writer.write_asm("IDIV EBX ; divisao") 
            return a // b
        elif self.valor == '>':
            Writer.write_asm("CMP EAX, EBX ; comparação maior")
            Writer.write_asm("CALL binop_jg ; comparação maior")
            return int(a > b)
        elif self.valor == '<':
            Writer.write_asm("CMP EAX, EBX ; comparação menor")
            Writer.write_asm("CALL binop_jl ; comparação menor")
            return int(a < b)
        elif self.valor == '==':
            Writer.write_asm("CMP EAX, EBX ; comparação igual")
            Writer.write_asm("CALL binop_je ; comparação igual")
            return int(a == b)
        elif self.valor == 'or':
            Writer.write_asm("OR EAX, EBX ; or")
            return int(a or b)
        elif self.valor == 'and':
            Writer.write_asm("AND EAX, EBX ; and")
            return int(a and b)

class UnOp(Node):
    def __init__(self, valor, child):
        super().__init__('UnOp', valor)
        self.children = [child]

    def evaluate(self, ST):
        a = self.children[0].evaluate(ST)
        if type(a) == tuple:
            a = a[0]
            atype = type(a)
        else:
            atype = type(a)

        if self.valor == '+':
            return a
        elif self.valor == '-':
            return -a
        elif self.valor == 'not':
            return int(not a)

class IntVal(Node):
    def __init__(self, valor):
        super().__init__('IntVal', valor)

    def evaluate(self, ST):
        #asm = "MOV EAX, "+str(self.valor) + " ; retorna {}".format(self.valor)
        #Writer.write_asm(asm)
        return self.valor
    
class StringVal(Node):
    def __init__(self, valor):
        super().__init__('StringVal', valor)

    def evaluate(self, ST):
        return self.valor
    
class NoOp(Node):
    def __init__(self):
        super().__init__('NoOp', None)

    def evaluate(self, ST):
        return None
    
class FuncDec(Node):
    def __init__(self, args, block):
        super().__init__('FuncDec', args)
        self.args = args
        self.block = block
        self.children = [block]

    def evaluate(self, ST):
        FT.setter(self.args[0], [self.args, 'int', self.block])

class FuncCall(Node):
    def __init__(self, value, children):
        super().__init__('FuncCall', value)
        self.value = value
        self.children = children

    def evaluate(self, ST):
        call = FT.getter(self.value)   
        nst = SymbolTable()
        for i in range(1, len(call[0])):
            nst.create(call[0][i], self.children[i-1].evaluate(ST), 'int')

        result = call[2].evaluate(nst)
        
        if result is not None:
            return result
            
class ReturnNode(Node):
    def __init__(self, value):
        super().__init__('Return', value)
        self.value = value

    def evaluate(self, ST):
        return self.value.evaluate(ST)

class Parser:
    def __init__(self, tokenizer):
        self.tokenizer = tokenizer
        self.tokenizer.selectNext()
    
    def run(self, ST):
        resultado = self.block()
        resultado.evaluate(ST)
        if self.tokenizer.parenteses != 0:
            raise ValueError(f"Parenteses fecha sem parênteses aberto")
        return resultado
    
    def block(self):
        resultado = Block()
        while self.tokenizer.next.tipo != 'EOF':
            resultado.addStatement(self.statement())
        return resultado
    
    def statement(self):
        # A princípio, o código já está funcionando traduzido, falta trocar o then/do/end por chaves

        if self.tokenizer.next.tipo == 'NOVALINHA':
            self.tokenizer.selectNext()
            return NoOp()
        
        elif self.tokenizer.next.tipo == 'LOCAL':
            self.tokenizer.selectNext()
            if self.tokenizer.next.tipo == 'VARIAVEL':
                var = self.tokenizer.next.valor
                self.tokenizer.selectNext()
                if self.tokenizer.next.tipo == 'NOVALINHA' or self.tokenizer.next.tipo == 'EOF':
                    self.tokenizer.selectNext()
                    #if var in symbolTable:
                    #    raise ValueError(f"Variável já declarada: {var}")
                    return Assign(var, None)
                # Eu acho que o caso abaixo não é necessário/inválido no compilador
                elif self.tokenizer.next.tipo == 'IGUAL':
                    self.tokenizer.selectNext()
                    exp = self.boolExpression()
                    if self.tokenizer.next.tipo == 'NOVALINHA' or self.tokenizer.next.tipo == 'EOF':
                        self.tokenizer.selectNext()
                        return Assign(var, exp)
                    else:
                        raise ValueError(f"É esperado um \\n após a expressão")
                else:
                    raise ValueError(f"É esperado um '=' após a declaração da variável")
            else:
                raise ValueError(f"É esperado um nome de variável após o 'local'")

        elif self.tokenizer.next.tipo == 'PRINT':
            self.tokenizer.selectNext()
            if self.tokenizer.next.tipo == 'ABRE PARENTESES':
                self.tokenizer.selectNext()
            else:
                raise ValueError(f"É esperado um '(' após o 'print'")
            exp = self.boolExpression()
            if self.tokenizer.next.tipo == 'FECHA PARENTESES':
                self.tokenizer.selectNext()
                if self.tokenizer.next.tipo == 'NOVALINHA' or self.tokenizer.next.tipo == 'EOF':
                    self.tokenizer.selectNext()
                    return Print(exp)
            else:
                raise ValueError(f"É esperado um ')' após a expressão")
            
        elif self.tokenizer.next.tipo == 'RETURN':
            self.tokenizer.selectNext()
            exp = ReturnNode(self.boolExpression())
            if self.tokenizer.next.tipo == 'NOVALINHA' or self.tokenizer.next.tipo == 'EOF':
                self.tokenizer.selectNext()
                return exp
            else:
                raise ValueError(f"É esperado um \\n após a expressão")
        
        elif self.tokenizer.next.tipo == 'VARIAVEL':
            var = self.tokenizer.next.valor
            self.tokenizer.selectNext()
            if self.tokenizer.next.tipo == 'IGUAL':
                self.tokenizer.selectNext()
                exp = self.boolExpression()
                if self.tokenizer.next.tipo == 'FECHA PARENTESES' or self.tokenizer.next.tipo == 'IGUAL':
                    raise ValueError(f"É esperado um \\n após a expressão")
                if self.tokenizer.next.tipo == 'NOVALINHA' or self.tokenizer.next.tipo == 'EOF':
                    self.tokenizer.selectNext()
                    return DefineDecalrado(var, exp)
                if self.tokenizer.next.tipo == 'ABRE PARENTESES' :
                    self.tokenizer.selectNext()
                    args = []
                    while self.tokenizer.next.tipo != 'FECHA PARENTESES':
                        args.append(self.boolExpression())
                        if self.tokenizer.next.tipo == 'VIRGULA':
                            self.tokenizer.selectNext()
                        else:
                            break
                    if self.tokenizer.next.tipo == 'FECHA PARENTESES':
                        self.tokenizer.selectNext()
                    if self.tokenizer.next.tipo == 'NOVALINHA' or self.tokenizer.next.tipo == 'EOF':
                        self.tokenizer.selectNext()
                        return DefineDecalrado(var, FuncCall(exp.valor, args))
                    else:
                        raise ValueError(f"É esperado um \\n após a chamada de função, '{self.tokenizer.next.tipo}', {self.tokenizer.next.valor}, {self.tokenizer.position}")
            elif self.tokenizer.next.tipo == 'ABRE PARENTESES':
                self.tokenizer.selectNext()

                if self.tokenizer.next.tipo != 'FECHA PARENTESES':
                    arg = self.boolExpression()
                    args = [arg]
                    while self.tokenizer.next.tipo == 'VIRGULA':
                        self.tokenizer.selectNext()
                        arg = self.boolExpression()
                        args.append(arg)
                    
                if self.tokenizer.next.tipo == 'FECHA PARENTESES':
                    self.tokenizer.selectNext()
                    return FuncCall(var, args)
                else:
                    raise ValueError(f"É esperado um ')' após a chamada de função, '{self.tokenizer.next.tipo}', {self.tokenizer.next.valor}, {self.tokenizer.position}")
            else:
                raise ValueError(f"Token inesperado: '{self.tokenizer.next.tipo}', {self.tokenizer.next.valor}, {self.tokenizer.position}")
        
        elif self.tokenizer.next.tipo == 'IF':
            bloco = Block()
            blocoElse = Block()
            self.tokenizer.selectNext()
            exp = self.boolExpression()
            if self.tokenizer.next.tipo == 'ABRE CHAVES':
                self.tokenizer.selectNext()
                if self.tokenizer.next.tipo == 'NOVALINHA':
                    self.tokenizer.selectNext()
                else:
                    raise ValueError(f"É esperado um \\n após o 'then'")
                #while self.tokenizer.next.tipo != 'ELSE' and self.tokenizer.next.tipo != 'END':
                while self.tokenizer.next.tipo != 'FECHA CHAVES':
                    bloco.addStatement(self.statement())
                self.tokenizer.selectNext() # le o que vem depois do bloco if
                if self.tokenizer.next.tipo == 'ELSE':
                    self.tokenizer.selectNext()
                    if self.tokenizer.next.tipo == 'ABRE CHAVES':
                        self.tokenizer.selectNext()
                    else:
                        raise ValueError(f"É esperado um \\n após o 'else'")
                    #self.tokenizer.selectNext()
                    if self.tokenizer.next.tipo == 'NOVALINHA':
                        self.tokenizer.selectNext()
                    else:
                        raise ValueError(f"É esperado um \\n após o 'else'")
                    while self.tokenizer.next.tipo != 'FECHA CHAVES':
                        blocoElse.addStatement(self.statement())
                if self.tokenizer.next.tipo == 'FECHA CHAVES':
                    self.tokenizer.selectNext()
                    if self.tokenizer.next.tipo == 'NOVALINHA' or self.tokenizer.next.tipo == 'EOF':
                        self.tokenizer.selectNext()
                        return If(exp, bloco, blocoElse)
                    else:
                        raise ValueError(f"É esperado um \\n após o 'end', '{self.tokenizer.next.tipo}', {self.tokenizer.next.valor}, {self.tokenizer.position}")
                if self.tokenizer.next.tipo == 'NOVALINHA' or self.tokenizer.next.tipo == 'EOF':
                    self.tokenizer.selectNext()
                    return If(exp, bloco, blocoElse)
                else:
                    raise ValueError(f"Token inesperado: '{self.tokenizer.next.tipo}', {self.tokenizer.next.valor}, {self.tokenizer.position}")
            else:
                raise ValueError(f"Token inesperado: '{self.tokenizer.next.tipo}', {self.tokenizer.next.valor}, {self.tokenizer.position}")
        
        elif self.tokenizer.next.tipo == 'WHILE':
            self.tokenizer.selectNext()
            exp = self.boolExpression()
            bloco = Block()
            if self.tokenizer.next.tipo != 'ABRE CHAVES':
                raise ValueError(f"É esperado um 'do' após a expressão condicional do while, '{self.tokenizer.next.tipo}', {self.tokenizer.next.valor}, {self.tokenizer.position}")
            self.tokenizer.selectNext()
            if self.tokenizer.next.tipo == 'NOVALINHA':
                self.tokenizer.selectNext()
            else:
                raise ValueError(f"É esperado um \\n após o 'do'")
            while self.tokenizer.next.tipo != 'FECHA CHAVES':
                bloco.addStatement(self.statement())
            if self.tokenizer.next.tipo == 'FECHA CHAVES':
                self.tokenizer.selectNext()
                if self.tokenizer.next.tipo == 'NOVALINHA' or self.tokenizer.next.tipo == 'EOF':
                    self.tokenizer.selectNext()
                    return While(exp, bloco)
                else:
                    raise ValueError(f"É esperado um \\n após o 'end'")
        
        elif self.tokenizer.next.tipo == 'FUNCTION':
            self.tokenizer.selectNext()
            if self.tokenizer.next.tipo == 'VARIAVEL':
                funcName = self.tokenizer.next.valor
                self.tokenizer.selectNext()
                if self.tokenizer.next.tipo == 'ABRE PARENTESES':
                    self.tokenizer.selectNext()
                else:
                    raise ValueError(f"É esperado um '(' após o nome da função")
                args = [funcName]
                if self.tokenizer.next.tipo == 'VARIAVEL':
                    args.append(self.tokenizer.next.valor)
                    self.tokenizer.selectNext()
                while self.tokenizer.next.tipo != 'FECHA PARENTESES':
                    if self.tokenizer.next.tipo == 'VIRGULA':
                        self.tokenizer.selectNext()
                        if self.tokenizer.next.tipo == 'VARIAVEL':
                            args.append(self.tokenizer.next.valor)
                            self.tokenizer.selectNext()
                        else:
                            raise ValueError(f"É esperado um nome de variável após a ','")
                    else:
                        raise ValueError(f"É esperado um nome de variável após o '('")
                self.tokenizer.selectNext()
                if self.tokenizer.next.tipo == 'ABRE CHAVES':
                    self.tokenizer.selectNext()
                else:
                    raise ValueError(f"É esperado um '{{' após a declaração da função")
                if self.tokenizer.next.tipo == 'NOVALINHA':
                    self.tokenizer.selectNext()
                else:
                    raise ValueError(f"É esperado um \\n após a declaração da função")
                bloco = Block()
                while self.tokenizer.next.tipo != 'FECHA CHAVES':
                    bloco.addStatement(self.statement())
                if self.tokenizer.next.tipo == 'FECHA CHAVES':
                    self.tokenizer.selectNext()
                    if self.tokenizer.next.tipo == 'NOVALINHA' or self.tokenizer.next.tipo == 'EOF':
                        self.tokenizer.selectNext()
                        return FuncDec(args, bloco)
                    else:
                        raise ValueError(f"É esperado um \\n após o 'end'")
                else:
                    raise ValueError(f"Token inesperado: '{self.tokenizer.next.tipo}', {self.tokenizer.next.valor}, {self.tokenizer.position}")
            else:
                raise ValueError(f"É esperado um nome de função após o 'function' '{self.tokenizer.next.tipo}', {self.tokenizer.next.valor}, {self.tokenizer.position}")
            
        else:
            raise ValueError(f"Token inesperado: '{self.tokenizer.next.tipo}', {self.tokenizer.next.valor}, {self.tokenizer.position}")
            
    def boolExpression(self):
        resultado = self.boolTerm()
        while self.tokenizer.next.tipo == 'OR':
            operador = self.tokenizer.next.valor
            self.tokenizer.selectNext()
            right = self.boolTerm()
            if right == None:
                raise ValueError(f"Token inesperado: '{self.tokenizer.next.tipo}'")
            if operador == 'ou':
                resultado = BinOp('or', resultado, right)
            else:
                raise ValueError(f"Token inesperado: '{self.tokenizer.next.tipo}'")
        return resultado
        
    def boolTerm(self):
        resultado = self.relExpression()
        while self.tokenizer.next.tipo == 'AND':
            operador = self.tokenizer.next.valor
            self.tokenizer.selectNext()
            right = self.relExpression()
            if right == None:
                raise ValueError(f"Token inesperado: '{self.tokenizer.next.tipo}'")
            if operador == 'e':
                resultado = BinOp('and', resultado, right)
            else:
                raise ValueError(f"Token inesperado: '{self.tokenizer.next.tipo}'")
        return resultado

    def relExpression(self):
        resultado = self.parseExpression()
        if self.tokenizer.next.tipo == 'MAIOR OU MENOR':
            operador = self.tokenizer.next.valor
            self.tokenizer.selectNext()
            right = self.parseExpression()
            if right == None:
                raise ValueError(f"Token inesperado: '{self.tokenizer.next.tipo}'")
            if operador == '>':
                return BinOp('>', resultado, right)
            else:
                return BinOp('<', resultado, right)
        elif self.tokenizer.next.tipo == 'IGUAL A':
            self.tokenizer.selectNext()
            return BinOp('==', resultado, self.parseExpression())
        return resultado

    def parseExpression(self):
        resultado = self.parseTerm()
        while self.tokenizer.next.tipo == 'OPERADOR' and self.tokenizer.next.valor in ['+', '-', '..']:
            operador = self.tokenizer.next.valor
            self.tokenizer.selectNext()
            if operador == '+':
                resultado = BinOp('+', resultado, self.parseTerm())
            elif operador == '-':
                resultado = BinOp('-', resultado, self.parseTerm())
            elif operador == '..':
                resultado = BinOp('..', resultado, self.parseTerm())
            else:
                raise ValueError(f"Token inesperado: '{self.tokenizer.next.tipo}'")
        return resultado
    
    def parseTerm(self):
        resultado = self.parseFactor()
        while self.tokenizer.next.tipo == 'OPERADOR' and self.tokenizer.next.valor in ['*', '/']:
            operador = self.tokenizer.next.valor
            self.tokenizer.selectNext()
            if operador == '*':
                resultado = BinOp('*', resultado, self.parseFactor())
            else:
                resultado = BinOp('/', resultado, self.parseFactor())
        return resultado
    
    def parseFactor(self): 

        if self.tokenizer.next.tipo == 'NUMERO':
            return self.parseNumber()
        
        if self.tokenizer.next.tipo == 'STRING':
            resultado = StringVal(self.tokenizer.next.valor)
            self.tokenizer.selectNext()
            return resultado
        
        elif self.tokenizer.next.tipo == 'ABRE PARENTESES':
            self.tokenizer.selectNext()
            resultado = self.boolExpression()
            if self.tokenizer.next.tipo == 'FECHA PARENTESES':
                self.tokenizer.selectNext()
                return resultado
            else:
                raise ValueError(f"Token inesperado: '{self.tokenizer.next.tipo}'")

        elif self.tokenizer.next.tipo == 'VARIAVEL':
            var = self.tokenizer.next.valor
            identi = Identifier(var)
            self.tokenizer.selectNext()
            if self.tokenizer.next.tipo == 'ABRE PARENTESES':
                self.tokenizer.selectNext()
                args = []
                while self.tokenizer.next.tipo != 'FECHA PARENTESES':
                    args.append(self.boolExpression())
                    if self.tokenizer.next.tipo == 'VIRGULA':
                        self.tokenizer.selectNext()
                    else:
                        break
                if self.tokenizer.next.tipo == 'FECHA PARENTESES':
                    self.tokenizer.selectNext()
                return FuncCall(var, args)
            else:
                return identi
        
        elif self.tokenizer.next.tipo == 'OPERADOR' and self.tokenizer.next.valor in ['+', '-']:
            operador = self.tokenizer.next.valor
            self.tokenizer.selectNext()
            if operador == '+':
                return UnOp('+', self.parseFactor())
            else:
                return UnOp('-', self.parseFactor())
            
        elif self.tokenizer.next.tipo == 'NOT':
            self.tokenizer.selectNext()
            return UnOp('not', self.parseFactor())
        
        elif self.tokenizer.next.tipo == 'ABRE PARENTESES':
            self.tokenizer.selectNext()
            resultado = self.boolExpression()
            if self.tokenizer.next.tipo == 'FECHA PARENTESES':
                self.tokenizer.selectNext()
                return resultado
            else:
                raise ValueError(f"Token inesperado: '{self.tokenizer.next.tipo}'")
            
        elif self.tokenizer.next.tipo == 'READ':
            self.tokenizer.selectNext()
            if self.tokenizer.next.tipo == 'NOVALINHA' or self.tokenizer.next.tipo == 'EOF':
                #self.tokenizer.selectNext()
                return Scan(None)
            else:
                raise ValueError(f"Token inesperado: '{self.tokenizer.next.tipo}'")

    def parseNumber(self):
        if self.tokenizer.next.tipo == 'NUMERO':
            resultado = IntVal(self.tokenizer.next.valor)
            self.tokenizer.selectNext()
            return resultado
        else:
            raise ValueError(f"Token inesperado: '{self.tokenizer.next.tipo}'")
        
if __name__ == '__main__':
    ST = SymbolTable()
    FT = FuncTable()
    expressao = open(sys.argv[1], 'r').read()
    expressao = PrePro().filter(expressao)
    tokenizer = Tokenizer(expressao)
    parser = Parser(tokenizer)

    resultado = parser.run(ST)

