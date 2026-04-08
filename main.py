from wsgiref.simple_server import make_server
import subprocess

def daemon(serverid, msgid):

    p = subprocess.Popen(
        ["serve-daemon.exe", serverid, msgid],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    data = p.stdout.readline()
    meta = p.stderr.readline()

def application(environ, start_response):
    path_info = environ['PATH_INFO']
    request_method = environ['REQUEST_METHOD']
    
    if path_info == '/':
        status = '200 OK'
        response_body = b"Hello, World!"
    elif path_info == '/hello' and request_method == 'GET':
        status = '200 OK'
        response_body = b"Hello from /hello!"
    else:
        status = '404 Not Found'
        response_body = b"404 Not Found"
    
    headers = [('Content-type', 'text/plain')]
    start_response(status, headers)
    return [response_body]

httpd = make_server('', 8000, application)
print("Serving on port 8000...")
httpd.serve_forever()
