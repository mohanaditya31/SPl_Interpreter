import math
import re
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
        elif op.val == "==":
            if a == b:
                return 1
            else:
                return 0
        elif op.val == "<":
            if b > a:
                return 1
            else:
                return 0
        


            
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
        
class Condition:
    def eval(condit,out1,out2):
        if condit != 0:
            return out1
        else:
            return out2
        


class Interpreter:

    def __init__(self,text,variable = None,made_functions=None):

        self.text =text 
        self.pos =0
        self.tokens = []
        self.operators = {"+","-","*","/","^","==","<"}
        self.functions = {"sin","cos","exp","log","sqrt"}
        self.type = None
        self.str =""
        self.parse_pos = 0
        self.variable = variable if variable is not None else {'a': 0, 'b': 0, 'c': 0}
        self.variable_write = ["a=","b=","c="]
        self.function = ["f","g"]
        self.made_functions = made_functions if made_functions is not None else {}




    def error(self):                                                    #Invalid Input
        print("Invalid Input")
        raise Exception('Error parsing input')
    
    def finalize_token(self):                                           # Used to make tokens and store it 
        if self.str == "":
            return

        if self.str.isdigit():
            self.tokens.append(Token(int(self.str), INTEGER))

        elif self.str in self.operators:
            self.tokens.append(Token(self.str, OPERATION))

        elif self.str in self.functions:
            self.tokens.append(Token(self.str, FUNCTION))

        elif self.str == "pi":
            self.tokens.append(Token(self.str, CONSTANT))

        elif self.str in self.variable:
            self.tokens.append(Token(self.str,"Variable_read"))
        
        elif self.str in self.variable_write:
            self.tokens.append(Token(self.str,"Variable_write"))

        elif self.str == "if":
            self.tokens.append(Token(self.str,"if_then"))

        elif self.str in self.function:
            self.tokens.append(Token(self.str,"Function_call"))

        

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

# -------------------------------------


    def capture_one(self):
            """Capture tokens for one complete expression without evaluating."""
            start = self.parse_pos
            self._skip_expr()
            return self.tokens[start:self.parse_pos]

    def _skip_expr(self):
        """Advance parse_pos past one complete expression without evaluating."""
        if self.parse_pos >= len(self.tokens):
            return
        token = self.tokens[self.parse_pos]
        self.parse_pos += 1

        if token.ty in (INTEGER, CONSTANT, "Variable_read"):
            return                          # single token, done
        elif token.ty == OPERATION:
            self._skip_expr()               # skip left
            self._skip_expr()               # skip right
        elif token.ty == FUNCTION:
            self._skip_expr()               # skip one argument
        elif token.ty == "if_then":
            self._skip_expr()               # skip condition
            self._skip_expr()               # skip true branch
            self._skip_expr()               # skip false branch
        elif token.ty in ("Variable_write", "Function_call"):
            self._skip_expr()               # skip one argument

    def tokens_to_string(self, tokens):
        """Convert a token list back to a space-separated string."""
        return " ".join(str(t.val) for t in tokens)



#------------------------------------

    def parse(self):                                                        #How tokens will work
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
        
        elif current_token.ty == "Variable_write":
            if current_token.val == 'a=':
                self.variable.update({"a":self.parse() })
                return self.variable["a"]

            elif current_token.val == 'b=':
                self.variable.update({"b":self.parse() })
                return self.variable["b"]
            elif current_token.val == 'c=':
                self.variable.update({"c":self.parse() })
                return self.variable["c"]
        
        elif current_token.ty == "Variable_read":
            if current_token.val == 'a':
                return self.variable["a"]
            elif current_token.val == 'b':
                return self.variable["b"]
            elif current_token.val == 'c':
                return self.variable["c"]
            elif current_token.val == 'x':
                return self.variable["x"]
            
        elif current_token.ty == "if_then":
            condit = self.parse()                       # evaluate condition eagerly
            true_tokens  = self.capture_one()           # capture, don't evaluate
            false_tokens = self.capture_one()           # capture, don't evaluate

            if condit != 0:
                true_str = self.tokens_to_string(true_tokens)
                temp = Interpreter(true_str, self.variable, self.made_functions)
                return temp.expr()
            else:
                false_str = self.tokens_to_string(false_tokens)
                temp = Interpreter(false_str, self.variable, self.made_functions)
                return temp.expr()
        
        elif current_token.ty == "Function_call":
            if current_token.val == "f":         
                arg = self.parse()                  # step 2: evaluate argument first
                self.variable['x'] = arg     
                body = self.made_functions['f']
                substituted = re.sub(r'\bx\b', str(arg), body)  # step 5: substitute
                interpreter2 = Interpreter(substituted,self.variable,self.made_functions)
                result = interpreter2.expr()
                return result
            elif current_token.val == "g":
                self.variable['x'] = self.parse()
                interpreter2 = Interpreter(self.made_functions['g'],self.variable,self.made_functions)
                result = interpreter2.expr()
                return result

        
        return 0
        

def main():
    variables = {'a':0 , 'b':0,'c':0,'x':0}
    made_functions = {'f':0,'g':0}
    
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

        if len(text) >= 2 and text[1] == '=' and (text[0] == 'f' or text[0] == 'g'):
            fname = text[0]              # "f"
            body  = text[2:].strip()     # "+ x 1"
            made_functions[fname] = body
            print(f"function {fname} defined")
            
            continue
        
        interpreter = Interpreter(text,variables,made_functions)
        result = interpreter.expr()
        print(result)


if __name__ == '__main__':
    main()
