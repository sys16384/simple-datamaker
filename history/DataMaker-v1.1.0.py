from random import randint
import math
from sys import argv
import zipfile
import json
import os


def generate(conf, sep=' ') -> str:
    if isinstance(conf, str):
        l = conf.split(',')
        if len(l) == 1:
            return conf[randint(0, len(conf)-1)]
        elif len(l) == 2:
            return str(randint(int(l[0]), int(l[1])))
        elif len(l) == 3:
            a, b, c = float(l[0]), float(l[1]), float(l[2])
            res = randint(round(a/c), round(b/c))*c
            d = max(0, math.ceil(-math.log10(c)))
            return ('%.'+str(d)+'f')%res
        else:
            return ''

    elif isinstance(conf, list):
        res = ''
        for t in conf:
            res += generate(t)+sep
        res = res.rstrip()
        return res

    elif isinstance(conf, dict):
        if 'data' not in conf:
            return ''
        n = 1
        if 'repeat' in conf:
            n = conf['repeat']
        if 'sep' in conf:
            sep = conf['sep']
        res = str()
        t = set()
        sep2 = ' '
        if n==1:
            sep2 = sep
        for i in range(n):
            tmp = generate(conf['data'], sep2)
            if ('distinct' in conf) and conf['distinct']:
                while tmp in t:
                    tmp=generate(conf['data'], sep2)
                t.add(tmp)
            res += tmp+sep
        return res

    else:
        return str(conf)


if __name__ == "__main__":
    confile="config.json"
    if len(argv)>1:
        confile=argv[1]
    if not os.path.exists(confile):
        exit(confile+' not found')
    f = open(confile)
    conf = json.load(f)
    f.close()
    print('loading config file ...\n')
    
    l, r = conf['test_range']
    
    title = '' if ('title' not in conf) else conf['title']
    std = 'std' if ('std' not in conf) else conf['std']
    path = './data' if ('path' not in conf) else conf['path']
    if not os.path.exists(path):
        print('creating path '+path,'\n')
        os.mkdir(path)
    
    if 'std_compile' in conf:
        print('compiling std source code ...\n')
        os.system(conf['std_compile'])
    
    for i in range(int(l), int(r)+1):
        file_name = title+str(i)
        print("generating file",file_name+'.in',"...")
        f = open(path+'/'+file_name+'.in', 'w')
        f.write(generate(conf['config'], '\n'))
        f.close()
        print("generating file",file_name+'.out',"...")
        os.system(std+' < '+path+'/'+file_name+'.in > '+path+'/'+file_name+'.out')
    
    if ('zip' in conf) and conf['zip']:
        print("adding files to zip file ...")
        pack=zipfile.ZipFile(title+'.zip','a')
        for i in range(int(l), int(r)+1):
            file_name = title+str(i)
            pack.write(path+'/'+file_name+'.in')
            pack.write(path+'/'+file_name+'.out')
    os.system("pause")