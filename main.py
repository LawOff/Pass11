import contextlib
from algo import AlgoCheck
import tkinter as tk
import js2py, os, ctypes, tksvg
import string, secrets
import customtkinter
from win32mica import MICAMODE, ApplyMica
#from BlurWindow.blurWindow import GlobalBlur

PATH = os.path.dirname(os.path.realpath(__file__))
default_path = os.getcwd()
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("./assets/dark-theme.json")
result, tempfile = js2py.run_file("assets\\js\\script.js");

class PassCheck(customtkinter.CTkFrame):
    def __init__(self, parent=None):
        customtkinter.CTkFrame.__init__(self, parent, fg_color="#000000")
        self._elapsedpass ="No Password Entered"
        self.strenstr = tk.StringVar()
        self.showval = False
        self.passstr = tk.StringVar()
        self.crackstr = tk.StringVar()
        self.passstr.trace("w", lambda name, index, mode, x=self.passstr: self._update(x))
        self.crackstr.trace("w", lambda name, index, mode, x=self.crackstr: self._update(x))
        #self.loader()
        self.makeWidgets()
    def makeWidgets(self): 
        
        self.lower_image = self.load_image("/assets/lower_image.svg")
        self.upper_image = self.load_image("/assets/upper_image.svg")
        self.number_image = self.load_image("/assets/number_image.svg")
        self.special_image = self.load_image("/assets/special_image.svg")
        self.lenght_image = self.load_image("/assets/lenght_image.svg") #newline
        
        self.showeye_image = self.load_image("/assets/showeye_image.svg")
        self.hideeye_image = self.load_image("/assets/hideeye_image.svg")
        self.loadd_image = self.load_image("/assets/load_image.svg")

        self.l = customtkinter.CTkLabel(self, textvariable=self.strenstr, text_color="#363636", text_font=("Segoe UI", 12))
        self.l.pack(fill=tk.X, expand=tk.NO, pady=2, padx=2)

        self.g = customtkinter.CTkFrame(self, fg_color="#000000")
        self.g.pack(fill=None, expand=tk.NO, pady=2, padx=2)
        
        self.random = customtkinter.CTkButton(self.g, text=None, image=self.loadd_image, fg_color="#181A1B", width=35, height=35, command=self.RandomPass)
        self.random.pack(side=tk.LEFT, padx=0, pady=5)

        self.passEntry = customtkinter.CTkEntry(self.g, textvariable=self.passstr, placeholder_text="Try a Password", justify='center', text_color="#DDE6E8", width=200, text_font=("Segoe UI", 15, "bold"))
        self.passEntry.pack(side=tk.LEFT, padx=0, pady=5)
        
        self.show = customtkinter.CTkButton(self.g, text=None, image=self.showeye_image, fg_color="#181A1B", width=35, height=35, command=self.ShowPass)
        self.show.pack(side=tk.RIGHT, padx=0, pady=5)
        

        self.progressbar = customtkinter.CTkProgressBar(self, orient=tk.HORIZONTAL, progress_color="#767676", width=250, fg_color="#1c1c1c")
        self.progressbar.set(0)
        self.progressbar.pack(fill=tk.X, expand=tk.NO, pady=2, padx=2)
        
        self.t = customtkinter.CTkLabel(self, textvariable=self.crackstr, text_color="#363636", text_font=("Segoe UI", 9))
        self.t.pack(fill=tk.X, expand=tk.NO, pady=2, padx=2)

        self.strenstr.set("No Password Entered")
        self.crackstr.set("Can be cracked in: 0 seconds")

        self.f = customtkinter.CTkFrame(self, fg_color="#000000")
        self.f.pack(expand=tk.NO, pady=10, padx=2)
        
        self.lowerc = customtkinter.CTkButton(self.f, text=None, image=self.lower_image, fg_color="#181A1B", state="disabled", width=30, height=30)
        self.upperc = customtkinter.CTkButton(self.f, text=None, image=self.upper_image, fg_color="#181A1B", state="disabled", width=30, height=30)
        self.numberc = customtkinter.CTkButton(self.f, text=None, image=self.number_image, fg_color="#181A1B", state="disabled", width=30, height=30)
        self.specialc = customtkinter.CTkButton(self.f, text=None, image=self.special_image, fg_color="#181A1B", state="disabled", width=30, height=30)
        self.length_entry = customtkinter.CTkEntry(self.f, justify='center', fg_color="#181A1B",text_color="#DDE6E8", width=31, height=31, text_font=("Segoe UI", 9, "bold"))
        
        self.lowerc.pack(side=tk.LEFT, padx=10, pady=2)
        self.upperc.pack(side=tk.LEFT, padx=10, pady=2)
        self.numberc.pack(side=tk.LEFT, padx=10, pady=2)
        self.specialc.pack(side=tk.LEFT, padx=10, pady=2)
        self.lenght.pack(side=tk.LEFT, padx=10, pady=2) ## newline

        self.length_entry.pack(side=tk.LEFT, padx=0, pady=5) ## newline


    def ShowPass(self):
        if self.showval:
            self.showval = False
            self.show.configure(image=self.showeye_image)
            self.passEntry.configure(show="")
        else:
            self.showval = True
            self.show.configure(image=self.hideeye_image)
            self.passEntry.configure(show="*")
        
    def RandomPass(self):
        length_str = self.length_entry.get()
        try:
            length = int(length_str)
        except ValueError:
        # Gestire il caso in cui l'input non sia un numero intero valido
            return
    
        alphabet = string.ascii_letters + string.digits + "@$!%*?&"
        password = "".join(secrets.choice(alphabet) for _ in range(length))
        self.passstr.set(password)
    
    def _update(self, *args):
        global tempfile
        self.step = 0.01
        password = self.passstr.get()
        res = AlgoCheck(password,tempfile)
        #print(res)
        self.value = int(res["nstrength"])/4
        self.progressbar.set(self.value)
        self.progressbar.configure(progress_color=res["color"])
        with contextlib.suppress(Exception):
            if res["length"] > 0:
                self._setPass(res["strength"], res["time"])
            else:
                self._setPass("No Password Entered", res["time"])
            if res["lowercase"] == True:
                self.lowerc.configure(fg_color="#107C10")
            else:
                self.lowerc.configure(fg_color="#181A1B")
            if res["uppercase"] == True:
                self.upperc.configure(fg_color="#107C10")
            else:
                self.upperc.configure(fg_color="#181A1B")
            if res["numbers"] == True:
                self.numberc.configure(fg_color="#107C10")
            else:
                self.numberc.configure(fg_color="#181A1B")
            if res["special"] == True:
                self.specialc.configure(fg_color="#107C10")
            else:
                self.specialc.configure(fg_color="#181A1B")

    def _setPass(self, password, time):
        self.strenstr.set(password)
        self.crackstr.set(f"Can be cracked in: {time}")

        
    def load_image(self, path):
        return tksvg.SvgImage(file=(PATH + path))
       
        
if __name__ == '__main__':
    root = customtkinter.CTk()
    root.title('')
    root.iconbitmap("./assets/icon_pass11.ico")
    root.geometry("420x180")
    root.resizable(False, False)
    root.eval('tk::PlaceWindow . center')
    root.configure(bg="#000000")
    root.deiconify()
    ApplyMica(HWND=ctypes.windll.user32.GetForegroundWindow(),ColorMode=MICAMODE.DARK)
    root.update()
    #GlobalBlur(ctypes.windll.user32.GetForegroundWindow(),hexColor="#1f1f1f00",Acrylic = True)
    #root.protocol('WM_DELETE_WINDOW', PassCheck().hide_window)
    PassCheck(root).pack()
    root.mainloop()
