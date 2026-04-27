import math
import re           #This is used for replacing x with the input from the user in user defined function
INTEGER, PLUS, EOF, OPERATION, FUNCTION,CONSTANT = 'INTEGER', 'PLUS', 'EOF', 'OPERATION', 'FUNCTION', 'CONSTANT' 

def isfloat(x):                         #Used to check if a number is integer or not
    try:
        y= float(x)
        return True
    except:
        return False

class SPLError(Exception):              #This is just used to pass when an invalid input is entered
    pass

class Token:                            #Self defined data type
    def __init__(self,val,ty):
        self.val =val  
        self.ty =ty 

class Operation:                        #This class is used to evaluate both Arithmetic and logical operations(+,-,*,/,^,==,<)
    def eval(op,a,b):                   #It takes to the operation and next to tokens to evaluate the operation
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
        


            
class Function:                         #This class is used to evaluate the inbuilt functions of the special language(sin,cos,log,sqrt,exp)
    def eval(fu,a):
        if fu.val =="sin":
            return math.sin(a)          #It uses the inbuilt math library to calculte all the functions
        elif fu.val == "cos":
            return math.cos(a)
        elif fu.val =="log":
            return math.log(a)
        elif fu.val =="exp":
            return math.exp(a)
        elif fu.val =="sqrt":
            return math.sqrt(a) 
        
class Condition:                       #This class is used to work on if else
    def eval(condit,out1,out2):        #If the condition expression is true than the second expression is returned otherwise the first expression is returned
        if condit != 0:
            return out1
        else:
            return out2
        

#This is the main Interpreter class which calculates every instruction and convert them into token and stores them in list 
#Then that list is given to the parser function inside it to evaluate the entire operation according to the instruction


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
        self.variable = variable if variable is not None else {'a': 0, 'b': 0, 'c': 0}      #List of variables 
        self.variable_write = ["a=","b=","c="]
        self.function = ["f","g"]
        self.made_functions = made_functions if made_functions is not None else {}          #List of self defined functions




    def error(self, invalid_term):                                                          #This function is called when a unidentified variable or value is given as input
        raise SPLError(f"Unrecognized expression: {invalid_term}")
    
    def finalize_token(self):                                           # Checks the type of token and decides which type should be assigned to it
        if self.str == "":
            return

        if self.str.isdigit():
            self.tokens.append(Token(int(self.str), INTEGER))

        elif isfloat(self.str):
            self.tokens.append(Token(float(self.str), "FLOAT"))
        
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
            return self.error(self.str)

        self.str = ""
        self.type = None
            
    def get_next_token(self):                                       #This functionn converts the entire text into a list of tokens 
        text = self.text

        if self.pos > len(text) - 1:
            self.finalize_token()
            return Token("EOF", None)

        current_char = text[self.pos]
        self.pos += 1

        if current_char.isspace():                                  #If a space is found than it transfers it to the finalize token 
            self.finalize_token()
            return
        else:                                                       #Otherwise the current character is added to the input string and next character is checked
            self.str += current_char
            return self.get_next_token()


    def expr(self):                                                 #Calculates the List of Tokens
        while(self.pos<len(self.text)):
            self.get_next_token()
        
        return self.parse()

# -------------------------------------


    def capture_one(self):                                          #Capture Token for one complete expression without evaluating
            start = self.parse_pos
            self._skip_expr()
            return self.tokens[start:self.parse_pos]

    def _skip_expr(self):                                           #Advance the parse position of one expression without evaluating
        if self.parse_pos >= len(self.tokens):
            return
        token = self.tokens[self.parse_pos]
        self.parse_pos += 1

        if token.ty in (INTEGER, CONSTANT, "Variable_read"):
            return                          
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

    def tokens_to_string(self, tokens):                             #Convert a list of tokens back to string
        return " ".join(str(t.val) for t in tokens)



#------------------------------------

    def parse(self):                                                        #Evaluate the list of tokens
        current_token = self.tokens[self.parse_pos]
        self.parse_pos +=1


        if current_token.ty == INTEGER:
            return current_token.val
        
        elif current_token.ty == "FLOAT":
            return current_token.val
        
        elif current_token.ty == OPERATION:                                #Takes to the operation class
            left = self.parse()
            right = self.parse()
            return Operation.eval(current_token,left,right)
            
        elif current_token.ty == FUNCTION:                                  #Takes to the function class
            next = self.parse()
            return Function.eval(current_token,next)
            
        elif current_token.ty == CONSTANT:
            return 3.141592653589793
        
        elif current_token.ty == "Variable_write":                          #Write the value of variable given by the user in dictionary stored in main class
            if current_token.val == 'a=':
                self.variable.update({"a":self.parse() })
                return self.variable["a"]
            elif current_token.val == 'b=':
                self.variable.update({"b":self.parse() })
                return self.variable["b"]
            elif current_token.val == 'c=':
                self.variable.update({"c":self.parse() })
                return self.variable["c"]
        
        elif current_token.ty == "Variable_read":                           #Returns the value of the stored variable
            if current_token.val == 'a':    
                return self.variable["a"]
            elif current_token.val == 'b':
                return self.variable["b"]
            elif current_token.val == 'c':
                return self.variable["c"]
            elif current_token.val == 'x':
                return self.variable["x"]
            
        elif current_token.ty == "if_then":                                 #This will calculate the expression 1 of if block
            condit = self.parse()                       
            true_tokens  = self.capture_one()           
            false_tokens = self.capture_one()           

            if condit != 0:                                                 #if Exp1 !=0 than expression 2 output is returned
                true_str = self.tokens_to_string(true_tokens)
                temp = Interpreter(true_str, self.variable, self.made_functions)
                return temp.expr()
            else:                                                           #Otherwise expression 3 result is returned
                false_str = self.tokens_to_string(false_tokens)
                temp = Interpreter(false_str, self.variable, self.made_functions)
                return temp.expr()
        
        elif current_token.ty == "Function_call":                           #If user defined function is called than this function is called     
            if current_token.val == "f":                    
                arg = self.parse()                  
                self.variable['x'] = arg                                    #Take the user input for function and store it in x
                body = self.made_functions['f']
                substituted = re.sub(r'\bx\b', str(arg), body)              #Replece x from the function with the input given by user
                interpreter2 = Interpreter(substituted,self.variable,self.made_functions)           #Then the function is calculated with the function as text
                result = interpreter2.expr()
                return result
            elif current_token.val == "g":
                arg = self.parse()                  # step 2: evaluate argument first
                self.variable['x'] = arg     
                body = self.made_functions['g']
                substituted = re.sub(r'\bx\b', str(arg), body)  # step 5: substitute
                interpreter2 = Interpreter(substituted,self.variable,self.made_functions)
                result = interpreter2.expr()
                return result

        
        return 0

 
 
 
def expression_length(tokens, i, variables, made_functions):            #Return length to tokens for completing the statement
    if i >= len(tokens):
        return 0

    token = tokens[i]

    if token.isdigit():
        return 1
    elif token == 'pi':
        return 1
    elif token in variables:
        return 1
    elif token in {'+', '-', '*', '/', '^', '==', '<'}:
        left  = expression_length(tokens, i + 1, variables, made_functions)
        right = expression_length(tokens, i + 1 + left, variables, made_functions)
        return 1 + left + right
    elif token in {'sin', 'cos', 'exp', 'log', 'sqrt'}:
        arg = expression_length(tokens, i + 1, variables, made_functions)
        return 1 + arg
    elif token == 'if':
        cond  = expression_length(tokens, i + 1, variables, made_functions)
        true  = expression_length(tokens, i + 1 + cond, variables, made_functions)
        false = expression_length(tokens, i + 1 + cond + true, variables, made_functions)
        return 1 + cond + true + false
    elif len(token) == 2 and token[1] == '=' and token[0].isalpha():
        arg = expression_length(tokens, i + 1, variables, made_functions)
        return 1 + arg
    elif token in made_functions:
        arg = expression_length(tokens, i + 1, variables, made_functions)
        return 1 + arg

    return 1


#This function is used for multiple expression calculation. It devides the text into tokens and check for the expression using the expression length and than store as statements

def split_statements(text, variables, made_functions):              
    tokens = text.split()
    statements = []
    i = 0

    while i < len(tokens):
        length = expression_length(tokens, i, variables, made_functions)
        statements.append(' '.join(tokens[i:i + length]))
        i += length

    return statements 
 
 




def main():
    variables = {'a':0 , 'b':0,'c':0,'x':0}                    #Variables are stored here
    made_functions = {'f':0,'g':0}                              #User defined functions are stored here
    
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

        if text.startswith('{') and text.endswith('}'):         #Checks for the block expression and using split_statement devides into multiple statements and evaluate all and return output of last expression
            inner = text[1:-1].strip()
            statements = split_statements(inner, variables, made_functions)

            result = None
            for stmt in statements:
                stmt = stmt.strip()
                if not stmt:
                    continue

                if len(stmt) >= 2 and stmt[1] == '=' and stmt[0].isalpha() and stmt[0] not in {'a', 'b', 'c'}:
                    fname = stmt[0]
                    body  = stmt[2:].strip()
                    made_functions[fname] = body
                    result = 0
                    continue

                try:
                    interpreter = Interpreter(stmt, variables, made_functions)
                    result = interpreter.expr()
                except SPLError as e:
                    print(e)
                    result = None
                    break                   # stop block on first error

            if result is not None:
                print(result)
            continue

        if len(text) >= 2 and text[1] == '=' and (text[0] == 'f' or text[0] == 'g'):            #This is used for function definition
            fname = text[0]              
            body  = text[2:].strip()     
            made_functions[fname] = body
            print("0")
            
            continue
        
        try:
            statements = split_statements(text, variables, made_functions)
            for stmt in statements:
                stmt = stmt.strip()
                if not stmt:
                    continue
                try:
                    interpreter = Interpreter(stmt, variables, made_functions)
                    print(interpreter.expr())
                except SPLError as e:
                    print(e)
                    break                   
        except SPLError as e:
            print(e)


if __name__ == '__main__':
    main()
