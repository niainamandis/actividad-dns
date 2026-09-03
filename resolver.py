import socket
import dnslib

if __name__ == "__main__":
  # setup inicial del proxy
  buff_size = 8129 
  IP_VM = "192.168.64.2" # amandis 192.168.64.2
                         # dani 10.0.2.15
  socket_address = (IP_VM, 8000)

  print(f"Creando socket servidor en {IP_VM}:8000")
  # creamos un socket no orientado a conexión
  dgram_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

  dgram_socket.bind(socket_address)

  print("Esperando consultas DNS...")

  while True:
    # recibimos el mensaje junto con su origen 
    message, address = dgram_socket.recvfrom(buff_size)

    print(f"Mensaje obtenido de {address}: {message}")
