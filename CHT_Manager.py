import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import re

DESCRIPTION = 0
CODE = 1
ENABLE = 2
SELECTED_ITEM = None

VERSION = "0.2"
DATE = "22/08/2023"

cheats = None

def load_file():
    global cheats
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
    global cheats
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
    global SELECTED_ITEM
    global cheats

    if cheat_list.curselection():
        selected = cheat_list.get(cheat_list.curselection()[0])
        SELECTED_ITEM = cheat_list.curselection()[0]
        print("SELECTED_ITEM: " + str(SELECTED_ITEM))
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
    global SELECTED_ITEM
    list_len = cheat_list.size()
    print(list_len)
    print(SELECTED_ITEM)

    if SELECTED_ITEM is not None and 0 <= SELECTED_ITEM < list_len: #len(cheats):
        selected = cheat_list.get(SELECTED_ITEM)
        cheat = selected

        new_description = description_entry.get()
        new_code = code_entry.get()
        modified_cheat = (new_description, new_code, "false")
        print("cheat: " + str(cheat_list))
        #cheats[SELECTED_ITEM] = modified_cheat
        cheat_list.delete(SELECTED_ITEM)
        cheat_list.insert(SELECTED_ITEM, modified_cheat)
        #print(cheats[SELECTED_ITEM])
        print(cheat_list)
        SELECTED_ITEM = None
        messagebox.showinfo("Save", "Changes have been successfully saved.")
    else:
        messagebox.showerror("Error", "Make sure you have selected a valid item.")


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
        messagebox.showinfo("New Cheat", "New cheat has been successfully created and added to the list.")
    else:
        messagebox.showerror("New Cheat", "Error while creating a new cheat.\nPlease insert values")

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
    messagebox.showinfo("Info", "Version: " + VERSION + " \n" + DATE + "\n\nCredits: Nicola Silveri\nGithub: https://github.com/nsilveri/CHT_Manager")

def open_parse_window():
    # Crea una nuova finestra per il parsing del testo
    parse_window = tk.Toplevel(root)
    parse_window.title("Parse Cheat")

    # Aggiungi una casella di testo multilinea per incollare il testo
    text_widget = tk.Text(parse_window, wrap=tk.WORD, width=40, height=10)
    text_widget.pack()

    
    def parse_text():
        # Ottieni il testo dalla casella di testo
        text = text_widget.get("1.0", "end-1c")

        # Utilizza espressioni regolari per trovare tutti i trucchi nel testo
        cheats = []
        cheat_pattern = r"([A-Za-z0-9\s]+?)(?:\s+(\d+))?\s+([A-Fa-f0-9\sX+]+)"

        for line in text.split("\n"):
            match = re.match(cheat_pattern, line)
            if match:
                name        = match.group(1).strip()
                if(match.group(2)):
                    name_number = " " + match.group(2)
                else:
                    name_number = ""
                code        = match.group(3).strip()
                cheats.append((name + str(name_number), code, "false"))

        # Aggiorna la lista dei trucchi
        #update_cheat_list(cheats)
        #new_cheat = (new_description, new_code, "false")

        for cheat in cheats:
            list_length = cheat_list.size()
            print("list_length: " + str(list_length))
            cheat_list.insert(list_length, cheat)


        # Chiudi la finestra di parsing
        parse_window.destroy()

    # Aggiungi un pulsante "Parse" per avviare l'analisi del testo
    parse_button = tk.Button(parse_window, text="Parse", command=parse_text)
    parse_button.pack()

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

#credits_label = tk.Label(root, text="Credits: Nicola Silveri")

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

# Aggiungi un pulsante "Parse cheat"
parse_button = tk.Button(root, text="Parse cheat", command=open_parse_window)
parse_button.grid(row=0, column=1)

#credits_label.grid(row=13, column=0, columnspan=6)

root.mainloop()
