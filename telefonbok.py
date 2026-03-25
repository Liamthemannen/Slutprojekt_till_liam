def telefon():

    telefonbok = {
        "Liam": "0723215088",
        "Julle": "0760406815"
    }  
    
    def lägga_till():   
        namn = input("Vad är deras namn ")
        telefonnummer = input("Vad är deras telefonnummer ")
        telefonbok[namn] = telefonnummer

    def ta_bort():
        tabort_val = input("Vilken vill du ta bort ")
        telefonbok.pop(tabort_val)
    
    def söka_namn():
        söknamn = input("Vilket namn vill du söka på? ")
        if söknamn in telefonbok:
            print("Telefonnumret är: ")
            print(telefonbok[söknamn])
        else:
            print("Personen finns inte")

    def meny():
        kör = True
        while kör:
            print()
            print("Skriv 1 för lägga till nummer ")
            print("Skriv 2 för få upp lista på nummer ")
            print("Skriv 3 för att ta bort nummer ")
            print("Skriv 4 för söka genom namn ")
            print("Skriv q för avsluta ")
        
        
            val = input("Vilken väljer du? ")
            print()
        
            if val == "1":
                lägga_till()
                print("Personen la tills")
                print()
        
            elif val == "2":
                if telefonbok:
                    print("Lista på allas nummer:")
                    for namn, telefonnummer in telefonbok.items():
                        print(namn, telefonnummer)
                        print()
                else:
                    print("Listan är tom ")
                
            elif val == "3":
                if telefonbok:
                    for namn, telefonnummer in telefonbok.items():
                        print(namn, telefonnummer)
                        print()
                    print("skriv namnet på personen du vill ta bort i listan ovan")
                    ta_bort()
                else:
                    print("Listan är tom ")
                
            elif val == "4":
                söka_namn()
                print()
            
            elif val == "q" or val == "Q":
                print("Stänger av...")
                kör = False
                
            else:
                print("Välj något i menyn" )
    meny()
    
telefon()
