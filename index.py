#!/usr/bin/env python2.7
import cgi
import cgitb
import pwd, sys, os, cdb, subprocess
from subprocess import check_output, Popen, PIPE
from os.path import expanduser

cgitb.enable()
home_dir = expanduser("~")

def check_form(formvars, form):
    for varname in formvars:
        if varname not in form.keys():
            return False
        else:
            if type(form[varname].value) is not type(''):
                return None
    return True

def read_template_file(filename, **vars):
    with open('tpl/' + filename, 'r') as f:
        template = f.read()
    for key in vars:
        template = template.replace('{$' + key + '}', vars[key])
    return template

def check_oldpw(accountname, oldpass):
    passwd_dbfile = os.path.abspath(home_dir + "/passwd.cdb");
    try:
        db = cdb.init(passwd_dbfile)
    except:
        return 'No user database found.'
    try:
        cdb_user_data=db[accountname]
    except:
        return 'User not found or password incorrect.'
    passhash = cdb_user_data[6:40]
    # Hash algorithm is given between first two $ of passhash (here only md5 based BSD password is used)
    hashtype = '1'
    # Salt is given between next two $
    salt = passhash[3:11]
    opensslargs = ['openssl', 'passwd', '-' + hashtype, '-salt', salt, oldpass];
    newhash = check_output(opensslargs).strip();
    if newhash == passhash:
        return ''
    return 'User not found or password incorrect.'

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
                if check_oldpw(accountname, oldpass) == '':
                    vpasswdargs = ['vpasswd', accountname]
                    # Environmental variable HOME is needed for vpasswd to work
                    os.environ['HOME'] = home_dir   
                    p = Popen(vpasswdargs, stdin=PIPE, stdout=PIPE, stderr=subprocess.STDOUT)   
                    p.stdin.write(newpass + '\n')
                    p.stdin.write(newpass2 + '\n')
                    p.stdin.close()
                    if p.wait() == 0:
                        # We did it
                        main_content = read_template_file('success.tpl')
                    else:
                        main_content = read_template_file('fail.tpl', message=cgi.escape(p.stdout.read()))
                else:
                    main_content = read_template_file('fail.tpl', message=cgi.escape( check_oldpw(accountname, oldpass)))
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
    print(response)

if __name__ == "__main__":
    main()

