from flask import Flask, render_template, request, session, redirect, jsonify
from flask_session import Session
from tempfile import mkdtemp
import sqlite3 as SQL
import threading as thr
from control.login_required import login_required, check_password_hash, generate_password_hash #gera e checa o hash de senha de usuario
import os.path
from control.control_units import validation_login, repeat_password, validation # verificação de entrada de dados corretos no cadastro e login

app = Flask(__name__)

app.config["TEMPLATES_AUTO_RELOAD"] = True

# -----------------------------------------------------------|
BASE_DIR = os.path.dirname(os.path.abspath(__file__))        #| conexao com os db de usuario
db_dir = (BASE_DIR + "\\login_user.db")                      #| Resolve o problema de pasta do DB                               
db_conn = SQL.connect(db_dir, check_same_thread=False)       #| conexão com banco de dado
cursor_DB = db_conn.cursor()                                 #/
                                                             #/ 
BASE_DIR_UNITS = os.path.dirname(os.path.abspath(__file__))  #/
db_units = (BASE_DIR_UNITS + "\\units.db")                   #/conexão com db de unidade
units_conn = SQL.connect(db_units, check_same_thread=False)  #/
cursor_units = units_conn.cursor()                           #/
#------------------------------------------------------------|

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# globals
data_API = [] # vai receber os dados para ser usado na API
data_thread_units = [] # contem os dados do banco de dados para ser usado
cursor_units.execute("SELECT * FROM units") 
total_unit_and_data = cursor_units.fetchall()
data_for_ping = []

# end globals

#WEB PAGE BLOCK
#------------------------------------
@app.route("/")
@login_required
def index(): 
    return render_template("index.html")

@app.route("/administration", methods=["GET", "POST"])
@login_required
def adm():
    return render_template("administration.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear() #limpa sessão)
    if request.method == "POST":
        message = validation_login(request.form.get('username'), request.form.get('password'))
        if message is not None:
            return render_template('login.html', message1=message)
        
        cursor_DB.execute("SELECT * FROM users WHERE username = ?", [request.form.get('username')])
        data_user = (cursor_DB.fetchall())

        if len(data_user) == 0:
            return render_template('login.html', message1='Usuário inexistente.')
        if len(data_user) != 1 or not check_password_hash(data_user[0][2], request.form.get('password')):
            return render_template('login.html', message1='Usuario ou senha invalidos.')
        session['user_id'] = data_user[0]
        return redirect("/")
    else:
        return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        message = validation_login(request.form.get('username'), request.form.get('password'))
        if message is not None:
            return render_template('register.html', message1=message)
        message = repeat_password(request.form.get('password'), request.form.get('repeat_password'))
        if message is not None:
            return render_template('register.html', message1=message)
      
        cursor_DB.execute("SELECT * FROM users WHERE username = ?", [request.form.get('username')])
        data_user = cursor_DB.fetchall() 
        
        if len(data_user) == 0 or request.form.get('username') not in data_user[0]:
            cursor_DB.execute("""INSERT INTO users (username, hash) VALUES (?,?)""", (request.form.get("username"), generate_password_hash(request.form.get("password"))))
            db_conn.commit()
            cursor_DB.execute("SELECT * FROM users WHERE username = ?", [request.form.get('username')])
            data_user = cursor_DB.fetchall()
            session['user_id'] = data_user[0]
            return redirect("/")
        else:
            return render_template('register.html', message1="Este usuário ja exite!")

    return render_template("register.html")
@app.route("/logout", methods=["GET", "POST"])
def logout():
    session.clear()
    return redirect("/")
#WEB PAGE END LOCK
#-------------------------------------------------
#-------------------
# block of units

@app.route("/H24", methods=["GET", "POST"])
@login_required
def H24(): # unit_tip (1)
    nameUnit = request.form.get('name_unit'); other_name = request.form.get('other_name'); address = request.form.get('address'); district = request.form.get('district'); director = request.form.get('director'); provider = request.form.get('provider'); loc = request.form.get('loc'); ip = request.form.get('ip'); acronym = request.form.get('acronym')
    if request.method == "POST":
        value = validation(nameUnit, other_name, address, district, director, loc, ip, acronym)
        if value is not None:
            return render_template('adm_24h.html', unit_tip='24h', message1=value)
        
        cursor_units.execute("SELECT * FROM units WHERE name = ?", [request.form.get('name_unit')])
        data_unit = cursor_units.fetchall()
        if len(data_unit) == 0 or request.form.get('name_unit') not in data_unit[0]:
            cursor_units.execute("""INSERT INTO units (name, nick, address, unit_tip, district, leader, provider, loc, ip, acronym) VALUES (?,?,?,?,?,?,?,?,?,?)""", (nameUnit, other_name, address, 1, district, director, provider, loc, ip, acronym))
            units_conn.commit()
        else:
            return render_template("adm_24h.html", unit_tip="24H", message1="Esta unidade 24H já esta cadastrada")
        
        cursor_units.execute("SELECT * FROM units WHERE unit_tip=1;"); UNIT_PAGE = cursor_units.fetchall()
        return render_template('adm_24h.html', unit_tip="24H", units_page=UNIT_PAGE)
    cursor_units.execute("SELECT * FROM units WHERE unit_tip=1;"); UNIT_PAGE = cursor_units.fetchall()
    return render_template('adm_24h.html', unit_tip="24H", units_page=UNIT_PAGE)

@app.route("/CEO", methods=["GET", "POST"])
@login_required
def CEO(): #unit_tip (2) 
    nameUnit = request.form.get('name_unit'); other_name = request.form.get('other_name'); address = request.form.get('address'); district = request.form.get('district'); director = request.form.get('director'); provider = request.form.get('provider'); loc = request.form.get('loc'); ip = request.form.get('ip'); acronym = request.form.get('acronym')
    if request.method == "POST":
        value = validation(nameUnit, other_name, address, district, director, loc, ip, acronym)
        if value is not None:
            return render_template('adm_CEO.html', unit_tip='CEO', message1=value)
    
        cursor_units.execute("SELECT * FROM units WHERE name=?", [request.form.get('name_unit')])
        data_unit = cursor_units.fetchall()
        UNIT_PAGE = data_unit
        if len(data_unit) == 0 or request.form.get('name_unit') not in data_unit[0]:
            cursor_units.execute("""INSERT INTO units (name, nick, address, unit_tip, district, leader, provider, loc, ip, acronym) VALUES (?,?,?,?,?,?,?,?,?,?)""", (nameUnit, other_name, address, 2, district, director, provider, loc, ip, acronym.upper()))
            units_conn.commit()
        else:
            return render_template("adm_CEO.html", unit_tip="CEO", message1="Esta unidade de CEO já esta cadastrada")

        cursor_units.execute("SELECT * FROM units WHERE unit_tip=2;"); UNIT_PAGE = cursor_units.fetchall()
        return render_template('adm_CEO.html', unit_tip="CEO", units_page=UNIT_PAGE)
    cursor_units.execute("SELECT * FROM units WHERE unit_tip=2;"); UNIT_PAGE = cursor_units.fetchall()
    return render_template('adm_CEO.html', unit_tip="CEO", units_page=UNIT_PAGE)

@app.route("/USF", methods=["GET", "POST"])
@login_required
def USF(): # unit_tip (3)
    nameUnit = request.form.get('name_unit'); other_name = request.form.get('other_name'); address = request.form.get('address'); district = request.form.get('district'); director = request.form.get('director'); provider = request.form.get('provider'); loc = request.form.get('loc'); ip = request.form.get('ip'); acronym = request.form.get('acronym')
    if request.method == "POST":
        value = validation(nameUnit, other_name, address, district, director, loc, ip, acronym)
        if value is not None:
            return render_template('adm_USF.html', unit_tip='USF', message1=value)
    
        cursor_units.execute("SELECT * FROM units WHERE name=?", [request.form.get('name_unit')])
        data_unit = cursor_units.fetchall()
        UNIT_PAGE = data_unit
        if len(data_unit) == 0 or request.form.get('name_unit') not in data_unit[0]:
            cursor_units.execute("""INSERT INTO units (name, nick, address, unit_tip, district, leader, provider, loc, ip, acronym) VALUES (?,?,?,?,?,?,?,?,?,?)""", (nameUnit, other_name, address, 3, district, director, provider, loc, ip, acronym.upper()))
            units_conn.commit()
        else:
            return render_template("adm_USF.html", unit_tip="USF", message1="Esta unidade de USF já esta cadastrada")

        cursor_units.execute("SELECT * FROM units WHERE unit_tip=3;"); UNIT_PAGE = cursor_units.fetchall()
        return render_template('adm_USF.html', unit_tip="USF", units_page=UNIT_PAGE)
    cursor_units.execute("SELECT * FROM units WHERE unit_tip=3;"); UNIT_PAGE = cursor_units.fetchall()
    return render_template('adm_USF.html', unit_tip="USF", units_page=UNIT_PAGE)

@app.route("/FISIO", methods=["GET", "POST"])
@login_required
def FISIO(): #unit_tip (4)
    nameUnit = request.form.get('name_unit'); other_name = request.form.get('other_name'); address = request.form.get('address'); district = request.form.get('district'); director = request.form.get('director'); provider = request.form.get('provider'); loc = request.form.get('loc'); ip = request.form.get('ip'); acronym = request.form.get('acronym')
    if request.method == "POST":
        value = validation(nameUnit, other_name, address, district, director, loc, ip, acronym)
        if value is not None:
            return render_template('adm_FISIO.html', unit_tip="FISIOTERAPIA", message1=value)
    
        cursor_units.execute("SELECT * FROM units WHERE name=?", [request.form.get('name_unit')])
        data_unit = cursor_units.fetchall()
        UNIT_PAGE = data_unit
        if len(data_unit) == 0 or request.form.get('name_unit') not in data_unit[0]:
            cursor_units.execute("""INSERT INTO units (name, nick, address, unit_tip, district, leader, provider, loc, ip, acronym) VALUES (?,?,?,?,?,?,?,?,?,?)""", (nameUnit, other_name, address, 4, district, director, provider, loc, ip, acronym.upper()))
            units_conn.commit()
        else:
            return render_template("adm_FISIO.html", unit_tip="FISIOTERAPIA", message1="Esta unidade de Fisioterapia já esta cadastrada")

        cursor_units.execute("SELECT * FROM units WHERE unit_tip=4;"); UNIT_PAGE = cursor_units.fetchall()
        return render_template('adm_FISIO.html', unit_tip="FISIOTERAPIA", units_page=UNIT_PAGE)
    cursor_units.execute("SELECT * FROM units WHERE unit_tip=4;"); UNIT_PAGE = cursor_units.fetchall()
    return render_template('adm_FISIO.html', unit_tip="FISIOTERAPIA", units_page=UNIT_PAGE)

@app.route("/OTHERS", methods=["GET", "POST"])
@login_required
def OTHERS(): #unit_tip(5)
    nameUnit = request.form.get('name_unit'); other_name = request.form.get('other_name'); address = request.form.get('address'); district = request.form.get('district'); director = request.form.get('director'); provider = request.form.get('provider'); loc = request.form.get('loc'); ip = request.form.get('ip'); acronym = request.form.get('acronym')
    if request.method == "POST":
        value = validation(nameUnit, other_name, address, district, director, loc, ip, acronym)
        if value is not None:
            return render_template('adm_OTHERS.html', unit_tip=" ", message1=value)
    
        cursor_units.execute("SELECT * FROM units WHERE name = ?", [request.form.get('name_unit')])
        data_unit = cursor_units.fetchall()
        UNIT_PAGE = data_unit
        if len(data_unit) == 0 or request.form.get('name_unit') not in data_unit[0]:
            cursor_units.execute("""INSERT INTO units (name, nick, address, unit_tip, district, leader, provider, loc, ip, acronym) VALUES (?,?,?,?,?,?,?,?,?,?)""", (nameUnit, other_name, address, 5, district, director, provider, loc, ip, acronym.upper()))
            units_conn.commit()
        else:
            return render_template("adm_OTHERS.html", unit_tip=" ", message1="Esta unidade já esta cadastrada")

        cursor_units.execute("SELECT * FROM units WHERE unit_tip=5;"); UNIT_PAGE = cursor_units.fetchall()
        return render_template('adm_OTHERS.html', unit_tip=" ", units_page=UNIT_PAGE)
    cursor_units.execute("SELECT * FROM units WHERE unit_tip=5;"); UNIT_PAGE = cursor_units.fetchall()
    return render_template('adm_OTHERS.html', unit_tip=" ", units_page=UNIT_PAGE)

# end block of units
#-------------------

#-------------------
#block of API 

@app.route('/ping/db_status', methods=['GET'])
def func():
    cursor_units.execute(f"SELECT * FROM status;")
    data_API = cursor_units.fetchall()
    
    """
    with open(f'{path}/api.csv', 'r') as data_API:
        current_list = csv.reader(data_API)
        for row in current_list:
            if row == []:
                continue
            else:
                data_API = row
                temp_data_API = []
                for item in data_API:
                    temp = item.split('"')
                    temp_data_API.append(temp)
                data_API = temp_data_API      """
    
    return jsonify(data_API)
#end block os API
#-------------------

@app.before_first_request
def server_ping():
    from ping.thread import system_ping
    global data_thread_units
    data_thread_units = thr.Thread(target=system_ping) #cria um multiprocessamento separado e mantem em funcionamento
    data_thread_units.start()
    
if __name__ == '__main__': 
    app.run(port=8085, host='0.0.0.0') # Executa a aplicação na porta 8085, vc poderá mudar tb para outro valor dentro o espectro permitido.
     