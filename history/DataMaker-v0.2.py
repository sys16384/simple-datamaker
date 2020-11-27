from random import randint
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
            return str(randint(round(a/c), round(b/c))*c)
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
        for i in range(n):
            res += generate(conf['data'])+sep
        return res

    else:
        return str(conf)


if __name__ == "__main__":
    f = open('config.json')
    conf = json.load(f)
    f.close()
    l, r = conf['test_range']
    if 'std_compile' in conf:
        os.system(conf['std_compile'])
    for i in range(int(l), int(r)+1):
        file_name = conf['title']+str(i)
        f = open(file_name+'.in', 'w')
        f.write(generate(conf['config'], '\n'))
        f.close()
        os.system(conf['std']+'.exe < '+file_name+'.in > '+file_name+'.out')
    
    if ('zip' in conf) and conf['zip']:
        pack=zipfile.ZipFile(conf['title']+'.zip','a')
        for i in range(int(l), int(r)+1):
            file_name = conf['title']+str(i)
            pack.write(file_name+'.in')
            pack.write(file_name+'.out')
