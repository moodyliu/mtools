import re
import sys
import os
import glob

# uncompress files in specified path by Bandizip
# file name rule: 'filename[(pwd].type' 
## for example 
### 'test(mood.zip'
### 'test.7z'

def get_pwd_re():
    return r'\..+?\('

def match_pwd(filename):
    filename = filename[::-1] #reverse
    pattern = get_pwd_re()
    #print pattern, filename
    res = re.search(pattern, filename)
    if res:
        pwd = res.group()[::-1]
        pwd = pwd[1:-1]
        return pwd
    else:
        return ''

def get_file_extensions():
    extensions = ['.7z', '.zip', '.rar']
    return extensions

def gen_cmd_header():
    return 'Bandizip x '

def remove_misc(filename):
    filename = filename.replace('.\\')
    return filename

def gen_cmd(filepath):
    cmd = gen_cmd_header()
    filename = os.path.splitext(filepath)[0]
    #filename = remove_misc(filename)
    pwd = match_pwd(filepath)

    if len(pwd):
        cmd = '{}-p:"{}" '.format(cmd,pwd)

    cmd = '{}-o:"{}" "{}"'.format(cmd, filename, filepath)
    return cmd

def compress_path():
    extensions = get_file_extensions()
    for extension in extensions:
        str_match = r'.\\*' + extension
        list_files = glob.glob(str_match)
        for filename in list_files:
            cmd = gen_cmd(filename)
            print cmd
            os.system(cmd)

if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print 'need path arg'
        exit()
    
    path = sys.argv[1]
    os.chdir(path)
    compress_path()
    #os.system('dir')
