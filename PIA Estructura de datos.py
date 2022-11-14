#CREACIÓN DE UNA BASE DE DATOS CON DOS TABLAS RELACIONADAS UNO A MUCHOS
from collections import namedtuple
import sys
import datetime
import sqlite3
from sqlite3 import Error
from datetime import (date, datetime,timedelta)
import openpyxl
import pandas as pd
#Crea una tabla en SQLite3



def Crear_tabla ():
  try:
    with sqlite3.connect("PIA.db") as conn:
        mi_cursor = conn.cursor()
        mi_cursor.execute("CREATE TABLE IF NOT EXISTS Usuarios (IDCLIENTE INTEGER PRIMARY KEY AUTOINCREMENT, nombre TEXT NOT NULL);")
        mi_cursor.execute("CREATE TABLE IF NOT EXISTS Salas (IDSALA INTEGER PRIMARY KEY AUTOINCREMENT, nombre TEXT NOT NULL, capacidad INTEGER NOT NULL);")
        #mi_cursor.execute("CREATE TABLE IF NOT EXISTS Reservaciones (folio INTEGER PRIMARY KEY, nombre TEXT NOT NULL, horario Text NOT NULL, fecha timestamp, IDCLIENTE INTENGER, FOREIGN KEY(IDCLIENTE) REFERENCES Usuarios(IDCLIENTE));")
        mi_cursor.execute("CREATE TABLE IF NOT EXISTS Turnos (Horario TEXT PRIMARY KEY, Letra TEXT NOT NULL);")
        mi_cursor.execute("CREATE TABLE IF NOT EXISTS Reservaciones (folio INTEGER PRIMARY KEY AUTOINCREMENT, nombre_evento TEXT NOT NULL, horario Text NOT NULL, fecha timestamp, IDCLIENTE INTENGER, nombreSala TEXT NOT NULL, Sala INTENGER, FOREIGN KEY(IDCLIENTE) REFERENCES Usuarios(IDCLIENTE), FOREIGN KEY(Sala) REFERENCES Salas(IDSALA));")
        mi_cursor.execute("SELECT * FROM Turnos;")
        Horariosss = mi_cursor.fetchall()
        if not Horariosss:
            mi_cursor.execute(f"INSERT INTO Turnos VALUES('Matutino','M'),('Vespertino','V'),('Nocturno','N');")
  except Error as e:
    print (e)
  except:
    print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
  finally:
    conn.close()

Crear_tabla ()

# Opcion 1-1
def Registrar_Reservacion ():
    while True:
        try:
            print ("************* Reservaciones *************")
            valor_clave = int(input("¿Cual es tu clave de cliente? "))
            with sqlite3.connect("PIA.db") as conn:
                mi_cursor = conn.cursor()
                valores = {"IDCLIENTE":valor_clave}
                mi_cursor.execute("SELECT IDCLIENTE, nombre FROM Usuarios WHERE IDCLIENTE = :IDCLIENTE", valores)
                registro = mi_cursor.fetchall()
                
                if registro:
                    for clave, nombree in registro:
                        print (f"{clave}\t")
                else:
                    print(f"No se encontro un usuario con la clave {valor_clave}")
                    return
        except ValueError:
            print ("No se puede dejar vacio")
            print("Reservaciones")
            print("*" * 20)
            print("1. Registrar una reservación\n"+
            "2. Modificar descripción\n"+
            "3. Consultar disponibilidad\n"+
            "4. Eliminar una reservacion\n"+
            "5. Volver al menú principal")
            return
        except:
            print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
        else:
            Nombre = input("Ingresa el nombre de la reservación: ")
            Condicion = Nombre.strip()
            if Condicion == '':
                print("No puedes dejarlo vacio")
                continue
            else:
                insertar_fecha = input("Qué dia quieres reservar?: ")
                Condicion2 = insertar_fecha.strip()
                if Condicion2 == '':
                  print("No puedes dejarlo vacio")
                  return
                else:
                  fecha_registrada = datetime.strptime(insertar_fecha, "%d/%m/%Y").date()
                  fecha_permitida = date.today() + timedelta( days = 2)
                  if fecha_registrada < fecha_permitida:
                      print("Debes hacer la reservacion con 2 dias de anticipación.")
                      continue
                  else:
                      #nivel = rd.randint(1,99)
                      print (f'\n{"*" * 41}')
                      for claveee, nombreee in registro:
                          print(f"ID: {claveee}")
                          print(f"Nombre Cliente: {nombreee}")
                      print(f"Fecha que vas a reservar: {fecha_registrada}\n")

                      mi_cursor.execute("SELECT * FROM Salas;")
                      registro2 = mi_cursor.fetchall()

                      if not registro2:
                          print(" **** No hay salas registradas, necesita registrar una sala ****")
                          ciclo_Reservaciones ()
                          break
                      else:
                          for salas, nombre, capacity in registro2:
                              print(f"{salas}\t{nombre}\t")
                              escoger = input("¿Que sala quieres? ")
                              if not escoger:
                                  print("No existe esa salas registrada")
                              else:
                                  letra = input("Que horario quieres? [M, V, N]: ").upper()
                                  if letra == "M":
                                      Horario = "Matutino"
                                  elif letra == "V":
                                      Horario = "Vespertino"
                                  elif letra == "N":
                                      Horario = "Nocturno"
                              try:
                                  with sqlite3.connect("PIA.db") as conn:
                                      mi_cursor = conn.cursor()
                                      Hola={"nombre_evento":Nombre,"horario":Horario,"fecha":fecha_registrada,"IDCLIENTE":valor_clave,"nombreSala":escoger}
                                      mi_cursor.execute("INSERT INTO Reservaciones (nombre_evento,horario,fecha,IDCLIENTE,nombreSala) VALUES(:nombre_evento,:horario,:fecha,:IDCLIENTE,:nombreSala)",Hola)
                              except Error as e:
                                  print (e)
                              except:
                                  print(f"Surgio una falla siendo esta la causa: {sys.exc_info()[0]}")
                              finally:
                                  if (conn):
                                      conn.close()
                                      fecha_consultar = input("Confirma la fecha (dd/mm/aaaa): ")
                                      ciclo_Reservaciones ()
                                      return
                                  else:
                                            fecha_consultar = datetime.strptime(fecha_consultar, "%d/%m/%Y").date()
                                            print("¡Reservacion Realizada con exito!")
                                            try:
                                                with sqlite3.connect("PIA.db", detect_types = sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES) as conn:
                                                    mi_cursor = conn.cursor()
                                                    criterios = {"fecha":fecha_consultar}
                                                    mi_cursor.execute("SELECT * FROM Reservaciones WHERE fecha = (:fecha);", criterios)
                                                    registros = mi_cursor.fetchall()
                                            
                                                    if registros:
                                                        print("Clave\t" + "Nombre\t"+ "Horario\t" + "            Fecha\t" + "IDCliente\t"+ "nombreSala\t")
                                                        for folio, nombre, horario, fecha, idcliente, nombreSala in registros:
                                                            print(f"{folio}\t{nombre}\t{horario}\t{fecha}\t{idcliente}\t{nombreSala}")
                                                            ciclo_Reservaciones ()
                                                            return
                                            except sqlite3.Error as e:
                                                print (e)
                                            except Exception:
                                                print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
                                            finally:
                                                if (conn):
                                                    conn.close()
                                                    print("Se ha cerrado la conexión")

#Opcion 2
def modificar_descripciones ():
    while True:
        try:
            llave = input("Cual es el nombre de tu evento actual: ")
            Condicion = llave.strip()
            if Condicion == '':
                print("No puedes dejarlo vacio")
                continue
            else:
                with sqlite3.connect("PIA.db") as conn:
                    mi_cursor = conn.cursor()
                    valores1 = {"nombre_evento":llave}
                    mi_cursor.execute("SELECT * FROM Reservaciones WHERE nombre_evento = :nombre_evento", valores1)
                    registro = mi_cursor.fetchall()

                    if registro:
                        for folio, nombre, horario, fecha, idcliente, nombreSala, Sala in registro:
                            print("Clave\t" + "Nombre\t"+ " Turno\t" + "            Fecha\t"+ "\tIDCLIENTE"+ "\tnombreSala" + "Sala")
                            print(f"{folio}\t{nombre}\t{horario}\t{fecha}\t{idcliente}\t{nombreSala}\t{Sala}")
                    else:
                        print(f"No se encontró una reservacion asociada con la sala {llave}")
                        ciclo_Reservaciones ()
                        return

        except Error as e:
            print (e)
        except:
            print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
        else:
            nuevo_nombre = input("A que nombre lo quieres cambiar?: ")
            id_number = folio
            Turno = horario
            fecha_dt = fecha
            try:
                with sqlite3.connect("PIA.db") as conn:
                    mi_cursor = conn.cursor()
                    Valoores7 = {"folio":id_number, "nombre_evento":nuevo_nombre,"turno":Turno,"fecha":fecha_dt,"IDCLIENTE":idcliente,"nombreSala":nombreSala}
                    mi_cursor.execute("UPDATE Reservaciones SET nombre_evento = (:nombre_evento) WHERE (folio) = (:folio);", Valoores7)
                    print("Modificacion realizada con exito.")
                    ciclo_Reservaciones ()
                    return
            except Error as e:
                print (e)
            except:
                print(f"Surgio una falla siendo esta la causa: {sys.exc_info()[0]}")

#Opcion 3
def consulta_fecha():
                print("*" * 80)
                print("**** Consultar Disponibilidad Salas por fecha ****")
                while True:
                    fecha_str = input("\nIngrese la fecha (DD/MM/YYYY): ")
                    Condicion = fecha_str.strip()
                    if Condicion == '':
                        print("No se puede dejar vacio")
                        continue
                    else:
                        try:
                            with sqlite3.connect("PIA.db") as conn:
                                mi_cursor = conn.cursor()
                                consultar_fecha = datetime.strptime(fecha_str, "%d/%m/%Y").date()
                                consultar_fecha = consultar_fecha.strftime('%Y-%m-%d')
                                mi_cursor.execute(f"""SELECT S.IDSALA, S.nombre, T.Horario
                                                FROM Salas as S, Turnos AS T
                                                WHERE NOT EXISTS (SELECT * FROM Reservaciones AS R WHERE S.IDSALA = R.nombreSala
                                                AND T.Horario = R.horario and fecha = ?);""",(consultar_fecha,))
                                libres = mi_cursor.fetchall()
                        except Error as e:
                            print(e)
                        except Exception:
                            print(f"Ha ocurrido un problema: {sys.exc_info()[0]}")
                        else:
                            print("*" * 43)
                            print(f"\nSalas Disponibles para renta el {consultar_fecha}\n")
                            print(f'{"ID de sala".center(5," "):<5} | {"SALA".center(20," "):<20} | {"Horario".center(10," "):<10} |')
                            print("*" * 43)
                            for clave_sala, nombre, cupo in libres:
                                print(f'{clave_sala:<6}     |  {nombre:<20} |{cupo:<8} |')
                            M_Reservaciones ()
                            return



#Opcion 3
def Registrar_Sala ():
    while True:
        SALA = input("Como se va a llamar la sala?(Escribe SALIR para regresar al menú): ")
        
        Condicion1 = SALA.strip()
        if Condicion1=='':
            print("No puedes dejarlo vacío")
            ciclo_menu_principal ()
            return
        else:
            capacity = int(input("Cual va a ser la capacidad?: "))
            if capacity <1:
                print("Necesitas un minimo de dos digitos para registrarte")
                continue
            try:
                with sqlite3.connect("PIA.db") as conn:
                    mi_cursor = conn.cursor()
                    Valores5={"nombre":SALA,"capacidad":capacity }
                    mi_cursor.execute("INSERT INTO Salas (nombre, capacidad) VALUES(:nombre,:capacidad)",Valores5)
                    print("Sala Registrada!!")
                    ciclo_menu_principal ()
                    return
            except Error as e:
                print (e)
            except:
                print(f"Surgio una falla siendo esta la causa: {sys.exc_info()[0]}")
            finally:
                if (conn):
                    conn.close()

# Opcion 4
def Registrar_Cliente ():
    while True:
        Usuario=input("Ingresa al usuario.: ")
        
        Condicion = Usuario.strip()
        if Condicion=='':
            print("No puedes dejarlo vacio")
            continue
        else:
            try:
                with sqlite3.connect("PIA.db") as conn:
                    mi_cursor = conn.cursor()
                    valores={"nombre":Usuario}
                    mi_cursor.execute("INSERT INTO Usuarios ( nombre) VALUES(:nombre)",valores)
                print("Usuario registrado!")
                break
            except Error as e:
                print (e)
            except:
                print(f"Surgio una falla siendo esta la causa: {sys.exc_info()[0]}")
            finally:
                if (conn):
                    conn.close()

# Opcion 5
def salir_del_programa ():
    while True:
        print ("*"*30)
        print ("Hasta pronto tenga un buen dia")
        print ("*"*30)
        print ("Vuelve a visitarnos pronto")
        print ("*"*30)
        break
# Opcion 8
def eliminar_reservacion ():
    while True:
        try:
            key_code = int(input("Dime tu clave de cliente: "))
            with sqlite3.connect("PIA.db") as conn:
                mi_cursor = conn.cursor()
                valores = {"IDCLIENTE":key_code}
                mi_cursor.execute("SELECT * FROM Usuarios WHERE IDCLIENTE = :IDCLIENTE", valores)
                registro = mi_cursor.fetchall()

                if registro:
                    for clave, nombre in registro:
                        print(f"{clave}\t{nombre}")
                else:
                    print(f"No se encontró una reservacion asociado con la clave {key_code}")
        except Error as e:
            print (e)
        except:
            print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
            ciclo_reportes ()
            return
        else:
            id_sala = input("¿Cual es el id de la sala que quieres eliminar?(Escribe SALIR para regresar al programa): ")
            if id_sala == '':
                continue
            elif id_sala == 'SALIR':
                return
            else:
                Name = input("Cual era tu nombre del evento?: ")
                Turno = input("Escribe tu horario: ")
                fecha_asignada = input("Ingresa la fecha por favor: ")
                fecha_dt = datetime.strptime(fecha_asignada, '%d/%m/%Y')
                fecha_permitida = datetime.now() + timedelta( days =+3)
                if fecha_dt < fecha_permitida:
                    print("Lo siento pero no la puedes cancelar, debes cancelarla con 3 dias de anticipación")
                else:
                    try:
                        with sqlite3.connect("PIA.db") as conn:
                            mi_cursor = conn.cursor()
                            delete = {"folio":id_sala,"nombre_evento":Name,"horario":Turno,"fecha":fecha_dt,"IDCLIENTE":key_code}
                            mi_cursor.execute("DELETE FROM Reservaciones WHERE folio = :folio;", delete)
                            #delete={"folio":id_sala,"nombre":Name,"horario":Turno,"fecha":fecha_dt}
                            #mi_cursor.execute("DELETE FROM Reservaciones WHERE (fecha) = (:fecha);", delete)
                            print("Reservacion eliminada. ¡Lamentamos que hayas decidido cancelar tu evento!")
                            return
                    except sqlite3.Error as e:
                        print (e)
                    except Exception:
                        print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
                    finally:
                        if (conn):
                            conn.close()
                            print("Se ha cerrado la conexión")







def Mi_menú_principal ():
    print("Conexion Establecida")
    #EstablecerConexion ()
    Crear_tabla ()
    print("Menú principal")
    print("*" * 20)
    print("1. Reservaciones\n"+
    "2. Reportes\n"+
    "3. Registrar una sala\n" +
    "4. Registrar un cliente\n" +
    "5. Salir")
    while True:
        try:
            Opcion = int(input("Seleccione el numero de la accion que quiere realizar \n:"))
        except:
            print(f"Ocurrió un problema {sys.exc_info()[0]}")
        else:
            if Opcion == 1:
                M_Reservaciones ()
                #Reservacion_de_prueba ()
            elif Opcion == 2:
                M_Reportes ()
            elif Opcion == 3:
                Registrar_Sala ()
                print("Menú principal")
                print("*" * 20)
                print("1. Reservaciones\n"+
                "2. Reportes\n"+
                "3. Registrar una sala\n" +
                "4. Registrar un cliente\n" +
                "5. Salir")
            elif Opcion == 4:
                Registrar_Cliente ()
                print("Menú principal")
                print("*" * 20)
                print("1. Reservaciones\n"+
                "2. Reportes\n"+
                "3. Registrar una sala\n" +
                "4. Registrar un cliente\n" +
                "5. Salir")
            elif Opcion == 5:
                salir_del_programa ()
                break
            else:
                print("Opción no disponible")

def M_Reservaciones():
    print("Reservaciones")
    print("*" * 20)
    print("1. Registrar una reservación\n"+
    "2. Modificar descripción\n"+
    "3. Consultar disponibilidad\n"+
    "4. Eliminar una reservacion\n"+
    "5. Volver al menú principal")
    while True:
        try:
            OpcionA = int(input("Seleccione el numero de la accion que quiere realizar \n:"))
        except Error as e:
            print (e)
        except:
            print(f"Ocurrió un problema {sys.exc_info()[0]}")
        else:
            if OpcionA == 1:
                Registrar_Reservacion ()
            elif OpcionA == 2:
                modificar_descripciones ()
            elif OpcionA == 3:
                consulta_fecha ()
            elif OpcionA == 4:
                eliminar_reservacion ()
            elif OpcionA == 5:
                ciclo_menu_principal ()
                return
            else:
                print("Eso no esta disponible checa el menú")

def M_Reportes ():
    print("Reportes")
    print("*" * 20)
    print("1. Reporte en pantalla de reservaciones para una fecha\n"+
        "2. Exportar reporte tabular en Excel\n"+
        "3. Volver al menú principal")
    try:
        OpcionB = int(input("Seleccione el numero de la accion que quiere realizar \n:"))
    except Error as e:
        print (e)
    except:
        print(f"Ocurrió un problema {sys.exc_info()[0]}")
    else:
        if OpcionB == 1:
            while True:
                try:
                    fecha_reporte = input("¿De que fecha quieres sacar el reporte? ")
                    fecha_convertida = datetime.strptime(fecha_reporte, '%d/%m/%Y').date()
                    print("*"* 75)
                    print("**            REPORTE DE RESERVACIONES PARA EL DIA", fecha_reporte, "           **")
                    with sqlite3.connect("PIA.db") as conn:
                        mi_cursor = conn.cursor()
                        valores = {"fecha":fecha_convertida}
                        mi_cursor.execute("SELECT * FROM Reservaciones WHERE fecha = :fecha", valores)
                        registrados = mi_cursor.fetchall()
                        if registrados:
                            print("Clave\t" + "Nombre\t"+ "Horario\t" + "  IDCLIENTE\t")
                            for folio, nombre, horario, fecha, idcliente, nombreSala, Sala in registrados:
                                print(f"{folio}\t{nombre}\t{horario}\t{idcliente}\t{nombreSala}")
                                print("************************* FIN DEL REPORTE *************************")
                                ciclo_menu_principal ()
                                return
                except:
                    print(f"{sys.exc_info()[0]}")
                    break
        elif OpcionB == 2:
                try:
                    folios = []
                    fechas = []
                    salas = []
                    clientes = []
                    eventos = []
                    turnos = []
                    try:
                        with sqlite3.connect("PIA.db") as conn:
                            cursor = conn.cursor()
                            cursor.execute(f"""SELECT R.folio, R.fecha, S.IDSALA, U.nombre, R.nombre_evento, R.horario
                                               FROM Reservaciones AS R
                                               INNER JOIN Usuarios AS U ON R.IDCLIENTE = U.IDCLIENTE
                                               INNER JOIN Salas AS S ON S.nombre = S.IDSALA;""")
                            reserva = cursor.fetchall()
                    except Error as e:
                        print(e)
                    except Exception:
                        print(f"Ha ocurrido un problema: {sys.exc_info()[0]}")
                    else:
                        for folio, fecha_reserva, nombre_sala, nombre_cliente, nombre_evento, turno in reserva:
                            folios.append(folio)
                            fechas.append(fecha_reserva)
                            salas.append(nombre_sala)
                            clientes.append(nombre_cliente)
                            eventos.append(nombre_evento)
                            turnos.append(turno)
                        e = {"FOLIO":folios,"FECHA":fechas ,"SALA":salas, "CLIENTE":clientes, "EVENTO":eventos, "TURNO":turnos}
                        try:
                            df = pd.DataFrame(e)
                            df.to_excel('Reporte_Reservaciones.xlsx',index=False)
                        except Error as e:
                            print(e)
                        except Exception:
                            print(" *** ERROR *** Ocurrio un problema para exportar el archivo")
                            input("\nEnter para continuar\n")
                        else:
                            print(f"\nSe ha generado un archivo XLSX en la ruta actual")
                            ciclo_menu_principal ()
                            return
                except PermissionError:
                    print (f"Surgió este problema {sys.exc_info()[0]}, comprueba que el archivo esta cerrado e intentalo de nuevo")
                    ciclo_menu_principal ()

        elif OpcionB == 3:
            ciclo_menu_principal ()
            return
        else:
            print("Eso no esta disponible checa el menú")


def ciclo_menu_principal ():
    print("Menú principal")
    print("*" * 20)
    print("1. Reservaciones\n"+
    "2. Reportes\n"+
    "3. Registrar una sala\n" +
    "4. Registrar un cliente\n" +
    "5. Salir")

def ciclo_reportes ():
    print("Reportes")
    print("*" * 20)
    print("1. Reporte en pantalla de reservaciones para una fecha\n"+
        "2. Exportar reporte tabular en Excel\n"+
        "3. Volver al menú principal")

def ciclo_Reservaciones():
    print("Reservaciones")
    print("*" * 20)
    print("1. Registrar una reservación\n"+
    "2. Modificar descripción\n"+
    "3. Consultar disponibilidad\n"+
    "4. Eliminar una reservacion\n"+
    "5. Volver al menú principal")

open_first = False
try:
    d = open("BD_RESERVACIONES.db",'r')
    d.close()
except FileNotFoundError:
    print("\nCreando una copia de la Base de datos.\n")
    print("\nEspera unos instantes...\n")
    input("\nCarga completada. Presionar enter para empezar.\n")
    open_first = True
finally:
    Mi_menú_principal ()

# Reservacion
# Disponibilidad
# Modificar
# Elimanar
# Reporte
# Reporte en excel
# Sala
# Cliente
# Salir

#fin
