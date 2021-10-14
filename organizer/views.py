from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth import authenticate
from django.shortcuts import redirect
import os
from pathlib import Path
import sqlite3
from datetime import datetime
import time


# ------------------------- file utility ------------------------------------------
# -- example: zvFileUtil("Help.txt", "r")
def zvFileUtil(file, action, data=None):
    _file = open(file, action)    
    _wrt = data
    if action == "w":
        _file.write(_wrt)
    if action == "a":
        _file.write(_wrt)
    if action == "r":
        _wrt = _file.read()
        return _wrt
    _file.close()
# ----------------------------------------------------------------------------------
# ------------------
# -- globals


# Build paths inside the project like this: BASE_DIR / 'subdir'.
zvBASE_DIR = Path(__file__).resolve().parent.parent
zvSvgDir = os.path.join(zvBASE_DIR, "files/svg/")
zvCssDir = os.path.join(zvBASE_DIR, "files/css/")
NL = '\n'
BR = '<br>'

zvRootUrl = "https://navercm.pythonanywhere.com"
try:
    zvRootUrl = zvFileUtil("mysite.cfg", "r")
    zvRootUrl = zvRootUrl.split('ROOT_URL="')[1].split('"')[0]
except:
    zvRootUrl = "https://navercm.pythonanywhere.com"
# --------------------------------------------------------------------------------------

# ========================== UTILS BEGIN ===============================================
# ----------------------- SQL Utils ------------------------------------------------
# -- update rec sql
def sql_udt(sql, zvar):
    # -- BosTagTer.db setup
    # UPDATE TG_TERRITORY
    # SET TERGJSON = ###
    # WHERE TERID = zvTerid
    zvSqlCon = sqlite3.connect(os.path.join(zvBASE_DIR, "db.sqlite3"))
    zvSql = zvSqlCon.cursor()
    _sql = sql
    _var = zvar
    zvSql.execute(_sql, _var)
    zvSqlCon.commit()
    zvSqlCon.close()

# -- delete rec sql
def sql_del(sql):
    # -- BosTagTer.db setup
    # "DELETE FROM TG_TERRITORY WHERE TERID = '"+ zvTerId +"'"
    zvSqlCon = sqlite3.connect(os.path.join(zvBASE_DIR, "db.sqlite3"))
    zvSql = zvSqlCon.cursor()
    _sql = sql
    zvSql.execute(_sql)
    zvSqlCon.commit()
    zvSqlCon.close()

# -- new rec sql
def sql_ins(sql, zvar):
    # -- BosTagTer.db setup
    # INSERT INTO TERRITORY(TERID,TERDESC,TERTYPE)
    # VALUES(?,?,?)
    zvSqlCon = sqlite3.connect(os.path.join(zvBASE_DIR, "db.sqlite3"))
    zvSql = zvSqlCon.cursor()
    _sql = sql
    _var = zvar
    zvSql.execute(_sql, _var)
    zvSqlCon.commit()
    _rtn = zvSql.lastrowid
    zvSqlCon.close()
    return _rtn

# -- return sql
def query(sql):
    # -- BosTagTer.db setup
    zvSqlCon = sqlite3.connect(os.path.join(zvBASE_DIR, "db.sqlite3"))
    zvSql = zvSqlCon.cursor()
    _sql = sql
    _rtn = zvSql.execute(_sql).fetchall()
    zvSqlCon.close()
    return _rtn

# ---------------------------- Format Utils ----------------------------------------
# -- load svg
def load_svg(svg):
    _svg = svg
    zvSvgFile = os.path.join(zvSvgDir, _svg)
    with open(zvSvgFile, 'r') as file:
        _data = file.read()
    return _data

# -- load css
def load_css(css):
    _css = css
    zvCssFile = os.path.join(zvCssDir, _css)
    with open(zvCssFile, 'r') as file:
        _data = file.read()
    return _data

# -- udt usr css
def udt_usr_css(usr):
    _usr = usr
    zvBgc = '#bbbcd0'
    zvFgc = '#293134'
    zvThc = '#8bc34a'
    zvTrc = '#eef7e3'
    #                      0            1          2            3
    zvUsrSql = "select USRPGFGCLR, USRPGBGCLR, USRTBHDCLR, USRTBRWCLR from auth_user where username = '"+ _usr +"'"
    zvUsrQry = query(zvUsrSql)
    for u in zvUsrQry:        
        zvFgc = str(u[0])
        zvBgc = str(u[1])
        zvThc = str(u[2])
        zvTrc = str(u[3])

    zvTmpCss = zvFileUtil(os.path.join(zvBASE_DIR, "files/css/template.css"), 'r')
    zvTmpCss = str(zvTmpCss)
    zvTmpCss = zvTmpCss.replace("###FGCOLOR###", zvFgc)
    zvTmpCss = zvTmpCss.replace("###BGCOLOR###", zvBgc)
    zvTmpCss = zvTmpCss.replace("###THCOLOR###", zvThc)
    zvTmpCss = zvTmpCss.replace("###TRCOLOR###", zvTrc)
    zvFileUtil(os.path.join(zvBASE_DIR, "files/css/"+ _usr +".css"), 'w', zvTmpCss)

# -- format phone number
def phone_format(n):
    _rtn = n
    _rtn = _rtn.replace(",","").replace("-","").replace(".","").replace("(","").replace(")","").replace(" ","")
    _rtn = int(_rtn)

    if (_rtn < 2010000000) or (_rtn > 9899999999):
        _rtn = "error"
    return _rtn

# ------------------ datetime stuff -----------------
# -- get current date time stamp
def date_time_now():
    _now = time.time() - 18000
    _now = int(_now)
    return _now

# -- date format
def date_format(dte):
    _dte = datetime.utcfromtimestamp(dte).strftime('%m/%d/%Y')
    return _dte

# -- time format
def time_format(tim):
    _tim = datetime.utcfromtimestamp(tim).strftime('%H:%M:%S')
    return _tim

# field format
def field_format(typ, ln='na'):
    _ln = ''
    _rtn = ''
    
    if ln != 'na':
        _ln = "{"+ ln +"}"
    else:
        _ln = ''

    if typ == 'zip':        
        _rtn = r'pattern="[0-9]{5}" title="Five digit zip code"'
        
    if typ == 'txt_only':
        if _ln != '':
            _rtn = 'pattern="[a-zA-Z]'+ _ln +'" title="text only"'
        else:
            _rtn = 'pattern="^[a-zA-Z]+$" title="text only"'
    if typ == 'txt_s_only':
        if _ln != '':
            _rtn = r'pattern="[a-zA-Z\s]'+ _ln +'" title="text and space only"'
        else:
            _rtn = r'pattern="^[a-zA-Z\s]+$" title="text only"'
    if typ == 'upper_txt_only':
        if _ln != '':
            _rtn = 'pattern="[A-Z]'+ _ln +'" title="uppercase text only"'
        else:
            _rtn = 'pattern="^[A-Z]+$" title="uppercase text only"'
    if typ == 'num_only':
        if _ln != '':
            _rtn = 'pattern="[0-9]'+ _ln +'" title="number only"'
        else:
            _rtn = 'pattern="^[0-9]+$" title="number only"'
    if typ == 'txt_num_only':
        if _ln != '':
            _rtn = 'pattern="[a-zA-Z0-9]'+ _ln +'" title="text & number only"'
        else:
            _rtn = 'pattern="^[a-zA-Z0-9]+$" title="text & number only"'
    if typ == 'txt_num_s_only':
        if _ln != '':
            _rtn = r'pattern="[a-zA-Z0-9\s]'+ _ln +'" title="text, number & space only"'
        else:
            _rtn = r'pattern="^[a-zA-Z0-9\s]+$" title="text & number only"'
    if typ == 'readonly':
        _rtn = 'readonly'
    if typ == 'disabled':
        _rtn = 'disabled'

    return _rtn
# ----------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------

# ========================== VIEWS BEGIN ===============================================
# /\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/|
# =================== MAIN BEGIN =====================================
# --------------- LOGIN -----------------
def login(request):

    # -- security
    
    template = loader.get_template('organizer/login.html')
    context = {}

    return HttpResponse(template.render(context, request))


# ---- HOMEPAGE -----------------
def index(request):

    # -- security
    zvCurUsr = str(request.user)

    if zvCurUsr == 'AnonymousUser':
        return redirect('organizer:login')

    else:

        zvCurUsr = str(zvCurUsr)
        zvUsrClr = query("Select USRPGFGCLR, USRPGBGCLR From auth_user Where username = '"+ zvCurUsr +"'")
        for c in zvUsrClr:
            zvBgc = str(c[1])
            zvFgc = str(c[0])
        # zvUsrSecLst = query("Select USRSEC From auth_user Where username = '"+ zvCurUsr +"'")
        zvCurUsrNam = query("select first_name||' '||last_name from auth_user where username = '"+ zvCurUsr +"'")
        zvCurUsrNam = str(zvCurUsrNam)
        zvCurUsrNam = zvCurUsrNam.split("'")[1]
        zvCurUsrNam = zvCurUsrNam.split("'")[0]

        zvHeader = "Welcome " + zvCurUsrNam
        # /home/CodeProjects/mysite/organizer/templates/organizer/index.html
        # /home/CodeProjects/mysite/organizer/templates/organizer/index.html
        template = loader.get_template(os.path.join(zvBASE_DIR,'organizer/templates/organizer/index.html'))

        zvItemList = []
        zvItemList.append('<a href="'+ zvRootUrl +'">'+ load_svg('house.svg') +'</a>')
        

        zvBody = '''
            <p>Mabuhay! . . .</p>
            <p>This can be used to organize and work territory.</p>
            <p>Other useful tools will be found here.</p>
            <p>Reports can be viewed here too.</p>
            <p>Maraming salamat!</p>
            '''
        try:
            zvCss = load_css(zvCurUsr +'.css')
        except:
            zvCss = load_css('default.css')

        context = {
            'zvCss': zvCss,
            'zvBgc': zvBgc,
            'zvFgc': zvFgc,
            'zvHeader': zvHeader,
            'zvFavicon': load_svg('events.svg'),
            'zvCurPage': "Home",
            'zvRootUrl':zvRootUrl,
            'zvItemList':zvItemList,
            'zvBody':zvBody
            }

    return HttpResponse(template.render(context, request))
# -------------------------------------------------------------