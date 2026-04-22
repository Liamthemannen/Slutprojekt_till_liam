import json
def telefon():

    def loadPhonebook():
        try:
            with open("phonebook.json", "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return {}
    
    def savePhonebook(Phonebook):
        with open("phonebook.json", "w") as file:
            json.dump(Phonebook, file, indent=4)
    Phonebook = loadPhonebook()
    
    def sortPhonebook():
        if not Phonebook:
            print("Listan är tom")
            return

        print("1. Sortera efter namn")
        print("2. Sortera efter nummer")
        choice = input("Välj: ")

        if choice == "1":
            sorted_list = sorted(Phonebook.items())
        elif choice == "2":
            sorted_list = sorted(Phonebook.items(), key=lambda x: x[1])
        else:
            print("Fel val")
            return

        for name, phonenumber in sorted_list:
            print(name, phonenumber)
        
    
    def addPerson():   
        name = input("Vad är deras namn ")
        bigLetter = name[0].upper()
        name = bigLetter + name[1:]
        print(name)
        phonenumber = input("Vad är deras telefonnummer ")
        Phonebook[name] = phonenumber

    def removePerson():
        removeChoice = input("Vilken vill du ta bort ").lower()
        for name in list(Phonebook.keys()):
            if removeChoice == name.lower():
                Phonebook.pop(name)
                print("Personen togs bort.")
                return
    
    def searchName():
        searchChoice = input("Vilket namn vill du söka på? ").lower()
        found = False

        for name, phonenumber in list(Phonebook.items()):
            if searchChoice == name.lower():
                print("Telefonnumret är:")
                print(phonenumber)
                found = True
                break
        if not found:
            print("Personen finns inte")
    
    def editContact():
        searchChoice = input("Vilket namn vill du söka på? ").lower()
        found = False

        for name, phonenumber in list(Phonebook.items()):
            if searchChoice == name.lower():
                print("Telefonnumret är: " + phonenumber)
                newName = input("Skriv nya namnet (Tryck enter för behålla det gamla) ")
                if newName:
                    newName = newName.title()
                else:
                    newName = name
                newPhonenumber = int(input("Skriv nya telefonnumret (Tryck enter för behålla det gamla) "))
                if newPhonenumber:
                    phonenumber = newPhonenumber
                Phonebook[newName] = phonenumber

                if newName != name:
                    del Phonebook[name]

                print("Kontakten har uppdaterats.")
                found = True
                break
        if not found:
            print("Personen finns inte")

    def meny():
        running = True
        while running:
            try:
                print()
                print("Skriv 1 för lägga till nummer")
                print("Skriv 2 för få upp lista på nummer")
                print("Skriv 3 för att ta bort nummer")
                print("Skriv 4 för söka genom kontakterna")
                print("Skriv 5 för ändra kontakt")
                print("Skriv q för avsluta")
                print()

                choice = input("Vilken väljer du? ")
                print()

                if choice == "1":
                    addPerson()
                    print("Personen la tills")
                    savePhonebook(Phonebook)
                    print()

                elif choice == "2":
                    if Phonebook:
                        print("Lista på allas nummer:")
                        for name, phonenumber in Phonebook.items():
                            print(name, phonenumber)
                        print()
                    else:
                        print("Listan är tom ")

                elif choice == "3":
                    if Phonebook:
                        for name, phonenumber in Phonebook.items():
                            print(name, phonenumber)
                        print()
                        print("skriv nameet på personen du vill ta bort i listan ovan")
                        removePerson()
                        savePhonebook(Phonebook)
                    else:
                        print("Listan är tom ")

                elif choice == "4":
                    searchName()
                    print()
                    
                elif choice == "5":
                    editContact()
                    print()

                elif choice.lower() == "q":
                    print("Stänger av...")
                    running = False

                else:
                    print("Välj något i menyn")

            except Exception:
                print("Något gick fel:")
                print("Testa igen.")
    meny()
    
telefon()
