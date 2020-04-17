import socket, time
import _thread as thread

#configuração e instanciação da socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#definição do ip e porta
s.connect(('localhost', 1234))
print('conectado com exito')
#status inicial do dispositivo
status  = 'desligado'
#tipo do dispositivo, responsável por ajudar o servidor a diferencia se é cliente ou dispositivo
tipo = 'd'

s.send(bytes(tipo, 'utf-8'))
data = s.recv(1024)

a  = data.decode('utf-8')

s.send(bytes(status, 'utf-8'))

#função que vai ser ativada como thread para ficar constantemente recebendo dados do servidor
#ela será a responsável por recebimento de comandos
def listen():
    global status
    while True:
        data = s.recv(1024)
        a = data.decode('utf-8')
        status = a
        print('dados atualizados: '+ a)


thread.start_new_thread(listen, ())

#fica periodicamente mudando o status e enviando pro servidor
while True:
    #envia dados de 6 em 6 segundos
    time.sleep(6)

    if (status == 'desligado'):
        status = 'ligado'
        s.send(bytes(status, 'utf-8'))

    elif (status == 'ligado'):
        status = 'desligado'
        s.send(bytes(status, 'utf-8'))