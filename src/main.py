# made by toasterclan1 or @toaster_clan_1 on discord

import os
import re
from datetime import datetime
import sys
from  tkinter import *
from tkinter import filedialog
import zipfile
from tkinter import messagebox
SAVE_FILE = ""

def extract_strings(data, min_length=4):
    pattern = rb"[\x20-\x7E]{" + str(min_length).encode() + rb",}"
    return [s.decode("utf-8", errors="ignore") for s in re.findall(pattern, data)]


def find_after_key(data, key):
    key_bytes = key.encode()

    idx = data.find(key_bytes)
    if idx == -1:
        return None

    chunk = data[idx:idx + 200]

    matches = re.findall(rb"[\x20-\x7E]{3,}", chunk)

    for m in matches:
        text = m.decode(errors="ignore").strip()

        if text and text not in [
            "DisplayName", "DisplayNameStr",
            "StrProperty", "None"
        ]:
            return text

    return None


def extract_save_info(path):

    try:

        with open(path, "rb") as f:
            data = f.read()
    except Exception as e:
        return {
            "save_name": "N/A",
            "gamemode": "N/A",
            "map": "N/A",
           "last_modified": "N/A"
        }

    strings = extract_strings(data)
    text = data.decode("utf-8", errors="ignore")

    info = {
        "save_name": "Unknown",
        "gamemode": "Unknown",
        "map": "Unknown",
        "last_modified": "Unknown"
    }


    info["save_name"] = (
        find_after_key(data, "DisplayName")
        or find_after_key(data, "DisplayNameStr")
        or "Unknown"
    )

    # fallback
    if info["save_name"] == "Unknown":
        for s in strings:
            if "Hosted game" in s:
                info["save_name"] = s
                break


    modes = ["Survival", "Creative", "Freedom", "Hardcore"]

    for mode in modes:
        if mode in text:
            info["gamemode"] = mode
            break


    map_match = re.search(r"/Game/Maps/[A-Za-z0-9_/]+", text)

    if map_match:
        info["map"] = map_match.group(0)

    modified = os.path.getmtime(path)

    info["last_modified"] = datetime.fromtimestamp(
        modified
    ).strftime("%Y-%m-%d %H:%M:%S")

    return info


save_info = extract_save_info(SAVE_FILE)



class Application(Frame):
    
    def createWdigets(self):
        self.title = Label(self, text="Subnautica 2 Save Sharer", fg="white", bg="#241414")
        self.title["font"] = ("Arial", 16)
        self.title["padx"] = 200
        self.title["pady"] = 50

        def save_to_zip():
            if not SAVE_FILE:
                print("No file selected")
                no_file = messagebox.showerror("Error", "No file selected. Please select a save file first.")
                return

            output_dir = filedialog.askdirectory(title="Select Output Folder")
            if not output_dir:
                return
            info_text = (
                f"Save Name: {save_info['save_name']}\n"
                f"Gamemode: {save_info['gamemode']}\n"
                f"Last Modified: {save_info['last_modified']}"
        )

            confirm = messagebox.askyesno(
                "Confirm Save",
                "Are you sure this is the file you want?\n\n" + info_text
            )



            if not confirm:
                return
            
            tell_how = messagebox.showinfo(
                "How to Share",
                "After clicking OK, a zip file will be created in the selected folder. You can share this zip file with others.\n\nTo use the zip file, the reciver must extract the zip into their Subnautica 2 saves folder. (Usually located at C:\\Users\\[Username]\\AppData\\local\\Subnautica2\\Saved\\SaveGames) You may have to unhide hidden folders to see this appdata folder.\n\n Make sure to backup Your saves before extracting in-case of any iussues.\n\nMake sure the extracted files do NOT overide your own (e.g. savegame_0_1.sav should be renamed to savegame_5_1 for example)\n\nHave fun! (ask me questions on discord @toasterclan1)"
            )
            name = "_" + save_info["save_name"].replace(" ", "_") if save_info["save_name"] != "Unknown" else ""
            date = "_" + save_info["last_modified"].replace(" ", "_").replace(":", "-") if save_info["last_modified"] != "Unknown" else ""
            mode = "_" + save_info["gamemode"] if save_info["gamemode"] != "Unknown" else ""
            zip_path = os.path.join(
                output_dir,
                os.path.splitext(os.path.basename(SAVE_FILE))[0] + name + mode + date + ".zip"
            )

            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                zipf.write(SAVE_FILE, os.path.basename(SAVE_FILE) + name + mode + date + ".sav")

            print(f"Saved {SAVE_FILE} to {zip_path}")

        def select_file():
            file_path = filedialog.askopenfilename(
                title="Select a file",
                filetypes=[("Save Files", "*.sav"), ("All files", "*.*")]
            )
    
            if file_path:
                global SAVE_FILE
                global save_info
                SAVE_FILE = file_path
                save_info = extract_save_info(SAVE_FILE)
                self.current_file.config(text="Current File: " + SAVE_FILE, fg="white", bg="#241414")
                self.save_info.config(text=f"Info: Save Name: {save_info['save_name']}, Gamemode: {save_info['gamemode']}, Last Modified: {save_info['last_modified']}", fg="#383838", bg="#241414")
                print(f"Selected: {file_path}")
        self.select_file_callback = select_file

        self.title.pack({"side": "top"})
        self.select_file = Button(self)
        self.select_file["text"] = "Select File"
        self.select_file["command"] = self.select_file_callback
        self.select_file.pack({"side": "top"})

        self.current_file = Label(self, text="Current File: None", fg="white", bg="#241414")
        self.current_file.pack({"side": "top"})


        self.save = Button(self, text="Save to zip", command=save_to_zip)
        self.save.pack(side="top")

        self.import_zip = Label(self, text="Soon...", fg="#383838", bg="#241414")
        self.import_zip.pack({"side": "top"})

        self.save_info = Label(self, text="Info: N/A", fg="#383838", bg="#241414")
        self.save_info.pack({"side": "top"})


    def __init__(self, master=None):
        Frame.__init__(self, master, bg="#241414")
        self.pack()
        self.createWdigets()

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

root = Tk()
root.configure(bg="#241414")
root.title("Subnautica 2 Save Sharer")
root.geometry("600x400")
root.iconbitmap(resource_path("src/icon.ico"))
app = Application(master=root)
if getattr(sys, "frozen", False):
    try:
        import pyi_splash
        pyi_splash.close()
    except ImportError:
        pass
app.mainloop()