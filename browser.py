import socket
import ssl

user_agents = [
    "WebBrowser/0.01 (Windows NT 10.0; Win64; x64)",
]

class URL:
    def __init__(self, url) -> None:            ### split the url into a scheme, a host, a port and a path                                  #
        self.scheme, url = url.split(':', 1)  ### https://browser.engineering/http.html becomes ('https', 'browser.engineering/http.html')#
        assert self.scheme in ["http", "https", "file", "data"]
        if self.scheme != 'data':
            url = url.replace('//', '', 1)                                                                  
        if "/" not in url:                      ### ensure that if the url provided doesnt have a '/' that the split still return 2 value   #
            url = url + "/"                     
        self.host, url = url.split("/", 1)      ### 'browser.engineering/http.html' becomes ('browser.engineering', 'http.html')            # 
        self.path = "/" + url                   ### 'http.html' becomes '/http.html'                                                        #            
        if self.scheme == 'http':               
            self.port = 80                      
        elif self.scheme == 'https':
            self.port = 443    
        elif self.scheme in ['file', 'data']:
            self.port = 8000                 
        if ':' in self.host and self.scheme != 'file':                    ### check if a port is specify in the url's hostname 'example.org:8080'                     #
            self.host, port = self.host.split(':', 1)
            self.port = int(self.port)
        if self.scheme == 'data':
            url, self.text = url.split(',', 1)

    def request(self):
        s = socket.socket(                      ### sockets are id that certify a connexion between two computers, allowing them to talk    #
            family=socket.AF_INET,              ### address familly tells where to find the other computer                                  #
            type=socket.SOCK_STREAM,            ### the type of conversation they'll be having                                              #
            proto=socket.IPPROTO_TCP,           ### the protocol they'll be using to establish the connexion                                #
        )
        user_agents_headers = {"User-Agent": user_agents[0]}
        s.connect((self.host, self.port))       ### connect take 1 arg which is a combinaison of the host and the port in this case         #
        
        if self.scheme == 'https':
            ctx = ssl.create_default_context()      ### create a new socket using TLS                                                       # 
            s = ctx.wrap_socket(s, server_hostname=self.host)   # save the socket with the new socket                                       #
        
        request_headers = f"GET {self.path} HTTP/1.1\r\n"   
        request_headers += f"Host: {self.host}\r\n"     ### the two newline sequence are essential for the other computer to understand that it is  #
        request_headers += "Connection: close\r\n"      ### indicate that the client is willing to close the connection after sending the request   #
        request_headers += "\r\n"                       ### the end of the message your are sending. otherwise it will wait indefinitly for it      #
        
        s.send(request_headers.encode("utf8"))          ### encode convert string to bytes                                                          #
        response = s.makefile("r", encoding="utf8", newline="\r\n") # turn bytes back to str and specify python of the weird http's newline #
        statusline = response.readline()
        version, status, explanation = statusline.split(" ", 2)     # expecting HTTP/1.x 200 OK                                             #  
       
        response_headers = {}
        while True:                             ### check the headers                                                                       #
            line = response.readline()
            if line == "\r\n": break            ### the first newline sequence is used to signify the end on the header                     #
            header, value = line.split(":", 1)
            response_headers[header.casefold()] = value.strip()
        assert "transfer-encoding" not in response_headers  # check that the data we’re trying to access isn't being sent in an unusual way #
        assert "content-encoding" not in response_headers

        content = response.read()
        s.close()                               # closing the socket                                                                        #
        return content

    def show_file(self):
        import os
        return os.listdir(self.path.split('/',1)[1])

    def show_data(self):
        return self.text

def show(body, endline):                                 # print the content of a page without the html tags                                         #
    entities = {'&lt;':'<','&rt;':'>'}
    tmp_entity = ''
    in_tag = False
    for c in body:
        if c == "<":
            in_tag = True
        elif c == ">":
            in_tag = False
        elif tmp_entity in entities:
            print(entities[tmp_entity], end=endline)
            print(c, end=endline)
            in_tag = False
            tmp_entity = ''
        elif in_tag == True:
            tmp_entity += c
        elif c == "&":
            in_tag = True
            tmp_entity += c
        elif  c == ";":
            in_tag = False
            tmp_entity += c
        elif not in_tag:
            print(c, end=endline)


def load(url):                                  # expect a URL class                                                                        #
    if url.scheme in ['http', 'https']:
        body = url.request()
        show(body, "")
    elif url.scheme == 'file':
        body = url.show_file()
        show(body, '\n')
    elif url.scheme == 'data':
        show(url.text, '')




if __name__ == "__main__":
    import sys
    load(URL(sys.argv[1]))
    