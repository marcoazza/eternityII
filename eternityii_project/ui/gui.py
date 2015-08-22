
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
        self.board = BoardGUI(master,width=500, height=500, bg='white',borderwidth=0,highlightthickness=1,highlightbackground='black')
        self.board.create_text(self.board.width/2,self.board.height/2,text='prova\nprova row 2')
        self.menubar = tk.Menu(master)
        self.button_container = tk.Frame(master,width=500, height=500)
        self.button_container.grid(row=0,column=1)
        self.board.grid(row=0,column=0)
        self.createWidgets(master=self.button_container)

        # create a pulldown menu, and add it to the menu bar
        filemenu = tk.Menu(self.menubar, tearoff=0)
        filemenu.add_command(label="Load Game File..", command=self.load_file)
        filemenu.add_command(label="Save", command=self.save_file)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=master.quit)
        self.menubar.add_cascade(label="File", menu=filemenu)

        master.config(menu=self.menubar)







    def createWidgets(self,master=None):
        self.solve = tk.Button(master,text='Solve',command=self.solve)
        self.load = tk.Button(master, text="Load Game File",command=self.load_file)
        self.timer_lbl = tk.Label(master,text='Evaluate for (sec):')
        self.entry_val = tk.IntVar()
        self.timer_entry = tk.Entry(master,textvariable=self.entry_val)
        self.load.pack()
        self.timer_lbl.pack()
        self.timer_entry.pack()
        self.solve.pack()

    def load_file(self):
        ftypes = [('Text files', '*.txt'), ('All files', '*')]
        dlg = tkFileDialog.Open(self, filetypes = ftypes)
        fl = dlg.show()

        if fl is not '':
            self.v.load_game_file(fl)
            self.board.load_board(fl)

    def save_file(self):
        pass



    def solve(self):
        try:
            self.v.compute(sec=self.entry_val.get())
            print 'evaluation ended....'
            self.board.update_board(self.v.best.get_snapshot())
            self.v.print_exit_file()
        except ValueError:
            print 'exception'
            pass




def main():
    root = tk.Tk()
    root.title('Eternity II game solver')
    app = Application(master=root)
    app.mainloop()
    root.mainloop()

if __name__ == "__main__":
    main()
