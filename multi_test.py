from djitellopy import Tello
import socket
import time

drone_socket_1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
drone_socket_1.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 'Wi-Fi'.encode())

drone_socket_2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
drone_socket_2.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 'Adaptor'.encode())

drone_socket_1.sendto('command'.encode(), 0, ('192.168.10.1', 8889))
drone_socket_2.sendto('command'.encode(), 0, ('192.168.10.1', 8889))

drone_socket_1.sendto('takeoff'.encode(), 0, ('192.168.10.1', 8889))
drone_socket_2.sendto('takeoff'.encode(), 0, ('192.168.10.1', 8889))

time.sleep(5)

# drone_socket_1.sendto('command'.encode(), 0, ('192.168.10.1', 8889))
# drone_socket_2.sendto('command'.encode(), 0, ('192.168.10.1', 8889))

drone_socket_1.sendto('land'.encode(), 0, ('192.168.10.1', 8889))
drone_socket_2.sendto('land'.encode(), 0, ('192.168.10.1', 8889))

# tello1 = Tello()
# tello1.connect()
#
# tello2 = Tello()
# tello2.connect()
#
# tello1.takeoff()
# tello2.takeoff()
#
# sleep(4)
#
# tello1.land()
# tello2.land()


