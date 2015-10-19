# VMailMgr chpw CGI

This is a Python CGI script that lets virtual `VMailMgr`/`qmail` users change
their own mail passwords via a web interface.

This script is specifically tailored to work on hosts at
[uberspace.de](https://uberspace.de). But it may also work on other qmail-based
systems as long as virtual mail users are managed via `VMailMgr`.

## Installation
In order to make this script executable, you need to install `python-cdb` as
it is a required dependency:

    easy_install-2.7 python-cdb

After that, simply extract all the repository contents into a folder under
your document root. No paths need to be configured. Only make sure that the
location is reachable via HTTPS.

## Acknowledgements
This is a majorly refined version of a script originally developed by Dirk Boye.
See [dirkboye/mailpw_change](https://github.com/dirkboye/mailpw_change) at GitHub
for the original source code.

## FAQ
* *Q:* Why still Python 2.7?<br>
  *A:* We need `python-cdb` to parse the weird binary password database.
  Unfortunately, `python-cdb` seems to be only available for Python 2.

* *Q:* Can I use the script via unencrypted HTTP?<br>
  *A:* No, HTTPS is hard-coded. So unless you change that in the code, you can't.
  And honestly, you really shouldn't.

* *Q:* Do I need to put the script in `/cgi-bin/`?<br>
  *A:* In most cases, no. The script comes with an `.htaccess` that enables CGI
  execution for the current directory. Generally, that should work. If not, your
  administrator may have disabled option overriding in which case you actually
  need to put it in `/cgi-bin/`. But in most cases (and especially on Uberspaces)
  it should work just fine.

* *Q:* I only get an error 500 and the log file says something about suEXEC
  policy violation. How do I fix that?<br>
  *A:* Make sure both the `index.py` as well as the containing directory have
  the permissions `0755`. Any higher permissions will usually result in that error.
