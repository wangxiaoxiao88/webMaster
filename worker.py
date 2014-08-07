#coding=utf-8
import subprocess
import time 
import os
import sys
from flask import Flask,render_template,request

app = Flask(__name__)

already_print_num = 0

@app.route('/start')
def start():
    choose = str(request.args.get('choose',''))
    command = ''
    if choose == 'resin':
        #start resin,please replace with absolute path
	command = 'sh httpd.sh start'
    elif choose == 'tomcat':
        #startup tomcat,please replace with absolute path 
	command = 'sh startup.sh'
    else:
	print 'no such type'
	return

    popen = subprocess.Popen(command,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True) 
        
    return ''

@app.route('/stop')
def stop():
    choose = str(request.args.get('choose',''))
    command = ''
    if choose == 'resin':
        #stop resin,please replace with absolute path
	command = 'sh httpd.sh stop'
    elif choose == 'tomcat':
        #stop tomcat,please replace with absolute path
	command = 'sh shutdown.sh'
    else:
	print 'no such type'
	return

    popen = subprocess.Popen(command,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True) 
        
    return ''

@app.route('/log')
def log():
    init = int(request.args.get('init',0))
    choose = str(request.args.get('choose',''))
    filename=''
    if choose == 'resin':
        #resin log
        filename = '/resin/log/stdout.log'
    elif choose == 'tomcat':
        #tomcat log
        filename = '/tomcat/logs/catalina.out'
    else:
        print 'no such type'
        return "" 
    return get_last_line(filename,init)

@app.route("/")
def index():
    return render_template('/index.html',name='wangxx')

def get_last_line(filepath,init):
        global already_print_num
        if not os.path.exists(filepath):
            print 'no such file %s' % filepath
            sys.exit()
            return

        if int(init) > 0:
            already_print_num = 0
        
        result=""
        readfile = open(filepath, 'r')
        lines = readfile.readlines()
        if len(lines) > 20 and already_print_num == 0:
                already_print_num = len(lines) - 20

        if already_print_num < len(lines):
            print_lines = lines[already_print_num - len(lines):]
            for line in print_lines:
                result = result + line + '<br>'

        already_print_num = len(lines)
        readfile.close()
        
        return result

if __name__ == "__main__":
    app.run(debug=True)

