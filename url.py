class URL:
    def __init__(self, url) -> None:
        self.scheme, url = url.split('://', 1)  ### https://browser.engineering/http.html becomes ('https', 'browser.engineering/http.html') #
        assert self.scheme == "http"            ### https not suported
        if "/" not in url:
            url = url + "/"                     
        self.host, url = url.split("/", 1)      ### 'browser.engineering/http.html' becomes ('browser.engineering', 'http.html')             #
        self.path = "/" + url                   ### 'http.html' becomes '/http.html'                                                         #
    
    def request(self):
        #...
    