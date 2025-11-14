from socket import socket

def server_init():
  server = socket(socket.AF_INET, socket.SOCK_STREAM)
  server.bind(('0.0.0.0', 8080))

  server.listen(1)

  while True:
      client, address = server.accept()
      print 'Connected by', address
      data = client.recv(1024)

if __name__ == '__main__':
  server_init()
