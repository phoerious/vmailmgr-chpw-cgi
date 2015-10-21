#!/usr/bin/env python3
import cgi, cgitb
import re
import sys, os, subprocess
from subprocess import check_output, Popen, PIPE, CalledProcessError
from os.path import expanduser

cgitb.enable()
home_dir = expanduser("~")
os.environ['HOME'] = home_dir

def check_form(formvars, form):
    for varname in formvars:
        if varname not in form.keys():
            return False
        else:
            if type(form[varname].value) is not type(''):
                return None
    return True

def read_template_file(filename, **vars):
    with open('tpl/' + filename, mode='r', encoding='utf-8') as f:
        template = f.read()
    for key in vars:
        template = template.replace('{$' + key + '}', vars[key])
    return template

def check_oldpw(accountname, oldpass):
    try:
        dumpvuserargs = ['dumpvuser', accountname]
        userdump = check_output(dumpvuserargs).strip().decode('utf-8')
        m = re.search('Encrypted-Password: (\$([^\$]+)\$([^\$]+)\$([^\$\n]+))', userdump)
        if None == m:
            return False
        oldhash = m.group(1)
        hashtype = m.group(2)
        salt = m.group(3)
    except CalledProcessError as e:
        print(e)
        return False

    opensslargs = ['openssl', 'passwd', '-' + hashtype, '-salt', salt, oldpass]
    newhash = check_output(opensslargs).strip().decode('utf-8');

    if newhash == oldhash:
        return True
    return False

def generate_headers():
    return "Content-Type: text/html; charset=utf-8\n"

def main():
    main_content = ''

    form = cgi.FieldStorage()
    if 'submit' in form.keys():
        formvars = ['accountname', 'oldpass', 'newpass', 'newpass2']
        form_ok = check_form(formvars, form)
        if form_ok == True:
            accountname = form['accountname'].value
            accountname = accountname.split("@")[0]
            oldpass = form['oldpass'].value
            newpass = form['newpass'].value
            newpass2 = form['newpass2'].value
            if newpass == newpass2:
                if check_oldpw(accountname, oldpass):
                    vpasswdargs = ['vpasswd', accountname]
                    p = Popen(vpasswdargs, stdin=PIPE, stdout=PIPE, stderr=subprocess.STDOUT)   
                    p.stdin.write(newpass.encode('utf-8') + b'\n')
                    p.stdin.write(newpass2.encode('utf-8') + b'\n')
                    p.stdin.close()
                    if p.wait() == 0:
                        # We did it
                        main_content = read_template_file('success.tpl')
                    else:
                        main_content = read_template_file('fail.tpl', message=cgi.escape(p.stdout.read()))
                else:
                    main_content = read_template_file('fail.tpl', message='User not found or wrong password entered.')
            else:
                main_content = read_template_file('fail.tpl', message='Passwords to not match.')
        elif form_ok == False:
            main_content = read_template_file('fail.tpl', message='All fields are required.')
        else:
            main_content = read_template_file('fail.tpl', message='Invalid data type supplied.')
    else:
        # Submit button not pressed, show form
        formaction = cgi.escape("https://" + os.environ["HTTP_HOST"] + os.environ["REQUEST_URI"])
        form = read_template_file('form.tpl', formaction=formaction)
        main_content = form

    response = generate_headers() + "\n"
    response += read_template_file('main.tpl', main_content=main_content)
    sys.stdout.buffer.write(response.encode('utf-8'))

if __name__ == "__main__":
    main()

