import socket

#lista de topicos inscritos pelo cliente
my_topics = []

#instanciação e configuração da socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('localhost', 1234))

#variavel que especifica que é um cliente e não um dispositivo
tipo = 'c'
s.send(bytes(tipo, 'utf-8'))

#menu da aplicação
while True:

    print('1-Ver status, 2-ligar/Desligar, 3 - listar lampadas, 4-Adicionar topicos, 5 - Remover topicos, q-Sair')
    b = input('Digite uma opção a ser realizada: ')
    print('\n')

    if b == 'q': break
    #solicita visualização dos topicos inscritos
    elif (b =='1'):
        if(len(my_topics)>0):
            s.send(bytes(b, 'utf-8'))
            data = s.recv(1024)
            print(data.decode('utf-8'))
        else:
            (print ('Você não está inscrito em topicos \n\n'))

    #envio de comandos aos dispositivos
    elif (b=='2'):
        s.send(bytes(b, 'utf-8'))
        print('Comando enviado \n')

    #Solicita uma lista de todas as lampadas conectadas ao servidor
    elif (b=='3'):
        s.send(bytes(b, 'utf-8'))
        data = s.recv(1024)
        print(data.decode('utf-8')+'\n')

    #envia uma string contendo o numero da lampada que o cliente deseja se inscrever
    elif (b == '4'):
        s.send(bytes(b, 'utf-8'))
        b = input('Digite o numero da lampada que deseja se conectar: ')
        print('\n')
        my_topics.append(b)
        s.send(bytes(b, 'utf-8'))
        print('Voce agora está conectado à lampada ' + b + '\n\n')

    #envia uma string contendo o numero da lampada que o cliente deseja se desinscrever
    elif (b == '5'):
        if (len(my_topics) > 0):
            s.send(bytes(b, 'utf-8'))
            b = input('Digite o numero da lampada que deseja se desconectar: ')
            print('\n')
            s.send(bytes(b, 'utf-8'))
            print('voce agora esta desconectado à lampada ' + b + '\n\n')
            b = int(b)
            del (my_topics[b])
        else:
            print('Não há lâmpadas conectadas \n\n')

    else:
        print('Digite uma opção válida \n\n')
#fecha a conexão
s.close()