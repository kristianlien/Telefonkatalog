import os
import time
import msvcrt
import mysql.connector

# Initialize MySQL connection
conn = mysql.connector.connect(
    host="10.2.2.172",
    user="username",
    password="password",
    database="telefonkatalog"
)
cursor = conn.cursor()

# Database initialization
def db_init():
    cursor.execute('''CREATE TABLE IF NOT EXISTS personer (
                fornavn VARCHAR(255),
                etternavn VARCHAR(255),
                telefonnummer VARCHAR(20)
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
    cursor.execute("INSERT INTO personer (fornavn, etternavn, telefonnummer) VALUES (%s, %s, %s)",
                   (fornavn, etternavn, tlf))
    conn.commit()

def db_delete(fornavn, etternavn, tlf):
    cursor.execute("DELETE FROM personer WHERE fornavn=%s AND etternavn=%s AND telefonnummer=%s",
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
        cursor.execute("UPDATE personer SET fornavn=%s, etternavn=%s WHERE fornavn=%s AND etternavn=%s",
                       (nytt_fornavn, nytt_etternavn, fornavn_endre, etternavn_endre))
        conn.commit()
        print(f"{fornavn_endre} {etternavn_endre} heter nå {nytt_fornavn} {nytt_etternavn}")
        trykk_tast_for_meny()

    elif endring == "2":
        nytt_tlf = input("Skriv nytt telefonnummer: ")
        cursor.execute("UPDATE personer SET telefonnummer=%s WHERE fornavn=%s AND etternavn=%s",
                       (nytt_tlf, fornavn_endre, etternavn_endre))
        conn.commit()
        print(f"{fornavn_endre} {etternavn_endre} har nå telefonnummer {nytt_tlf}")
        trykk_tast_for_meny()

    elif endring == "3":
        nytt_fornavn = input("Skriv nytt fornavn: ")
        nytt_etternavn = input("Skriv nytt etternavn: ")
        nytt_tlf = input("Skriv nytt telefonnummer: ")
        cursor.execute("UPDATE personer SET fornavn=%s, etternavn=%s, telefonnummer=%s WHERE fornavn=%s AND etternavn=%s",
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
            "UPDATE personer SET fornavn=%s, etternavn=%s, telefonnummer=%s WHERE fornavn=%s AND etternavn=%s AND telefonnummer=%s",
            (nytt_fornavn, nytt_etternavn, nytt_tlf, selected_entry[0], selected_entry[1], selected_entry[2])
        )
        conn.commit()
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
        cursor.execute("DELETE FROM personer WHERE fornavn=%s AND etternavn=%s AND telefonnummer=%s",
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
                "DELETE FROM personer WHERE fornavn=%s AND etternavn=%s AND telefonnummer=%s",
                (selected_entry[0], selected_entry[1], selected_entry[2])
            )
            conn.commit()
            print("Personen har blitt slettet.")
            trykk_tast_for_meny()
        else:
            slettPerson()
    else:
        print("Nummeret du skrev er ugyldig. Prøv igjen.")
        time.sleep(1)
        multiResult_deleteEntry(results)

# Menu option functions
def registrerPerson():
    fornavn = input("Fornavn: ")
    etternavn = input("Etternavn: ")
    tlf = input("Telefonnummer: ")

    db_add(fornavn, etternavn, tlf)
    print(f"Ny person lagt til: {fornavn} {etternavn} med telefonnummer {tlf}")
    trykk_tast_for_meny()

def sokPerson():
    sok_fornavn = input("Skriv fornavn på personen du vil søke opp: ")
    sok_etternavn = input("Skriv etternavn på personen du vil søke opp: ")
    cursor.execute("SELECT * FROM personer WHERE fornavn=%s AND etternavn=%s", (sok_fornavn, sok_etternavn))
    result = cursor.fetchall()
    
    if result:
        print("Fant følgende personer:")
        for person in result:
            print(f"{person[0]} {person[1]} - Telefon: {person[2]}")
    else:
        print("Fant ingen personer med det navnet.")

    trykk_tast_for_meny()

def visAllePersoner():
    cursor.execute("SELECT * FROM personer")
    results = cursor.fetchall()

    if results:
        print("Alle personer i katalogen:")
        for person in results:
            print(f"{person[0]} {person[1]} - Telefon: {person[2]}")
    else:
        print("Ingen personer funnet i katalogen.")

    trykk_tast_for_meny()

def slettPerson():
    slett_fornavn = input("Skriv fornavn på personen du vil slette: ")
    slett_etternavn = input("Skriv etternavn på personen du vil slette: ")
    cursor.execute("SELECT * FROM personer WHERE fornavn=%s AND etternavn=%s", (slett_fornavn, slett_etternavn))
    results = cursor.fetchall()

    if len(results) == 0:
        print("Fant ingen personer med det navnet.")
        trykk_tast_for_meny()
    elif len(results) == 1:
        oneResult_deleteEntry(results, slett_fornavn, slett_etternavn)
    else:
        multiResult_deleteEntry(results)

def endrePerson():
    fornavn_endre = input("Skriv fornavn på personen du vil endre: ")
    etternavn_endre = input("Skriv etternavn på personen du vil endre: ")
    cursor.execute("SELECT * FROM personer WHERE fornavn=%s AND etternavn=%s", (fornavn_endre, etternavn_endre))
    results = cursor.fetchall()

    if len(results) == 0:
        print("Fant ingen personer med det navnet.")
        trykk_tast_for_meny()
    elif len(results) == 1:
        oneResult_changeEntry(results, fornavn_endre, etternavn_endre)
    else:
        multiResult_changeEntry(results)

# Start application
printMeny()
