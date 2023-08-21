import tkinter as tk
from tkinter import filedialog, messagebox, ttk

DESCRIPTION = 0
CODE = 1
ENABLE = 2
SELECTED_ITEM = None

def load_file():
    filepath = filedialog.askopenfilename(filetypes=[("CHT File", "*.cht")])
    if filepath:
        with open(filepath, "r") as file:
            file_content = file.read()
        cheats = parse_file_content(file_content)
        update_cheat_list(cheats)

def extract_value(input_string):
    if (input_string.find("desc") != -1) or (input_string.find("code") != -1):
        start_index = input_string.find('"')
        end_index = input_string.find('"', start_index + 1)
        extracted_text = input_string[start_index + 1:end_index]
    elif (input_string.find("enable") != -1):
        if input_string.find("true"):
            extracted_text = "true"
        elif input_string.find("false"):
            extracted_text = "false"
    return extracted_text

def parse_file_content(content):
    cheats = []
    lines = content.split("\n")
    current_cheat = None

    cheat_number = None  
    for line in lines:
        line = line.strip()
        if line.startswith("cheats = "):
            cheat_number = 0
        elif line.startswith("cheat" + str(cheat_number)):
            if line.startswith("cheat" + str(cheat_number) + "_desc"):
                current_cheat = (extract_value(line),)  
            elif line.startswith("cheat" + str(cheat_number) + "_code"):
                current_cheat += (extract_value(line),)  
            elif line.startswith("cheat" + str(cheat_number) + "_enable"):
                current_cheat += ("false",)  
                cheats.append(current_cheat)  
                cheat_number += 1
    return cheats

def update_cheat_list(cheats):
    print_bool = True
    cheat_list.delete(0, tk.END)
    for cheat in cheats:
        if print_bool:
            print("cheat_desc: " + str(cheat[0]))
            print_bool = False
        cheat_list.insert(tk.END, cheat)

def show_cheat_details(event):
    if cheat_list.curselection():
        selected = cheat_list.get(cheat_list.curselection()[0])
        SELECTED_ITEM = selected
        print(selected)
        print(type(selected))

        # Enable the widgets when an item is selected
        description_entry.config(state=tk.NORMAL)
        code_entry.config(state=tk.NORMAL)
        save_button.config(state=tk.NORMAL)
        delete_button.config(state=tk.NORMAL)

        cheat = selected
        description_entry.delete(0, tk.END)
        description_entry.insert(0, cheat[DESCRIPTION])  
        code_entry.delete(0, tk.END)
        code_entry.insert(0, cheat[CODE])
    else:
        # Disable the widgets when no item is selected
        description_entry.delete(0, tk.END)
        code_entry.delete(0, tk.END)
        description_entry.config(state=tk.DISABLED)
        code_entry.config(state=tk.DISABLED)
        save_button.config(state=tk.DISABLED)
        delete_button.config(state=tk.DISABLED)

def save_changes():
    if cheat_list.curselection():
        selected_index = cheat_list.curselection()[0]
        selected = cheat_list.get(selected_index)
        cheat = selected
        
        new_description = description_entry.get()
        new_code = code_entry.get()
        modified_cheat = (new_description, new_code, "false")  
        cheats[selected_index] = modified_cheat
        cheat_list.delete(selected_index)  
        cheat_list.insert(selected_index, modified_cheat)  
        print(cheats[selected_index])
        print(cheat_list)
        SELECTED_ITEM = None
        messagebox.showinfo("Save", "Changes have been successfully saved.")
    else:
        messagebox.showerror("Error", "Make sure you have selected an item.")

def delete_cheat():
    if cheat_list.curselection():
        selected_index = cheat_list.curselection()[0]
        cheat_list.delete(selected_index)  

def create_new_cheat():
    new_description = new_description_entry.get()
    new_code = new_code_entry.get()
    if new_description and new_code:
        new_cheat = (new_description, new_code, "false")  
        list_length = cheat_list.size()
        cheat_list.insert(list_length, new_cheat)
        new_description_entry.delete(0, tk.END)
        new_code_entry.delete(0, tk.END)
        messagebox.showinfo("New Cheat", "New cheat have been successfully created and added to list.")
    else:
        messagebox.showerror("New Cheat", "Error while creating new cheat.\nPlease insert values")

def save_content_to_file():
    content = []

    content.append(f"cheats = {str(cheat_list.size())}")
    content.append("")

    for i in range(cheat_list.size()):
        cheat = cheat_list.get(i)
        content.append(f"cheat{i}_desc = \"{cheat[DESCRIPTION]}\"")
        content.append(f"cheat{i}_code = \"{cheat[CODE]}\"")
        content.append(f"cheat{i}_enable = {cheat[ENABLE]}")
        content.append("")
    
    filepath = filedialog.asksaveasfilename(defaultextension=".cht", filetypes=[("CHT File", "*.cht")])
    
    if filepath:
        with open(filepath, "w") as file:
            file.write("\n".join(content))

def info_window():
    messagebox.showinfo("Info", "Version: 0.1.1 \n21/08/2023\n\nCredits: Nicola Silveri\nGithub: https://github.com/nsilveri/CHT_Manager")

root = tk.Tk()
root.title("Cheat Code Management")

load_button = tk.Button(root, text="Load .cht File", command=load_file)
cheat_list = tk.Listbox(root)

modification_cheat_label = tk.Label(root, text="Mod selected cheat")
description_label = tk.Label(root, text="Description:")
description_entry = tk.Entry(root, state=tk.DISABLED)

code_label = tk.Label(root, text="Code:")
code_entry = tk.Entry(root, state=tk.DISABLED)

save_button = tk.Button(root, text="Save Changes", command=save_changes, state=tk.DISABLED)
delete_button = tk.Button(root, text="Delete", command=delete_cheat, state=tk.DISABLED)

new_cheat_label = tk.Label(root, text="Add new cheat")
new_description_label = tk.Label(root, text="New Description:")
new_description_entry = tk.Entry(root)
new_code_label = tk.Label(root, text="New Code:")
new_code_entry = tk.Entry(root)
new_cheat_button = tk.Button(root, text="Create New Cheat", command=create_new_cheat)

save_as_file_button = tk.Button(root, text="Save As...", command=save_content_to_file)
info_button = tk.Button(root, text="Info", command=info_window)

separator_mod_new_code = ttk.Separator(root, orient="horizontal")
separator_save_file_h = ttk.Separator(root, orient="horizontal")
separator_save_file_v = ttk.Separator(root, orient="vertical")

credits_label = tk.Label(root, text="Credits: Nicola Silveri")

cheat_list.bind("<Double-Button-1>", show_cheat_details)

load_button.grid(row=0, column=0)
cheat_list.grid(row=1, column=0, rowspan=6)

modification_cheat_label.grid(row=1, column=2)
description_label.grid(row=2, column=1)
description_entry.grid(row=2, column=2)
code_label.grid(row=3, column=1)
code_entry.grid(row=3, column=2)
save_button.grid(row=4, column=1, columnspan=2)
delete_button.grid(row=4, column=2, columnspan=2)

new_cheat_label.grid(row=6, column=2)
new_description_label.grid(row=7, column=1)
new_description_entry.grid(row=7, column=2)
new_code_label.grid(row=8, column=1)
new_code_entry.grid(row=8, column=2)
new_cheat_button.grid(row=9, column=1, columnspan=2)

save_as_file_button.grid(row=12, column=3)
info_button.grid(row=12, column=4, columnspan=2)

separator_mod_new_code.grid(row=5, column=1, columnspan=3, sticky="ew")

#separator_save_file_h.grid(row=11, column=3, columnspan=1, sticky="ew")
#separator_save_file_v.grid(row=12, column=3, rowspan=1, sticky="ns")

cheats = {}

root.mainloop()