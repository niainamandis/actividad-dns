import socket
import dnslib 

def parse_dns(message):
  # parseamos primero con dnslib
  d = dnslib.DNSRecord.parse(message)

  # nombre del dominio consultado
  qname = d.questions[0].qname

  # contadores: se obtienen midiendo el tamaño de las listas
  ancount = len(d.rr)     # respuestas
  nscount = len(d.auth)   # registros de autoridad
  arcount = len(d.ar)     # registros adicionales

  # secciones
  answer_section = d.rr       
  authority_section = d.auth  
  additional_section = d.ar  

  # almacenamos y retornamos un diccionario 
  return {
    "Qname": qname,
    "ANCOUNT": ancount,
    "NSCOUNT": nscount, 
    "ARCOUNT": arcount,
    "Answer": answer_section, 
    "Authority": authority_section,
    "Additional": additional_section,
  }

if __name__ == "__main__":
  # setup inicial del proxy
  buff_size = 8129 
  IP_VM = "127.0.1.1" # amandis 192.168.64.2
                      # dani 10.0.2.15
                      # localhost 127.0.1.1
  socket_address = (IP_VM, 8000)

  print(f"Creando socket servidor en {IP_VM}:8000")
  # creamos un socket no orientado a conexión
  dgram_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

  dgram_socket.bind(socket_address)

  print("Esperando consultas DNS...")

  while True:
    # recibimos el mensaje junto con su origen 
    message, address = dgram_socket.recvfrom(buff_size)

    # parseamos el mensaje
    parsed_req = parse_dns(message)

    print(f"Mensaje obtenido de {address}")
    print(f"Contenido: {parsed_req}")
