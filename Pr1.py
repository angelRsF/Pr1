import time
import psutil
import os
import subprocess
import pyperclip #para usar los portapapeles


#parte 1
def exploYGestionFicheros():
    try:
        #Itero sobre todos los procesos del sistema
        for proc in psutil.process_iter():
            # Obtengo el nombre y el PID de cada proceso
            processName = proc.name()
            processID = proc.pid
            processMemory= proc.memory_percent()
            # Imprimimos el nombre y PID de cada proceso
            print(processName, ' --> ', processID,
                  "\nMemoria --> ", processMemory)

        #Variable de salida del bucle While
        salida=False


        while(salida==False):
            #Menú
            print()
            print("Si desea finalizar un proceso escriba 1.")
            print("Si desea salir del programa escriba otro número.")

            #Elección del usuario introduciendo número por pantalla
            try:
                eleccion=int(input())
            except ValueError as e:
                print("Introduzca solo números enteros.")

            #finalizar proceso
            if eleccion==1:
                print("Introduzca el PID del proceso que desee finalazar: ")
                try:
                    processIDfinalizar=int(input())
                except ValueError as e:
                    print("Introduzca solo números enteros.")

                #itero para encontrar el proceso con mismo PID que el introducido
                for proc in psutil.process_iter():
                    processName = proc.name()
                    processID = proc.pid

                    #condicion que compara los PID
                    try:
                        if processIDfinalizar ==processID:
                            psutil.Process(processIDfinalizar).terminate() #finaliza el proceso
                            time.sleep(1)
                            print("El proceso ", processName, " fué finalizado con éxito.")
                    except psutil.NoSuchProcess as e:
                        print("Proceso no encontrado o inexistente")

            #salida del bucle
            else:
                print("¡Gracias por usar este programa!")
                salida=True

    except Exception as e:
        print("Ocurrió un error, se finalizó el programa.")

#parte 2
def comunicacionInterprocesos():
    readFd, writeFd = os.pipe()
    archivo = 'texto.txt'#en mi caso está creado el archivo en la misma carpeta que el programa

    # Crear proceso hijo
    pid = os.fork()

    if pid > 0:
        # Proceso padre
        os.close(readFd)

        # Leer y enviar el contenido del archivo
        with open(archivo, 'r') as file:
            contenido = file.read()
        os.write(writeFd, contenido.encode())
        os.close(writeFd)

        # Leer el resultado del hijo
        readFd, writeFd = os.pipe()
        os.close(writeFd)
        resultado = os.read(readFd, 1024).decode()
        print("Resultado del hijo:", resultado)
    else:
        # Proceso hijo
        os.close(writeFd)

        # Leer el contenido del archivo del padre
        contenido = os.read(readFd, 1024).decode()
        os.close(readFd)

        # Contar líneas y palabras
        lineas = contenido.count('\n')
        palabras = len(contenido.split())

        # Enviar el conteo de vuelta al padre
        readFd, writeFd = os.pipe()
        os.close(readFd)
        resultado = (f"Líneas: ",lineas," Palabras: ",palabras)
        os.write(writeFd, resultado.encode())
        os.close(writeFd)


#parte 3
def ejecucionSincYAsinc():
    print("Introduzca la letra s si desea ejecutar Notepad de forma síncrona.")
    print("Introduzca la letra a si desea ejecutar Notepad de forma asíncrona.")
    modo = input()

    if modo.lower() == 's':
        #ejecución síncrona
        inicio = time.time()
        subprocess.run("notepad.exe")
        fin = time.time()
        print(f"Ejecución síncrona: ",fin - inicio," segundos.")

    elif modo.lower() == 'a':
        #ejecución asíncrona
        inicio = time.time()
        proceso = subprocess.Popen("notepad.exe")
        fin = time.time()
        print(f"Ejecución asíncrona",fin - inicio," segundos.")
    else:
        print("La letra introducida no es válida.")


#parte 4
def trasnferenciaDatosManipuPortapapeles():
    ftpCommand = [
        "ftp",
        "-n",
        "ftp.dlptest.com"  #cambia por un servidor FTP válido
    ]
    ftpProcess = subprocess.Popen(ftpCommand, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    #autenticación en FTP
    ftpProcess.stdin.write(b"user anonymous\n")
    ftpProcess.stdin.write(b"pass anonymous@\n")
    ftpProcess.stdin.write(b"get testfile.txt\n")
    ftpProcess.stdin.write(b"bye\n")
    ftpProcess.stdin.flush()
    ftpProcess.communicate()

    #lectura del archivo descargado y copiar al portapapeles
    with open("testfile.txt", "r") as file:
        contenido = file.read()
        pyperclip.copy(contenido)

    #monitoreo del portapapeles
    contenidoAnterior = contenido
    while True:
        time.sleep(5)  # Verificar cada 5 segundos
        contenidoACtual = pyperclip.paste()
        if contenidoACtual != contenidoAnterior:
            print("El contenido del portapapeles ha cambiado.")
            contenidoAnterior = contenidoACtual


#función para el menú del main
def main():
    print("Introduce el número según lo que desees hacer:")
    print("1 -> Exploración y Gestion de Procesos")
    print("2 -> Comunicación Interprocesos con Pipes")
    print("3 -> Ejecución de Programas Síncrona y Asíncrona")
    print("4 -> Automatización con FTP y Portapapeles")

    eleccion= input()

    if eleccion == '1':
        exploYGestionFicheros()
    elif eleccion == '2':
        comunicacionInterprocesos()
    elif eleccion == '3':
        ejecucionSincYAsinc()
    elif eleccion == '4':
        trasnferenciaDatosManipuPortapapeles()
    else:
        print("La opción introducida no es válida.")

if __name__ == "__main__":
    main()