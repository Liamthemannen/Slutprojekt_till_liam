import json
import customtkinter as ctk
from tkinter import messagebox

FILE_NAME = "phonebook.json"
CATEGORIES = ["Övrig", "Kompis", "Familj", "Kollega"]


def load_phonebook():
    try:
        with open(FILE_NAME, "r") as file:
            data = json.load(file)

            # Gör gamla kontakter kompatibla
            for name, value in list(data.items()):
                if isinstance(value, str):
                    data[name] = {
                        "number": value,
                        "category": "Övrig"
                    }

            return data

    except FileNotFoundError:
        return {}


def save_phonebook(phonebook):
    with open(FILE_NAME, "w") as file:
        json.dump(phonebook, file, indent=4)


class PhonebookApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.phonebook = load_phonebook()
        self.selected_name = None

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        self.title("Telefonbok")
        self.geometry("1100x700")
        self.minsize(900, 600)
        self.configure(fg_color="#0B0F1E")

        self.create_sidebar()
        self.create_main_area()
        self.show_contacts()

    def create_sidebar(self):
        self.sidebar = ctk.CTkFrame(self, width=250, corner_radius=0, fg_color="#10142A")
        self.sidebar.pack(side="left", fill="y")

        title = ctk.CTkLabel(
            self.sidebar,
            text="☎ Telefonbok",
            font=("Arial", 28, "bold"),
            text_color="white"
        )
        title.pack(pady=(35, 40))

        self.nav_button("Kontakter", self.show_contacts)
        self.nav_button("Lägg till", self.open_add_window)
        self.nav_button("Sök", self.search_contacts)
        self.nav_button("Sortera A-Z", self.sort_az)
        self.nav_button("Sortera Z-A", self.sort_za)

        self.exit_button = ctk.CTkButton(
            self.sidebar,
            text="Avsluta",
            height=50,
            corner_radius=14,
            fg_color="transparent",
            border_width=2,
            border_color="#E84AAE",
            hover_color="#2A163B",
            command=self.destroy
        )

        self.exit_button.pack(side="bottom", pady=35, padx=25, fill="x")

    def nav_button(self, text, command):
        button = ctk.CTkButton(
            self.sidebar,
            text=text,
            height=50,
            corner_radius=14,
            fg_color="transparent",
            hover_color="#6C2DC7",
            anchor="w",
            font=("Arial", 18),
            command=command
        )

        button.pack(pady=8, padx=25, fill="x")

    def create_main_area(self):
        self.main = ctk.CTkFrame(
            self,
            corner_radius=22,
            fg_color="#111827",
            border_width=1,
            border_color="#6C2DC7"
        )

        self.main.pack(side="right", fill="both", expand=True, padx=25, pady=25)

        header_frame = ctk.CTkFrame(self.main, fg_color="transparent")
        header_frame.pack(fill="x", padx=40, pady=(35, 10))

        self.title_label = ctk.CTkLabel(
            header_frame,
            text="Kontakter",
            font=("Arial", 42, "bold"),
            text_color="#E84AAE"
        )

        self.title_label.pack(side="left")

        self.search_entry = ctk.CTkEntry(
            header_frame,
            width=320,
            height=45,
            corner_radius=22,
            placeholder_text="Sök kontakt...",
            fg_color="#151B2E",
            border_color="#A64DFF",
            font=("Arial", 16)
        )

        self.search_entry.pack(side="right")
        self.search_entry.bind("<KeyRelease>", lambda event: self.search_contacts())

        button_frame = ctk.CTkFrame(self.main, fg_color="transparent")
        button_frame.pack(fill="x", padx=40, pady=25)

        self.add_button = ctk.CTkButton(
            button_frame,
            text="+ Lägg till",
            height=55,
            corner_radius=12,
            fg_color="#B832FF",
            hover_color="#8E24AA",
            font=("Arial", 18, "bold"),
            command=self.open_add_window
        )

        self.add_button.pack(side="left", expand=True, fill="x", padx=8)

        self.remove_button = ctk.CTkButton(
            button_frame,
            text="Ta bort",
            height=55,
            corner_radius=12,
            fg_color="#F43F5E",
            hover_color="#BE123C",
            font=("Arial", 18, "bold"),
            command=self.remove_contact
        )

        self.remove_button.pack(side="left", expand=True, fill="x", padx=8)

        self.edit_button = ctk.CTkButton(
            button_frame,
            text="Ändra",
            height=55,
            corner_radius=12,
            fg_color="#4F46E5",
            hover_color="#3730A3",
            font=("Arial", 18, "bold"),
            command=self.open_edit_window
        )

        self.edit_button.pack(side="left", expand=True, fill="x", padx=8)

        self.update_button = ctk.CTkButton(
            button_frame,
            text="Uppdatera",
            height=55,
            corner_radius=12,
            fg_color="#7C3AED",
            hover_color="#5B21B6",
            font=("Arial", 18, "bold"),
            command=self.show_contacts
        )

        self.update_button.pack(side="left", expand=True, fill="x", padx=8)

        self.contact_frame = ctk.CTkScrollableFrame(
            self.main,
            fg_color="#151B2E",
            corner_radius=15,
            border_width=1,
            border_color="#30384F"
        )

        self.contact_frame.pack(fill="both", expand=True, padx=40, pady=(5, 20))

        self.total_label = ctk.CTkLabel(
            self.main,
            text="Totalt: 0 kontakter",
            font=("Arial", 18),
            text_color="white"
        )

        self.total_label.pack(pady=(0, 25))

    def clear_contacts(self):
        for widget in self.contact_frame.winfo_children():
            widget.destroy()

    def show_contacts(self):
        self.search_entry.delete(0, "end")
        self.display_contacts(self.phonebook.items())

    def display_contacts(self, contacts):
        self.clear_contacts()

        contacts = list(contacts)
        count = 0

        for category in CATEGORIES:
            category_contacts = []

            for name, info in contacts:
                if info["category"] == category:
                    category_contacts.append((name, info))

            if not category_contacts:
                continue

            category_label = ctk.CTkLabel(
                self.contact_frame,
                text=category,
                font=("Arial", 24, "bold"),
                text_color="#E84AAE",
                anchor="w"
            )

            category_label.pack(fill="x", padx=15, pady=(20, 8))

            header = ctk.CTkFrame(
                self.contact_frame,
                fg_color="#1F2937",
                height=50,
                corner_radius=6
            )

            header.pack(fill="x", pady=(0, 8), padx=8)

            ctk.CTkLabel(
                header,
                text="Namn",
                font=("Arial", 17, "bold"),
                width=300,
                anchor="w"
            ).pack(side="left", padx=25, pady=10)

            ctk.CTkLabel(
                header,
                text="Telefonnummer",
                font=("Arial", 17, "bold"),
                width=250,
                anchor="w"
            ).pack(side="left", padx=25, pady=10)

            ctk.CTkLabel(
                header,
                text="Kategori",
                font=("Arial", 17, "bold"),
                anchor="w"
            ).pack(side="left", padx=25, pady=10)

            for name, info in category_contacts:
                count += 1
                number = info["number"]
                category = info["category"]

                is_selected = self.selected_name == name

                outer_row = ctk.CTkFrame(
                    self.contact_frame,
                    corner_radius=12,
                    fg_color="#D8B4FE" if is_selected else "#151B2E"
                )

                outer_row.pack(fill="x", pady=5, padx=10)

                inner_row = ctk.CTkFrame(
                    outer_row,
                    height=62,
                    corner_radius=10,
                    fg_color="#111827"
                )

                inner_row.pack(
                    fill="x",
                    padx=2 if is_selected else 0,
                    pady=2 if is_selected else 0
                )

                outer_row.bind("<Button-1>", lambda event, n=name: self.select_contact(n))
                inner_row.bind("<Button-1>", lambda event, n=name: self.select_contact(n))

                icon = ctk.CTkLabel(inner_row, text="👤", font=("Arial", 24), width=60)
                icon.pack(side="left", padx=(15, 5), pady=8)

                name_label = ctk.CTkLabel(
                    inner_row,
                    text=name,
                    font=("Arial", 18),
                    width=250,
                    anchor="w"
                )

                name_label.pack(side="left", padx=10, pady=8)

                number_label = ctk.CTkLabel(
                    inner_row,
                    text=number,
                    font=("Arial", 18),
                    width=230,
                    anchor="w"
                )

                number_label.pack(side="left", padx=25, pady=8)

                category_text = ctk.CTkLabel(
                    inner_row,
                    text=category,
                    font=("Arial", 18),
                    anchor="w"
                )

                category_text.pack(side="left", padx=25, pady=8)

                for widget in [icon, name_label, number_label, category_text]:
                    widget.bind("<Button-1>", lambda event, n=name: self.select_contact(n))

        self.total_label.configure(text=f"Totalt: {count} kontakter")

    def select_contact(self, name):
        self.selected_name = name
        self.display_contacts(self.phonebook.items())

    def search_contacts(self):
        search = self.search_entry.get().lower()

        results = []

        for name, info in self.phonebook.items():
            if search in name.lower() or search in info["number"] or search in info["category"].lower():
                results.append((name, info))

        self.display_contacts(results)

    def sort_az(self):
        sorted_contacts = sorted(self.phonebook.items())
        self.display_contacts(sorted_contacts)

    def sort_za(self):
        sorted_contacts = sorted(self.phonebook.items(), reverse=True)
        self.display_contacts(sorted_contacts)

    def open_add_window(self):
        self.contact_window("Lägg till kontakt")

    def open_edit_window(self):
        if not self.selected_name:
            messagebox.showwarning("Fel", "Välj en kontakt först.")
            return

        self.contact_window("Ändra kontakt", self.selected_name)

    def contact_window(self, title, old_name=None):
        window = ctk.CTkToplevel(self)

        window.title(title)
        window.geometry("400x430")
        window.configure(fg_color="#111827")
        window.grab_set()

        ctk.CTkLabel(
            window,
            text=title,
            font=("Arial", 28, "bold"),
            text_color="#E84AAE"
        ).pack(pady=(30, 20))

        ctk.CTkLabel(
            window,
            text="Namn",
            font=("Arial", 16, "bold"),
            text_color="white"
        ).pack()

        name_entry = ctk.CTkEntry(
            window,
            width=300,
            height=45,
            placeholder_text="Skriv namn",
            corner_radius=14
        )

        name_entry.pack(pady=(5, 15))

        ctk.CTkLabel(
            window,
            text="Telefonnummer",
            font=("Arial", 16, "bold"),
            text_color="white"
        ).pack()

        def only_numbers(text):
            return text.isdigit() or text == ""

        validate_command = window.register(only_numbers)

        number_entry = ctk.CTkEntry(
            window,
            width=300,
            height=45,
            placeholder_text="Skriv telefonnummer",
            corner_radius=14,
            validate="key",
            validatecommand=(validate_command, "%P")
        )

        number_entry.pack(pady=(5, 15))

        ctk.CTkLabel(
            window,
            text="Kategori (Frivillig)",
            font=("Arial", 16, "bold"),
            text_color="white"
        ).pack()

        category_menu = ctk.CTkOptionMenu(
            window,
            width=300,
            height=45,
            corner_radius=14,
            values=CATEGORIES
        )

        category_menu.pack(pady=(5, 10))
        category_menu.set("Övrig")

        if old_name:
            name_entry.insert(0, old_name)
            number_entry.insert(0, self.phonebook[old_name]["number"])
            category_menu.set(self.phonebook[old_name]["category"])

        def save_contact():
            name = name_entry.get().strip().title()
            number = number_entry.get().strip()
            category = category_menu.get()

            if not name or not number:
                messagebox.showwarning("Fel", "Skriv både namn och telefonnummer.")
                return

            if name in self.phonebook and old_name != name:
                replace = messagebox.askyesno(
                    "Kontakten finns redan",
                    f"{name} finns redan.\n\nVill du ersätta kontakten?"
                )

                if not replace:
                    return

            if old_name and old_name != name:
                del self.phonebook[old_name]

            self.phonebook[name] = {
                "number": number,
                "category": category
            }

            save_phonebook(self.phonebook)

            self.selected_name = name
            self.show_contacts()

            window.destroy()

        ctk.CTkButton(
            window,
            text="Spara",
            height=45,
            corner_radius=14,
            fg_color="#B832FF",
            hover_color="#8E24AA",
            font=("Arial", 17, "bold"),
            command=save_contact
        ).pack(pady=25)

    def remove_contact(self):
        if not self.selected_name:
            messagebox.showwarning("Fel", "Välj en kontakt först.")
            return

        answer = messagebox.askyesno(
            "Ta bort kontakt",
            f"Vill du ta bort {self.selected_name}?"
        )

        if answer:
            del self.phonebook[self.selected_name]

            save_phonebook(self.phonebook)

            self.selected_name = None
            self.show_contacts()


app = PhonebookApp()
app.mainloop()