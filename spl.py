class parse_input:
    def __init__(self,inp):

        self.inp=inp

        self.legal_objects={"variables":list("abc"),"binary_operations":list("+-*/^"),"functions":["sin","cos","exp","log","sqrt"],"constants":["pi"],"exit":["exit"],"writing_variables":["a=","b=","c="],"reading_variables":list("abc"),"logical_operations":["==","<"],"conditional":["if"],"writing_functions":["f=","g="],"calling_functions":list("fg"),"parameter":"x"}

        self.look_ahead={"variables":0,"binary_operations":2,"functions":1,"constants":0,"exit":0,"writing_variables":1,"reading_variables":0,"logical_operations":2,"conditional":3,"writing_functions":1,"calling_functions":1,"parameter":0,"literal":0}

    def is_float(self,chk):
        try:
            value=float(chk)
            return True

        except:
            return False


    def lexical_analyzer(self):
        input_split=list(self.inp.split())
        print(input_split)
        all_check=True
        for i in input_split:
            if self.is_float(i):
                continue

            else:
                l_o=False
                for categories in self.legal_objects:
                    if i in self.legal_objects[categories]:
                        l_o=True
                        break
                
                if not l_o:
                    print("unrecognized expression:",i)
                    all_check=False
        return all_check
             
    def return_expression(self):
        return list(self.inp.split())

    def evaluate(self,expression,idx=0):
        while idx!=len(expression)-1:
            top=expression[idx]
            cls=""
            if self.is_float(top):
                look_ahead_exp=0
                cls="literal"
            else:
                for cl in self.look_ahead:
                    if top in self.legal_objects[cl]:
                        cls=cl
                        look_ahead_exp=self.look_ahead[cls] 
                        break
            idx+=1
            vals={}
            for i in range(look_ahead_exp):
                val_=self.evaluate(expression,idx)
                vals[i]=val_
            
    class variables:
        

        

        





