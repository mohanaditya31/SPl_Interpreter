import math
INTEGER, PLUS, EOF, OPERATION, FUNCTION,CONSTANT = 'INTEGER', 'PLUS', 'EOF', 'OPERATION', 'FUNCTION', 'CONSTANT'


class Token:
    def __init__(self,val,ty):
        self.val =val  
        self.ty =ty 

class Operation:
    def eval(op,a,b):
        if op.val =="+":
            return a+b 
        elif op.val == "-":
            return a-b
        elif op.val =="*":
            return a*b
        elif op.val =="/":
            return a/b 
        elif op.val =="^":
            return a**b 
            
class Function:
    def eval(fu,a):
        if fu.val =="sin":
            return math.sin(a) 
        elif fu.val == "cos":
            return math.cos(a)
        elif fu.val =="log":
            return math.log(a)
        elif fu.val =="exp":
            return math.exp(a)
        elif fu.val =="sqrt":
            return math.sqrt(a) 

class Interpreter:

    def __init__(self,text):

        self.text =text 
        self.pos =0
        self.tokens = []
        self.operators = {"+","-","*","/","^"}
        self.functions = {"sin","cos","exp","log","sqrt"}
        self.type = None
        self.str =""
        self.parse_pos = 0

    def error(self):
        print("Invalid Input")
        raise Exception('Error parsing input')
    
    def finalize_token(self):
        if self.str == "":
            return

        if self.str.isdigit():
            self.tokens.append(Token(int(self.str), "INTEGER"))

        elif self.str in self.operators:
            self.tokens.append(Token(self.str, OPERATION))

        elif self.str in self.functions:
            self.tokens.append(Token(self.str, FUNCTION))

        elif self.str == "pi":
            self.tokens.append(Token(self.str, CONSTANT))

        else:
            return self.error()

        self.str = ""
        self.type = None
            
    def get_next_token(self):
        text = self.text

        if self.pos > len(text) - 1:
            self.finalize_token()
            return Token("EOF", None)

        current_char = text[self.pos]
        self.pos += 1

        if current_char.isspace():
            self.finalize_token()
            return
        else:
            self.str += current_char
            return self.get_next_token()


    def expr(self):
        while(self.pos<len(self.text)):
            self.get_next_token()
        
        return self.parse()

    def parse(self):
        current_token = self.tokens[self.parse_pos]
        self.parse_pos +=1


        if current_token.ty == INTEGER:
            return current_token.val
        
        elif current_token.ty == OPERATION:
            left = self.parse()
            right = self.parse()
            return Operation.eval(current_token,left,right)
            
        elif current_token.ty == FUNCTION:
            next = self.parse()
            return Function.eval(current_token,next)
            
        elif current_token.ty == CONSTANT:
            return 3.141592653589793
        
        
        
        return 0
        

def main():
    while True:
        try:
            text = input('spl> ')
        except EOFError:
            break
        if not text:
            continue
        if text == "exit":
            print("bye!")
            break
        interpreter = Interpreter(text)
        result = interpreter.expr()
        print(result)


if __name__ == '__main__':
    main()
