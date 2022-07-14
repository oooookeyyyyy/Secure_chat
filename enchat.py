from socket import socket , AF_INET , SOCK_STREAM
from random import choice, randint
from colorama import Fore, Back
from threading import Thread
from time import ctime
from os import system
from qaes import aes

def bind(port, passwrd) :
    s = socket(AF_INET, SOCK_STREAM)
    s.bind(('', port))
    print('Done! Waiting for opponent...')
    s.listen(5)
    while True :
        conn, addr = s.accept()
        file = open(str(addr[0])+'.txt','a')
        file.write(ctime()+'\n')
        file.close()
        password = conn.recv(1024).decode('utf-8')
        password = decrypt(password)
        if password != passwrd :
            conn.send(b'')
            conn.close()
        else :
            conn.send(b'1')
            system('cls')
            print(addr[0]+' Connected!')
            def send_message():
                while True :
                    try :
                        send = input('\n')
                        if send == '' :
                            continue
                        file = open(str(addr[0])+'.txt','a')
                        file.write(ctime().split()[3]+' >> '+send+'\n')
                        file.close()
                        send = encrypt(send)
                        conn.send(bytes(send , 'utf-8'))
                    except :
                        print(addr[0]+' has left the chat!')
                        break
                s.close()
            def receive_message() :
                while True :
                    try :
                        receive = conn.recv(10240).decode('utf-8')
                        receive = decrypt(receive)
                        file = open(str(addr[0])+'.txt','a')
                        file.write(ctime().split()[3]+' << '+receive+'\n')
                        file.close()
                        print('\n' + '     '*12 + Fore.BLUE + Back.CYAN + receive + Fore.WHITE + Back.BLACK)
                    except :
                        break
            Thread(target=send_message).start()
            Thread(target=receive_message).start()
            break

def connect(ip, port, passwrd) :
    try :
        s = socket(AF_INET, SOCK_STREAM)
        s.connect((ip, port))
        file = open(str(ip)+'.txt','a')
        file.write(ctime()+'\n')
        file.close()
        passwrd = encrypt(passwrd)
        s.send(bytes(passwrd , 'utf-8'))
        if not s.recv(1024) :
            s.close()
            print('\n Wrong password')
            system('pause')
            main()
        else :
            system('cls')
            print('connected to '+ip)
            def send_message():
                while True :
                    try :
                        send = input('\n')
                        if send == '' :
                            continue
                        file = open(str(ip)+'.txt','a')
                        file.write(ctime().split()[3]+' >> '+send+'\n')
                        file.close()
                        send = encrypt(send)
                        s.send(bytes(send , 'utf-8'))
                    except :
                        print(ip+' has left the chat!')
                        break
                s.close()
            def receive_message() :
                while True :
                    try :
                        receive = s.recv(10240).decode('utf-8')
                        receive = decrypt(receive)
                        file = open(str(ip)+'.txt','a')
                        file.write(ctime().split()[3]+' << '+receive+'\n')
                        file.close()
                        print( '\n' + '     '*12 + Fore.BLUE + Back.CYAN + receive + Fore.WHITE + Back.BLACK)
                    except :
                        break
            Thread(target=send_message).start()
            Thread(target=receive_message).start()
    except :
        print(ip+' is offline!')
        system('pause')
        main()

def encrypt(text) :
    def e(text) :
        chars = ['2','f','*','t',':','n','g','F','u','Z','T','8','9','a','C','"','7','h','0','y','K','[','/','d','B','c','6','w','k','@','H','P',' ','_',')','m','A','v','$','=','j','r','{','z','x','R','3','&','e','Q','Y','|','q',';','(','.','S','M','D','o','5','#','}','~','V','^','+','s',"'",'L','X','O','G','E','<','>','W','U','?','1','l','J','4','I',',','-',']','N','!','p','\\','b','`','i','%']
        encrypt = ''
        for ch in text :
            if ch in chars :
                ind = chars.index(ch)
                rand = randint(1,92)
                chert = randint(1,9)
                if rand < 10 :
                    srand = '0'+str(rand)
                else :
                    srand = str(rand)
                Sum = ind+rand
                if Sum > 93 :
                    Sum -= 94
                enc = chars[Sum]
                encrypt += chars[rand]+srand+enc
        for n in range(chert) :
            encrypt += choice(chars)
        encrypt += str(chert)
        return encrypt
    rep = choice([1,2])
    if rep == 1 :
        state = str(choice([1, 3, 5, 7, 9]))
        return state+aes.encrypt(e(text))
    else :
        state = str(choice([0, 2, 4, 6, 8]))
        return state+e(e(text))

def decrypt(text) :
    def d(text) :
        chars = ['2','f','*','t',':','n','g','F','u','Z','T','8','9','a','C','"','7','h','0','y','K','[','/','d','B','c','6','w','k','@','H','P',' ','_',')','m','A','v','$','=','j','r','{','z','x','R','3','&','e','Q','Y','|','q',';','(','.','S','M','D','o','5','#','}','~','V','^','+','s',"'",'L','X','O','G','E','<','>','W','U','?','1','l','J','4','I',',','-',']','N','!','p','\\','b','`','i','%']
        decrypt = ''
        dec = []
        chert = int(text[-1])
        text = text[:-(chert+1)]
        while text :
            dec.append(text[1:4])
            text = text[4:]
        for ch in dec :
            char = ch[2]
            key = int(ch[:2])
            ind = chars.index(char)
            Sum = ind - key
            if Sum < 0 :
                Sum += 94
            decrypt += chars[Sum]
        return decrypt
    rep = int(text[0])
    if rep % 2 != 0 :
        return d(aes.decrypt(text[1:]))
    else :
        return d(d(text[1:]))

def main() :
    system('cls')
    print('''\n
    ███╗   ███╗ █████╗ ███╗   ███╗ █████╗ ██████╗  ██████╗ ███████╗ MMD SecreT Messenger
    ████╗ ████║██╔══██╗████╗ ████║██╔══██╗██╔══██╗██╔═══██╗██╔════╝ 
    ██╔████╔██║███████║██╔████╔██║███████║██║  ██║██║   ██║█████╗   TeL : @Amo_codzan
    ██║╚██╔╝██║██╔══██║██║╚██╔╝██║██╔══██║██║  ██║██║   ██║██╔══╝   
    ██║ ╚═╝ ██║██║  ██║██║ ╚═╝ ██║██║  ██║██████╔╝╚██████╔╝██║      VersioN 1.69
    ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝╚═════╝  ╚═════╝ ╚═╝      
    \n''')
    system('pause')
    system('cls')
    inp = input('''
    [1] Bind A server
    [2] Connect to host
    [3] Exit
 >> ''')
    if inp == '1' :
        system('cls')
        port = int(input('\n Set port >>'))
        passwrd = input('\n set password >>')
        bind(port , passwrd)
    elif inp == '2' :
        system('cls')
        ip = input('\n Set ip >>')
        port = int(input('\n Set port >>'))
        passwrd = input('\n enter password >>')
        connect(ip, port , passwrd)
    elif inp == '3' :
        exit()
    else :
        main()

if __name__ == '__main__':
    main()