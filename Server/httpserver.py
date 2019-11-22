import socketserver
import time         # to know current time
import mimetypes    # to map filenames to MIME types
import headers      # your module 'headers.py'
import io
import os

class HTTPHandler(socketserver.StreamRequestHandler):
    def handle(self):
        # read a request message
        buffer = self.request.recv(1024).strip()
        file = io.BytesIO(buffer)
        request_headers = headers.parse_headers(file)
        # print('request_headers: ', request_headers)

        # read content from file name: '.' + path   
        PATH = ''
        PATH = request_headers['PATH']

        METHOD = ''
        METHOD = request_headers['METHOD']

        senddata=b'\r\n'
        print(PATH,METHOD)

        if METHOD != 'GET':
            PATH = '/notget.html'

        print(PATH,METHOD)

        if PATH == '/public/index.html':
            f = open('./public/index.html', 'rb')
        elif PATH:
            if PATH == '/css/style.css' or PATH == '/favicon.ico':
                f = open('./public' + PATH, 'rb')
            elif PATH == '/notget.html':
                f = open('./public' + PATH, 'rb')
            elif os.path.isfile("." + PATH):
                f = open('.'+PATH, 'rb')
            else:
                f = open('./public/404.html', 'rb')
        else:
            f = open('./public/404.html', 'rb')
        
        data = f.read(1024)

        while data:
            senddata+=data
            data = f.read(1024)
        f.close()  

        # Build the response message
        res_status_line = ''
        res_status_line = 'HTTP/1.1 404 Not found'

        res_headers = {}
        res_headers['Date'] = time.asctime()
        res_headers['Server'] = 'MyServer/1.0'
        res_headers['Accept-range'] = 'bytes'

        if PATH == '/public/index.html':
            f = open('./public/index.html', 'rb')
            res_headers['Content-type'] = 'text/html'
            res_headers['Content-Length'] = str(os.path.getsize('./public'+'/index.html'))
            res_status_line = 'HTTP/1.1 200 OK\r\n'
        elif PATH:
            if PATH == '/css/style.css' or PATH == '/favicon.ico':
                f = open('./public' + PATH, 'rb')
                res_headers['Content-type'] = mimetypes.guess_type('./public' + PATH)[0]
                res_headers['Content-Length'] = str(os.path.getsize('./public'+PATH))
                res_status_line = 'HTTP/1.1 200 OK\r\n'
            elif os.path.isfile("." + PATH):
                f = open('.'+PATH, 'rb')
                res_headers['Content-type'] = mimetypes.guess_type(PATH)[0]
                res_headers['Content-Length'] = str(os.path.getsize('.'+PATH))
                # res_headers['Content-Length'] = '10000'
                res_status_line = 'HTTP/1.1 200 OK\r\n'
            else:
                f = open('./public/404.html', 'rb')
                res_headers['Content-type'] = 'text/html'
                res_headers['Content-Length'] = str(os.path.getsize('./public'+'/404.html'))
        else:
            f = open('./public/404.html', 'rb')
            res_headers['Content-type'] = 'text/html'
            res_headers['Content-Length'] = str(os.path.getsize('./public'+'/404.html'))
            if PATH == '/notget.html':
                res_headers['Content-Length'] = str(os.path.getsize('./public'+'/notget.html'))

            
        for k in res_headers:
            line = k+': '+res_headers[k]+'\r\n'
            res_status_line += line

        sbuff = res_status_line.encode()
        sbuff += senddata
        self.wfile.write(sbuff)    
        self.wfile.flush()  # Flush-out output buffer for immediate sending
    
# create a TCPServer object with your handler class
http_server = socketserver.TCPServer(('', 8082), HTTPHandler)
http_server.serve_forever()