from wsgiref.simple_server import make_server
import subprocess

def serve_daemon_read(serverid, msgid):
    p = subprocess.run(
        ["serve-daemon.exe", "read", serverid, msgid],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )  

    data = p.stdout.split("\n")
    err = p.stderr
    if "404 not found" in err:
        return {"code":"404 Not Found"}
    else:
        user = data[0]
        date = data[1]
        title = data[2]
        text = "\n".join(data[2+1:])
        return {"user":user, "title":title, "text":text, "date":date, "code":"200 OK"}

def application(environ, start_response):
    path_info = environ['PATH_INFO']
    path = path_info.split("/")
    if path[0] == "":
        path.pop(0)
    request_method = environ['REQUEST_METHOD']
    
    if path_info == '/':
        status = '200 OK'
        response_body = b"Hello, World!"
    elif request_method == 'GET':
        if path[0] == "s":
            print(path)
            dat = serve_daemon_read(path[1], path[2])
            print(dat)
            print(dat["user"], "said: ", dat["title"])
            status = dat["code"]
            with open("post.html") as f:
                t = f.read()
            response_body = f"{t.replace("{BODYTEXT}", dat["text"]).replace("{TITLE}", dat["title"]).replace("{DATE}", dat["date"]).replace("{USER}", dat["user"])}".encode("utf-8")
        else:
            status = '404 Not Found'
            response_body = b"404 Not Found"

    else:
        status = '404 Not Found'
        response_body = b"404 Not Found"
    
    headers = [('Content-type', 'text/html')]
    start_response(status, headers)
    return [response_body]

print("Starting server...")
httpd = make_server('', 8000, application)
print("Serving on port 8000...")
httpd.serve_forever()
