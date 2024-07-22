import socket

class URL:
    def __init__(self, url) -> None:
        self.scheme, url = url.split('://', 1)  ### https://browser.engineering/http.html becomes ('https', 'browser.engineering/http.html')#
        assert self.scheme == "http"            ### https not suported                                                                      #
        if "/" not in url:                      ### ensure that if the url provided doesnt have a path that the split still work            #
            url = url + "/"                     
        self.host, url = url.split("/", 1)      ### 'browser.engineering/http.html' becomes ('browser.engineering', 'http.html')            #        
        self.path = "/" + url                   ### 'http.html' becomes '/http.html'                                                        #            
    
    def request(self):
        s = socket.socket(                      ### sockets are id that certify a connexion between two computers, allowing them to talk    #
            family=socket.AF_INET,              ### address familly which tells where to find the other computer                            #
            type=socket.SOCK_STREAM,            ### the type of conversation they'll be having                                              #
            proto=socket.IPPROTO_TCP,           ### the protocol they'll be using to establish the connexion                                #
        )
        s.connect((self.host, 80))              ### connect take 1 arg which is a combinaison of the host and the port in this case         #
        request = f"GET {self.path} HTTP/1.0\r\n"
        request += f"Host: {self.host}\r\n"     ### the two newline sequence are essential for the other computer to understand that it is  #
        request += "\r\n"                       ### the end of the message your are sending. otherwise it will wait indefinitly for it      #
        s.send(request.encode("utf8"))          ### encode convert string to bytes                                                          #
        response = s.makefile("r", encoding="utf8", newline="\r\n") # turn bytes back to str and specify python of the weird http's newline #
        statusline = response.readline()
        version, status, explanation = statusline.split(" ", 2)     # expecting HTTP/1.x 200 OK                                             #  
        response_headers = {}
        while True:
            line = response.readline()
            if line == "\r\n": break
            header, value = line.split(":", 1)
            response_headers[header.casefold()] = value.strip()
        assert "transfer-encoding" not in response_headers
        assert "content-encoding" not in response_headers
        content = response.read()
        s.close()
        return content


def main():
    url = URL(input("url :"))
    print(url.request())

if __name__ == "__main__":
    main()
    