import matplotlib.pyplot as plt
import socket
import numpy as np
from time import sleep


host = "84.237.21.36"
port = 5152


def distance(img):
    res = []
    for y in range(1, img.shape[0] - 1):
        for x in range(1, img.shape[1] - 1):
            neighbors = np.array([img[y + 1, x], img[y, x + 1],
                                                 img[y - 1, x], img[y, x - 1]])
            if img[y,x] > np.max(neighbors):
                res.append(y)
                res.append(x)
    return res


def recvall(sock, n):
    data = bytearray()
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None

        data.extend(packet)

    return data


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect((host, port))

    beat = b"nope"

    plt.ion()
    plt.figure()

    while beat != b"yep":
        flag = False
        sock.send(b"get")
        bts = recvall(sock, 40002)

        img = np.frombuffer(bts[2:], dtype = "uint8").reshape(bts[0], bts[1])
        coords = distance(img)
        
        try:
            result = ((coords[0] - coords[2]) ** 2 + \
                        (coords[1] - coords[3]) ** 2) ** 0.5
        
        except IndexError as err:
            print(f'Ошибка при вычислении результата - {err}')
            result = 0.0
            flag = True
            
        sock.send(f"{round(result, 1)}".encode())
        print(sock.recv(10))
        
        plt.clf()
        plt.imshow(img)
        plt.pause(1)
        if flag: sleep(5)       # чтобы успеть рассмотреть звездочки.
                                       # у других людей код принтит nope,
                                       # а у меня почему-то поднимает
                                       # исключение. сделал такой костыль
                                       # в виде обработчика исключений 
        sock.send(b"beat")
        beat = sock.recv(10)
