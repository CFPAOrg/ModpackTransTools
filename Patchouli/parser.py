import pprint
import os
import sys
import json
def get_all_json(path):
    l=[]
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith('.json') and not file.startswith('.'):
                l.append(os.path.join(root, file))
    return l

class Visitor:
    def __init__(self,base_path):
        self.base_path=base_path
        self.lang={}
        self.target_fields=['name','description','title','text','title2','pages']

    def visit(self,node,prefix):
        if type(node)==dict:
            for key in node:
                if key in self.target_fields:
                    val=node[key]
                    lang_key="%s.%s"%(prefix,key)
                    if type(val)==str:
                        self.lang[lang_key]=val
                    elif type(val)==list:
                        self.visit(val,lang_key)
        elif type(node)==list:
            for i in range(len(node)):
                self.visit(node[i],"%s.%d"%(prefix,i))
                

if __name__=="__main__":
    path=sys.argv[1]
    l=get_all_json(path)
    visitor=Visitor(path)
    for filepath in l:
        with open(filepath) as f:
            node=json.load(f)
        prefix=os.path.relpath(filepath,path).replace('/','.')[:-5]
        visitor.visit(node,prefix)
    with open(sys.argv[2],'w') as f:
        json.dump(visitor.lang,f)
