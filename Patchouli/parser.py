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
    def __init__(self,mode,lang):
        self.mode=mode
        self.lang=lang
        self.target_fields=['name','description','title','text','title2','pages']
        self.visit0=getattr(self,mode)

    def parse(self,lang_key,base,index):
        self.lang[lang_key]=base[index]

    def render(self,lang_key,base,index):
        if lang_key in self.lang:
            base[index]=self.lang[lang_key]

    def visit(self,node,prefix):
        if type(node)==dict:
            for key in node:
                if key in self.target_fields:
                    val=node[key]
                    lang_key="%s.%s"%(prefix,key)
                    if type(val)==str:
                        self.visit0(lang_key,node,key)
                    elif type(val)==list:
                        self.visit(val,lang_key)
        elif type(node)==list:
            for i in range(len(node)):
                self.visit(node[i],"%s.%d"%(prefix,i))
                

if __name__=="__main__":
    mode=sys.argv[1]
    assert mode=='parse' or mode=='render'
    
    #path=assets/.../patchouli_books/.../en_us/
    path=sys.argv[2]
    l=get_all_json(path)
    
    json_file=sys.argv[3]
    lang={}
    if mode=='render':
        with open(json_file) as f:
            lang=json.load(f)
    visitor=Visitor(mode,lang)
    for filepath in l:
        with open(filepath) as f:
            root=json.load(f)
        prefix=os.path.relpath(filepath,path).replace('/','.')[:-5]
        visitor.visit(root,prefix)
        #直接在原文件位置写的，用的时候要注意
        if mode=='render':
            with open(filepath,'w') as f:
                f.write(json.dumps(root,indent=4))
    if mode=='parse':
        with open(json_file,'w') as f:
            f.write(json.dumps(lang,indent=4))
