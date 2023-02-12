"""
Benedikt Fichtner
Python-Version: 3.8.10

Matrix Calculator / GUI - Version 1.0
"""
import sys,os,customtkinter,argparse,json,threading,time
from tkinter import *
from rich import (pretty, console as cons)


class CONFIG():
    def __init__(self) -> None:
        pass
    
    def get(self,*args:list):
        data = None
        try:
            with open(self.conf_filepath,'r') as json_file_data:
                data = json.load(json_file_data)
                for arg in args: data = data[arg]
        except Exception as error:
            self.console.log(f"[red]Couldn't read config-file '{self.conf_filepath}':[bold red] {str(error)}")
        return data


class CALCULATOR(CONFIG):
    def __init__(self) -> None:
        super().__init__()
        
    def multiply_matrices(self) -> None: ### Falk-Schema
        output:str = ""
        try:
            if len(self.matrix_A) > 0 and len(self.matrix_B) > 0:
                if self.matrix_A_dim[1] == self.matrix_B_dim[0]:
                    ces:list = []
                    for row in self.matrix_A:
                        for coll in range(0,self.matrix_B_dim[1]):
                            c:int = 0
                            for e in row:
                                c += e * self.matrix_B[row.index(e)][coll]
                            ces.append(c)
                    output:str = ""
                    (row,coll) = (0,0)
                    for c in ces:
                        output += str(c)+"   "
                        coll += 1
                        if coll == self.matrix_B_dim[1]:
                            row += 1
                            output += "\n"
                            coll = 0
                    self.console.log(f"[green]The product of two matrices was calculated successfully.")
                else:
                    raise Exception("The number of columns of matrix A is not equal to the number of rows of matrix B!")
            else:
                raise Exception("Matrix A or/and Matrix B is/are empty!")
        except Exception as error:
            self.console.log(f"[red]Couldn't multiply matrices:[bold red] {str(error)}")
            output = str(error)
            self.show_error(error_text = str(error))
        self.multiply_output_textbox.configure(state = NORMAL)
        self.multiply_output_textbox.delete(1.0,END)
        self.multiply_output_textbox.insert(1.0,output)
        self.multiply_output_textbox.configure(state = DISABLED)

class GUI(CALCULATOR):
    def __init__(self,console,conf_filepath:str) -> None:
        (self.console,self.conf_filepath) = (console,conf_filepath)
        self.show_error_state:bool = False
        self.time_to_show_error_text:int = 5
        (self.matrix_A,self.matrix_B) = ([],[])
        super().__init__()
    
    def set_tabview(self) -> None:
        tabview = customtkinter.CTkTabview(self.root)
        tabs:dict = self.get("Content","Tabs")
        for tab in tabs:
            tabview.add(tab)
        tab_keys:list[str] = list(tabs.keys())
        tabview.set(tab_keys[0])
        tabview.pack(fill = BOTH, expand = True, padx = 20, pady = 20)
        self.tabview = tabview
        del tabs
    
    def counter_thread(self,error_label:str) -> None:
        self.console.log(f"[white]Started 'counter-thread'")
        for i in range(0,self.time_to_show_error_text):
            time.sleep(1)
        self.show_error_state = False
        error_label.destroy()
        self.error_frame.configure(height = 1)
        self.console.log(f"[white]Stopped 'counter-thread'")
        sys.exit()

    def show_error(self,error_text:str) -> None:
        if self.show_error_state == False:
            label_style:dict = self.get("Style","Main","error_frame","error_label")
            font:list[str,int] = label_style['font']
            error_label = customtkinter.CTkLabel(self.error_frame,text=f"{error_text}",
                text_color = label_style['text_color'],
                font = (font[0],font[1])
            )
            error_label.pack(side = TOP, fill = X, ipady = 3)
            counter = threading.Thread(
                target = self.counter_thread,
                args = (error_label,),
                daemon = True
            )
            counter.start()
            self.show_error_state = True

    ###
    
    def set_matrices(self) -> None:
        try:
            # Matrix A
            matrix_A:list = [[]]
            (row,coll) = (0,1)
            for element in self.textvars_1:
                matrix_A[row].append(int(element.get()))
                if coll == self.matrix_A_dim[1]:
                    coll = 0
                    row += 1
                    if self.textvars_1.index(element) != (len(self.textvars_1)-1):
                        matrix_A.append([])
                coll += 1
            self.console.log(matrix_A)
            self.console.rule()
            # Matrix B
            matrix_B:list = [[]]
            (row,coll) = (0,1)
            for element in self.textvars_2:
                matrix_B[row].append(int(element.get()))
                if coll == self.matrix_B_dim[1]:
                    coll = 0
                    row += 1
                    if self.textvars_2.index(element) != (len(self.textvars_2)-1):
                        matrix_B.append([])
                coll += 1
            self.console.log(matrix_B)
            (self.matrix_A,self.matrix_B) = (matrix_A,matrix_B)
        except Exception as error:
            self.console.log(f"[red]Couldn't set matrices:[bold red] {str(error)}")
            self.show_error(error_text = str(error))
    
    def set_matrices_dimension(self) -> None:
        try:
            matrix_A_dim:list[int] = [int(e.get()) for e in self.matrix_1_dim]
            matrix_B_dim:list[int] = [int(e.get()) for e in self.matrix_2_dim]
            (self.matrix_A_dim,self.matrix_B_dim) = (matrix_A_dim,matrix_B_dim)
            for widget in self.matrix_input_frame1.winfo_children():
                widget.destroy()
            for widget in self.matrix_input_frame2.winfo_children():
                widget.destroy()
            # Matrix A
            textvars_1:list = []
            (row,col) = (0,0)
            for i in range(0,matrix_A_dim[0]*matrix_A_dim[1]):
                textvars_1.append(StringVar())
                customtkinter.CTkEntry(
                    self.matrix_input_frame1, textvariable = textvars_1[i],
                    width = 25,
                    border_width = 1,
                    corner_radius = 3
                ).grid(row = row, column = col, pady = 1, padx = 1)
                col += 1
                if col == matrix_A_dim[1]:
                    row += 1
                    col = 0
            # Matrix B
            textvars_2:list = []
            (row,col) = (0,0)
            for i in range(0,matrix_B_dim[0]*matrix_B_dim[1]):
                textvars_2.append(StringVar())
                customtkinter.CTkEntry(
                    self.matrix_input_frame2, textvariable = textvars_2[i],
                    width = 25,
                    border_width = 1,
                    corner_radius = 3
                ).grid(row = row, column = col, pady = 1, padx = 1)
                col += 1
                if col == matrix_B_dim[1]:
                    row += 1
                    col = 0
            (self.textvars_1,self.textvars_2) = (textvars_1,textvars_2)
            self.console.log("[green]Created two matrices")
        except Exception as error:
            self.console.log(f"[red]Couldn't 'set-matrices-dimension:[bold red] {str(error)}")
            self.show_error(error_text = str(error))
            
    
    def set_matrix_input_tab(self) -> None:
        tabs:dict = self.get("Content","Tabs")
        tab_name:str = list(tabs.keys())[0]
        tab_style:dict = self.get("Style","Tabs",tab_name)
        font:list = tab_style['title']['font']
        title = customtkinter.CTkLabel(self.tabview.tab(tab_name),
            text = tabs[tab_name]['title'],
            font = (font[0],font[1])
        )
        title.pack(side = TOP, fill = X, ipady = 3)
        ask_for_dim_frame = customtkinter.CTkFrame(self.tabview.tab(tab_name), fg_color = tab_style['ask_for_dim_frame']['fg_color'], width = 50)
        ask_for_dim_frame.pack(side = TOP)
        ask_for_dim_frame.grid_columnconfigure(2, weight=1)
        ask_for_dim_frame.grid_rowconfigure(2, weight=1)
        matrix_A_dim_frame = customtkinter.CTkFrame(ask_for_dim_frame, fg_color = tab_style['ask_for_dim_frame']['matrix_A_dim_frame']['fg_color'])
        matrix_A_dim_frame.grid(row = 0, column = 0)
        customtkinter.CTkLabel(matrix_A_dim_frame,text = tabs[tab_name]['ask_for_dim_frame']['matrix_A_dim_frame']['title']).grid(row = 0, column = 1)
        (self.matrix_1_dim,self.matrix_2_dim) = ([],[])
        font:list[str,int] = tab_style['ask_for_dim_frame']['matrix_A_dim_frame']['entry']['font']
        for i in range(0,3):
            if i == 1:
                customtkinter.CTkLabel(matrix_A_dim_frame,text = "x").grid(row = 1, column = i)
            else:
                var = StringVar()
                self.matrix_1_dim.append(var)
                customtkinter.CTkEntry(matrix_A_dim_frame, width = 5,
                    textvariable = var,
                    font = (font[0],font[1])
                ).grid(row = 1, column = i)
        matrix_B_dim_frame = customtkinter.CTkFrame(ask_for_dim_frame, fg_color = tab_style['ask_for_dim_frame']['matrix_B_dim_frame']['fg_color'])
        matrix_B_dim_frame.grid(row = 0, column = 3)
        customtkinter.CTkLabel(matrix_B_dim_frame,text = tabs[tab_name]['ask_for_dim_frame']['matrix_B_dim_frame']['title']).grid(row = 0, column = 4)
        font:list[str,int] = tab_style['ask_for_dim_frame']['matrix_A_dim_frame']['entry']['font']
        for i in range(3,6):
            if i == 4:
                customtkinter.CTkLabel(matrix_B_dim_frame,text = "x").grid(row = 1, column = i)
            else:
                var = StringVar()
                self.matrix_2_dim.append(var)
                customtkinter.CTkEntry(matrix_B_dim_frame, width = 5,
                    textvariable = var,
                    font = (font[0],font[1])
                ).grid(row = 1, column = i)
        customtkinter.CTkButton(ask_for_dim_frame,text = tabs[tab_name]['ask_for_dim_frame']['set_btn']['text'],
            command = self.set_matrices_dimension
        ).grid(
            row = 2, column = 2, pady = 10
        )
        # Input
        font:list = tab_style['input_frame']['title']['font']
        input_frame = customtkinter.CTkFrame(self.tabview.tab(tab_name),fg_color = tab_style['input_frame']['fg_color'])
        input_frame.pack(side = TOP, fill = BOTH, pady = 10, padx = 10, ipady = 3)
        input_frame.grid_columnconfigure(3, weight=1)
        input_frame.grid_rowconfigure(3, weight=1)
        input_frame_title = customtkinter.CTkLabel(input_frame,
            text = tabs[tab_name]['input_frame']['title'],
            font = (font[0],font[1])
        )
        input_frame_title.grid(sticky = W, ipadx = 5, ipady = 3)
        
        # Matrix A
        matrix_input_frame1 = customtkinter.CTkFrame(input_frame,
            fg_color = tab_style['input_frame']['matrix_input_frame1']['fg_color'])
        matrix_input_frame1.grid(row = 1, column = 2, sticky = N)
        max_rows:int = tabs[tab_name]['input_frame']['max_rows']
        max_columns:int = tabs[tab_name]['input_frame']['max_columns']
        matrix_input_frame1.grid_columnconfigure(max_columns, weight=1)
        matrix_input_frame1.grid_rowconfigure(max_rows, weight=1)
        self.matrix_input_frame1 = matrix_input_frame1
        
        # Matrix B
        matrix_input_frame2 = customtkinter.CTkFrame(input_frame,
            fg_color = tab_style['input_frame']['matrix_input_frame2']['fg_color'])
        matrix_input_frame2.grid(row = 1, column = 3)
        matrix_input_frame2.grid_columnconfigure(max_columns, weight=1)
        matrix_input_frame2.grid_rowconfigure(max_rows, weight=1)
        self.matrix_input_frame2 = matrix_input_frame2
        customtkinter.CTkButton(self.tabview.tab(tab_name),text = tabs[tab_name]['set_matrices_btn']['text'],
            command = self.set_matrices
        ).pack(
            side = BOTTOM, fill = X
        )
    
    def set_multiplication_tab(self) -> None:
        tabs:dict = self.get("Content","Tabs")
        tab_name:str = list(tabs.keys())[1]
        tab_style:dict = self.get("Style","Tabs",tab_name)
        font:list = tab_style['title']['font']
        title = customtkinter.CTkLabel(self.tabview.tab(tab_name),
            text = tabs[tab_name]['title'],
            font = (font[0],font[1])
        )
        title.pack(side = TOP, fill = X, ipady = 3)
        customtkinter.CTkButton(self.tabview.tab(tab_name),text=tabs[tab_name]['multiply_btn']['text'],
            command = self.multiply_matrices
        ).pack(side = TOP, fill = BOTH, pady = 50, padx = 250)
        # Output 
        font:list = tab_style['output_frame']['title']['font']
        output_frame = customtkinter.CTkFrame(self.tabview.tab(tab_name))
        output_frame.pack(side = BOTTOM, fill = X, pady = 10, padx = 10, ipady = 3)
        output_frame_title = customtkinter.CTkLabel(output_frame,
            text = tabs[tab_name]['output_frame']['title'],
            font = (font[0],font[1])
        )
        font:list = tab_style['output_frame']['output_textbox']['font']
        output_frame_title.pack(side = TOP, anchor = W, ipadx = 5, ipady = 3)
        self.multiply_output_textbox = customtkinter.CTkTextbox(output_frame,
            font = (font[0],font[1]),
            fg_color = tab_style['output_frame']['output_textbox']['fg_color'],
            corner_radius = 7,
            text_color = tab_style['output_frame']['output_textbox']['text_color']
        )
        self.multiply_output_textbox.pack(side = TOP, fill = BOTH, expand = True, pady = 20, padx = 20, ipady = 3)
        self.multiply_output_textbox.configure(state = DISABLED)
        #
        del tabs, tab_style, font
    
    ###
    
    def run(self) -> None:
        self.console.log(f"[white]Started GUI")
        customtkinter.set_appearance_mode(self.get("Style","Main","appearance_mode"))
        customtkinter.set_default_color_theme(self.get("Style","Main","default_color_theme"))
        self.root = customtkinter.CTk()
        self.root.title(self.get("Content","Main","title"))
        self.root.minsize(self.get("Style","Main","min_width"),self.get("Style","Main","min_height"))
        # self.root.resizable(False,False)
        self.error_frame = customtkinter.CTkFrame(self.root,height = 1)
        self.error_frame.pack(side = TOP, fill = X)
        self.set_tabview(), self.set_matrix_input_tab(), self.set_multiplication_tab()
        
        self.root.mainloop()
        self.console.log(f"[white]Stopped GUI")
    
    
#
pretty.install()
console = cons.Console()
#
default_conf_filepath:str = os.path.dirname(os.path.abspath(__file__))+'/config.json'
#
parser = argparse.ArgumentParser(f"python3 {__file__}")
parser.add_argument(
    '-c', '--config', help=f"Config-filepath (default = '{default_conf_filepath}')", type = str,
    default = default_conf_filepath
)
args = parser.parse_args()

if ".json" not in args.config:
    parser.print_help()
    sys.exit()
#

if __name__ == '__main__':
    # os.system("clear") # 
    gui = GUI(console = console, conf_filepath = args.config)
    gui.run()