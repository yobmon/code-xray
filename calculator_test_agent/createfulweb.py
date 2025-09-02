
from http.server import BaseHTTPRequestHandler, HTTPServer
import cgi

class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"""
        <html>
        <head>
            <title>Simple Form</title>
        </head>
        <body>
            <form method="post">
                <label>Name: <input type="text" name="name"></label><br>
                <button type="submit">Submit</button>
            </form>
        </body>
        </html>
        """)

    def do_POST(self):
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD':'POST', 'CONTENT_TYPE':self.headers['Content-Type']}
        )

        name = form.getvalue("name")

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"<html><body><h1>Hello, " + name.encode() + b"!</h1></body></html>")



server_address = ('', 8000)
httpd = HTTPServer(server_address, MyHandler)
print('Starting server...')
httpd.serve_forever()
