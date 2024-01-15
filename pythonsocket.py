import socket

URL = 'www.naver.com'
PORT = 80


def main():
    url = f'{URL}:{PORT}'
    print('보낼 데이터 입력!')
    print('종료는 Ctrl+C')
    content = ''
    try:
        while True:
            line = input('<')
            content = f'{content}{line}\r\n'
    except KeyboardInterrupt:
        print('입력 완료! 입력된 내용:')
        print(f'{content}')


    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((URL, PORT))
        s.sendall(content.encode('utf-8'))
        response = b''
        while True:
            data = s.recv(1500)
            if len(data) == 0:
                break
            response = response + data
        res = response.decode('utf-8')
        print('응답 도착!:')
        print(f'{res}')

if __name__ == '__main__':
    main()
