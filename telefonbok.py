import json
import customtkinter as ctk
from tkinter import messagebox, simpledialog

FILE_NAME = "phonebook.json"
SETTINGS_FILE = "settings.json"

DEFAULT_CATEGORIES = ["Övrig", "Kompis", "Familj", "Kollega"]

# Läser inställningar från JSOn-fil
def load_settings():

    # Försöker läsa JSON-filen och skapar standardkategorier ifall det ej finns
    try:
        with open(SETTINGS_FILE, "r") as file:
            settings = json.load(file)

            if "show_categories" not in settings:
                settings["show_categories"] = True

            if "categories" not in settings:
                settings["categories"] = DEFAULT_CATEGORIES

            if "Övrig" not in settings["categories"]:
                settings["categories"].insert(0, "Övrig")

            return settings
    # Retunerar standardiställningar
    except FileNotFoundError:
        return {
            "show_categories": True,
            "categories": DEFAULT_CATEGORIES
        }

# Sparar inställningarna
def save_settings(settings):
    with open(SETTINGS_FILE, "w") as file:
        json.dump(settings, file, indent=4)

#Läser in kontakterna från JSON-fil
def load_phonebook():
    try:
        with open(FILE_NAME, "r") as file:
            data = json.load(file)

            #Går igenom alla kontakter och gör om det till rättstruktur i JSON
            for name, value in list(data.items()):
                if isinstance(value, str):
                    data[name] = {
                        "numbers": [value],
                        "email": "",
                        "category": "Övrig"
                    }

                # Byter ut gamla "keyn" till nya
                if "number" in data[name]:
                    data[name]["numbers"] = [data[name]["number"]]
                    del data[name]["number"]

                # Skapar tomma datatyper ifall det saknas
                if "numbers" not in data[name]:
                    data[name]["numbers"] = []

                if "email" not in data[name]:
                    data[name]["email"] = ""

                if "category" not in data[name]:
                    data[name]["category"] = "Övrig"

            return data

    # Ifall JSON-filen inte finns så retuneras en tom dictonary
    except FileNotFoundError:
        return {}

# Sparar kontakterna
def save_phonebook(phonebook):
    with open(FILE_NAME, "w") as file:
        json.dump(phonebook, file, indent=4)

#Klass för vår telefonbok
class PhonebookApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Läser in all data
        self.settings = load_settings()
        self.phonebook = load_phonebook()
        self.selected_name = None

        # Appens utseende
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        # Skapar huvudmeny
        self.title("Telefonbok")
        self.geometry("1100x700")
        self.minsize(900, 600)
        self.configure(fg_color="#0B0F1E")

        # Skapar menyn till sidan av huvudmenyn
        self.create_sidebar()
        self.create_main_area()

        # Visar kontakterna
        self.show_contacts()
        
    # Skapar nytt namn ifall kontakten redan finns
    def make_unique_name(self, name):

        # Retunerar vanliga namnet
        if name not in self.phonebook:
            return name

        # Start number, tex finns det 2 st Liam blir det Liam (2)
        number = 2
        new_name = f"{name} ({number})"

        # Ökar numret tills det blir unikt
        while new_name in self.phonebook:
            number += 1
            new_name = f"{name} ({number})"

        return new_name

    # skapar "sidebar" till programmet
    def create_sidebar(self):

        # skapar sidobarens utseende
        self.sidebar = ctk.CTkFrame(
            self,
            width=250,
            corner_radius=0,
            fg_color="#10142A"
        )
        self.sidebar.pack(side="left", fill="y")

        # Logga högst upp med titel
        title = ctk.CTkLabel(
            self.sidebar,
            text="☎ Telefonbok",
            font=("Arial", 28, "bold"),
            text_color="white"
        )
        title.pack(pady=(35, 40))

        # Skapar de specifika sidoknapparna
        self.nav_button("Kontakter", self.show_contacts)
        self.nav_button("Lägg till", self.open_add_window)
        self.nav_button("Settings", self.show_settings)
        self.nav_button("Sortera A-Z", self.sort_az)
        self.nav_button("Sortera Z-A", self.sort_za)

        # Avsluta knapp
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

    # Skapar en generell knapp i "Sidemenu"
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

            #Funktionen som körs när knappen klickas
            command=command
        )

        #Placerar knappen
        button.pack(pady=8, padx=25, fill="x")

    # Skapar huvudytan
    def create_main_area(self):

        # Skapar ramen
        self.main = ctk.CTkFrame(
            self,
            corner_radius=22,
            fg_color="#111827",
            border_width=1,
            border_color="#6C2DC7"
        )
        self.main.pack(
            side="right",
            fill="both",
            expand=True,
            padx=25,
            pady=25
        )

        # Skapar ramen högst upp
        header_frame = ctk.CTkFrame(self.main, fg_color="transparent")
        header_frame.pack(fill="x", padx=40, pady=(35, 10))

        # Sidans titel
        self.title_label = ctk.CTkLabel(
            header_frame,
            text="Kontakter",
            font=("Arial", 42, "bold"),
            text_color="#E84AAE"
        )
        self.title_label.pack(side="left")

        # Ruta för sökakontakter
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

        # Gör så sökningen fungerar
        self.search_entry.bind("<KeyRelease>", lambda event: self.search_contacts())

        # Frame för knapparna
        self.button_frame = ctk.CTkFrame(self.main, fg_color="transparent")
        self.button_frame.pack(fill="x", padx=40, pady=25)

        # Knapp för lägga till kontakt
        self.add_button = ctk.CTkButton(
            self.button_frame,
            text="+ Lägg till",
            height=55,
            corner_radius=12,
            fg_color="#B832FF",
            hover_color="#8E24AA",
            font=("Arial", 18, "bold"),
            command=self.open_add_window
        )
        self.add_button.pack(side="left", expand=True, fill="x", padx=8)

        # Knapp för ta bort kontakt
        self.remove_button = ctk.CTkButton(
            self.button_frame,
            text="Ta bort",
            height=55,
            corner_radius=12,
            fg_color="#F43F5E",
            hover_color="#BE123C",
            font=("Arial", 18, "bold"),
            command=self.remove_contact
        )
        self.remove_button.pack(side="left", expand=True, fill="x", padx=8)

        # Knapp för ändra kontakt
        self.edit_button = ctk.CTkButton(
            self.button_frame,
            text="Ändra",
            height=55,
            corner_radius=12,
            fg_color="#4F46E5",
            hover_color="#3730A3",
            font=("Arial", 18, "bold"),
            command=self.open_edit_window
        )
        self.edit_button.pack(side="left", expand=True, fill="x", padx=8)

        # Knapp för uppdatera listan
        self.update_button = ctk.CTkButton(
            self.button_frame,
            text="Uppdatera",
            height=55,
            corner_radius=12,
            fg_color="#7C3AED",
            hover_color="#5B21B6",
            font=("Arial", 18, "bold"),
            command=self.show_contacts
        )
        self.update_button.pack(side="left", expand=True, fill="x", padx=8)

        # Skroll för kontakter ifall alla inte får plats
        self.contact_frame = ctk.CTkScrollableFrame(
            self.main,
            fg_color="#151B2E",
            corner_radius=15,
            border_width=1,
            border_color="#30384F"
        )
        self.contact_frame.pack(fill="both", expand=True, padx=40, pady=(5, 20))

        # Text som visar antal kontakter
        self.total_label = ctk.CTkLabel(
            self.main,
            text="Totalt: 0 kontakter",
            font=("Arial", 18),
            text_color="white"
        )
        self.total_label.pack(pady=(0, 25))

    # Funktion som gömemr kontakterna
    def hide_contact_buttons(self):
        self.button_frame.pack_forget()

    # FUnktion som visar kontakterna
    def show_contact_buttons(self):
        self.button_frame.pack(fill="x", padx=40, pady=25)

    # Rensar alla kontakter
    def clear_contacts(self):
        for widget in self.contact_frame.winfo_children():
            widget.destroy()

    # Visar alla i telefonboken
    def show_contacts(self):
        self.show_contact_buttons()
        self.title_label.configure(text="Kontakter")
        self.search_entry.delete(0, "end")
        self.display_contacts(self.phonebook.items())

    # Visar kontakterna i kontaktlistan 
    def display_contacts(self, contacts):
        self.clear_contacts()

        contacts = list(contacts)
        count = 0

        # Om man satt på kategorier i settings, ska det visas annars inte
        if self.settings["show_categories"]:
            categories_to_show = self.settings["categories"]
        else:
            categories_to_show = ["Alla kontakter"]

        # Lägger till kontakten beroende på om kategorier är på eller inte
        for category in categories_to_show:
            category_contacts = []

            for name, info in contacts:
                if self.settings["show_categories"]:
                    if info["category"] == category:
                        category_contacts.append((name, info))
                else:
                    category_contacts.append((name, info))

            if not category_contacts:
                continue

            # Visar kategoriens namn
            if self.settings["show_categories"]:
                category_label = ctk.CTkLabel(
                    self.contact_frame,
                    text=category,
                    font=("Arial", 24, "bold"),
                    text_color="#E84AAE",
                    anchor="w"
                )
                category_label.pack(fill="x", padx=15, pady=(20, 8))

             # Skapar rubrikrad
            header = ctk.CTkFrame(
                self.contact_frame,
                fg_color="#1F2937",
                height=50,
                corner_radius=6
            )
            header.pack(fill="x", pady=(0, 8), padx=8)

            # Rubrik för namn
            ctk.CTkLabel(
                header,
                text="Namn",
                font=("Arial", 17, "bold"),
                width=300,
                anchor="w"
            ).pack(side="left", padx=25, pady=10)

             # Rubrik för telefonnummer
            ctk.CTkLabel(
                header,
                text="Telefonnummer",
                font=("Arial", 17, "bold"),
                width=250,
                anchor="w"
            ).pack(side="left", padx=25, pady=10)

             # Rubrik för kategori
            if self.settings["show_categories"]:
                ctk.CTkLabel(
                    header,
                    text="Kategori",
                    font=("Arial", 17, "bold"),
                    anchor="w"
                ).pack(side="left", padx=25, pady=10)

            # Skapar en ny rad för varje kontakt som finns
            for name, info in category_contacts:
                count += 1

                number = info["numbers"][0] if info["numbers"] else "Inget nummer" # Hämtar första numret eller standardtext
                category = info["category"]

                # Kontrollerar om kontakten är vald
                is_selected = self.selected_name == name

                # Ram som Visar vald kontakt
                outer_row = ctk.CTkFrame(
                    self.contact_frame,
                    corner_radius=12,
                    fg_color="#D8B4FE" if is_selected else "#151B2E"
                )
                outer_row.pack(fill="x", pady=5, padx=10)

                # Ram som visar information
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

                # Gör så att de olika raderna går att klicka på
                outer_row.bind("<Button-1>", lambda event, n=name: self.select_contact(n))
                inner_row.bind("<Button-1>", lambda event, n=name: self.select_contact(n))

                # Logga för kontakt
                icon = ctk.CTkLabel(
                    inner_row,
                    text="👤",
                    font=("Arial", 24),
                    width=60
                )
                icon.pack(side="left", padx=(15, 5), pady=8)

                # Kontaktens namn
                name_label = ctk.CTkLabel(
                    inner_row,
                    text=name,
                    font=("Arial", 18),
                    width=250,
                    anchor="w"
                )
                name_label.pack(side="left", padx=10, pady=8)

                # Kontaktens nummer
                number_label = ctk.CTkLabel(
                    inner_row,
                    text=number,
                    font=("Arial", 18),
                    width=230,
                    anchor="w"
                )
                number_label.pack(side="left", padx=25, pady=8)

                widgets_to_bind = [icon, name_label, number_label] # Samlar widgets som ska vara klickbara


            # Visar kategori om kategorier är aktiverade
                if self.settings["show_categories"]:
                    category_text = ctk.CTkLabel(
                        inner_row,
                        text=category,
                        font=("Arial", 18),
                        anchor="w"
                    )
                    category_text.pack(side="left", padx=25, pady=8)
                    widgets_to_bind.append(category_text)

                # Gör alla texter på raden klickbara
                for widget in widgets_to_bind:
                    widget.bind("<Button-1>", lambda event, n=name: self.select_contact(n))

        self.total_label.configure(text=f"Totalt: {count} kontakter") # Uppdaterar antalet kontakter


    # Gör så man kan välja kontakt
    def select_contact(self, name):
        self.selected_name = name
        self.show_contact_details(name)

    # Funktion för söka kontakt
    def search_contacts(self):
        if self.title_label.cget("text") == "Settings": # Felhantering ifall man söker medan man är i settingmenyn
            return

        # Hämtar texten från sökrutan och gör den till små bokstäver
        search = self.search_entry.get().lower()
        results = []

        # Går igenom alla kontakter, om den hittar något som matchar så lägger den in det i resultat
        for name, info in self.phonebook.items():
            if (
                search in name.lower()
                or any(search in number for number in info["numbers"])
                or search in info["category"].lower()
            ):
                results.append((name, info))
        
        # Visar resultaten
        self.display_contacts(results)

    # Visar information om vald kontakt tex e-mail
    def show_contact_details(self, name):
        self.clear_contacts() # Rensar kontakterna 
        self.title_label.configure(text=name) # Gör om titel till valda kontaktens namn

        info = self.phonebook[name]

        # Skapar en frame för personens information
        details_frame = ctk.CTkFrame(
            self.contact_frame,
            fg_color="#111827",
            corner_radius=16
        )
        details_frame.pack(fill="x", padx=25, pady=25)

        # Visar kontaktens namn
        ctk.CTkLabel(
            details_frame,
            text=name,
            font=("Arial", 32, "bold"),
            text_color="#E84AAE"
        ).pack(pady=(25, 15))

        # Visar personens kategori
        ctk.CTkLabel(
            details_frame,
            text=f"Kategori: {info['category']}",
            font=("Arial", 20),
            text_color="white"
        ).pack(pady=8)

        # Visar personens telefonnummer, kan vara fler
        ctk.CTkLabel(
            details_frame,
            text="Telefonnummer",
            font=("Arial", 24, "bold"),
            text_color="#E84AAE"
        ).pack(pady=(25, 10))

        for number in info["numbers"]:
            ctk.CTkLabel(
                details_frame,
                text=number,
                font=("Arial", 20),
                text_color="white"
            ).pack(pady=4)

        # Visar personens e-mail om det finns tillagt
        ctk.CTkLabel(
            details_frame,
            text="Email",
            font=("Arial", 24, "bold"),
            text_color="#E84AAE"
        ).pack(pady=(25, 10))

        email_text = info["email"] if info["email"] else "Ingen email"

        ctk.CTkLabel(
            details_frame,
            text=email_text,
            font=("Arial", 20),
            text_color="white"
        ).pack(pady=4)

        # Tillbaka knapp ifall man vill ut ur menyn
        back_button = ctk.CTkButton(
            details_frame,
            text="Tillbaka",
            height=45,
            corner_radius=14,
            fg_color="#B832FF",
            hover_color="#8E24AA",
            font=("Arial", 17, "bold"),
            command=self.show_contacts
        )
        back_button.pack(pady=30)

    # Sorterar kontakterna från a-z
    def sort_az(self):
        if self.title_label.cget("text") == "Settings":
            return

        sorted_contacts = sorted(self.phonebook.items())
        self.display_contacts(sorted_contacts)

    # Sorterar kontakterna från z-a
    def sort_za(self):
        if self.title_label.cget("text") == "Settings":
            return

        sorted_contacts = sorted(self.phonebook.items(), reverse=True)
        self.display_contacts(sorted_contacts)

    
    def show_settings(self):
        self.hide_contact_buttons()
        self.search_entry.delete(0, "end")
        self.clear_contacts()

        self.title_label.configure(text="Settings")

        settings_frame = ctk.CTkFrame(
            self.contact_frame,
            fg_color="#111827",
            corner_radius=16
        )
        settings_frame.pack(fill="x", padx=25, pady=25)

        ctk.CTkLabel(
            settings_frame,
            text="Inställningar",
            font=("Arial", 30, "bold"),
            text_color="#E84AAE"
        ).pack(pady=(25, 20))

        self.category_switch = ctk.CTkSwitch(
            settings_frame,
            text="Visa kategorier",
            font=("Arial", 20),
            progress_color="#B832FF"
        )
        self.category_switch.pack(pady=15)

        if self.settings["show_categories"]:
            self.category_switch.select()
        else:
            self.category_switch.deselect()

        add_category_button = ctk.CTkButton(
            settings_frame,
            text="+ Lägg till kategori",
            height=50,
            corner_radius=14,
            fg_color="#4F46E5",
            hover_color="#3730A3",
            font=("Arial", 18, "bold"),
            command=self.open_add_category_window
        )
        add_category_button.pack(pady=15, padx=35, fill="x")

        ctk.CTkLabel(
            settings_frame,
            text="Kategorier",
            font=("Arial", 22, "bold"),
            text_color="white"
        ).pack(pady=(20, 10))

        self.category_list_frame = ctk.CTkFrame(
            settings_frame,
            fg_color="#151B2E",
            corner_radius=12
        )
        self.category_list_frame.pack(fill="x", padx=35, pady=10)

        self.show_category_list()

        save_button = ctk.CTkButton(
            settings_frame,
            text="Spara",
            height=50,
            corner_radius=14,
            fg_color="#B832FF",
            hover_color="#8E24AA",
            font=("Arial", 18, "bold"),
            command=self.save_settings_menu
        )
        save_button.pack(pady=(20, 30), padx=35, fill="x")

        self.total_label.configure(text="")

    def show_category_list(self):
        for widget in self.category_list_frame.winfo_children():
            widget.destroy()

        for category in self.settings["categories"]:
            row = ctk.CTkFrame(
                self.category_list_frame,
                fg_color="transparent"
            )
            row.pack(fill="x", padx=15, pady=6)

            ctk.CTkLabel(
                row,
                text=f"• {category}",
                font=("Arial", 18),
                text_color="white",
                anchor="w"
            ).pack(side="left", fill="x", expand=True)

            if category != "Övrig":
                ctk.CTkButton(
                    row,
                    text="Ta bort",
                    width=90,
                    height=35,
                    corner_radius=10,
                    fg_color="#F43F5E",
                    hover_color="#BE123C",
                    command=lambda c=category: self.remove_category(c)
                ).pack(side="right", padx=5)

    def open_add_category_window(self):
        window = ctk.CTkToplevel(self)

        window.title("Lägg till kategori")
        window.geometry("400x250")
        window.configure(fg_color="#111827")
        window.grab_set()

        ctk.CTkLabel(
            window,
            text="Lägg till kategori",
            font=("Arial", 28, "bold"),
            text_color="#E84AAE"
        ).pack(pady=(30, 25))

        category_entry = ctk.CTkEntry(
            window,
            width=300,
            height=45,
            placeholder_text="Skriv kategori",
            corner_radius=14
        )
        category_entry.pack(pady=10)

        def save_category():
            category = category_entry.get().strip().title()

            if not category:
                messagebox.showwarning(
                    "Fel",
                    "Skriv ett kategorinamn."
                )
                return

            if category in self.settings["categories"]:
                messagebox.showwarning(
                    "Fel",
                    "Den kategorin finns redan."
                )
                return

            self.settings["categories"].append(category)
            self.show_category_list()

            window.destroy()

        ctk.CTkButton(
            window,
            text="Lägg till",
            height=45,
            corner_radius=14,
            fg_color="#B832FF",
            hover_color="#8E24AA",
            font=("Arial", 17, "bold"),
            command=save_category
        ).pack(pady=25)
        
    def remove_category(self, category):
        answer = messagebox.askyesno(
            "Ta bort kategori",
            f"Vill du ta bort kategorin {category}?\n\nAlla kontakter i den kategorin flyttas till Övrig."
        )

        if not answer:
            return

        self.settings["categories"].remove(category)

        for name, info in self.phonebook.items():
            if info["category"] == category:
                info["category"] = "Övrig"

        save_phonebook(self.phonebook)
        save_settings(self.settings)

        self.show_category_list()

    def save_settings_menu(self):
        answer = messagebox.askyesno(
            "Spara inställningar",
            "Är du säker på att du vill spara inställningarna?"
        )

        if not answer:
            return

        self.settings["show_categories"] = bool(self.category_switch.get())

        save_settings(self.settings)

        messagebox.showinfo(
            "Sparat",
            "Inställningarna har sparats."
        )

        self.show_contacts()

    def open_add_window(self):
        self.contact_window("Lägg till kontakt")

    def open_edit_window(self):
        if not self.selected_name:
            messagebox.showwarning(
                "Fel",
                "Välj en kontakt först."
            )
            return

        self.contact_window("Ändra kontakt", self.selected_name)

    def contact_window(self, title, old_name=None):
        window = ctk.CTkToplevel(self)

        window.title(title)
        window.geometry("450x600")
        window.configure(fg_color="#111827")
        window.grab_set()

        scroll_frame = ctk.CTkScrollableFrame(
            window,
            fg_color="#111827",
            corner_radius=0
        )
        scroll_frame.pack(fill="both", expand=True)

        ctk.CTkLabel(
            scroll_frame,
            text=title,
            font=("Arial", 28, "bold"),
            text_color="#E84AAE"
        ).pack(pady=(25, 15))

        ctk.CTkLabel(
            scroll_frame,
            text="Namn",
            font=("Arial", 16, "bold"),
            text_color="white"
        ).pack()

        name_entry = ctk.CTkEntry(
            scroll_frame,
            width=330,
            height=45,
            placeholder_text="Skriv namn",
            corner_radius=14
        )
        name_entry.pack(pady=(5, 15))

        ctk.CTkLabel(
            scroll_frame,
            text="Telefonnummer",
            font=("Arial", 16, "bold"),
            text_color="white"
        ).pack()

        numbers_frame = ctk.CTkFrame(scroll_frame, fg_color="transparent")
        numbers_frame.pack()

        number_entries = []

        def only_numbers(text):
            return text.isdigit() or text == ""

        validate_command = window.register(only_numbers)

        def add_number_field(number=""):
            row = ctk.CTkFrame(numbers_frame, fg_color="transparent")
            row.pack(pady=5)

            entry = ctk.CTkEntry(
                row,
                width=270,
                height=45,
                placeholder_text="Skriv telefonnummer",
                corner_radius=14,
                validate="key",
                validatecommand=(validate_command, "%P")
            )
            entry.pack(side="left", padx=(0, 8))
            entry.insert(0, number)

            number_entries.append(entry)

            plus_button = ctk.CTkButton(
                row,
                text="+",
                width=45,
                height=45,
                corner_radius=14,
                fg_color="#22C55E",
                hover_color="#16A34A",
                font=("Arial", 22, "bold"),
                command=lambda: add_number_field()
            )
            plus_button.pack(side="left")

        add_number_field()

        ctk.CTkLabel(
            scroll_frame,
            text="Email (frivillig)",
            font=("Arial", 16, "bold"),
            text_color="white"
        ).pack(pady=(15, 0))

        email_entry = ctk.CTkEntry(
            scroll_frame,
            width=330,
            height=45,
            placeholder_text="Skriv email",
            corner_radius=14
        )
        email_entry.pack(pady=(5, 15))

        ctk.CTkLabel(
            scroll_frame,
            text="Kategori (frivillig)",
            font=("Arial", 16, "bold"),
            text_color="white"
        ).pack()

        category_menu = ctk.CTkOptionMenu(
            scroll_frame,
            width=330,
            height=45,
            corner_radius=14,
            values=self.settings["categories"]
        )
        category_menu.pack(pady=(5, 10))
        category_menu.set("Övrig")

        if old_name:
            name_entry.insert(0, old_name)

            for widget in numbers_frame.winfo_children():
                widget.destroy()

            number_entries.clear()

            for number in self.phonebook[old_name]["numbers"]:
                add_number_field(number)

            email_entry.insert(0, self.phonebook[old_name]["email"])
            category_menu.set(self.phonebook[old_name]["category"])

        def save_contact():
            name = name_entry.get().strip().title()
            email = email_entry.get().strip()
            category = category_menu.get()

            numbers = []

            for entry in number_entries:
                number = entry.get().strip()

                if number:
                    numbers.append(number)

            if not name or not numbers:
                messagebox.showwarning(
                    "Fel",
                    "Skriv namn och minst ett telefonnummer."
                )
                return

            if old_name and old_name != name:
                del self.phonebook[old_name]

            self.phonebook[name] = {
                "numbers": numbers,
                "email": email,
                "category": category
            }

            save_phonebook(self.phonebook)

            self.selected_name = name
            self.show_contacts()

            window.destroy()

        ctk.CTkButton(
            scroll_frame,
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
            messagebox.showwarning(
                "Fel",
                "Välj en kontakt först."
            )
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