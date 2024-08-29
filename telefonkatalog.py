import os
import time
import msvcrt
import sqlite3

# Initialize SQLite connection
conn = sqlite3.connect("telefonkatalog.db")
cursor = conn.cursor()

# Database initialization
def db_init():
    cursor.execute('''CREATE TABLE IF NOT EXISTS personer (
                fornavn TEXT,
                etternavn TEXT,
                telefonnummer TEXT
            )''')
    conn.commit()

db_init()

# Utility functions
def trykk_tast_for_meny():
    print("Trykk på en tast for å gå tilbake til menyen")
    get_keypress()
    printMeny()

def get_keypress():
    return msvcrt.getch().decode('utf-8')

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
            conn.close()
            exit()
        else:
            printMeny()
    else:
        print("Ugyldig valg. Velg et tall mellom 1-5: ")
        utfoerMenyvalg(input())

# Database interaction functions
def db_add(fornavn, etternavn, tlf):
    cursor.execute("INSERT INTO personer (fornavn, etternavn, telefonnummer) VALUES (?, ?, ?) ",
                   (fornavn, etternavn, tlf))
    conn.commit()

def db_delete(fornavn, etternavn, tlf):
    cursor.execute("DELETE FROM personer WHERE fornavn=? AND etternavn=? AND telefonnummer=?",
                   (fornavn, etternavn, tlf))
    conn.commit()

def oneResult_changeEntry(results, fornavn_endre, etternavn_endre):
    console_clear()
    print(f"Fant {results[0][0]} {results[0][1]} med telefonnummer {results[0][2]}. Hva ønsker du å endre?")
    print("(1: Navn, 2: Telefonnummer, 3: Begge, 4: Tilbake)")
    endring = get_keypress()

    if endring == "1":
        nytt_fornavn = input("Skriv nytt fornavn: ")
        nytt_etternavn = input("Skriv nytt etternavn: ")
        cursor.execute("UPDATE personer SET fornavn=?, etternavn=? WHERE fornavn=? AND etternavn=?",
                       (nytt_fornavn, nytt_etternavn, fornavn_endre, etternavn_endre))
        conn.commit()
        print(f"{fornavn_endre} {etternavn_endre} heter nå {nytt_fornavn} {nytt_etternavn}")
        trykk_tast_for_meny()

    elif endring == "2":
        nytt_tlf = input("Skriv nytt telefonnummer: ")
        cursor.execute("UPDATE personer SET telefonnummer=? WHERE fornavn=? AND etternavn=?",
                       (nytt_tlf, fornavn_endre, etternavn_endre))
        conn.commit()
        print(f"{fornavn_endre} {etternavn_endre} har nå telefonnummer {nytt_tlf}")
        trykk_tast_for_meny()

    elif endring == "3":
        nytt_fornavn = input("Skriv nytt fornavn: ")
        nytt_etternavn = input("Skriv nytt etternavn: ")
        nytt_tlf = input("Skriv nytt telefonnummer: ")
        cursor.execute("UPDATE personer SET fornavn=?, etternavn=?, telefonnummer=? WHERE fornavn=? AND etternavn=?",
                       (nytt_fornavn, nytt_etternavn, nytt_tlf, fornavn_endre, etternavn_endre))
        conn.commit()
        print(f"{fornavn_endre} {etternavn_endre} heter nå {nytt_fornavn} {nytt_etternavn}, og har telefonnummer {nytt_tlf}")
        trykk_tast_for_meny()

    elif endring == "4":
        endrePerson()

    else:
        print("Skriv 1, 2 eller 3")
        time.sleep(1)
        oneResult_changeEntry(results, fornavn_endre, etternavn_endre)

def multiResult_changeEntry(results):
    print("Flere personer funnet:")
    for index, person in enumerate(results, start=1):
        print(f"{index}. {person[0]} {person[1]} - Telefon: {person[2]}")

    selection = int(input("Skriv nummeret til personen du ønsker å endre (skriv 0 for å gå tilbake): "))

    if selection == 0:
        endrePerson()

    if 1 <= selection <= len(results):
        selected_entry = results[selection - 1]
        nytt_fornavn = input("Skriv inn det nye fornavnet: ")
        nytt_etternavn = input("Skriv inn det nye etternavnet: ")
        nytt_tlf = input("Skriv inn det nye telefonnummeret: ")

        cursor.execute(
            "UPDATE personer SET fornavn=?, etternavn=?, telefonnummer=? WHERE fornavn=? AND etternavn=? AND telefonnummer=?",
            (nytt_fornavn, nytt_etternavn, nytt_tlf, selected_entry[0], selected_entry[1], selected_entry[2])
        )
        conn.commit()
        print(" ")
        print(f"{selected_entry[0]} {selected_entry[1]} heter nå {nytt_fornavn} {nytt_etternavn}")
        trykk_tast_for_meny()
    else:
        print("Nummeret du skrev er ugyldig. Prøv igjen.")
        time.sleep(1)
        multiResult_changeEntry(results)

def oneResult_deleteEntry(results, fornavn_slett, etternavn_slett):
    console_clear()
    print(f"Fant {results[0][0]} {results[0][1]} med telefonnummer {results[0][2]}. Ønsker du å slette {results[0][0]}? (J/N)")
    endring = input()

    if endring.lower() == "j":
        cursor.execute("DELETE FROM personer WHERE fornavn=? AND etternavn=? AND telefonnummer=?",
                       (fornavn_slett, etternavn_slett, results[0][2]))
        conn.commit()
        print(f"{fornavn_slett} {etternavn_slett} er slettet.")
        trykk_tast_for_meny()

    elif endring.lower() == "n":
        slettPerson()

    else:
        print("Skriv J/N")
        time.sleep(1)
        oneResult_deleteEntry(results, fornavn_slett, etternavn_slett)

def multiResult_deleteEntry(results):
    print("Flere personer funnet:")
    for index, person in enumerate(results, start=1):
        print(f"{index}. {person[0]} {person[1]} - Telefon: {person[2]}")

    selection = int(input("Skriv nummeret til personen du ønsker å slette: (skriv '0' for å gå tilbake) "))

    if selection == 0:
        slettPerson()

    elif 1 <= selection <= len(results):
        selected_entry = results[selection - 1]
        print(f"Er du sikker du ønsker å slette {selected_entry[0]} {selected_entry[1]} med telefonnummer {selected_entry[2]}? (J/N)")
        endring = get_keypress()

        if endring.lower() == "j":
            cursor.execute(
                "DELETE FROM personer WHERE fornavn=? AND etternavn=? AND telefonnummer=?",
                (selected_entry[0], selected_entry[1], selected_entry[2])
            )    
            conn.commit()
            print("Personopplysningene har blitt oppdatert.")
            trykk_tast_for_meny()
        else:
            print("Nummeret du skrev er ugyldig. Prøv igjen.")
            time.sleep(1)
            multiResult_deleteEntry(results)

def registrerPerson():
    console_clear()
    fornavn = input("Skriv inn fornavn: ").strip()
    etternavn = input("Skriv inn etternavn: ").strip()
    telefonnummer = input("Skriv inn telefonnummer: ").strip()
    db_add(fornavn, etternavn, telefonnummer)

    console_clear()
    print(f"{fornavn} {etternavn} er registrert med telefonnummer {telefonnummer}")
    time.sleep(2)
    printMeny()

def sokPerson():
    console_clear()
    print("Søk i telefonkatalogen")

    search_type = input("Ønsker du å søke etter navn (N) eller telefonnummer (T)? ").strip().lower()

    if search_type == "n":
        fornavn_sok = input("Skriv inn fornavn: ").strip()
        etternavn_sok = input("Skriv inn etternavn: ").strip()

        # Use SQL parameters to avoid SQL injection
        cursor.execute("SELECT * FROM personer WHERE fornavn=? AND etternavn=?", (fornavn_sok, etternavn_sok))
        results = cursor.fetchall()

    elif search_type == "t":
        tlf_sok = input("Skriv inn telefonnummer: ").strip()
        cursor.execute("SELECT * FROM personer WHERE telefonnummer=?", (tlf_sok,))
        results = cursor.fetchall()

    else:
        print("Ugyldig valg. Velg 'N' eller 'T'.")
        time.sleep(1)
        sokPerson()

    if len(results) == 1:
        print(f"Fant en person: {results[0][0]} {results[0][1]} - Telefon: {results[0][2]}")
        time.sleep(2)
    elif len(results) > 1:
        print(f"Fant {len(results)} personer:")
        for result in results:
            print(f"{result[0]} {result[1]} - Telefon: {result[2]}")
        time.sleep(2)
    else:
        print("Ingen resultater funnet.")
        time.sleep(2)

def visAllePersoner():
    console_clear()
    print("Alle registrerte personer:")
    cursor.execute("SELECT fornavn, etternavn, telefonnummer FROM personer")
    personer = cursor.fetchall()

    if personer:
        for person in personer:
            print(f"{person[0]} {person[1]} - Telefon: {person[2]}")
    else:
        print("Ingen personer registrert i katalogen.")

    print("")
    trykk_tast_for_meny()

def slettPerson():
    console_clear()
    print("Slett en person fra telefonkatalogen")
    fornavn_slett = input("Skriv inn fornavn: ").strip()
    etternavn_slett = input("Skriv inn etternavn: ").strip()

    cursor.execute("SELECT * FROM personer WHERE fornavn=? AND etternavn=?", (fornavn_slett, etternavn_slett))
    results = cursor.fetchall()

    if len(results) == 1:
        oneResult_deleteEntry(results, fornavn_slett, etternavn_slett)
    elif len(results) > 1:
        multiResult_deleteEntry(results)
    else:
        print("Ingen personer funnet med dette navnet.")
        trykk_tast_for_meny()

def endrePerson():
    console_clear()
    print("Endre en person i telefonkatalogen")
    fornavn_endre = input("Skriv inn fornavn (skriv 'meny' for å gå tilbake): ").strip()
    if fornavn_endre == "meny" or fornavn_endre == "MENY":
        printMeny()
    etternavn_endre = input("Skriv inn etternavn: ").strip()

    cursor.execute("SELECT * FROM personer WHERE fornavn=? AND etternavn=?", (fornavn_endre, etternavn_endre))
    results = cursor.fetchall()

    if len(results) == 1:
        oneResult_changeEntry(results, fornavn_endre, etternavn_endre)
    elif len(results) > 1:
        multiResult_changeEntry(results)
    else:
        print("Ingen personer funnet med dette navnet.")
        trykk_tast_for_meny()

# Start the program
printMeny()