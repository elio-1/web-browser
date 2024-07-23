import socket
import ssl


class URL:
    def __init__(self, url) -> None:            ### split the url into a scheme, a host, a port and a path                                  #
        self.scheme, url = url.split('://', 1)  ### https://browser.engineering/http.html becomes ('https', 'browser.engineering/http.html')#
        assert self.scheme in ["http", "https"]                                                                  
        if "/" not in url:                      ### ensure that if the url provided doesnt have a '/' that the split still return 2 value   #
            url = url + "/"                     
        self.host, url = url.split("/", 1)      ### 'browser.engineering/http.html' becomes ('browser.engineering', 'http.html')            # 
        self.path = "/" + url                   ### 'http.html' becomes '/http.html'                                                        #            
        if self.scheme == 'http':               
            self.port = 80                      
        elif self.scheme == 'https':
            self.port = 443                     
        if ':' in self.host:                    ### check if a port is specify in the url's hostname 'example.org:8080'                     #
            self.host, port = self.host.split(':', 1)
            self.port = int(self.port)

    def request(self):
        s = socket.socket(                      ### sockets are id that certify a connexion between two computers, allowing them to talk    #
            family=socket.AF_INET,              ### address familly tells where to find the other computer                                  #
            type=socket.SOCK_STREAM,            ### the type of conversation they'll be having                                              #
            proto=socket.IPPROTO_TCP,           ### the protocol they'll be using to establish the connexion                                #
        )
        s.connect((self.host, self.port))       ### connect take 1 arg which is a combinaison of the host and the port in this case         #
        if self.scheme == 'https':
            ctx = ssl.create_default_context()      ### create a new socket using TLS                                                       # 
            s = ctx.wrap_socket(s, server_hostname=self.host)   # save the socket with the new socket                                       #
        request = f"GET {self.path} HTTP/1.0\r\n"
        request += f"Host: {self.host}\r\n"     ### the two newline sequence are essential for the other computer to understand that it is  #
        request += "\r\n"                       ### the end of the message your are sending. otherwise it will wait indefinitly for it      #
        s.send(request.encode("utf8"))          ### encode convert string to bytes                                                          #
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
    

def show(body):                                 # print the content of a page without the html tags                                         #
    in_tag = False
    for c in body:
        if c == "<":
            in_tag = True
        elif c == ">":
            in_tag = False
        elif not in_tag:
            print(c, end="")


def load(url):                                  # expect a URL class                                                                        #
    body = url.request()
    show(body)




if __name__ == "__main__":
    import sys
    load(URL(sys.argv[1]))
    