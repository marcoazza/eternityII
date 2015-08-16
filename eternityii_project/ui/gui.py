
try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk

from board_ui import BoardGUI
from ..vns import vns
import tkFileDialog


class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.v = vns.VNS()
        self.board = BoardGUI(self, width=500, height=500, bg='white',borderwidth=0,highlightthickness=1,highlightbackground='black')
        self.menubar = tk.Menu(master)
        self.pack()
        self.createWidgets()

        # create a pulldown menu, and add it to the menu bar
        filemenu = tk.Menu(self.menubar, tearoff=0)
        filemenu.add_command(label="Open", command=self.load_file)
        filemenu.add_command(label="Save", command=self.save_file)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=master.quit)
        self.menubar.add_cascade(label="File", menu=filemenu)

        master.config(menu=self.menubar)







    def createWidgets(self):
        self.solve = tk.Button(self,text='Solve',command=self.solve)
        self.solve.pack()

        self.QUIT = tk.Button(self, text="QUIT", fg="red",
                                            command=self.master.destroy)
        self.QUIT.pack(side="bottom")

    def load_file(self):
        ftypes = [('Text files', '*.txt'), ('All files', '*')]
        dlg = tkFileDialog.Open(self, filetypes = ftypes)
        fl = dlg.show()

        if fl is not '':
            #text = self.readFile(fl)
            self.v.load_game_file(fl)
            self.board.load_board(fl)

    def save_file(self):
        pass



    def solve(self):
        #v = VNS()
        #v.load_game_file('e2_5x5.txt')
        self.v.compute()
        print 'evaluation ended'
        self.board.update_board(self.v.best.get_snapshot())
        self.v.print_exit_file()





def main():
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()
    root.mainloop()

if __name__ == "__main__":
    main()
