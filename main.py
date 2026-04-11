from wsgiref.simple_server import make_server
import subprocess, os, sys, json, random
from datetime import datetime

args = sys.argv[1:]
if args == []:
    port = 8000
else:
    port = args[0]

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
    return msgid

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
    request_method = environ['REQUEST_METHOD']
    if path[0] == "":
        path.pop(0)
    if path == [] or path == [""]:
        with open("index.html") as f:
            response_body = f.read().encode("utf-8")
            headers = [('Content-type', 'text/html')]
            status = '200 OK'
            start_response(status, headers)
            return [response_body]
    
    w = os.listdir("db/server")
    sidebar = "".join(f"<a href=\"/s/{i}\" class=\"sidebarlnk\">s/{i}</a>" for i in w[:min(25, len(w))])
    try:
        rightbar = "".join(f"<a href=\"/post{"" if path[0] == "home" else f"?comm={path[1]}"}\" class=\"newpostbtn\">New Post</a>")
    except:
        rightbar = ""
    topbar = "Demkr: The Democratic Central of the Internet" # temporary (meaning forever)

    def read_global(f, left="") -> str:
        return f.read().replace("{TOPBAR}", topbar).replace("{SIDEBAR}", sidebar).replace("{RIGHTBAR}", rightbar).replace("{MARGIN-LEFT}", left)
    
    if request_method == 'GET':
        if path[0] == "s":
            if path[-1] == "":
                path.pop()
            try:
                dat = daemon_read(path[1], path[2])
                status = dat["code"]
                if status == "404 Not Found":
                    with open("global.html") as f:
                        x = read_global(f)
                    with open("404.html") as f:
                        t = f.read()
                        t = x.replace("{PAGEBODY}", t).replace("{PAGETITLE}", f"Page Not Found | Demkr, the Democratic Central")
                    response_body = t.encode("utf-8")
                else:
                    with open("global.html") as f:
                        x = read_global(f)
                    with open("post.html") as f:
                        t = f.read()
                        t = x.replace("{PAGEBODY}", t).replace("{PAGETITLE}", f"{dat["title"]} | Demkr, the Democratic Central")
                        t = t.replace("{TOPIC}", path[1])
                    response_body = f"{t.replace("{BODYTEXT}", dat["text"]).replace("{TITLE}", dat["title"]).replace("{DATE}", dat["date"]).replace("{USER}", dat["user"]).replace("{path[2]}", f"{path[2]}")}".encode("utf-8")
            
            except IndexError:
                with open("global.html") as f:
                    x = read_global(f)
                with open("topicpage.html") as f:
                    t = f.read()
                    t = x.replace("{PAGEBODY}", t)
                with open("topicheader.html") as f:
                    t = t.replace("{TOPICHEADER}", f.read())
                    t = t.replace("{COMMUNITYNAME}", f"?comm={path[1]}")
                    t = t.replace("{TOPICINTERNAL}", "".join([f"<a href=\"{path[1]}/{a}\"><iframe class=\"post\" title=\"\" width=\"100%\" height=\"250px\" src=\"{path[1]}/{a}\"></iframe></a><br>" for a in sorted(os.listdir(f"db/server/{path[1]}"), reverse=True)])).replace("{PAGETITLE}", f"s/{path[1]} | Demkr, the Democratic Central")
                response_body = t.encode("utf-8")
                status = '200 OK'
            except FileNotFoundError:
                with open("global.html") as f:
                    x = read_global(f)
                with open("404.html") as f:
                    t = f.read()
                    t = x.replace("{PAGEBODY}", t).replace("{PAGETITLE}", f"Page Not Found | Demkr, the Democratic Central")
                response_body = t.encode("utf-8")
                
        elif path[0] == "post":
            with open("global.html") as f:
                x = read_global(f)
            with open("newpost.html") as f:
                t = f.read()
                t = x.replace("{PAGEBODY}", t).replace("{PAGETITLE}", f"New Post | Demkr, the Democratic Central")
            response_body = t.encode("utf-8")
            status = '200 OK'
            
        elif path[0] == "home":
            with open("global.html") as f:
                x = read_global(f)
            with open("topicpage.html") as f:
                t = x.replace("{PAGEBODY}", f.read())
            with open("topicheader.html") as f:
                t = t.replace("{TOPICHEADER}", f.read())
                t = t.replace("{COMMUNITYNAME}", "")
            loc = {g:os.listdir(g) for g in [f"db/server/{f}" for f in os.listdir('db/server') if not os.path.isfile(os.path.join('db', 'server', f))]}
            q = []
            for i in loc:
                for j in loc[i]:
                    q.append(f"{i}/{j}")
            x = random.sample(q, min(len(q), 25))
            t = t.replace("{TOPICINTERNAL}", "".join([f"<a href=\"{i}\"><iframe class=\"post\" title=\"\" width=\"100%\" height=\"250px\" src=\"{i}\"></iframe></a><br>" for i in x])).replace("db/server", "s")
            response_body = t.replace("{PAGETITLE}", "Home | Demkr, the Democratic Central").encode("utf-8")
            status = '200 OK'

        elif path[0] == "post.js":
            with open("post.js") as f:
                x = f.read()
            response_body = x.encode("utf-8")
            status = '200 OK'

        elif path[0] == "postiframetest.js":
            with open("postiframetest.js") as f:
                x = f.read()
            response_body = x.encode("utf-8")
            status = '200 OK'

        elif path[0] == "tohome.js":
            with open("tohome.js") as f:
                x = f.read()
            response_body = x.encode("utf-8")
            status = '200 OK'
            
        else:
            status = '404 Not Found'
            with open("global.html") as f:
                x = read_global(f)
            with open("404.html") as f:
                t = f.read()
                t = x.replace("{PAGEBODY}", t).replace("{PAGETITLE}", f"Page Not Found | Demkr, the Democratic Central")
            response_body = t.encode("utf-8")

    elif request_method == 'POST':
        request = environ['wsgi.input'].read().decode("utf-8")
        req = json.loads(request)
        print(req)
        date = datetime.now().strftime("%H:%M:%S, %d/%m/%Y")
        a = daemon_write(req["comm"], req["user"], date, req["title"], req["body"])
        status = '200 OK'
        response_body = str(a).encode("utf-8")

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
