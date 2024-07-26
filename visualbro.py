import tkinter
import browser

WIDTH, HEIGHT = 800, 600                        ## the size of the browser window
HSTEP, VSTEP = 13, 18                           ## intercharacter space and interline space. Replace with font value later
SCROLL_STEP = 100

class Browser:
    def __init__(self):
        self.window = tkinter.Tk()              ## root
        self.canvas = tkinter.Canvas(           ## widget that manage 2D objects 
            self.window,
            width=WIDTH,
            height=HEIGHT
        )
        self.canvas.pack()
        self.scroll = 0
        self.window.bind("<Down>", self.scrolldown)
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def scrolldown(self, event):
        self.scroll += SCROLL_STEP
        self.draw()
    
    def _on_mousewheel(self, event):
        if event.delta < 0:
            self.scroll += SCROLL_STEP
        else:
            self.scroll -= SCROLL_STEP
        self.draw()

    def draw(self):
        self.canvas.delete('all')                   ## delete all is used to avoid displaying char on top of another
        for x, y, c in self.display_list:           ## expect a tuple where x is cursor_x, y is cursor_y and c is a character
            self.canvas.create_text(x, y - self.scroll, text=c) 

    def load(self, text):
        self.display_list = layout(text)
        self.draw()
            
def layout(text):
    display_list = []
    cursor_x, cursor_y = HSTEP, VSTEP                ## represent where the char will be drawn
    for c in text:
        display_list.append((cursor_x, cursor_y, c)) ## append a tuple
        cursor_x += HSTEP
        if c == '\n':                               
            cursor_y += VSTEP
            cursor_x = HSTEP
        if cursor_x >= WIDTH - HSTEP:
            cursor_y += VSTEP
            cursor_x = HSTEP
    return display_list                             ## return a list of tuple containing the char to draw with it's x and x pos


if __name__ == "__main__":
    import sys
    url = sys.argv[1]
    content = browser.load(browser.URL(url=url))
    Browser().load(content)
    tkinter.mainloop()