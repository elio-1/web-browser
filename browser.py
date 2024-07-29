import tkinter
import url

WIDTH, HEIGHT = 800, 600                        ## the size of the browser window
HSTEP, VSTEP = 13, 18                           ## intercharacter space and interline space. Replace with font value later
SCROLL_STEP = 100
display_list = []               ### all the content can be display
displayed_list = []             ### the content that is currently displayed
content = None

class Browser:
    def __init__(self):
        self.window = tkinter.Tk()              ## root
        self.canvas = tkinter.Canvas(           ## widget that manage 2D objects 
            self.window,
            width=WIDTH,
            height=HEIGHT
        )
        # window size
        self.width = WIDTH
        self.height = HEIGHT
        self.window.bind("<Configure>", self.resize_window)

        # binds
        self.scroll = 0
        self.window.bind("<Down>", self.scrolldown)
        self.window.bind("<Up>", self.scrollup)
        self.window.bind_all("<MouseWheel>", self.on_mousewheel)
        
        # scrollbar
        self.scrollbar = tkinter.Scrollbar(self.window, command=self.handle_scroll, orient='vertical')
        self.scrollbar.pack( side ="right", fill="y" )


        
    def handle_scroll(self, moveto, pos):
        if float(pos) > 0.01:
            self.scroll += SCROLL_STEP
            self.draw()   
        
    def resize_window(self, event):
        self.width = int(event.width)
        self.height = int(event.height)  
        self.load(content)

    def scrolldown(self, event):
        if displayed_list[-1][1] != display_list[-1][1]:
            self.scroll += SCROLL_STEP
            self.draw()

    def scrollup(self, event):
        if displayed_list[0][1] != display_list[0][1]:
            self.scroll -= SCROLL_STEP
            self.draw()
    
    def on_mousewheel(self, event):
        if event.delta < 0:
            self.scrolldown(event)
        else:
            self.scrollup(event)
        

    def draw(self):
        self.canvas.delete('text')                   ## delete all is used to avoid displaying char on top of another
        displayed_list.clear()
        for x, y, c in self.display_list:           ## expect a tuple where x is cursor_x, y is cursor_y and c is a character
            if y > self.scroll + self.height: continue            ## skip the character if its bellow the viewing window for optimization
            if y + VSTEP < self.scroll: continue    ## skip the above. +vstep is for drawing char that are half way
            displayed_list.append((x, y, c))
            self.canvas.create_text(x, y - self.scroll, text=c, tags="text")
        self.canvas.pack(side="left", fill="both" ,expand=1)


    def load(self, content):
        self.display_list = layout(content, self.width) # [(posx, posy, char), ...]
        self.draw()


def layout(text, width):
    display_list.clear()

    cursor_x, cursor_y = HSTEP, VSTEP                ## represent where the char will be drawn
    for c in text:
        display_list.append((cursor_x, cursor_y, c)) ## append a tuple
        cursor_x += HSTEP
        if c == '\n':                               
            cursor_y += VSTEP
            cursor_x = HSTEP
        if cursor_x >= width - HSTEP:
            cursor_y += VSTEP
            cursor_x = HSTEP
    return display_list                             ## return a list of tuple containing the char to draw with it's x and x pos


if __name__ == "__main__":
    import sys
    urlarg = sys.argv[1]
    content = url.load(url.URL(url=urlarg))
    Browser().load(content)
    tkinter.mainloop()