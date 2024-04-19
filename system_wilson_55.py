
#from translate import Translator
#from unidecode import unidecode
import webbrowser
import re
import sys
import io
import threading
import subprocess
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox, scrolledtext
import random
import requests
from bs4 import BeautifulSoup
import textwrap
import black
#from autocorrect import Speller


window_expanded=0

def toggle_read_only():
    state = text_entry.cget("state")
        
    if state == "normal":
        text_entry.config(state=tk.DISABLED)                                 
    elif state == "disabled":
        text_entry.config(state=tk.NORMAL)
                                    

def notepad():
    def open_file():
    	file_path = filedialog.askopenfilename()
    	if file_path:
    	       with open(file_path, "r") as file:
    	       	text_entry.delete("1.0", tk.END)
    	       	text_entry.insert(tk.END, file.read())
        
    def save_file():
    	file_path = filedialog.asksaveasfilename(defaultextension=".txt")
    	if file_path:
    	       with open(file_path, "w") as file:
    	       	file.write(text_entry.get("1.0", tk.END))
    
    
    root = tk.Tk()
    root.geometry("620x440+30+850")
    root.config(bg="white")
    menu_bar = tk.Menu(root)
    menu_bar.config(font=("Times", 16, "bold"))
    root.config(menu=menu_bar)
    file_menu = tk.Menu(menu_bar, tearoff=0, font=("Times", 16, "bold"))
    menu_bar.add_cascade(label="File", menu=file_menu)
    file_menu.add_command(label="Open", command=open_file)
    file_menu.add_command(label="Save", command=save_file)
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=root.destroy)
    
    text_entry = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=("Courier New", 15), height=25, width=25, bg=f"#{210:02x}{255:02x}{255:02x}", fg="black", padx=15, pady=15)
    text_entry.pack(padx=16, pady=25)
    text_entry.config(insertwidth=6)
    text_entry.config(insertbackground="black")
    text_entry.focus_set()
    text_entry.config(insertborderwidth=2)
    
    root.mainloop()
    
    
    
   

def error_highlight():
    try:
        error_string = result_text.get("1.0", "end-1c").split("'")[1]

        index = "1.0"
        while index:
            index = text_entry.search(error_string, index, stopindex=tk.END)
            if index:
                end_index = f"{index}+{len(error_string)}c"
                background_color = "cyan"
                foreground_color = "black"                
                text_entry.tag_add("search", index, end_index)
                text_entry.tag_config("search", background=background_color, foreground=foreground_color)
                text_entry.mark_set("insert", end_index)
                text_entry.config(insertwidth=5)
                text_entry.see(end_index)
                index = end_index
    except IndexError:
        print("Error: Unable to extract string within single quotes.")

def find_error_line():
        result_text_content = result_text.get("1.0", "end-1c")
        line_match = re.search(r'line (\d+)', result_text_content)
        line_number = int(line_match.group(1)) if line_match else None

        if line_number is not None:
            line_end = text_entry.index(f"{line_number + 1}.0")
            line_end_last_char = f"{line_end}-1c"
            text_entry.mark_set("insert", line_end_last_char)
            text_entry.see(line_end_last_char)
                 

def find_error_highlight():
	error_highlight()
	find_error_highlight()
	
                                                
def maximize_top():
        global window_expanded
        window_expanded += 1
        if window_expanded > 1:
            window_expanded = 0

        if window_expanded:
            root.geometry("700x1600+0+0")
            text_entry.config(height=18)
            
            
        else:
            reset_window()
                        
   


def rgb_ultra():
    global text_entry
    def update_color(*args):
        
        red_bg = red_slider.get()
        green_bg = green_slider.get()
        blue_bg = blue_slider.get()
        color = f"#{red_bg:02x}{green_bg:02x}{blue_bg:02x}"
        
        text_area.config(bg=color)
        text_entry.config(bg=color)
        text_area.delete(1.0, tk.END)
        text_area.insert(1.0, color)
        
        
    root = tk.Tk()
    root.title("Color Picker")
    root.geometry("400x600+150+700")

    text_area = scrolledtext.ScrolledText(root, bg='white', width=20, height=3, font=("Courier New", 15))
    
    text_area.pack()
    
    red_slider = tk.Scale(root, from_=0, to=255, orient=tk.HORIZONTAL, label="Red", command=update_color)
    red_slider.pack()
    green_slider = tk.Scale(root, from_=0, to=255, orient=tk.HORIZONTAL, label="Green", command=update_color)
    green_slider.pack()
    blue_slider = tk.Scale(root, from_=0, to=255, orient=tk.HORIZONTAL, label="Blue", command=update_color)
    blue_slider.pack()
    root.mainloop()
           		
       		    		
       		    		    		
       		    		    		    		    		

def highlight_keywords(event=None):
    
    keyword_colors = {
        "assert break class continue def": "red",
        "elif else except finally from global": "red",
        "import lambda nonlocal raise return": "red",
        "yield while": "red"
    }

    text = text_entry.get("1.0", tk.END)
    text_entry.tag_remove("highlight", "1.0", tk.END)

    for keywords, color in keyword_colors.items():
        for keyword in keywords.split():
            start_idx = "1.0"
            while True:
                start_idx = text_entry.search(keyword, start_idx, stopindex=tk.END)
                if not start_idx:
                    break
                end_idx = f"{start_idx}+{len(keyword)}c"
                text_entry.tag_add("highlight", start_idx, end_idx)
                text_entry.tag_config("highlight", foreground=color)
                start_idx = end_idx
   	       	   

def evaluate_math(event=None):
        current_widget = root.focus_get()        
        try:       	
        	line_number = int(current_widget.index(tk.INSERT).split('.')[0])
        	expression = str(current_widget.get(str(float(line_number)), tk.INSERT)).strip()      	        	
        	ans = eval(expression)        	
        	current_widget.insert(tk.END, f" ≈ {round(ans, 5)}\n")
        	current_widget.focus_set()
        	current_widget.strip()       	
        except:
        	pass





def open_file():
        current_widget = root.focus_get()
        file_path = filedialog.askopenfilename(
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if file_path:
            with open(file_path, "r") as file:
                content = file.read()
                current_widget.delete("1.0", tk.END)
                current_widget.insert(tk.END, content)
                
def save_file():
        current_widget = root.focus_get()
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
        )
        if file_path:
            content = current_widget.get("1.0", tk.END)
            with open(file_path, "w") as file:
                file.write(content)



def format_python_code():
        current_widget = root.focus_get()
        
        try:
        	input_code = current_widget.get("1.0", "end-1c")
        	reformatted_code = black.format_str(input_code, mode=black.FileMode())
        	
        	current_widget.delete("1.0", "end")
        	current_widget.insert("1.0", reformatted_code)
        	
        except:
        	pass



def search_replace():
    current_widget = root.focus_get()
    
    
    text_to_search = simpledialog.askstring("Search", "Enter text to search:")
    text_to_replace = simpledialog.askstring("Replace", "Enter text to replace:")
    index = "1.0"
    while index:
        index = current_widget.search(text_to_search, index, stopindex=tk.END)
        if index:
            end_index = f"{index}+{len(text_to_search)}c"
            current_widget.delete(index, end_index)
            current_widget.insert(index, text_to_replace)
            index = end_index   



def python_exec(event=None):
    	current_widget = root.focus_get()	    	
    	code = current_widget.get("1.0", "end-1c")
    	output = io.StringIO()
    	sys.stdout = output
    	try:    		    		
    		exec(code)    		    		
    	except Exception as e:  		
    		output.write(f"Error:\n{e}")   		
    		    	
    	sys.stdout = sys.__stdout__
    	result = output.getvalue()   	    	
    	result_text.delete(1.0, tk.END)
    	result_text.insert(tk.END, result)    		
    		    		    		
   
def cut_insert_space():   
    current_widget = root.focus_get()
    
    if current_widget:
        if current_widget.tag_ranges("sel"):
        
            selected_text = current_widget.selection_get()
            selected_length = len(selected_text)
            current_widget.delete("sel.first", "sel.last")
            current_widget.insert("insert", " " * selected_length)

        else:
            cursor_pos = current_widget.index("insert")
            if cursor_pos != "1.0":
                current_widget.delete(cursor_pos + "-1c")
                
                
                       
def select_all():
    current_widget = root.focus_get()
    current_widget.tag_add("sel", "1.0", "end")        
                             
def copy():
        current_widget = root.focus_get()
        root.clipboard_clear()
        root.clipboard_append(current_widget.selection_get())
        	
              
       
def cut():
    focused_widget = root.focus_get()
    if focused_widget:
        if focused_widget.tag_ranges("sel"):
            focused_widget.event_generate("<<Cut>>")
        else:
            cursor_pos = focused_widget.index("insert")
            if cursor_pos != "1.0":
                focused_widget.delete(cursor_pos + "-1c")
                              
                     
def paste():
    focused_widget = root.focus_get()
    if focused_widget:
        if focused_widget.tag_ranges("sel"):
            focused_widget.delete("sel.first", "sel.last")

    if focused_widget == text_entry:
        text_entry.insert("insert", root.clipboard_get())
    else:
        result_text.insert("insert", root.clipboard_get())
                           
def clear_all():       
    text_entry.delete(1.0, tk.END)
    result_text.delete(1.0, tk.END)
                                       
             
def clear_widget():
    current_widget = root.focus_get()
    response = messagebox.askyesno("Clear Window", "Clear the window?")

    if response:
        current_widget.delete(1.0, tk.END)


def exit_program():
        root.destroy()    
    
def change_font(font_name):
        text_entry.config(font=(font_name, 12))

def upper_case():
        current_widget = root.focus_get()
        text = current_widget.get(1.0, tk.END)
        upper = text.upper()
        current_widget.delete(1.0, tk.END)
        current_widget.insert(1.0, upper)

def lower_case():
        current_widget = root.focus_get()
	
        text = current_widget.get(1.0, tk.END)
        lower = text.lower()
        current_widget.delete(1.0, tk.END)
        current_widget.insert(1.0, lower)



def search_selected():
	current_widget = root.focus_get()
		
	selected_text = str(current_widget.selection_get())
	
	
	if current_widget.tag_ranges("sel"):				
		webbrowser.open_new("https://google.com/search?q="+selected_text)
				
		
def search_selected_via_soup():
	current_widget = root.focus_get()
		
	selected_text = str(current_widget.selection_get())
	if current_widget.tag_ranges("sel"):
		current_widget.delete(1.0, tk.END)
		current_widget.insert(1.0, selected_text)
	search_web()
	
	
def open_selected_url():
	current_widget = root.focus_get()	
	url= "https://"+str(current_widget.selection_get())	
	if current_widget.tag_ranges("sel"):
		webbrowser.open_new(url)
				

def highlight_selected(event=None):
    	current_widget = root.focus_get()
    	
    	current_bg_color = current_widget.cget("bg")
    	current_fg_color = current_widget.cget("fg")
    	
    	selected_text = current_widget.selection_get()
    	
    	current_widget.tag_config("custom_tag", background=current_fg_color, foreground=current_bg_color)
    	current_widget.tag_add("custom_tag", "sel.first", "sel.last")
    	current_widget.tag_remove("sel", "1.0", "end") 
    	

    
def font_14():
        current_widget = root.focus_get()
        current_widget.config(font=("Courier New", 14))
        

        
def font_16():
        current_widget = root.focus_get()
        current_widget.config(font=("Courier New", 16))
                            

def font_18():
        current_widget = root.focus_get()
        current_widget.config(font=("Courier New", 18))


def font_22():
        current_widget = root.focus_get()
        current_widget.config(font=("Courier New", 22))


def font_24():
        current_widget = root.focus_get()
        current_widget.config(font=("Courier New", 24))
    
def font_bold():
        current_widget = root.focus_get()        
        current_widget.config(font=("Times", 20, "bold"))
    
def font_courier():
	current_widget = root.focus_get()
	current_widget.config(font=("Courier New", 20))
	
def font_times():
	current_widget = root.focus_get()
	current_widget.config(font=("Times", 20))
	
		    	    
def font_ariel():
	current_widget = root.focus_get()
	current_widget.config(font=("Ariel", 20))	            
	
def search_web(event=None):
        current_widget = root.focus_get()
        query = str(current_widget.get(1.0, tk.END).strip())

        current_widget.delete(1.0, tk.END)
        url = f"https://www.google.com/search?q={query}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        }
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            search_results = soup.find_all("div", class_="BNeawe s3v9rd AP7Wnd")
            if search_results:
                for result in search_results:
                    current_widget.insert(tk.END, result.get_text())
                
            #    text_wrap()
              

            else:
                pass
        else:
            search_selected()



def webpage(event=None):
        current_widget = root.focus_get()
        
        query = str(current_widget.get(1.0, tk.END).strip())
        if ".com" in str(current_widget.get(1.0, tk.END)):
        	current_widget.delete(1.0, tk.END)
        url = "https://" + query if not query.startswith("https://") else query
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            current_widget.insert(tk.END, soup.get_text())
            text_wrap()       

        else:
            text_entry.insert(tk.END, "\n\nCheck Internet Connection..")
            
           
def text_wrap():
        data = str(text_entry.get(1.0, tk.END))
        wrapped_text = textwrap.fill(data, width=45)
        text_entry.delete(1.0, tk.END)
        text_entry.insert(1.0, wrapped_text)

def random_menu_bar_bg():
    	random_bg = "#{:02x}{:02x}{:02x}".format(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    	
    	menu_bar.config(bg=random_bg)
        	    	    	    	

def random_menu_bar_fg():
    	random_fg = "#{:02x}{:02x}{:02x}".format(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    	
    	menu_bar.config(fg=random_fg)
        	

def menu_bar_light():
    	random_bg = "#{:02x}{:02x}{:02x}".format(random.randint(150, 255), random.randint(150, 255), random.randint(150, 255))
    	
    	menu_bar.config(bg=random_bg)
        	    	    	    
    	random_fg = "#{:02x}{:02x}{:02x}".format(random.randint(0, 75), random.randint(0, 75), random.randint(0, 75))
    	
    	menu_bar.config(fg=random_fg)   
      
            
def random_root_bg():
        root_bg = "#{:02x}{:02x}{:02x}".format(random.randint(200, 255), random.randint(200, 255), random.randint(200, 255))
        
        root.config(bg=root_bg)

def random_light_theme():
        random_menu_bar_bg()
        menu_bar_light()
        current_widget = root.focus_get()             
        random_bg_color = "#{:02x}{:02x}{:02x}".format(
            random.randint(130, 255), random.randint(130, 255), random.randint(130, 255))
        random_fg_color = "#{:02x}{:02x}{:02x}".format(
            random.randint(0, 110), random.randint(0, 110), random.randint(0, 110))
                
        current_widget.config(bg=random_bg_color, fg=random_fg_color)        
        
        current_widget.focus_set()
     
def random_dark_theme():
        current_widget = root.focus_get()             
        random_bg_color = "#{:02x}{:02x}{:02x}".format(
            random.randint(0, 60), random.randint(0, 60), random.randint(0, 60))
        random_fg_color = "#{:02x}{:02x}{:02x}".format(
            random.randint(170, 255), random.randint(170, 255), random.randint(170, 255))
                
        current_widget.config(bg=random_bg_color, fg=random_fg_color)                        
        
        
        current_widget.focus_set()
        
                
def random_bg():
        current_widget = root.focus_get()  
        random_bg_color = "#{:02x}{:02x}{:02x}".format(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        current_widget.config(bg=random_bg_color)
                                  
        
def random_fg():
        current_widget = root.focus_get()  
        
        random_fg_color = "#{:02x}{:02x}{:02x}".format(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        current_widget.config(fg=random_fg_color)            
                
                                
        
def save_theme_to_file():
    current_widget = root.focus_get()
    theme_data = current_widget.get("1.0", tk.END).strip()
    if theme_data:
        with open("my_themes.txt", "a") as file:
            file.write(theme_data + "\n")
            messagebox.showinfo("Save Theme", "Theme data saved to 'my_themes.txt'")
    else:
        messagebox.showwarning("No Theme Data", "There is no theme data to save.")        
        
     

submenu_bg="white"
submenu_fg="blue"


def grey_theme():
        global submenu_bg
        root.config(bg="white")
        menu_bar.config(bg="#fbb89c", fg="#16090a")
        text_entry.config(bg="lightblue", fg="black")
        text_entry.config(insertbackground="black")
        text_entry.focus_set()   
        
             
        

def invert_colors():
        current_widget = root.focus_get()  
        current_menubar_bg=menu_bar.cget("bg")
        current_menubar_fg=menu_bar.cget("fg")
        menu_bar.config(bg=current_menubar_fg, fg=current_menubar_bg)
        
        current_fg = current_widget.cget("fg")
        current_bg = current_widget.cget("bg")
        current_widget.config(fg=current_bg, bg=current_fg)


def get_cursor_color():
        current_widget = root.focus_get()
        cursor_color_top = text_entry.cget('insertbackground')
        cursor_color_bottom = result_text.cget('insertbackground')
        
        current_widget.insert(tk.END, f"Top Curs= {cursor_color_top}\n")
        current_widget.insert(tk.END, f"Bottom Curs= {cursor_color_bottom}\n")
        
        
       


def get_colors():
        current_widget = root.focus_get()
        cursor_color_top = text_entry.cget('insertbackground')
        cursor_color_bottom = result_text.cget('insertbackground')
                 
        root_bg_color = root.cget("bg")
        menu_bg_color = menu_bar.cget("background")
        menu_fg_color = menu_bar.cget("foreground")                
        bg_entry = text_entry.cget("background")
        fg_entry = text_entry.cget("foreground")
        bg_result = result_text.cget("background")
        fg_result = result_text.cget("foreground")
      # --------------+------------
        current_widget.insert(tk.END, f"Root = {root_bg_color}\n")        
        current_widget.insert(tk.END, f"Menu Bg = {menu_bg_color}\n")
        current_widget.insert(tk.END, f"Menu Fg = {menu_fg_color}\n")        
        current_widget.insert(tk.END, f"Top bg = {bg_entry}\n")
        current_widget.insert(tk.END, f"Top fg = {fg_entry}\n")
        current_widget.insert(tk.END, f"Bottom bg = {bg_result}\n")
        current_widget.insert(tk.END, f"Bottom fg = {fg_result}\n")
        
        current_widget.insert(tk.END, f"Cursor Top = {cursor_color_top}\n")
        current_widget.insert(tk.END, f"Cursor Bottom = {cursor_color_bottom}\n")
              
        function_string=f"""def name_theme():
    root.config(bg="{root_bg_color}")
    menu_bar.config(bg="{menu_bg_color}", fg="{menu_fg_color}")
    text_entry.config(bg="{bg_entry}", fg="{fg_entry}")
    text_entry.config(insertbackground="lightblue")
    result_text.config(bg="{bg_result}", fg="{fg_result}")
    result_text.config(insertbackground="lightblue")
    
    text_entry.focus_set() 
        """
        result_text.insert(1.0, function_string)
    
          
        
def calculator_theme():
    root.config(bg="#f2fff4")
    menu_bar.config(bg="#9fc69f", fg="#061307")
    text_entry.config(bg="#babb9f", fg="#1d144f")
    text_entry.config(insertbackground="black")
    result_text.config(bg="#f2e19e", fg="#38400e")
    result_text.config(insertbackground="darkgreen")
          
def auto_indent(event):
    current_widget = root.focus_get()
        
    current_line = int(current_widget.index("insert").split(".")[0])
    start_of_line = f"{current_line}.0"
    text_contents = current_widget.get(start_of_line, start_of_line + " lineend")
    indentation = text_contents[: len(text_contents) - len(text_contents.lstrip())]
    if indentation and current_line == int(current_widget.index("insert").split(".")[0]) and event.keysym == "Return":
    		current_widget.insert("insert", "\n" + indentation)
    		current_widget.see("insert")
    		return "break"   	  


def random_submenu_colors():
	global submenu_bg, submenu_fg
	bg_submenu_color = "#{:02x}{:02x}{:02x}".format(random.randint(200, 255), random.randint(200, 255), random.randint(200, 255))
	fg_submenu_color = "#{:02x}{:02x}{:02x}".format(random.randint(0, 75), random.randint(0, 75), random.randint(0, 75))
	
	
	submenu_bg=bg_submenu_color
	submenu_fg=fg_submenu_color


def get_submenu_colors():
	global submenu_bg, submenu_fg
	
	text_entry.delete(1.0, tk.END)
	text_entry.insert(1.0, f"bg = {submenu_bg}")
	text_entry.insert(tk.END, f"\nfg = {submenu_fg}")
		
def activate_python():
	
	text_entry.insert(1.0, "#python\n\n")
	
	python_exec()
		
			
def youtube_search():
    current_widget = root.focus_get()
    
    
    query = current_widget.get("1.0", tk.END).strip()
    if query:
        url = "https://www.youtube.com/search?q=" + "+".join(query.split())
        webbrowser.open_new_tab(url)
    else:
        messagebox.showinfo("Info", "Please enter a query to search")							
										
def run_command(command):  
    current_widget = root.focus_get()
     
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True )
    
    if current_widget == text_entry:
        for line in process.stdout:
        	result_text.insert(tk.END, line)
        	result_text.see(tk.END)
        	result_text.update()
    else:
       for line in process.stdout:
        	text_entry.insert(tk.END, line)
        	text_entry.see(tk.END)
        	text_entry.update()
       
     


def result_view_reset():
	result_text.yview_moveto(0)	


def system_command():
    current_widget = root.focus_get()  
    command = current_widget.get("1.0", tk.END).strip()
    if current_widget == text_entry:
    	result_text.delete("1.0", tk.END)
    else:   	
    	text_entry.delete("1.0", tk.END)   
    try:
        threading.Thread(target=run_command, args=(command,), daemon=True).start()        
       
    except Exception as e:
        result_text.insert(tk.END, f"Error: {e}\n")		
        
        
        
def links_dashboard():
    root = tk.Tk()
    root.title("Web Navigation")
    root.geometry("300x500+30+520")
    root.config(bg="white")  
    
    def open_link(url):
        webbrowser.open_new(url)

    links_data = [
        ("Yahoo", "https://www.yahoo.com"),
        ("Google", "https://www.google.com"),
        ("Labor Gigs", "https://newyork.craigslist.org/search/lbg#search=1~thumb~0~0"),
        ("Domestic Gigs", "https://newyork.craigslist.org/search/mnh/dmg#search=1~thumb~0~0"),
        ("Google News", "https://news.google.com/foryou?hl=en-US&gl=US&ceid=US:en")        
    ]
    for link_text, link_url in links_data:
        btn_link = tk.Button(root, text=link_text, fg="blue", font=("Times", 10, "bold"), cursor="hand2", bd=0, padx=0, pady=0, relief=tk.FLAT,
                             command=lambda url=link_url: open_link(url))
        btn_link.pack(anchor=tk.W, padx=10, pady=5)

    root.mainloop()
      	   

def google_search():
    current_widget = root.focus_get()
    
    search=str(current_widget.get(1.0, tk.END).strip())
    
    url_search="google.com/search?q="+search
    current_widget.delete(1.0, tk.END)
    current_widget.insert(1.0, url_search)
    webpage()
 

def translate_to_spanish():	
    widget = root.focus_get()
    current_line = float(widget.index(tk.INSERT).split('.')[0])
    text_to_translate = widget.get(current_line, "end-1c")       
    translator = Translator(to_lang="es")
    translation = translator.translate(text_to_translate)   
    widget.insert("end", f" = {translation}\n")   	
    widget.focus_set()
                                                                                                                            
def see_bottom():
    current_widget = root.focus_get()
    current_widget.see(tk.END)                                                                             
   
                                                
def wiki_search():
    
    current_widget = root.focus_get()
    search=str(current_widget.get(1.0, tk.END).strip())
    
    url_search="https://en.m.wikipedia.org/wiki/"+search
    current_widget.delete(1.0, tk.END)
    current_widget.insert(1.0, url_search)
    webpage()
                 

def see_top():
    current_widget = root.focus_get()
    current_widget.see(1.0)
    current_widget.see(tk.INSERT)
    
                      																		
														
random_submenu_colors()
    
def dark_theme():
    root.config(bg="white")
    menu_bar.config(bg="darkblue", fg="white")
    text_entry.config(bg="#090328", fg="lightgrey")
    text_entry.config(insertbackground="lightblue")
        
    
  
    
def clasroom_theme():
    root.config(bg="#def4f0")
    menu_bar.config(bg="#bf9a97", fg="#33250a")
    text_entry.config(bg="#82cda7", fg="#380449")
    text_entry.config(insertbackground="lightblue")
    result_text.config(bg="#c4e0a7", fg="#253302")
    result_text.config(insertbackground="lightblue")
    
  
    
def green_theme():
    root.config(bg="#d1ecce")
    menu_bar.config(bg="#919e80", fg="#1d3508")
    text_entry.config(bg="#14331e", fg="#c1fab5")
    text_entry.config(insertbackground="lightblue")
    result_text.config(bg="#c4e0a7", fg="#253302")
    result_text.config(insertbackground="lightblue")
            

def blue_theme():
    root.config(bg="white")
    menu_bar.config(bg="white", fg="darkblue")
    text_entry.config(bg="white", fg="darkblue", font=("Courier New", 16))
    text_entry.config(insertbackground="blue")
    result_text.config(bg="white", fg="darkblue")
    result_text.config(insertbackground="blue")
    
    

def reset_window():
    root.geometry("680x1000+0+0")
    text_entry.config(height=9)    
                      
           
        	
  
def light_grey_theme():
    root.config(bg="#def4f0")
    menu_bar.config(bg="#cfc2b0", fg="#0a1d1f")
    text_entry.config(bg="#e3e0ea", fg="#29214b")
    text_entry.config(insertbackground="lightblue")
    result_text.config(bg="#b6afb0", fg="#342728")
    result_text.config(insertbackground="lightblue")
    
    

def select_all_copy():
        select_all()
        copy()
        
        
        
def random_bg_cursor():
        current_widget=root.focus_get()
        red=random.randint(0,255)
        green=random.randint(0,255)
        blue=random.randint(0,255)
        cursor_color=f"#{red:02x}{green:02x}{blue:02x}"
        current_widget.config(insertbackground=cursor_color)        
        
        
            
def sky_theme():
    root.config(bg="#f2fff4")
    menu_bar.config(bg="#9abdd8", fg="#032a08")
    text_entry.config(bg="#c4f8fb", fg="#2b033f")
    text_entry.config(insertbackground="lightblue")
    result_text.config(bg="#9df0d7", fg="#0c2741")
    result_text.config(insertbackground="lightblue")
    
    text_entry.focus_set() 
        
                    
 

def switch_data():
    top = text_entry.get(1.0, tk.END)
    bottom = result_text.get(1.0, tk.END)
    text_entry.delete(1.0, tk.END)
    text_entry.insert(1.0, bottom)
    result_text.delete(1.0, tk.END)
    result_text.insert(1.0, top)
    



def check_if_python(event=None):
	if "#python" in text_entry.get(1.0, tk.END):
		python_exec()		
		highlight_keywords()			
	else:
		pass			                    
                                       

                  		                                              		                                              		                               
########################
root = tk.Tk()

root.geometry("680x1000+0+0")
root.title("System Wilson")
root.config(bg="white")

text_entry = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=("Courier New", 20), height=9, width=24, bg=f"#090328", fg="#b5d0fb", padx=15, pady=15)

text_entry.pack(fill=tk.BOTH, side=tk.TOP, expand=True, padx=15, pady=15)

text_entry.config(state=tk.NORMAL)

result_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=("Courier New", 22), height=6, width=25, bg=f"#{23:02x}{12:02x}{25:02x}", fg="lightgreen", padx=15, pady=12)

result_text.pack(fill=tk.BOTH, side=tk.BOTTOM, expand=True, padx=10, pady=10)

result_text.config(state=tk.NORMAL)

########################
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)
menu_bar.config(font=("Times", 16, "bold"))

file_menu = tk.Menu(menu_bar, tearoff=0, font=("Times", 16, "bold"), bg=submenu_bg, fg=submenu_fg)
menu_bar.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Save", command=save_file)

file_menu.add_command(label="Maximize Top", command=maximize_top)

file_menu.add_command(label="See Top", command=see_top)

file_menu.add_command(label="Get Colors", command=get_colors)

file_menu.add_command(label="get_cursor_color", command=get_cursor_color)




file_menu.add_command(label="Read-Only On/Off", command=toggle_read_only)



file_menu.add_command(label="Reset Window", command=reset_window)

file_menu.add_command(label="get_submenu_colors", command=get_submenu_colors)

file_menu.add_separator()

file_menu.add_command(label="Exit", command=root.destroy)

edit_menu = tk.Menu(menu_bar, tearoff=0, font=("Times", 16, "bold"),
bg=submenu_bg, fg=submenu_fg)

menu_bar.add_cascade(label="Edit", menu=edit_menu)

edit_menu.add_command(label="Select All", command=select_all)
edit_menu.add_command(label="Copy", command=copy)
edit_menu.add_command(label="Cut", command=cut)
edit_menu.add_command(label="Paste", command=paste)

edit_menu.add_command(label="Cut& Insert Space", command=cut_insert_space)

edit_menu.add_command(label="Clear", command=clear_all)

my_themes_menu = tk.Menu(menu_bar, tearoff=0, font=("Times", 16, "bold"), bg=submenu_bg, fg=submenu_fg)

menu_bar.add_cascade(label="Theme", menu=my_themes_menu)

my_themes_menu.add_command(label="Green", command=green_theme)

my_themes_menu.add_command(label="Blue", command=blue_theme)

my_themes_menu.add_command(label="Classroom", command=clasroom_theme)

my_themes_menu.add_command(label="Calculator", command=calculator_theme)

my_themes_menu.add_command(label="Grey", command=grey_theme)

my_themes_menu.add_command(label="Light Grey", command=light_grey_theme)

my_themes_menu.add_command(label="Dark", command=dark_theme)

my_themes_menu.add_command(label="Background", command=random_bg)

my_themes_menu.add_command(label="Foreground", command=random_fg)

developer_menu = tk.Menu(menu_bar, tearoff=0, font=("Times", 16, "bold"), bg=submenu_bg, fg=submenu_fg)

menu_bar.add_cascade(label="Developer", menu=developer_menu)

developer_menu.add_command(label="System Command", command=system_command)

developer_menu.add_command(label="------------", command=None)





developer_menu.add_command(label="Python ./.py", command=python_exec)


developer_menu.add_command(label="Invert bg/fg", command=invert_colors)

developer_menu.add_command(label="Eval()", command=evaluate_math)

developer_menu.add_command(label="Search & Replace", command=search_replace)

developer_menu.add_command(label="Notebook", command=notepad)

developer_menu.add_command(label="RGB Control", command=rgb_ultra)

developer_menu.add_command(label="Format Python", command=format_python_code)

developer_menu.add_command(label="Swap Windows", command=switch_data)



developer_menu.add_command(label="Expand Top", command=maximize_top)


developer_menu.add_command(label="Read-Only On/Off", command=toggle_read_only)


developer_menu.add_command(label="Highlight(selected)", command=highlight_selected)

developer_menu.add_command(label="Keywords", command=highlight_keywords)



developer_menu.add_command(label="Find Error", command=find_error_highlight)

developer_menu.add_command(label="Cursor Color", command=random_bg_cursor)

translate_menu = tk.Menu(menu_bar, tearoff=0, font=("Times", 16, "bold"), bg=submenu_bg, fg=submenu_fg)

menu_bar.add_cascade(label="Lang.", menu=translate_menu)

translate_menu.add_command(label="Spanish", command=translate_to_spanish)

math_menu = tk.Menu(menu_bar, tearoff=0, font=("Times", 16, "bold"), bg=submenu_bg, fg=submenu_fg)

menu_bar.add_cascade(label="Math", menu=math_menu)

math_menu.add_command(label="evaluate_math", command=evaluate_math)

font_menu = tk.Menu(menu_bar, tearoff=0, font=("Times", 16, "bold"), bg=submenu_bg, fg=submenu_fg)

menu_bar.add_cascade(label="Font", menu=font_menu)

font_menu.add_command(
    label="Times New Roman", command=lambda: change_font("Times New Roman"))

font_menu.add_command(label="Times", command=font_times)

font_menu.add_command(label="Courier", command=font_courier)

font_menu.add_command(label="Ariel", command=font_ariel)

font_menu.add_command(label="Times Bold", command=font_bold)

#font_menu.add_command(label="font 14", command=font_14())

font_menu.add_command(label="font 16", command=font_16())

font_menu.add_command(label="font_18", command=font_18())

font_menu.add_command(label="font_22", command=font_22())

font_menu.add_command(label="font_24", command=font_24())

font_menu.add_command(label="upper_case", command=upper_case)

font_menu.add_command(label="lower_case", command=lower_case)


web_menu = tk.Menu(menu_bar, tearoff=0, font=("Times", 16, "bold"),
bg=submenu_bg, fg=submenu_fg)

menu_bar.add_cascade(label="WEB", menu=web_menu)

web_menu.add_command(label="------", command=None)

web_menu.add_command(label="URL", command=webpage)

web_menu.add_command(label="Search Web", command=search_web)

web_menu.add_command(label="Search Selected Text", command=search_selected)

web_menu.add_command(label="Links Dashboard", command=links_dashboard)

web_menu.add_command(label="Google Search", command=google_search)

web_menu.add_command(label="Wiki Search", command=wiki_search)

web_menu.add_command(label="Open Selected URL", command=open_selected_url)

web_menu.add_command(label="YouTube ", command=youtube_search)

theme_menu = tk.Menu(menu_bar, tearoff=0, font=("Times", 16, "bold"),
bg=submenu_bg, fg=submenu_fg)

menu_bar.add_cascade(label="Extra", menu=theme_menu)

theme_menu.add_command(label="Light Menu Bar", command=menu_bar_light)
theme_menu.add_command(label="Light Theme", command=random_light_theme)
theme_menu.add_command(label="Menu bg", command=random_menu_bar_bg)
theme_menu.add_command(label="Menu fg", command=random_menu_bar_fg)

theme_menu.add_command(label="Background", command=random_bg)
theme_menu.add_command(label="Foreground", command=random_fg)
theme_menu.add_command(label="Root", command=random_root_bg)
theme_menu.add_command(label="Invert", command=invert_colors)

theme_menu.add_command(label="Cursor Color", command=random_bg_cursor)

theme_menu.add_command(label="Get Colors", command=get_colors)
theme_menu.add_command(label="blue_theme", command=blue_theme)

theme_menu.add_command(label="Save Theme", command=save_theme_to_file)
theme_menu.add_command(label="Dark Theme", command=dark_theme)



########################################3
###[ Buttons ]#####################3



button_bg="white"
button_fg="darkblue"

bottom_menu_frame = tk.Frame(root, bg="black")
bottom_menu_frame.pack(side=tk.BOTTOM, fill=tk.X)

search_web_button = tk.Button(bottom_menu_frame, text="W3M", command=search_web,
font=("Courier New", 16), bg=button_bg, fg=button_fg)

search_web_button.pack(side=tk.LEFT, padx=1)

clear_widget_button = tk.Button(bottom_menu_frame, text="Clear", command=clear_widget,
font=("Courier New", 16), bg=button_bg, fg=button_fg)

clear_widget_button.pack(side=tk.LEFT, padx=1)

python_exec_button = tk.Button(bottom_menu_frame, text="./py ",    command=python_exec, font=("Courier New", 16), bg=button_bg, fg=button_fg)

python_exec_button.pack(side=tk.LEFT, padx=1)

system_command_button = tk.Button(bottom_menu_frame, text="Sys",    command=system_command, font=("Courier New", 16), bg=button_bg, fg=button_fg)

system_command_button.pack(side=tk.LEFT, padx=1)

second_row_frame = tk.Frame(root, bg="black")
second_row_frame.pack(side=tk.BOTTOM, fill=tk.X)

select_all_copy_button = tk.Button(second_row_frame, text="Cp-A", command=select_all_copy, font=("Courier New", 16), bg=button_bg, fg=button_fg)

select_all_copy_button.pack(side=tk.LEFT, padx=1)

copy_button = tk.Button(second_row_frame, text="Copy", command=copy, font=("Courier New", 16), bg=button_bg, fg=button_fg)

copy_button.pack(side=tk.LEFT, padx=1)
cut_button = tk.Button(second_row_frame, text="Cut", command=cut, font=("Courier New", 16), bg=button_bg, fg=button_fg)

cut_button.pack(side=tk.LEFT, padx=1)

paste_button = tk.Button(second_row_frame, text="Paste", command=paste, font=("Courier New", 16), bg=button_bg, fg=button_fg)

paste_button.pack(side=tk.LEFT, padx=1)

text_entry.config(insertwidth=9)

text_entry.config(insertborderwidth=5)

text_entry.config(insertbackground="lightblue")

result_text.config(insertwidth=9)

result_text.config(insertbackground="darkgreen")
result_text.config(insertborderwidth=5)

text_entry.focus_set()



text_entry.bind("<Return>", auto_indent)

result_text.bind("<Return>", auto_indent)

text_entry.bind("<KeyRelease>", check_if_python)

blue_theme()

text_entry.bind("<KeyRelease>", highlight_keywords)






						
root.mainloop()



