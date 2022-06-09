import socket, time, os

# Constants
HOST = "localhost"
PORT = 5000
BUFFER_SIZE = 1024

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

if client_socket.connect:
    data = client_socket.recv(1024)
    data = data.decode()
    while True:
        command = input("Input your command > ")
        cmd = command.split()[0]

        if cmd == "USER":
            username = input("Input username: ")
            cmduser = 'USER {}'.format(username)
            client_socket.send(cmduser.encode())
            user_msg = client_socket.recv(4096)
            print(user_msg.decode())
            
            password = input("Input password: ")
            cmdpass = 'PASS {}'.format(password).encode()
            client_socket.send(cmdpass)
            user_msg = client_socket.recv(1024)
            print(user_msg.decode())
        
        elif cmd == "QUIT":
            client_socket.send(cmd.encode())
            user_msg = client_socket.recv(10000)
            print(user_msg.decode())
            break
        
        elif cmd == "PWD":
            client_socket.send(cmd.encode())
            user_msg = client_socket.recv(10000)
            print(user_msg.decode())

        elif cmd == "HELP":
            client_socket.send(cmd.encode())
            user_msg = client_socket.recv(10000)
            print(user_msg.decode())

        elif cmd == "LIST":
            client_socket.send(cmd.encode())
            user_msg = client_socket.recv(10000)
            print(user_msg.decode())
        
        elif cmd == "MKD":
            foldername = input("Input directory name to be created: ")
            command = ('MKD {}'.format(foldername).encode())
            client_socket.send(command)
            user_msg = client_socket.recv(10000)
            print(user_msg.decode())
        
        elif cmd == "RMD":
            foldername = input("Input directory name to be removed: ")
            command = ('RMD {}'.format(foldername).encode())
            client_socket.send(command)
            user_msg = client_socket.recv(10000)
            print(user_msg.decode())

        elif cmd == "STOR":
            fn = input("Input file name to be uploaded: ")
            command = ("STOR {}".format(fn))
            client_socket.send(command.encode())

            file_name = command.split()[1]
            local = os.getcwd()
            upload = os.path.join(local, file_name)
            check = os.path.isfile(upload)
            file_size = os.path.getsize(upload)

            client_socket.send(str(check).encode())
            client_socket.send(str(file_size).encode())

            if check:
                user_msg = client_socket.recv(4096)
                print(user_msg.decode())
 
                with open(upload, 'rb') as f:
                    data = f.read()
                    print(f.read())
                client_socket.sendall(data)

            user_msg = client_socket.recv(4096)
            print(user_msg.decode())

        elif cmd == 'RETR':
            fn = input("Input file name to be downloaded: ")
            command = ("RETR {}".format(fn))
            client_socket.send(command.encode())

            file_name = command.split()[1]
            local = os.getcwd()
            download = os.path.join(local, file_name)
            check = client_socket.recv(4).decode()
            file_size = int(client_socket.recv(BUFFER_SIZE).decode())

            data=""
            
            if check == 'True':
                print("masuk")
                accepted = ''.encode()

                with open(download, 'wb') as file:
                    while file_size > len(accepted):
                        data = client_socket.recv(BUFFER_SIZE*4)
                        # print(data)
                        if not data:
                            break
                        accepted += data
                        file.write(data)
                        # file_size -= len(data)
                        
            user_msg = client_socket.recv(BUFFER_SIZE*4)
            print(user_msg.strip().decode())

        elif cmd == 'RNFR':
            fn = input("Input file or directory name to be renamed: ")
            command = ("RNFR {}".format(fn).encode())

            client_socket.send(command)
            user_msg = client_socket.recv(10000)
            print(user_msg.decode())

            if '350' in user_msg.decode():
                new = input("Input new file or directory name: ")
                command = ("RNTO {}".format(new).encode())
                client_socket.send(command)
            
            user_msg = client_socket.recv(10000)
            print(user_msg.decode())
        
        elif cmd == "DELE":
            file_name = input("Input file name to be deleted: ")
            command = ('DELE {}'.format(file_name).encode())
            client_socket.send(command)
            user_msg = client_socket.recv(10000)
            print(user_msg.decode())
                        

client_socket.close()
