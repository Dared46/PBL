import socket
import _thread as thread
import time

#lista de dispositivos conectados, contendo o id, status e endereço
list_device = []
#status inicial do servidor
status = 'sem dispositivos'
#variável que controla o envio de comandos
comandos = 0

#instanciamento e configuração do servidor, passando ip e porta como parametros
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('localhost',1234))
s.listen(5)

#função responsável por controlar as solicitações do cliente
def manager_client(clientsocket):
    #essas variáveis são específicas de cada thread
    topics = ''
    client_topics = []
    global status
    global comandos

    while True:
        #laço responsável por recever solicitações de operações e iniciar a execução das mesmas
        data = clientsocket.recv(1024)
        a = data.decode('utf-8')
        #estruturas condicionais responsáveis por diferenciar qual ação o usuário deseja fazer
        if(a == '1'):
            #envia os status dos topicos em que o cliete está inscrito
            if (len(list_device) > 0):
                for i in range(len(list_device)):
                    if(i in client_topics):
                        topics += 'lampada '+ str(list_device[i][1]) +': '+ str(list_device[i][0]) + '\n'

                clientsocket.send(bytes(topics, 'utf-8'))
                topics = ''
                print('Dados enviados com sucesso')
            else:
                a = 'Voce nao esta inscrito em topicos'
                clientsocket.send(bytes(a, 'utf-8'))

        elif (a == '2'):
            #executa comandos, enviando informações a serem atualizadas no publisher
            if (comandos ==0):
                comandos = 1
            else:
                comandos = 0

        elif (a == '3'):
            #envia a lista de lampadas conectadas ao servidor
            if (len(list_device)>0):
                for i in range(len(list_device)):
                    topics += 'lampada '+ str(list_device[i][1]) + '\n'

                clientsocket.send(bytes(topics, 'utf-8'))
                topics = ''
                print('Dados enviados com sucesso')

            else:
                a = 'Nao ha dispositivos conectados'
                clientsocket.send(bytes(a, 'utf-8'))

        elif(a=='4'):
            #adiciona à lista de topicos especifica de cada thread determinado topico, o cliente escolhe, envia pra essa thread e ela add à lista
            data = clientsocket.recv(1024)
            topico = data.decode('utf-8')
            client_topics.append(int(topico))
            print('cliente se conectou a lampada '+ topico)

        elif (a == '5'):
            #remove topicos da lista de topicos da thread
            data = clientsocket.recv(1024)
            topico = data.decode('utf-8')
            del(client_topics[int(topico)])
            print('cliente se conectou a lampada ' + topico)

#função responsável por controlar o tráfego de dados realizados entre o servidor e as lampadas
def manager_device(clientsocket, address):
    global status
    clientsocket.send(bytes(status, 'utf-8'))
    data = clientsocket.recv(1024)
    a = data.decode('utf-8')
    status = a

    #id de cada lampada
    id = len(list_device)
    #lista que vai salvar o id, status e endereço da lampada da thead em execução
    device=[]
    device.append(a)
    device.append(id)
    device.append(address)
    list_device.append(device)

    #imprimindo no terminal os status das lampadas conectadas
    for i in range(len(list_device)):
        print('Dispositivo ' + str(list_device[i][1]) + ' : ' + list_device[i][0])

    #laço que fica recebendo atualizações do publisher e atualizando na lista
    while True:
        time.sleep(6)
        data = clientsocket.recv(1024)
        b = data.decode('utf-8')
        list_device[id][0] = b
        #quando o usuário solicita o comando esse if é ativado e manda comando para as lampadas
        if (comandos == 1):
            clientsocket.send(bytes(status, 'utf-8'))
        for i in range (len(list_device)):
            print('Dispositivo ' + str(list_device[i][1]) +' : ' + str(list_device[i][0]))

#função que vai controlar as conecções de clientes e dispositivos
def inicia():
    global list_device
    while True:
        #aceita a conexão e cria um socket para a msm
        clientsocket, address = s.accept()
        print('server conectado por: ', address)
        data = clientsocket.recv(1024)
        tipo = data.decode('utf-8')
        #Se for um cliente normal, inicia uma nova thread de clientes
        if (tipo == 'c'):
            print('Tipo: Cliente')
            thread.start_new_thread(manager_client,(clientsocket,))
        #Se for um dispositivo, inicia uma nova thread de dispositivo
        elif (tipo == 'd'):
            print('Tipo: Dispositivo')
            thread.start_new_thread(manager_device, (clientsocket, address))



inicia()