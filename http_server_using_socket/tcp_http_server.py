import os
import socket

HOST = ''
PORT = 8080

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(1)
    print('Start server')
    while True:
        try:
            conn, addr = s.accept()
            with conn:
                print(f'Connected by {addr}')
                data = conn.recv(1500)
                ptr = data.find('\r\n'.encode('utf-8'))
                header = data[:ptr]
                left = data[ptr:]
                request = header.decode('utf-8')
                method, path, protocol = request.split(' ')
                print(f'Received: {method} {path} {protocol}')
                if not data:
                    break
                if path == '/':
                    path = '/index.html'
                path = f'.{path}'
                if not os.path.exists(path):
                    header = 'HTTP/1.1 404 Not Found\r\n'
                    header = f'{header}Server: Our server\r\n'
                    header = f'{header}Connection: close\r\n'
                    header = f'{header}Content-Type: text/html;charset=utf-8\r\n'
                    header = f'{header}\r\n'
                    header = header.encode('utf-8')
                    body = ''.encode('utf-8')
                else:
                    ext = os.path.splitext(path)[-1].lower()
                    with open(path, 'r') as f:
                        body = f.read()
                        body = body.encode('utf-8')
                    header = 'HTTP/1.1 200 OK\r\n'
                    header = f'{header}Server: Our server\r\n'
                    header = f'{header}Connection: close\r\n'

                    if ext == '.html':
                        header = f'{header}Content-Type: text/html;charset=utf-8\r\n'
                    elif ext == '.css':
                        header = f'{header}Content-Type: text/css;charset=utf-8\r\n'
                    elif ext == '.js':
                        header = f'{header}Content-Type: text/javascript;charset=utf-8\n\n'
                    elif ext == './jpg' or ext == '.jpeg':
                        header = f'{header}Content-Type: image/jpeg\r\n'
                    elif ext == './png':
                        header = f'{header}Content-Type : image/png\r\n'
                    header = f'{header}Content-Length: {len(body)}\r\n'
                    header = f'{header}\r\n'
                    header = header.encode('utf-8')
                response = header + body
                conn.sendall(response)

        except KeyboardInterrupt:
            print('Shutdown server')
            break
