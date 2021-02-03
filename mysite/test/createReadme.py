import sys
import os, re, datetime


def createReadme(path='./'):
    f=open(path+'README.txt','w')
    for root,dirs,files in os.walk(path):
        for file in files:
            if os.path.isfile(path+'/'+file)==False:
                continue
            if file=='createReadme.py':
                continue
            
            with open(path+'/'+file,'r') as fp:
                content = fp.read()
                pattern = re.compile(r'"""(\s?.*?\s?)"""')
                reStr = pattern.findall(content)
                if len(reStr)!=0: 
                    f.write("##########"+file+"#################\n")
                    for line in reStr:
                        line=line.strip()            
                        f.write("  "+line)
                        f.write('\n')
    f.close

createReadme('/root/gp/mysite/test/')


    