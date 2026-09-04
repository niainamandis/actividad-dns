import socket
import dnslib 

buff_size = 8129 
root_ip = "198.41.0.4"

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

def resolver(mensaje_consulta:bytes, ip_addr=root_ip, name_server='.') -> bytes:

  #implementando debug
  parsed_consulta = parse_dns(mensaje_consulta)
  qname = str(parsed_consulta["Qname"])
  print(f"(debug) Consultando '{qname}' a '{name_server}' con dirección IP '{ip_addr}'")

  # creamos una variable temp para no interferir con el socket principal
  socket_temp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  socket_temp.sendto(mensaje_consulta, (ip_addr, 53))
  respuesta_bytes, _ = socket_temp.recvfrom(buff_size)
  
  parsed = parse_dns(respuesta_bytes)

  # revisamos si viene una respuesta tipo A en Answer
  for rr in parsed["Answer"]:
    if rr.rtype == dnslib.QTYPE.A:
      return respuesta_bytes
  
  # si no, revisar si hay respuestas de tipo NS
  ns_records = []
  for rr in parsed["Authority"]:
    if rr.rtype == dnslib.QTYPE.NS:
      ns_records.append(rr)
  # si venian ese tipo de respuesta, envíamos la query inicial
  # a la dirección ip contenida en Additional
  if ns_records:
    new_domain = str(ns_records[0].rdata)
    for rr in parsed["Additional"]:
      if rr.rtype == dnslib.QTYPE.A:
        nueva_ip = str(rr.rdata)
        return resolver(mensaje_consulta, nueva_ip, new_domain)

    # si no hay nueva ip, tomamos el nombre de un NameServer
    # y llamamos recursivamente a la función para resolver la IP
    new_query = dnslib.DNSRecord.question(new_domain, qtype="A").pack()
    new_response = resolver(new_query, root_ip, '.')

    if new_response:
      parsed = parse_dns(new_response)
      for rr in parsed["Answer"]:
        if rr.rtype == dnslib.QTYPE.A:
          new_ip = str(rr.rdata)
          return resolver(mensaje_consulta, new_ip, new_domain)

if __name__ == "__main__":
  # setup inicial del proxy
  IP_VM = "10.0.2.15" # amandis 192.168.64.2
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

    """
    # parseamos el mensaje
    parsed_req = parse_dns(message)

    print(f"Mensaje obtenido de {address}")
    print(f"Contenido: {parsed_req}")
    """

    dns_response = resolver(message)
    # ejecutar solo si existe respuesta por si la función retorna None
    if dns_response:
      dgram_socket.sendto(dns_response, address)
