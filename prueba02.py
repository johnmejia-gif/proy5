''' BASE DE DATOS AGENDA DE GOLF'''
from datetime import datetime, date, time, timedelta
from mysql.connector import MySQLConnection, Error
from python_mysql_dbconfig import read_db_config

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
            user="serrezuela@serrezuela.com"
            crea=hoy+'&/&'+user #en posición 9 se almacena: (fecha actua/usuario:creacion desde cero)
            data=(clu,cam,fec,fm,tac,tt,hor,tur,ju1,ju2,ju3,ju4,vac,crea)
            # print(clu)
            # print(cam)
            # print(fec)
            # print(fm)
            # print(tac)
            # print(tt)
            # print(hor)
            # print(tur)
            # print(ju1)
            # print(ju2)
            # print(ju3)
            # print(ju4)
            # print(vac)
            # print(crea)
            # print(query)
            # print(data)
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
            print(row)
            row = cursor.fetchone()
    except Error as error:
        print(error)
    finally:
        cursor.close()
        conn.close()
    return turnosjugador
def consultadatoAgendaGolf(clu,cam,fec,tur,dato):
    q1=" SELECT "
    q2=" FROM agenda_golf WHERE club=%s AND campo=%s AND fecha = %s AND turno=%s "
    query=q1+dato+q2
    data=(clu,cam,fec,tur)
    dbconfig = read_db_config()
    hora:''
    try:
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        cursor.execute(query,data)
        row=cursor.fetchone()
        print(row)
        hora=row[0]
    except Error as error:
        print(error)
    finally:
        cursor.close()
        conn.close()
    return hora

def main():
    clu='Serrezuela'
    cam='Hoyo1Serrezuela'
    fec='2020-07-01'
    hora=consultadatoAgendaGolf(clu=clu,cam=cam,fec=fec,tur=3,dato='hora')
    print(hora)
#****************
    # turnosjugador=turnosjuadorAgendaGolf(usuario='jcmejia@live.com',fec='2020-07-01')
    # print('******* los turnos del jugador son: **********')
    # print(turnosjugador)
#****************
    # clu='Serrezuela'
    # cam='Hoyo1Serrezuela'
    # fec='2020-07-01'
    # encontrado=existeAgendaGolf(clu=clu,cam=cam,fec=fec)
    # print(encontrado)
#**************
    # tur=TotalTurnos(hi=6,mi=30,fm=15,hf=16,mf=30,txr=2,desa=0) # tur=[turnos entre cruces, turnos totales]
    # turnos=generahorarios(hi=6,mi=30,fm=15,hf=16,mf=30,turnos=tur)  #genera los tunos en hora decimales
    # turnossexa=ConvierteTurnoenHorarios(turnos) #conviertelos turnos decimales en formato horas
    # tac=tur[0]
    # creaAgendaGolf(clu='Serrezuela',cam='Hoyo1Serrezuela',fec='2020-07-02',turnos=turnossexa,fm=15,tac=tac,numjug=3)
#*****************
    # clu='Serrezuela'
    # cam='Hoyo1Serrezuela'
    # fec='2020-07-01'
    # progclubcampo=recuperaAgendaGolf(clu=clu,cam=cam,fec=fec)
    # print(progclubcampo[0])
#*******************
    # clu='Serrezuela'
    # cam='Hoyo10Serrezuela'
    # fec='2020-07-01'
    # lineaturno=recuperaturnoAgendaGolf(clu=clu,cam=cam,fec=fec,tur=5)
    # print(lineaturno)
    # print(lineaturno[12])
    # lineaturno[12]="6"
    # print(lineaturno[12])
#'****************
    # clu='Serrezuela'
    # cam='Hoyo1Serrezuela'
    # fec='2020-07-01'
    # tur=3
    # dato='huella'
    # valor='chorrera de cosasa que se escriban de acuerdo a los cambios'
    # cambiadatotalAgendaGolf(clu=clu,cam=cam,fec=fec,tur=tur,dato=dato,valor=valor)


if __name__ == '__main__':
    main()
