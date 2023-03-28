import socket

IP = input("entre com o endereço de IP: ")

def ping(IP):
    try:
        socket.setdefaulttimeout(5)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = IP
        s.connect((host, 80))
        s.shutdown(socket.SHUT_RDWR)
        return True
    except:
        return False
result = ping(IP)
print(result)