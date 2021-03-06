import re
import flask
from flask import Flask, render_template, request, session
from flask_bootstrap import Bootstrap
import os
from datetime import datetime, date, time, timedelta
from flask_mail import Mail
from flask_mail import Message
from random import randint, uniform,random,randrange,choice
import random
import string
from flask import flash
from mysql.connector import MySQLConnection, Error
from python_mysql_dbconfig import read_db_config

canchasprserrezuela=[1,2,3,4,7,8]
canchasclserrezuela=[9,10,11,12,13,14,15,16,17,18]

def existeUsuarios(co): #revisa la base de datos para saber si el usuario existe, devueve si ó n0
    query=" SELECT nombre FROM usuarios WHERE correo = %s "
    dbconfig = read_db_config()
    try:
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        cursor.execute(query, (co,))
        row=cursor.fetchone()
        if row is not None:
            encontrado='si'
        else:
            encontrado='no'
    except Error as error:
        print(error)
    finally:
        cursor.close()
        conn.close()
    return encontrado
def datotalUsuarios(co,tal): #recupera un dato (tal) de la base de usuairios del ucuairo (correo)
    dbconfig = read_db_config()
    q1="SELECT "
    q2=" FROM usuarios WHERE correo = %s"
    query=q1+tal+q2
    data=(tal,co)
    try:
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        cursor.execute(query,(co,))
        try:
            row=cursor.fetchone()
            dato=row[0]
        except:
            dato='errror'
    except Error as error:
        dato='errror'
    finally:
        cursor.close()
        conn.close()
    return dato
def crearUsuario(co,no,ap,cn,id,cl,ac,cf,ind,fr,ty): #Escribe un usuairo nuevo en la base de datos usuarios
    dbconfig = read_db_config()
    q1="INSERT INTO usuarios (correo,nombre,apellido,contrasena,telefono,club,aval_club,codigo_fed,indice,fecha_registro,tipo) VALUES ("
    q2=")"
    query=q1+"%s"+","+"%s"+","+"%s"+","+"%s"+","+"%s"+","+"%s"+","+"%s"+","+"%s"+","+"%s"+","+"%s"+","+"%s"+q2
    print(query)
    data=(co,no,ap,cn,id,cl,ac,cf,ind,fr,ty)
    try:
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        cursor.execute(query,data)
        print(co)
        if cursor.lastrowid:
            print('last insert id', cursor.lastrowid)
        else:
            print('last insert id not found')
        conn.commit()
    except Error as error:
        dato='errror'
    finally:
        cursor.close()
        conn.close()
def cambiodatoUsauarios(co,dato,valor): #cambia el valor de un dato de la base de datos entrando por correo
    dbconfig = read_db_config()
    q1="UPDATE usuarios SET "
    q2= " = %s WHERE "
    q3=" = %s"
    query=q1+dato+q2+"correo"+q3
    data=(valor,co)
    try:
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        cursor.execute(query,data)
        conn.commit()
    except Error as error:
        dato='errror'
    finally:
        cursor.close()
        conn.close()
def todosdatosUsuarios(co): #Devuelve una lista de los datos del ususario co
    dbconfig = read_db_config()
    query="SELECT * FROM usuarios WHERE correo = %s"
    datusuario=[]
    try:
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        cursor.execute(query,(co,))
        try:
            row=cursor.fetchone()
            datusuario=row
        except:
            dato='errror'
    except Error as error:
        print(error)
        dato='errror'
    finally:
        cursor.close()
        conn.close()
    return datusuario
def sinavalUsuarios(cl):#Devuelve una lista con los datos de los jugadores que tinen en aval_club = NO
    dbconfig = read_db_config()
    query="SELECT * FROM usuarios WHERE club = %s AND aval_club='NO'"
    sinaval=[]
    try:
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        cursor.execute(query,(cl,))
        try:
            row=cursor.fetchone()
            while row is not None:
                sinaval.append(row)
                print(row)
                row = cursor.fetchone()
        except:
            dato='errror'
    except Error as error:
        print(error)
        dato='errror'
    finally:
        cursor.close()
        conn.close()
    return sinaval

def creaAgendaGolf(clu,cam,fec,turnos,fm,tac,numjug):
    dbconfig = read_db_config()
    q1="INSERT INTO agenda_golf (club,campo,fecha,frecuencia,tac,turnostotal,hora,turno,ju1,ju2,ju3,ju4,vacios,crea) VAlUES ("
    q2=")"
    query=q1+"%s"+","+"%s"+","+"%s"+","+"%s"+","+"%s"+","+"%s"+","+"%s"+","+"%s"+","+"%s"+","+"%s"+","+"%s"+","+"%s"+","+"%s"+","+"%s"+q2
    try:
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        tt=len(turnos)
        tur=0
        numjug=int(numjug)
        jugs=[]
        bloquear= 4 - numjug
        for i in range (bloquear):
            jugs.append('club@club.com')
        for i in range(bloquear,4):
            jugs.append('vacio')
        ju1=jugs[0]
        ju2=jugs[1]
        ju3=jugs[2]
        ju4=jugs[3]
        for i in range(tt):
            hor=turnos[i]
            tur=tur+1
            vac=numjug
            hoy=date.today()
            hoy=str(hoy)
            user=flask.session["username"]
            crea=hoy+'&/&'+user #en posición 9 se almacena: (fecha actua/usuario:creacion desde cero)
            data=(clu,cam,fec,fm,tac,tt,hor,tur,ju1,ju2,ju3,ju4,vac,crea)
            cursor.execute(query,data)
            conn.commit()
    except Error as error:
        dato='errror'
    finally:
        cursor.close()
        conn.close()
def existeAgendaGolf(clu,cam,fec):
    query=" SELECT hora FROM agenda_golf WHERE club = %s AND campo = %s AND fecha = %s AND turno=1"
    data=(clu,cam,fec)
    dbconfig = read_db_config()
    try:
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        cursor.execute(query,data)
        row=cursor.fetchone()
        if row is not None:
            encontrado='si'
            row=cursor.fetchone()
        else:
            encontrado='no'
    except Error as error:
        print(error)
    finally:
        cursor.close()
        conn.close()
    return encontrado
def recuperaAgendaGolf(clu,cam,fec):
    query=" SELECT * FROM agenda_golf WHERE club = %s AND campo = %s AND fecha = %s "
    data=(clu,cam,fec)
    dbconfig = read_db_config()
    try:
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        cursor.execute(query,data)
        progclubcampo=cursor.fetchall()
    except Error as error:
        print(error)
    finally:
        cursor.close()
        conn.close()
    return progclubcampo
def recuperaturnoAgendaGolf(clu,cam,fec,tur):
    lineaturno=[]
    query=" SELECT * FROM agenda_golf WHERE club = %s AND campo = %s AND fecha = %s AND turno = %s "
    data=(clu,cam,fec,tur)
    dbconfig = read_db_config()
    try:
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        cursor.execute(query,data)
        lineaturno=cursor.fetchone()
    except Error as error:
        print(error)
    finally:
        cursor.close()
        conn.close()
    return lineaturno
def cambiadatotalAgendaGolf(clu,cam,fec,tur,dato,valor):
    dbconfig = read_db_config()
    q1="UPDATE agenda_golf SET "
    q2= " = %s WHERE club = %s AND campo=%s AND fecha=%s AND turno=%s"
    query=q1+dato+q2
    data=(valor,clu,cam,fec,tur)
    try:
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        cursor.execute(query,data)
        conn.commit()
    except Error as error:
        dato='errror'
    finally:
        cursor.close()
        conn.close()
def turnosjuadorAgendaGolf(usuario,fec):
    turnosjugador=[]
    query=" SELECT * FROM agenda_golf WHERE fecha = %s "
    data=(fec)
    dbconfig = read_db_config()
    try:
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        cursor.execute(query,(data,))
        row=cursor.fetchone()
        while row is not None:
            for i in range(8,12):
                if row[i]==usuario:
                    turnosjugador.append(row)
            row = cursor.fetchone()
    except Error as error:
        print(error)
    finally:
        cursor.close()
        conn.close()
    return turnosjugador

def creaTarjetasGolf(tarjeta):
    dbconfig = read_db_config()
    q1="INSERT INTO tarjetas_golf (fecha, hora, jugador, marcador, campo, h01, h02, h03, h04, h05, h06, h07, h08, h09, ida, h10, h11, h12 ,h13 ,h14 ,h15 ,h16 ,h17 ,h18 ,vuelta ,total ,firma_jugador) VALUES ("
    q2="%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    query=q1+q2
    try:
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        cursor.execute(query,tarjeta)
        conn.commit()
    except Error as error:
        dato='errror'
    finally:
        cursor.close()
        conn.close()
def existeTarjetasGolf(fec,hora,co):
    query=" SELECT campo FROM tarjetas_golf WHERE fecha = %s AND hora = %s AND jugador = %s "
    data=(fec,hora,co)
    dbconfig = read_db_config()
    try:
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        cursor.execute(query,data)
        row=cursor.fetchone()

        if row is not None:
            encontrado='si'
            row=cursor.fetchone()
        else:
            encontrado='no'
    except Error as error:
        print(error)
    finally:
        cursor.close()
        conn.close()
    return encontrado
def marcadorTarjetasGolf(mc):
    query="SELECT * FROM tarjetas_golf WHERE marcador = %s and fecha= %s"
    dbconfig = read_db_config()
    asignadomarcador='no'
    tars=[]
    fec=date.today()
    fec=str(fec)
    data=(mc,fec)
    try:
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        cursor.execute(query,data)
        row=cursor.fetchone()
        while row is not None:
            asignadomarcador='si'
            tars.append(row)
            row=cursor.fetchone()
    except Error as error:
        print(error)
    finally:
        cursor.close()
        conn.close()
    respuesta=[asignadomarcador,tars]
    return respuesta
def cambiadatotalTarjetaGolf(fec,hora,co,dato,valor):
    dbconfig = read_db_config()
    q1="UPDATE tarjetas_golf SET "
    q2= " = %s WHERE fecha = %s AND hora=%s AND jugador=%s "
    query=q1+dato+q2
    data=(valor,fec,hora,co)
    try:
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        cursor.execute(query,data)
        conn.commit()
    except Error as error:
        dato='errror'
    finally:
        cursor.close()
        conn.close()
def recuperaTarjetasGolf(fec,cam):
    tarjetas=[]
    query=" SELECT * FROM tarjetas_golf WHERE fecha= %s AND campo = %s "
    data=(fec,cam)
    dbconfig = read_db_config()
    try:
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        cursor.execute(query,data)
        tarjetas=cursor.fetchall()
    except Error as error:
        print(error)
    finally:
        cursor.close()
        conn.close()
    return tarjetas

class Campos:
    def __init__(self):
        self.lista=[]
    def iniciarCampos(self):
        archivo=open('campos','a')
        archivo.close()
    def leerCampos(self):
        archivo=open('campos', 'r')
        linea=archivo.readline()
        if linea:
            while linea:
                if linea[-1] =='\n':
                    linea = linea[:-1]
                self.lista.append(linea)
                linea=archivo.readline()
        archivo.close()
    def buscarCampos(self,campo):
        for elemento in self.lista:
            arreglo=elemento.split('$*!$')
            if campo == arreglo[0]:
                listacampos=arreglo
                return listacampos
    def devolverCampos(self):  #genera una lista de cmapos
        listacampos=[]
        for elemento in self.lista:
            arreglo=elemento.split('$*!$')
            listacampos.append(arreglo[0])
        return listacampos

class Agenda:
    def __init__(self):
        self.lista=[]
    def iniciarAgenda(self):
        archivo=open('agenda_juego','a')
        archivo.close()
    def leerAgenda(self):
        archivo=open('agenda_juego','r')
        linea=archivo.readline()
        if linea:
            while linea:
                if linea[-1] == '\n':
                    linea = linea[:-1]
                self.lista.append(linea)
                linea=archivo.readline()
    def escribirAgenda(self): # se usa pra adicionar la agenda del archivo provisional en el programa al archivo agenda_Juego en la base de dtos
        archivo=open('agenda_juego','a')
        for elemento in self.lista:
            archivo.write(elemento+"\n")
        archivo.close()
    def grabarturnoAgenda(self): # se usa pra escribir la agenda una vez se ha incluido el turno escogido por el jugador
        archivo=open('agenda_juego','w')
        for elemento in self.lista:
            archivo.write(elemento+"\n")
        archivo.close()
    def adicioncampoAgenda(self,clu,cam,fec,turnos,hi,mi,fm,hf,mf,tac,tt,numjug): #crea la agenda en el archivo provisional
        turnostotal=len(turnos)
        tur=0
        numjug=int(numjug)
        jugs=[]
        bloquear= 4 - numjug
        for i in range (bloquear):
            jugs.append('club@club.com')
        for i in range(bloquear,4):
            jugs.append('vacio')
        ju1=jugs[0]
        ju2=jugs[1]
        ju3=jugs[2]
        ju4=jugs[3]
        pos0=clu+'&/&'+cam+'&/&'+fec #en la posición 0 de la fila se almacena el club, el campo y la fecha con separador '&/&'
        hi=str(hi)
        mi=str(mi)
        fm=str(fm)
        hf=str(hf)
        mf=str(mf)
        tac=str(tac)
        tt=str(tt)
        pos1=hi+'&/&'+mi+'&/&'+fm+'&/&'+hf+'&/&'+mf+'&/&'+tac+'&/&'+tt #en la posición 1 de la fila se almacenan parámetros del agendamiento separados por '&/&'
        for i in range(turnostotal):
            hor=turnos[i]
            hor=str(hor)
            tur=tur+1
            turstr=str(tur)
            vac=str(numjug)
            hoy=date.today()
            hoy=str(hoy)
            user=flask.session["username"]
            pos9=hoy+'&/&'+user+'&/&'+'C0' #en posición 9 se almacena: (fecha actua/usuario/C0:creacion desde cero)
            self.lista.append(pos0+'$*!$'+pos1+'$*!$'+hor+'$*!$'+turstr+'$*!$'+ju1+'$*!$'+ju2+'$*!$'+ju3+'$*!$'+ju4+'$*!$'+vac+'$*!$'+pos9)
    def consultaclubcampoAgenda(self,clu,cam,fec): #consulta si existe agenda en el archivo agenda_juego y devuelve Fasle ó True
        existeagenda=False
        for linea in self.lista:
            filaagenda=linea.split('$*!$')
            pos0=clu+'&/&'+cam+'&/&'+fec
            if filaagenda[0] == pos0:
                existeagenda=True
        return existeagenda
    def cambiaturnoAgenda(self,p1,club,campo,fecha,tur,ljugadores):
        for filota in self.lista:
            filaagenda=filota.split('$*!$')
            if filaagenda[0]== (club+'&/&'+campo+'&/&'+fecha):
                if filaagenda[3]==tur:
                    uno=str(date.today())
                    dos=flask.session["username"]
                    tres='A'+str(ljugadores)
                    huella=uno+'&/&'+dos+'&/&'+tres
                    filaagenda.append(huella)
                    for p in range(4,9):
                        filaagenda[p]=p1[p]
                    lfilaagenda=len(filaagenda)
                    self.lista.remove(filota)
                    filita=filaagenda[0]
                    for i in range (1,(lfilaagenda)):
                        filaagenda[i]=str(filaagenda[i])
                        filita=filita+'$*!$'+filaagenda[i]
        self.lista.append(filita)
        self.lista.sort()
    def recuperaclubcampoAgenda(self,clu,cam,fec): # recupera la programacion para un club en un campo y una fecha específica
        progclubcampo=[]
        for linea in self.lista:
            filaagenda=linea.split('$*!$')
            pos0=clu+'&/&'+cam+'&/&'+fec
            if filaagenda[0] == pos0:
                progclubcampo.append(filaagenda)
        return progclubcampo
    def recuperaTurnoAgenda(self,clu,cam,fec,tur): # recupera el turno deseado por el jugador
        lineaturno=[]
        for linea in self.lista:
            filaagenda=linea.split('$*!$')
            pos0=clu+'&/&'+cam+'&/&'+fec
            if filaagenda[0] == pos0:
                pos3=tur
                if filaagenda[3]==pos3:
                    lineaturno.append(filaagenda)
        return lineaturno
    def turjugAgenda(self,usuario,fecha): #Devuelve una lista con los turnos del jugador en la fecha
        turnosjugador=[]
        fecha=str(fecha)
        for linea in self.lista:
            existe='no'
            filaagenda=linea.split('$*!$')
            clubcamfe=filaagenda[0].split('&/&')
            if clubcamfe[2] == fecha:
                for i in range(4,8):
                    if filaagenda[i]==usuario:
                        existe='si'
            if existe=='si':
                turnosjugador.append(filaagenda)
        return turnosjugador
class Agendatenis:
    def __init__(self):
        self.lista=[]
    def iniciarAgendatenis(self):
        archivo=open('agenda_tenis','a')
        archivo.close()
    def leerAgendatenis(self):
        archivo=open('agenda_tenis','r')
        linea=archivo.readline()
        if linea:
            while linea:
                if linea[-1] == '\n':
                    linea = linea[:-1]
                self.lista.append(linea)
                linea=archivo.readline()
    def escribirAgendatenis(self): # se usa pra adicionar la agenda del archivo provisional en el programa al archivo agenda_tenis en la base de dtos
        archivo=open('agenda_tenis','a')
        for elemento in self.lista:
            archivo.write(elemento+"\n")
        archivo.close()
    def grabarturnoAgendatenis(self): # se usa pra escribir la agenda una vez se ha incluido el turno escogido por el jugador
        archivo=open('agenda_tenis','w')
        for elemento in self.lista:
            archivo.write(elemento+"\n")
        archivo.close()


def TotalTurnos(hi,mi,fm,hf,mf,txr,desa):#devuelve una lista con [numero de turnos antes del cruce, turnos en total del día]
    hi=int(hi)
    mi=float(mi)
    fm=float(fm)
    hf=int(hf)
    mf=float(mf)
    mia = mi/60
    mfa = mf/60
    horaincio = hi+mia
    horacierre = hf+mfa
    frecuencia=fm/60
    tiempox18 = (desa+(2*txr))
    turnosantescruce=int((desa+txr)/frecuencia) #grupoturnos
    horasoperacion = horacierre - horaincio
    rondasdisponibles = horasoperacion/tiempox18
    realrondas=int(rondasdisponibles)
    saldo = float(rondasdisponibles-realrondas)
    saldoturnos = saldo * turnosantescruce * 2
    saldoturnos = int(saldoturnos)
    if saldoturnos < turnosantescruce:
        turnosad=saldoturnos+1
    else:
        turnosad=turnosantescruce
    turnostotal=((realrondas-1)*turnosantescruce)+turnosad
    turnos=[turnosantescruce ,turnostotal]
    return turnos
def generahorarios(hi,mi,fm,hf,mf,turnos): #Entrega los horaios de los turnos en una lista (decimal)
    tac=int(turnos[0])
    tt=int(turnos[1])
    horasagenda=[]
    hi=int(hi)
    mi=float(mi)
    fm=float(fm)
    hf=int(hf)
    mf=float(mf)
    mia = mi/60
    mfa = mf/60
    inicioturno = hi+mia
    rondas=int(tt/tac)
    for i in range((rondas)):
        j=1
        while j<(tac+1):
            horasagenda.append(inicioturno)
            inicioturno=inicioturno+(fm/60)
            j=j+1
        inicioturno=inicioturno+(tac*fm/60)
    restoturnos=tt-(rondas*tac)
    for i in range((restoturnos)):
        horasagenda.append(inicioturno)
        inicioturno=inicioturno+(fm/60)
    return horasagenda
def ConvierteTurnoenHorarios(turnos,): #convierte los turnos de decimal a sexadecimal para mostrar en una lista
    devuelve=[]
    for turnito in turnos:
        enteroturnito=int(turnito)
        decimaturnito=turnito-enteroturnito
        minuto=int(decimaturnito*60)
        if minuto < 10:
            minuto=str(minuto)
            minuto=('0'+minuto)
        else:
            minuto=str(minuto)
        if enteroturnito<10:
            enteroturnito=str(enteroturnito)
            enteroturnito=('0'+enteroturnito)
        else:
            enteroturnito=str(enteroturnito)
        horaturno=(enteroturnito+":"+minuto)
        devuelve.append(horaturno)
    return devuelve
def InsertaCruces(turnossexa,tur): #inserta los cruces para mostrar los horarios
    mostrarturnos=[]
    if tur[0] != 0:
        partes=tur[1]/tur[0]
        partesenteras=int(partes)
        saldo=(partes-partesenteras)*tur[0]
        saldo=int(saldo)
        j=0
        for i in range(partesenteras):
            for k in range((tur[0])):
                mostrarturnos.append(turnossexa[j])
                j=j+1
            cruce='C_R_U_C_E_S'
            mostrarturnos.append(cruce)
        if saldo>0:
            for m in range(saldo):
                mostrarturnos.append(turnossexa[j])
                j=j+1
            mostrarturnos.append(cruce)
        return mostrarturnos
    else:
        mensaje='NO HAY AGENDA DISPONIBLE'
        mostrarturnos.append(mensaje)
        return mostrarturnos
def GeneraClave():
    clavej='asdfghjklqwertyuiopzxcvbnm1203456789AZQWSXCDERFVBGTYHNMJUIKLOP'
    c1=random.choice(clavej)
    c2=random.choice(clavej)
    c3=random.choice(clavej)
    c4=random.choice(clavej)
    c5=random.choice(clavej)
    c6=random.choice(clavej)
    c7=random.choice(clavej)
    c8=random.choice(clavej)
    contrasegna=c1+c2+c3+c4+c5+c6+c7+c8
    return contrasegna#Genera clave aleatoria de 8 dígitos

app = Flask(__name__) #esto crea un objeto que lo llamamos app
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME']= 'tee.shot.principal@gmail.com'
app.config['MAIL_PASSWORD'] = 'Tshot2009'
mail=Mail(app)


@app.route('/', methods=["GET", "POST"]) #es como decirle: esta  es la página principal, es la turata p4ra la apgina principal
def home():
    flask.session["logged_in"] = False
    flask.session["name"]=''
    flask.session["username"]=''
    flask.session["course"]=''
    flask.session["tusu"]=''
    return render_template('autenticacion.html')

@app.route('/logout', methods=["GET","POST"])
def logout():
    flask.session["logged_in"] = False
    flask.session["name"]=''
    flask.session["username"]=''
    flask.session["course"]=''
    flask.session["tusu"]=''
    return flask.redirect(flask.url_for("home"))

@app.route('/autentication', methods=["POST","GET"])   #Valida los datos que viene del formulario de autenticacion en 'inicio'
def autenticar():
    if (flask.request.method == "POST"):
        flask.session["logged_in"]=False
        usuario = flask.request.form["usuario"]
        contrasena = flask.request.form["contrasena"]
        encontrado=existeUsuarios(co=usuario) #devuelve si ó no , encontró el usuario?
        if encontrado=='si':
            contrasenabase=datotalUsuarios(co=usuario,tal='contrasena')
            if contrasena==contrasenabase:
                flask.session["logged_in"]=True
                flask.session["name"]=datotalUsuarios(co=usuario,tal='nombre')
                flask.session["surname"]=datotalUsuarios(co=usuario,tal='apellido')
                flask.session["username"]=usuario
                flask.session["course"]=datotalUsuarios(co=usuario,tal='club')
                tusuario=datotalUsuarios(co=usuario,tal='tipo') #lee el tipo de usuario
                flask.session["tusu"]=tusuario
                if tusuario==1:
                    return flask.render_template("res_pos_jug_autentic.html") #direcciona a formulario positivo de autenticacion de jugador
                elif tusuario==2:
                    return flask.render_template("res_pos_adclu_autentic.html") # direcciona a formulario positivo de autenticacion administrador de club
                elif tusuario==0:
                    return flask.render_template("res_pos_admin.html")
                    tusu = tusu #************construir el menu de administrador
            else:
                return flask.render_template("res_neg_autentic.html",dato='Contraseña incorrecta') #direcciona a error de autenticación
        else:
            return flask.render_template("res_neg_autentic.html", dato='No está registrado en Tee-Shot')
    else:
        return flask.redirect(flask.url_for("home"))

@app.route('/administrator_club', methods=["GET","POST"])
def inicioadclub(): #procedimiento para direccionar al menu inicial del administrador del club
    return render_template("res_pos_adclu_autentic.html")

@app.route('/players', methods=["GET","POST"])
def iniciojugadores():#procedimiento para direccionar al menu inicial del jugador
    return render_template("res_pos_jug_autentic.html")

@app.route('/generate_new_password', methods=["GET", "POST"]) #se usara para la seccion de olvido su contraseña
def olvidocontrasegna():
    return render_template('olvido_contra.html')

@app.route('/generate_new_password/assing', methods=["GET", "POST"])
def procolvidocontrasegna():
    usuario=flask.request.form["usuario"]
    encontrado=existeUsuarios(co=usuario)
    mensajerapido=''
    if encontrado=='si':
        contra1=GeneraClave()
        cambiodatoUsauarios(co=usuario,dato='contrasena',valor=contra1)
    else:
        mensajerapido='Usuario no registrado en TEE-SHOT'
    if mensajerapido=='':
        flash('Hemos enviado una nueva contraseña a su correo electrónico.')
        msg = Message('Reestablecimiento de contraseña en TEE-SHOT', sender = app.config['MAIL_USERNAME'], recipients=[usuario])
        msg.html = render_template('mail03.html',contrasegna=contra1)
        mail.send(msg)
        return render_template('olvido_contra.html')
    else:
        flash(mensajerapido)
        return render_template('olvido_contra.html')

@app.route('/registration_TEE_SHOT', methods=["GET","POST"]) # Crear usuario como jugador
def registro():
    campos=Campos()
    campos.leerCampos()
    lista_campos=campos.devolverCampos()
    largo=len(lista_campos)
    return render_template('registro.html',campos=lista_campos, largo=largo) # Direcciona al formulario de registro de usuario jugador

@app.route('/condiciones_uso',methods=["GET","POST"])
def condiciones_uso():
    return render_template('condiciones_uso.html')

@app.route('/registration_TEE_SHOT/result_registration', methods=["POST"])
def terminaregistro():
    registro=False
    if(flask.request.method == "POST"):
        usuario = flask.request.form["usuario"]
        nombre = flask.request.form["nombre"]
        apellido = flask.request.form["apellido"]
#        contrasena1 = flask.request.form["contrasena1"]
#        contrasena2 = flask.request.form["contrasena2"]
        identificacion = flask.request.form["identificacion"]
        club = flask.request.form["club"]
        indice_fedegolf = flask.request.form["indice_fedegolf"]
        cod_fedegolf = flask.request.form["cod_fedegolf"]
        aval_club='NO'     #validar los avales mas adelante
        tipo_usuario=1
        fecha=date.today()
        fecha=str(fecha)
        contrasegna=GeneraClave()
        encontrado=existeUsuarios(co=usuario)
        print(encontrado)
        if encontrado=='si':
            return render_template('error_registro.html', error='****ERROR****    Usuario Ya Registrado en TEE-SHOT')
        else:
            crearUsuario(co=usuario,no=nombre,ap=apellido,cn=contrasegna,id=identificacion,cl=club,ac=aval_club,cf=cod_fedegolf,ind=indice_fedegolf,fr=fecha,ty=tipo_usuario)
            msg = Message('Gracias por inscribirse en TEE-SHOT', sender = app.config['MAIL_USERNAME'], recipients=[usuario])
            msg.html = render_template('mail01.html', nombre=nombre,usuario=usuario, contrasegna=contrasegna)
            mail.send(msg)
            return render_template('result_registro.html', mensaje='Felicitaciones. Su registro en TEE-SHOT ha sido exitoso')
    else:
        return render_template("autenticacion.html")

@app.route('/autentication/user_profile', methods=["GET","POST"])
def perfilusuario():
    usuario=flask.session["username"]
    datusuario=todosdatosUsuarios(co=usuario)
    return render_template('cambioperfil.html',datusuario=datusuario)

@app.route('/autentication/change_password', methods=["GET","POST"])
def cambiocontrasegna():
    return render_template('cambiopasword.html')

@app.route('/autentication/change_password/realize', methods=["GET","POST"])
def realizacambiocontrasegna():
    contra0=flask.request.form["contra0"]
    contra1=flask.request.form["contra1"]
    contra2=flask.request.form["contra2"]
    usuario=flask.session["username"]
    print(contra0)
    print(contra1)
    print(contra2)
    mensajeerror=''
    if contra1 == contra2:
        contrasegna=datotalUsuarios(co=usuario,tal='contrasena')
        if contra0 == contrasegna:
            cambiodatoUsauarios(co=usuario,dato='contrasena',valor=contra1)
        else:
            mensajeerror='Su contraseña actual está errada'
    else:
        mensajeerror='Las contraseñas son diferentes'
    if mensajeerror =='':
        flash('Contraseña cambiada de manera Exitosa')
        msg = Message('Cambio de contraseña en TEE-SHOT', sender = app.config['MAIL_USERNAME'], recipients=[usuario])
        msg.html = render_template('mail02.html')
        mail.send(msg)
        return render_template('cambiopasword.html')
    else:
        flash(mensajeerror)
        return render_template('cambiopasword.html')

@app.route('/players/cards', methods=["GET","POST"])
def tarjetasjugador():#juador define quien va a ser su marcador en la tajeta
    fecha=date.today()
    usuario=flask.session["username"]
    turnosjugador=turnosjuadorAgendaGolf(usuario=usuario,fec=fecha)
    lturnosjugador=len(turnosjugador)
    if lturnosjugador !=0:
        clubjugado=[]
        colegas=['club@club.com']
        horas=[]
        for turno in turnosjugador:
            clubjugado.append(turno[0])
            hora=turno[6]
            horas.append(hora)
            for i in range (8,12):
                if turno[i]!=usuario:
                    colegas.append(turno[i])
        return render_template('menuju05.html',clubjugado=clubjugado,colegas=colegas,turnosjugador=turnosjugador,fecha=fecha,horas=horas)
    else:
        mensajerapido='*** Usted no tiene agendado juego para hoy, debe estar agendado para entregar tarjeta de juego ***'
        flash(mensajerapido)
        return render_template('res_pos_jug_autentic.html')

@app.route('/players/cards/send', methods=["GET","POST"])
def tarjetasjugadorsend():#Jugador llene los escores de la tajeta y la envíe para que la firme el marcador
    if(flask.request.method=="POST"):
        club=flask.request.form["club"]
        marcador=flask.request.form["marcador"]
        hora=flask.request.form["hora"]
        co=flask.session["username"]
        hoy=date.today()
        encontrado=existeTarjetasGolf(fec=hoy,hora=hora,co=co)
        if encontrado=='no':
            return render_template('menuju06.html',club=club,marcador=marcador,hoy=hoy,hora=hora)
        else:
            flash('Ya tiene una tarjeta registrada')
            return render_template('res_pos_jug_autentic.html')
    else:
        return render_template("autenticacion.html")

@app.route('/players/cards/send/record', methods=["GET","POST"])
def rectarjetajugador():#graba en la base de datos la tarjeta envida por el jugador
    if(flask.request.method=="POST"):
        fec=date.today()
        co=flask.session["username"]
        mc=flask.request.form["marcador"]
        cam=flask.request.form["club"]
        hora=flask.request.form["hora"]
        encontrado=existeTarjetasGolf(fec=fec,hora=hora,co=co)
        if encontrado=='no':
            tarjeta=[]
            tarjeta.append(fec)
            tarjeta.append(hora)
            tarjeta.append(co)
            tarjeta.append(mc)
            tarjeta.append(cam)
            ida=0
            for i in range(1,10):
                adicion=str(i)
                hoyo='hoyo'+adicion
                golpes=flask.request.form[hoyo]
                tarjeta.append(golpes)
                golpes=int(golpes)
                ida=ida+golpes
            tarjeta.append(ida)
            vuelta=0
            for i in range(10,19):
                adicion=str(i)
                hoyo='hoyo'+adicion
                golpes=flask.request.form[hoyo]
                tarjeta.append(golpes)
                golpes=int(golpes)
                vuelta=vuelta+golpes
            tarjeta.append(vuelta)
            total=ida+vuelta
            tarjeta.append(total)
            tarjeta.append(co)
            creaTarjetasGolf(tarjeta=tarjeta)
            ida=str(ida)
            vuelta=str(vuelta)
            total=str(total)
            flash('Tarjeta enviada para firma del marcador. Ida= '+ida+ ' Vuelta= '+vuelta+ ' Total= ' +total)
            return render_template("res_pos_jug_autentic.html")
        else:
            flash('Ya se envió la tajeta')
            return render_template("res_pos_jug_autentic.html")

    else:
        return render_template("autenticacion.html")

@app.route('/players/cards/send/record/validate', methods=["GET","POST"])
def tarjetascolega():
    mc=flask.session["username"]
    respuesta=marcadorTarjetasGolf(mc=mc)
    asignadomarcador=respuesta[0]
    if asignadomarcador=='si':
        tars0=respuesta[1]
        tars=[]
        for tarjeta in tars0:
            if tarjeta[27]==None:
                tars.append(tarjeta)
                mensaje=''
        if tars==[]:
            mensaje='No tiene tarjetas pendientes por firmar como marcador'
    else:
        mensaje='No tiene tarjetas pendientes por firmar como marcador'
    if mensaje=='':
        return render_template('menuju07.html',respuesta=respuesta,tars=tars)
    else:
        flash(mensaje)
        return render_template('res_pos_jug_autentic.html')

@app.route('/players/cards/send/record/validate/show', methods=["GET","POST"])
def tarjetafirmada():
    mc=flask.session["username"]
    fec=flask.request.form["fec"]
    co=flask.request.form["co"]
    hora=flask.request.form["hora"]
    print(fec)
    print(hora)
    print(co)
    print(mc)
    cambiadatotalTarjetaGolf(fec=fec,hora=hora,co=co,dato='firma_marcador',valor=mc)

    flash('La tarjeta avalada por usted, ha sido enviada con exito')
    return render_template('res_pos_jug_autentic.html')

@app.route('/creating_agenda', methods=["GET","POST"])
def formturnos():
        usuario=flask.session["username"]
        club=flask.session["course"]
        course=Campos()
        course.leerCampos()
        campos=course.buscarCampos(campo=club)
        campo1=campos[1]
        largo=len(campos)
        hoy=date.today()
        fecha1=hoy+timedelta(days=1)
        fecha2=hoy+timedelta(days=10)
        return render_template("menuac02.html",club=club, campos=campos, largo=largo, fecha1=fecha1, fecha2=fecha2)

@app.route('/creating_agneda/view01', methods=["GET","POST"])
def clubcreaagendadia():#CREAR DIA Agenda para un campo específico
    if(flask.request.method == "POST"):
        fecha=flask.request.form["fechainicial"]
        numjug=flask.request.form["numjug"]
        hora_apertura=flask.request.form["hora_apertura"]
        hora_cierre=flask.request.form["hora_cierre"]
        frecuencia=flask.request.form["frecuencia"]
        txrhu=flask.request.form["txrh"] #Horas por ronda
        txrmu=flask.request.form["txrm"] #minutos por ronda
        desau=flask.request.form["desa"] #minutos para desayuno
        numjug=int(numjug)
        txrhu=int(txrhu)
        txrmu=int(txrmu)
        txr= txrhu + (txrmu/60)
        desau=int(desau)
        desa= desau/60
        hora1=[]
        hora1=hora_apertura.split(':')
        hi=float(hora1[0])
        mi=float(hora1[1])
        hi=int(hi)
        mi=int(mi)
        hora2=[]
        hora2=hora_cierre.split(':')
        hf=float(hora2[0])
        mf=float(hora2[1])
        hf=int(hf)
        mf=int(mf)
        usuario=flask.session["username"]
        club=flask.session["course"]
        course=Campos()
        course.leerCampos()
        campos=course.buscarCampos(campo=club) #Genera lista de campos del club, almacena en vaiable campos
        clu=club
        lcampos=len(campos)
        cam=campos[1]
        fec=fecha
        fm=frecuencia
        tur=TotalTurnos(hi=hi,mi=mi,fm=fm,hf=hf,mf=mf,txr=txr,desa=desa) # tur=[turnos entre cruces, turnos totales]
        turnos=generahorarios(hi=hi,mi=mi,fm=fm,hf=hf,mf=mf,turnos=tur)  #genera los tunos en hora decimales
        turnossexa=ConvierteTurnoenHorarios(turnos) #conviertelos turnos decimales en formato horas
        mostrarturnos=InsertaCruces(turnossexa=turnossexa,tur=tur)
        lmt=len(mostrarturnos)
        tac=tur[0]
        tt=tur[1]
        checkagenda=existeAgendaGolf(clu=clu,cam=cam,fec=fec) #comprueba si existe agenda para ese club,campo y fecha
        if checkagenda == 'no':
            for i in range(1,len(campos)):
                archivoprov=Agenda()
                cam=campos[i]
                creaAgendaGolf(clu=clu,cam=cam,fec=fec,turnos=turnossexa,fm=fm,tac=tac,numjug=numjug)
            return render_template("menu03ac.html", f1=fec, h1=hora_apertura, h2=hora_cierre,fr=frecuencia,tur=tur,turnos=mostrarturnos,campos=campos,club=club,lcampos=lcampos,lmt=lmt,numjug=numjug)
        else:
            return render_template("menu03ac_error.html", f1=fec,club=club,mensajeerror='YA HAY AGENDA PROGRAMADA PARA LA FECHA SELECCIONADA')
    else:
        return render_template("autenticacion.html")

@app.route('/view_agenda_parameters', methods=["GET","POST"])
def vaparameters(): #Direcciona al administrador del club para que pueda ver agenda de alguno de sus campos
    usuario=flask.session["username"]
    club=flask.session["course"]
    course=Campos()
    course.leerCampos()
    campos=course.buscarCampos(campo=club)
    campo1=campos[1]
    largo=len(campos)
    del course
    return render_template("menuac04.html",club=club,campos=campos,largo=largo)

@app.route('/view_agenda_parameters/visulization', methods=["GET","POST"])
def clubveragenda(): #El club puede ver la agenda en un día específico
    if(flask.request.method=="POST"):
        club=flask.session["course"]
        campo=flask.request.form["campo"]
        fecha=flask.request.form["fecha"]
        existeagenda=existeAgendaGolf(clu=club,cam=campo,fec=fecha)
        if existeagenda=='si':
            progclubcampo=recuperaAgendaGolf(clu=club,cam=campo,fec=fecha)

            return render_template("menuac05.html", club=club,campo=campo,fecha=fecha,progclubcampo=progclubcampo)
        else:
            mensajeerror='No existe agenda para el día seleccionado'
            return render_template("menuac_error05.html", mensajeerror=mensajeerror)
    else:
        return render_template("autenticacion.html")

@app.route('/view_agenda_parameters/visualization/changes', methods=["GET","POST"])
def clubcambioagenda():#procedimiento para que el club escriba los cambios de algún turno de la agenda
    if(flask.request.method=="POST"):
        club=flask.session["course"]
        campo=flask.request.form["campo"]
        fecha=flask.request.form["fecha"]
        turno=flask.request.form["turno"]
        filaagenda=recuperaturnoAgendaGolf(clu=club,cam=campo,fec=fecha,tur=turno)
        return render_template("menuac06.html",filaagenda=filaagenda,campo=campo,fecha=fecha,turno=turno)

    else:
        return render_template("autenticacion.html")

@app.route('/view_agenda_parameters/visualization/changes/record', methods=["GET","POST"])
def clubrealizacambioagenda(): #procedimiento para grabar los cambios definidos pór el club para algún truno de la agenda
    if(flask.request.method=="POST"):
        club=flask.session["course"]
        co=flask.session["username"]
        campo=flask.request.form["campo"]
        fecha=flask.request.form["fecha"]
        turno=flask.request.form["turno"]
        jug01=flask.request.form["jug01"]
        jug02=flask.request.form["jug02"]
        jug03=flask.request.form["jug03"]
        jug04=flask.request.form["jug04"]
        jugadores=[jug01,jug02,jug03,jug04]
        mensajeerror=''
        for jugador in jugadores:
            if jugador != '':
                if jugador !='vacio':
                    existejug=existeUsuarios(co=jugador)
                    if existejug=='no':
                        mensajeerror='Solo puede inscribir usuarios registrados en TEE-SHOT, '+jugador+' no está registrado en TEE-SHOT. *** Invítalo a inscribirse ***'
        if mensajeerror == '':
            filaagenda=recuperaturnoAgendaGolf(clu=club,cam=campo,fec=fecha,tur=turno)
            p1=filaagenda #lista de agendamiento que se va a modificar
            pjug=8
            vacios=0
            for i in range(4): #actualza jugadores respecto a la solicitud del club y lo que había en la agenda.
                if jugadores[i]=='':
                    jugadores[i]=p1[pjug]
                if jugadores[i]=='vacio':
                    vacios=vacios+1 #actualiza cuántos cupos quedan
                pjug=pjug+1
            if vacios > 0:
                nuevojugadores=[]
                for jugador in jugadores:
                    if jugador !='vacio':
                        nuevojugadores.append(jugador)
                for i in range(vacios):
                    nuevojugadores.append('vacio')
                for i in range(4):
                    jugadores[i]=nuevojugadores[i]
            hoy=date.today()
            hoy=str(hoy)
            huella=str(p1[14])
            if len(huella)<100:
                huella=huella+hoy+'&/&'+co+'$/$'
            else:
                huella=hoy+'&/&'+co+'$/$'
            cambiadatotalAgendaGolf(clu=club,cam=campo,fec=fecha,tur=turno,dato='ju1',valor=jugadores[0])
            cambiadatotalAgendaGolf(clu=club,cam=campo,fec=fecha,tur=turno,dato='ju2',valor=jugadores[1])
            cambiadatotalAgendaGolf(clu=club,cam=campo,fec=fecha,tur=turno,dato='ju3',valor=jugadores[2])
            cambiadatotalAgendaGolf(clu=club,cam=campo,fec=fecha,tur=turno,dato='ju4',valor=jugadores[3])
            cambiadatotalAgendaGolf(clu=club,cam=campo,fec=fecha,tur=turno,dato='vacios',valor=vacios)
            cambiadatotalAgendaGolf(clu=club,cam=campo,fec=fecha,tur=turno,dato='huella',valor=huella)
            return render_template("menuac07.html",jugadores=jugadores,club=club,campo=campo,fecha=fecha,turno=turno)
        else:
            return render_template("menuac07_error.html",mensajeerror=mensajeerror)


    else:
        return render_template("autenticacion.html")

@app.route('/recognition_playerbyclub',methods=["GET","POST"])
def avalarjugadoresclub(): #inicia el aval del club para los jugadores del mismo club
    club=flask.session["course"]
    sinaval=sinavalUsuarios(cl=club)
    return render_template('menuac10.html',sinaval=sinaval)

@app.route('/recognition_playerbyclub/tramit',methods=["GET","POST"])
def daravalxclub():
    co=flask.request.form["co"]
    valor='SI'
    cambiodatoUsauarios(co=co,dato="aval_club",valor=valor)
    flash('Autorizado '+co+ 'para agendar')
    return render_template('res_pos_adclu_autentic.html')

@app.route('/players/begin/', methods=["GET","POST"])
def inicioagendajugador():
    ya=datetime.now()
    hora=ya.hour
    minuto=ya.minute
    if flask.session['course']=='Serrezuela':
        if hora<24 and hora>=1: #hora en el servidor donde está alojada la aplicación  HORASERVIDOR de 12 a 20
            co=flask.session["username"]
            aval=datotalUsuarios(co=co,tal="aval_club")
            club=flask.session["course"]
            if aval == 'SI':
                return render_template("menu01ju.html", club=club)
            else:
                flash('No tiene aval de del club '+club+' para pedir turnos')
                return render_template('res_pos_jug_autentic.html')
        else:
            flash('SERREZUELA definió que el horario para ingresar a seleccionar turno es de 7 am a 3 pm')
            return render_template('res_pos_jug_autentic.html')
    else:
        co=flask.session["username"]
        aval=datotalUsuarios(co=co,tal="aval_club")
        if aval == 'SI':
            club=flask.session["course"]
            return render_template("menu01ju.html", club=club)
        else:
            club=flask.session["course"]
            flash('No tiene aval de del club '+club+' para pedir turnos')
            return render_template('res_pos_jug_autentic.html')

@app.route('/players/begin/add_players', methods=["POST","GET"])
def rejugrupo(): #revisa la viavilidad de los jugadores para inscribirse
    if(flask.request.method == "POST"):
        jugadores=[]
        jug01=flask.session["username"]
        jugadores.append(jug01)
        jug02=flask.request.form["jug02"]
        jug03=flask.request.form["jug03"]
        jug04=flask.request.form["jug04"]
        club=flask.request.form["clu"]
        error_jugador=''
        if jug02 != '':
            existejug2=existeUsuarios(co=jug02)
            if existejug2=='si':
                jugadores.append(jug02)
            else:
                error_jugador='Solo puede inscribir usuarios registrados en TEE-SHOT, '+jug02+' No está registrado. *** invítalo a inscribirse ***'
        if jug03 != "":
            existejug3=existeUsuarios(co=jug03)
            if existejug3=='si':
                jugadores.append(jug03)
            else:
                error_jugador='Solo puede inscribir usuarios registrados en TEE-SHOT, '+jug03+' No está registrado. *** invítalo a inscribirse ***'
        if jug04 != "":
            existejug4=existeUsuarios(co=jug04)
            if existejug4=='si':
                jugadores.append(jug04)
            else:
                error_jugador='Solo puede inscribir usuarios registrados en TEE-SHOT, '+jug04+' No está registrado. *** invítalo a inscribirse ***'
        if error_jugador == '':
            j2=[]
            for k in range(len(jugadores)):
                j2.append(jugadores[k])
            j2.sort()
            for i in range(len(j2)):
                if len(jugadores)!=1:
                    if j2[i]==j2[i-1]:
                        error_jugador='No se puede repetir jugador'
            if error_jugador == '':
                ljugadores=len(jugadores)
                fecha0=date.today()
                fecha1=date.today()+timedelta(days=1)
                fecha2=fecha0+timedelta(days=1)
                archivo2=Campos()
                archivo2.leerCampos()
                campos=archivo2.buscarCampos(campo=club)
                lcampos=len(campos)
                return render_template("menu02ju.html",jugadores=jugadores,ljugadores=ljugadores,fecha1=fecha1,fecha2=fecha2,campos=campos,lcampos=lcampos,club=club)
            else:
                return render_template("menu02ju_error.html", mensaje=error_jugador)

        else:
            return render_template("menu02ju_error.html", mensaje=error_jugador)
    else:
        return render_template("autenticacion.html")

@app.route('/players/begin/add_players/select_option_game', methods=["POST","GET"])
def moptjug(): # mostrar opciones para que el jugador defina un turno
    if(flask.request.method == "POST"):
        fecha=flask.request.form["fecha_deseada"]
        campo=flask.request.form["campo"]
        jugadores=flask.request.form["jugadores"]
        ljugadores=flask.request.form["ljugadores"]
        club=flask.request.form["club"]
        listajugadores=re.findall("[a-zA-Z0-0]\S+@\S+[a-zA-Z]",jugadores)
        print('********jugadores*********')
        print(listajugadores)
        consulta1=existeAgendaGolf(clu=club,cam=campo,fec=fecha)
        if consulta1 == 'si':
            contador=0
            for jugador in listajugadores:
                turnosjugador=turnosjuadorAgendaGolf(usuario=jugador,fec=fecha)
                if turnosjugador!=[]:
                    mensajerapido=jugador+' ya tiene turno para la fecha seleccionada'
                    contador=contador+1
            if contador==0:
                progclubcampo=recuperaAgendaGolf(clu=club, cam=campo,fec=fecha)
                ljugadores=int(ljugadores)
                return render_template("menu03ju.html",fecha=fecha,campo=campo,jugadores=jugadores,ljugadores=ljugadores,club=club,consulta1=consulta1,progclubcampo=progclubcampo)
            else:
                flash(mensajerapido)
                return render_template("res_pos_jug_autentic.html")
        else:
            return render_template("menu03ju_error.html", mensaje="no hay agenda por parte del club para ese día")
    else:
        return render_template("autenticacion.html")

@app.route('/players/begin/add_players/select_option_game/record_aggend', methods=["GET","POST"])
def brabagenjugador(): #grabar la opción decidida por el jugador en la agenda del club
    if(flask.request.method == "POST"):
        fecha=flask.request.form["fecha"]
        co=flask.session["username"]
        campo=flask.request.form["campo"]
        jugadores=flask.request.form["jugadores"]
        ljugadores=flask.request.form["ljugadores"]
        club=flask.request.form["club"]
        turno_sel=flask.request.form["tur"]
        listajugadores=re.findall("[a-zA-Z0-0]\S+@\S+[a-zA-Z]",jugadores)
        contador=0
        for jugador in listajugadores:
            turnosjugador=turnosjuadorAgendaGolf(usuario=jugador,fec=fecha)
            if turnosjugador!=[]:
                mensajerapido=jugador+' ya tiene turno para la fecha seleccionada'
                contador=contador+1
        if contador==0:
            tur=int(turno_sel)
            filaagenda=recuperaturnoAgendaGolf(clu=club,cam=campo,fec=fecha,tur=tur)
            p1=filaagenda
            cupos=int(p1[12]) #cupos
            ljugadores=int(ljugadores) #cuántos voy a inscribir
            if ljugadores <= cupos: #si voy a inscribir menos que los cupos disponibles
                inicial=8+(4-(cupos))
                final=inicial+(ljugadores)
                cupos=cupos - ljugadores
                for i in range (ljugadores):
                    digito=inicial-7+i
                    digito=str(digito)
                    player='ju'+digito
                    cambiadatotalAgendaGolf(clu=club,cam=campo,fec=fecha,tur=tur,dato=player,valor=listajugadores[i])
                cambiadatotalAgendaGolf(clu=club,cam=campo,fec=fecha,tur=tur,dato='vacios',valor=cupos)
                hoy=date.today()
                hoy=str(hoy)
                huella=str(p1[14])
                if len(huella)<100:
                    huella=huella+hoy+'&/&'+co+'$/$'
                else:
                    huella=hoy+'&/&'+co+'$/$'
                cambiadatotalAgendaGolf(clu=club,cam=campo,fec=fecha,tur=tur,dato='huella',valor=huella)
                titulo='Confirmación de turnno TEE-SHOT__'+club+' '+fecha
#***************ACTIVAR EN PRODUCCION SOLAMENTE
                # msg = Message(titulo, sender = app.config['MAIL_USERNAME'], recipients=listajugadores)
                # msg.html = render_template('mail04.html',clu=club,cam=campo,fec=fecha,usuario=co,filaagenda=filaagenda)
                # mail.send(msg)
                return render_template("menu04ju.html",fecha=fecha,campo=campo,jugadores=jugadores,ljugadores=ljugadores,club=club,turno_sel=turno_sel,filaagenda=filaagenda)
            else:
                mensajeerror='No hay cupos disponibles en la selección, por favor vuelva escoger un horaio deseado'
                return render_template("menu04ju_error.html", mensaje=mensajeerror)
        else:
            flash(mensajerapido)
            return render_template("res_pos_jug_autentic.html")
    else:
        return render_template("autenticacion.html")

@app.route('/viewcards', methods=["GET","POS"])
def selclubtarjetas():#Procedimiento para que el club selccione la fecha que desea ver tarjetas
    return render_template('menuac08.html')

@app.route('/viewcards/showdatecards',methods=["GET","POST"])
def vertarjetasclub():
    cam=flask.session["course"]
    fecha=flask.request.form["fecha"]
    fecha=str(fecha)
    tarjetas=recuperaTarjetasGolf(fec=fecha,cam=cam)
    listatarjetas=[]
    for tarjeta in tarjetas:
        nombre=datotalUsuarios(co=tarjeta[2],tal='nombre')
        apellido=datotalUsuarios(co=tarjeta[2],tal='apellido')
        cf=datotalUsuarios(co=tarjeta[2],tal='codigo_fed')
        card=[nombre,apellido,cf]
        for i in range(5,14):
            card.append(tarjeta[i])
        for i in range(15,24):
            card.append(tarjeta[i])
        card.append(tarjeta[26])
        card.append(tarjeta[27])
        listatarjetas.append(card)

    return render_template('menuac09.html',fecha=fecha,tarjetas=listatarjetas)

@app.route('/tenis_creating_agenda', methods=["GET","POST"])
def formturnostenis():
        usuario=flask.session["username"]
        club=flask.session["course"]
        hoy=date.today()
        fecha1=hoy+timedelta(days=1)
        fecha2=hoy+timedelta(days=10)
        return render_template("menuac11.html",club=club, fecha1=fecha1, fecha2=fecha2)

@app.route('/tenis_creating_agneda/view01', methods=["GET","POST"])
def clubcreaagendadiatenis():#CREAR DIA Agenda para un campo específico
    if(flask.request.method == "POST"):
        fecha=flask.request.form["fechainicial"]
        canchaspr=flask.request.form["chancaspr"]
        canchascl=flask.request.form["chanchascl"]
        hora_apertura=flask.request.form["hora_apertura"]
        hora_cierre=flask.request.form["hora_cierre"]
        frecuencia=flask.request.form["frecuencia"]
        club=flask.session["course"]
        hora1=[]
        hora1=hora_apertura.split(':')
        hi=float(hora1[0])
        mi=float(hora1[1])
        hi=int(hi)
        mi=int(mi)
        hora2=[]
        hora2=hora_cierre.split(':')
        hf=float(hora2[0])
        mf=float(hora2[1])
        hf=int(hf)
        mf=int(mf)
        usuario=flask.session["username"]
        course=Campos()
        course.leerCampos()
        campos=course.buscarCampos(campo=club) #Genera lista de campos del club, almacena en vaiable campos
        clu=club
        lcampos=len(campos)
        cam=campos[1]
        fec=fecha
        fm=frecuencia
        tur=TotalTurnos(hi=hi,mi=mi,fm=fm,hf=hf,mf=mf,txr=txr,desa=desa) # tur=[turnos entre cruces, turnos totales]
        turnos=generahorarios(hi=hi,mi=mi,fm=fm,hf=hf,mf=mf,turnos=tur)  #genera los tunos en hora decimales
        turnossexa=ConvierteTurnoenHorarios(turnos) #conviertelos turnos decimales en formato horas
        mostrarturnos=InsertaCruces(turnossexa=turnossexa,tur=tur)
        lmt=len(mostrarturnos)
        tac=tur[0]
        tt=tur[1]
        archivoagenda=Agenda()
        archivoagenda.iniciarAgenda()
        archivoagenda.leerAgenda()
        checkagenda=archivoagenda.consultaclubcampoAgenda(clu=clu,cam=cam,fec=fec) #comprueba si existe agenda para ese club,campo y fecha
        if checkagenda == False:
            for i in range(1,len(campos)):
                archivoprov=Agenda()
                cam=campos[i]
                archivoprov.adicioncampoAgenda(clu=clu,cam=cam,fec=fec,turnos=turnossexa,hi=hi,mi=mi,fm=fm,hf=hf,mf=mf,tac=tac,tt=tt,numjug=numjug)
                archivoprov.escribirAgenda()
            return render_template("menu03ac.html", f1=fec, h1=hora_apertura, h2=hora_cierre,fr=frecuencia,tur=tur,turnos=mostrarturnos,campos=campos,club=club,lcampos=lcampos,lmt=lmt,numjug=numjug)
        else:
            return render_template("menu03ac_error.html", f1=fec,club=club,mensajeerror='YA HAY AGENDA PROGRAMADA PARA LA FECHA SELECCIONADA')
    else:
        return render_template("autenticacion.html")



if __name__ == '__main__':  #para mantener activa la página
    app.run(debug=True, port=8000)
    mail.init_app(app)
