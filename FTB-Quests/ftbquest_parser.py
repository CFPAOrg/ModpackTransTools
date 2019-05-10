import nbt
import os
import json
import sys
import argparse

def clean_mkdirs(path):
    if os.path.exists(path):
        shutil.rmtree(path)
    os.makedirs(path)

def write_lang_file(lang,filepath,output_format):
    with open(filepath,'w') as f:
        if output_format=="lang":
            for key in lang:
                f.write('%s=%s\n'%(key,lang[key]))
        elif output_format=="json":
            json.dump(lang,f)
        else:
            assert False, "expect output format to be json or lang"

def parse_lang(file_path):
    f=open(file_path)
    lang={}
    if file_path.endswith('.lang'):
        for line in f:
            line=line.strip()
            if len(line)>0 and not line.startswith('#') and '=' in line:
                pair=line.split('=',1)
                lang[pair[0]]=pair[1]
    elif file_path.endswith('.json'):
        lang=json.load(f)
    else:
        assert False, "expect a json or lang file"
    f.close()
    return lang

class Visitor:
    def __init__(self,target_lang,reference_lang=None,hardcode=False,generate_nbt=False):
        self.target_lang=target_lang
        self.reference_lang=reference_lang
        self.hardcode=hardcode
        self.diff_lang={}
        self.lang={}
        self.generate_nbt=generate_nbt

    def setvalue(self,n, key):
        if not self.generate_nbt:
            return
        if str(n)=="":
            return
        self.lang[key]=str(n)
        if self.hardcode:
            if key in self.target_lang and (self.reference_lang==None or self.reference_lang[key] == str(n)):
                n.value=self.target_lang[key]
            else:
                self.diff_lang[key]=str(n)
        else:
            n.value='{%s}'%key
            if not (key in self.target_lang and (self.reference_lang==None or self.reference_lang[key] == str(n))):
                self.diff_lang[key]=str(n)

    def visit(self,key,node,prefix):
        n=node.get(key)
        if type(n)==nbt.nbt.TAG_String:        
            lang_key='%s.%s'%(prefix,key)
            self.setvalue(n,lang_key)
        elif type(n)==nbt.nbt.TAG_List:
            tags=n.tags
            prefix='%s.%s'%(prefix,key)
            for i in range(len(tags)):
                prefix_i='%s.%d'%(prefix,i)
                tag=tags[i]
                if type(tag)==nbt.nbt.TAG_String:
                    self.setvalue(tag, prefix_i)
                elif type(tag)==nbt.nbt.TAG_Compound:
                    if 'title' in tag.keys():
                        self.visit('title',tag,prefix_i)

def main(srcdir,dstdir,tar_lang,ref_lang,generate_nbt=False,hardcoding=True,namespace='modpack.ftbquests'):
    FTBQ_path=os.path.join(dstdir,'config/ftbquests/normal/')
    clean_mkdirs(FTBQ_path)
    visitor=Visitor(tar_lang,ref_lang,hardcoding,generate_nbt)
    chapters=os.listdir(srcdir)
    if generate_nbt:
        os.mkdir(os.path.join(dstdir,'chapters'))
    for chapter in chapters:
        #TODO os.path.isdir()
        if chapter=='index.nbt':
            continue
        if generate_nbt:
            os.mkdir(os.path.join(dstdir,'chapters',chapter))
        files=os.listdir(os.path.join(srcdir,chapter))
        for NBTfilename in files:
            filepath=os.path.join(srcdir,chapter,NBTfilename)
            n=nbt.nbt.NBTFile(filepath,'rb')
            keys=n.keys()
            prefix='%s.%s.%s'%(namespace,chapter,NBTfilename.split('.')[0])
            for key in ['description','text','title','tasks']:
                if key in keys:
                    visitor.visit(key,n,prefix)
            if generate_nbt:
                n.write_file(os.path.join(dstdir,'chapters',chapter,NBTfilename))
    return visitor.lang,visitor.diff_lang

def bool_of_str(string):
    dic={'false':False,'False':False,'True':True,'true':True}
    assert string in dic, "expect a boolean value"
    return dic[string]

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--srcdir', help='source directory. e.g., "config/ftbquests/normal/chapters"',required=True)
    parser.add_argument('--dstdir', help='destination directory',required=False)
    parser.add_argument('--hardcode', help='whether to hardcode texts or not (default: %(default)s)',type=bool_of_str,required=False,default='False')
    parser.add_argument('--lang', help='localized language file',type=parse_lang,required=False)
    parser.add_argument('--reflang', help='original language file for reference',type=parse_lang,required=False)
    parser.add_argument('--generate_nbt', help='whether to generate nbt file or not',type=bool_of_str,required=True)
    parser.add_argument('--namespace', help='namespace for language keys (default: %(default)s)',type=str,required=False, default='modpack.ftbquests')
    parser.add_argument('--output_diff', help='diff file to output, valid only when REFLANG provided',type=str,required=False)
    parser.add_argument('--output_lang', help='language file to outout',type=str,required=False)
    parser.add_argument('--output_format', help='format of output file (json/lang) (default: %(default)s)',type=str,required=False, default='json')
    args=parser.parse_args()
    #print(args)
    lang,diff=main(args.srcdir,args.dstdir,args.lang,args.reflang,args.generate_nbt,args.hardcode,args.namespace)
    if args.output_lang != None:
        write_lang_file(lang,args.output_lang,args.output_format)
    if args.output_diff != None:
        write_lang_file(diff,args.output_diff,args.output_format)
