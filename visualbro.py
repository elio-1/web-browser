import tkinter
import browser

WIDTH, HEIGHT = 800, 600
HSTEP, VSTEP = 13, 18
SCROLL_STEP = 100

class Browser:
    def __init__(self):
        self.window = tkinter.Tk()
        self.canvas = tkinter.Canvas(
            self.window,
            width=WIDTH,
            height=HEIGHT
        )
        self.canvas.pack()
        self.scroll = 0
        self.window.bind("<Down>", self.scrolldown)

    def scrolldown(self, e):
        self.scroll += SCROLL_STEP
        self.draw()

    def draw(self):
        self.canvas.delete('all')
        for x, y, c in self.display_list:
            self.canvas.create_text(x, y - self.scroll, text=c)

    def load(self, text):
        self.display_list = layout(text)
        self.draw()
            
def layout(text):
    display_list = []
    cursor_x, cursor_y = HSTEP, VSTEP
    for c in text:
        display_list.append((cursor_x, cursor_y, c)) ## append a tuple
        cursor_x += HSTEP
        if c == '\n':
            cursor_y += VSTEP
            cursor_x = HSTEP
        if cursor_x >= WIDTH - HSTEP:
            cursor_y += VSTEP
            cursor_x = HSTEP
    return display_list


if __name__ == "__main__":
    import sys
    url = sys.argv[1]
    content = browser.load(browser.URL(url=url))
    # print(content)
    Browser().load(content)
    tkinter.mainloop()