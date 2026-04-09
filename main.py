from wsgiref.simple_server import make_server
import subprocess, os

def start_read_daemon(serverid, msgid):
    p = subprocess.run(
        ["serve-daemon.exe", "read", serverid, msgid],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1
    )  
    return p.stdout, p.stderr

def daemon_write(serverid, user, date, title, body):
    try:
        x = sorted(os.listdir(f"db/server/{serverid}"))
    except:
        os.mkdir(f"db/server/{serverid}")
        with open(f"db/server/{serverid}/0000000000000000") as f:
            d = """TheLuckyCuber999
08/04/2026
New Community
Hello, welcome to your new community!"""
            f.write(d)
        x = ["0000000000000000"]
    msgid = "".join(hex(int(x[-1], 16) + 1)[2:])
    p = subprocess.run(
        ["serve-daemon.exe", "write", serverid, msgid, user, date, title, body],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1
    )  
    return p.stdout, p.stderr

def daemon_read(serverid, msgid):
    data, err = start_read_daemon(serverid, msgid)
    data = data.split("\n")

    if "404 not found" in err:
        return {"code":"404 Not Found"}
    else:
        user = data[0]
        date = data[1]
        title = data[2]
        text = "\n".join(data[2+1:])
        return {"user":user, "title":title, "text":text, "date":date, "code":"200 OK"}

def application(environ, start_response):
    global p
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
            dat = daemon_read(path[1], path[2])
            print(dat)
            print(dat["user"], "said: ", dat["title"])
            status = dat["code"]
            with open("global.html") as f:
                x = f.read()
            with open("post.html") as f:
                t = f.read()
                t = x.replace("{PAGEBODY}", t).replace("{PAGETITLE}", f"{dat["title"]} | Demkr, the Democratic Central")
            response_body = f"{t.replace("{BODYTEXT}", dat["text"]).replace("{TITLE}", dat["title"]).replace("{DATE}", dat["date"]).replace("{USER}", dat["user"])}".encode("utf-8")
        else:
            status = '404 Not Found'
            response_body = b"404 Not Found"
    elif request_method == 'POST':
        pass

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
