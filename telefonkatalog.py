import os
import time
import msvcrt

telefonkatalog = []  # listeformat ["fornavn", "etternavn", "telefonnummer"]
fil = "telefondat.txt"

def get_keypress():
    return msvcrt.getch().decode('utf-8')

def hent_personer_fra_fil(filnavn):
    if not os.path.exists(filnavn):
        return
    with open(filnavn, 'r') as fil:
        for linje in fil:
            person = linje.strip().split("-")
            if len(person) == 3:  # Ensure the format is correct
                telefonkatalog.append(person)

hent_personer_fra_fil(fil)

def skriv_til_fil(filnavn):
    with open(filnavn, "w") as txt_file:
        for line in telefonkatalog:
            txt_file.write("-".join(line) + "\n")

def console_clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def printMeny():
    console_clear()
    print("-------------------- Telefonkatalog --------------------")
    print("| 1. Legg til ny person                                 |")
    print("| 2. Søk opp person eller telefonnummer                 |")
    print("| 3. Vis alle personer                                  |")
    print("| 4. Slett person                                       |")
    print("| 5. Endre person                                       |")
    print("| 6. Avslutt                                            |")
    print("--------------------------------------------------------")
    menyvalg = input("Skriv inn tall for å velge fra menyen: ")
    utfoerMenyvalg(menyvalg)

def utfoerMenyvalg(valgtTall):
    if valgtTall == "1":
        registrerPerson()
    elif valgtTall == "2":
        sokPerson()
        printMeny()
    elif valgtTall == "3":
        visAllePersoner()
    elif valgtTall == "4":
        slettPerson()
    elif valgtTall == "5":
        endrePerson()
    elif valgtTall == "6":
        bekreftelse = input("Er du sikker på at du vil avslutte? J/N ")
        if bekreftelse.lower() == "j":
            skriv_til_fil(fil)
            exit()
        else:
            printMeny()
    else:
        print("Ugyldig valg. Velg et tall mellom 1-5: ")
        utfoerMenyvalg(input())

def endrePerson():
    console_clear()
    fornavn_endre = input("Skriv fornavnet til personen du ønsker å endre (eller skriv 'meny' for å gå tilbake): ")
    if fornavn_endre == "meny" or fornavn_endre == "MENY" or fornavn_endre == "Meny":
        printMeny()
    etternavn_endre = input("Skriv etternavnet til personen du ønsker å endre: ")
    for person in telefonkatalog:
        if person[0] == fornavn_endre:
            if person[1] == etternavn_endre:
                console_clear()
                print("Fant", person[0], person[1], "med telefonnummer", person[2])
                nytt_fornavn = input("Skriv nytt fornavn: ").strip()
                nytt_etternavn = input("Skriv nytt etternavn: ").strip()
                nytt_tlf = input("skriv nytt telefonnummer: ").strip()
                telefonkatalog.remove(person)
                ny_registrering = [nytt_fornavn, nytt_etternavn, nytt_tlf]
                telefonkatalog.append(ny_registrering)
                print(fornavn_endre, etternavn_endre, "er nå registrert som", nytt_fornavn, nytt_etternavn, "med telefonnummer", nytt_tlf)
                print("Trykk på en tast for å gå tilbake")
                get_keypress()
                printMeny()
            else:
                break
        else:
            continue
    print("Fant ikke", fornavn_endre, etternavn_endre)
    time.sleep(1)
    endrePerson()
    

def registrerPerson():
    console_clear()
    fornavn = input("Skriv inn fornavn: ").strip()
    etternavn = input("Skriv inn etternavn: ").strip()
    telefonnummer = input("Skriv inn telefonnummer: ").strip()

    nyRegistrering = [fornavn, etternavn, telefonnummer]
    telefonkatalog.append(nyRegistrering)
    console_clear()
    print("{0} {1} er registrert med telefonnummer {2}"
          .format(fornavn, etternavn, telefonnummer))
    time.sleep(2)
    printMeny()

def visAllePersoner():
    console_clear()
    if not telefonkatalog:
        print("Det er ingen registrerte personer i katalogen")
    else:
        print("***************************************")
        for personer in telefonkatalog:
            print("* Fornavn: {:15s} Etternavn: {:15s} Telefonnummer: {:8s}"
                  .format(personer[0], personer[1], personer[2]))
        print("***************************************")
        print("Trykk på en tast for å gå tilbake")
        get_keypress()
        printMeny()

def sokPerson():
    console_clear()
    if not telefonkatalog:
        print("Det er ingen registrerte personer i katalogen")
    else:
        print("1. Søk på fornavn")
        print("2. Søk på etternavn")
        print("3. Søk på telefonnummer")
        print("4. Tilbake til hovedmeny")
        sokefelt = input("Velg ønsket søk 1-3, eller 4 for å gå tilbake: ").strip()
        if sokefelt == "1":
            navn = input("Fornavn: ").strip()
            finnPerson("fornavn", navn)
        elif sokefelt == "2":
            navn = input("Etternavn: ").strip()
            finnPerson("etternavn", navn)
        elif sokefelt == "3":
            tlfnummer = input("Telefonnummer: ").strip()
            finnPerson("telefonnummer", tlfnummer)
        elif sokefelt == "4":
            printMeny()
        else:
            console_clear()
            print("Ugyldig valg. Velg et tall mellom 1-4: ")
            sokPerson()

def finnPerson(typeSok, sokeTekst):
    found = False
    for personer in telefonkatalog:
        if (typeSok == "fornavn" and personer[0] == sokeTekst) or \
           (typeSok == "etternavn" and personer[1] == sokeTekst) or \
           (typeSok == "telefonnummer" and personer[2] == sokeTekst):
            print("{0} {1} har telefonnummer {2}"
                  .format(personer[0], personer[1], personer[2]))
            found = True
    if not found:
        print("Ingen personer funnet.")
    print("Trykk på en tast for å gå tilbake til søkemenyen")
    get_keypress()
    sokPerson()

def slettPerson():
    console_clear()
    fornavn_slett = input("Skriv fornavnet ti personen du ønsker å slette (eller skriv 'meny' for å gå tilbake): ")
    if fornavn_slett == "meny" or fornavn_slett == "MENY" or fornavn_slett == "Meny":
        printMeny()
    etternavn_slett = input("Skriv etternavnet til personen du ønsker å slette: ")
    for person in telefonkatalog:
        if person[0] == fornavn_slett:
            if person[1] == etternavn_slett:
                console_clear()
                confirmation = input("Vil du slette {0} {1} med telefonnummer {2} (J/N)?"
                                     .format(person[0], person[1], person[2]))
                if confirmation == "J" or confirmation == "j":
                    telefonkatalog.remove(person)
                    console_clear()
                    print(fornavn_slett, "er slettet")
                    time.sleep(1)
                    printMeny()
                else:
                    print("Operasjon avbrutt")
                    time.sleep(1.5)
                    printMeny()
            else:
                break
        else:
            continue
    print("Fant ikke", fornavn_slett, etternavn_slett)
    time.sleep(1)
    slettPerson()


    

printMeny()  # Starter programmet ved å skrive menyen første gang
