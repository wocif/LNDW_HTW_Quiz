import csv
import os
import time


quiz = [
    {
        "frage": "Wofür steht WWW?",
        "antworten": ["Willi wills wissen",
                      "World Wide Web",
                      "Wunder Wunder Wunder",
                      "Wireless Web Work"],
        "richtig": 1
    },
    {
        "frage": "Was ist der Unterschied zwischen einer IP-Adresse und einer MAC-Adresse?",
        "antworten": ["Die Mac-Adresse ist die IP-Adresse für Apple-Geräte",
                      "Es sind zwei unterschiedliche Begriffe für ein und das selbe.",
                      "Die MAC-Adresse wird nur in Europa verwendet, IP-Adresse in Amerika.",
                      "Die MAC-Adresse ist hardwarebasiert, Die IP-Adresse softwarebasiert."],
        "richtig": 3
    },
    {
        "frage": "Was ist Python?",
        "antworten": ["Ein abfälliger Begriff für die Arbeitsweise fauler Kolleg*innen in der IT",
                      "Ein Betriebssystem",
                      "Eine Programmiersprache",
                      "Ein Zauberspruch aus Harry Potter"],
        "richtig": 2
    },
    {
        "frage": "Was ist ein Byte",
        "antworten": ["eine Einheit zur Messung der Internetgeschwindigkeit.",
                      "ein persistenter Cookie",
                      "ein Hardware-Hersteller",
                      "eine Einheit für digitale Information und besteht aus 8 Bits"],
        "richtig": 3
    },
    {
        "frage": "Welches davon ist kein Betriebssystem",
        "antworten": ["Linux",
                      "Windows V",
                      "Mac OS X",
                      "Windows NT"],
        "richtig": 1
    },
    {
        "frage": "Was ist ein Cookie?",
        "antworten": ["eine Datei, die Passwörter für Webseiten speichert",
                      "ein Sicherheitsprotokoll für Internetverbindungen",
                      "eine kleine Datei, die von Webseiten auf deinem Computer gespeichert wird, um Informationen zu speichern und deine Nutzung der Webseite zu verfolgen",
                      "eine Art digitaler Keks, den man benutzen kann, um seinen Networktraffic kurz zu pausieren"],
        "richtig": 2
    },
    {
        "frage": "Was ist ein Byte",
        "antworten": ["eine Einheit zur Messung der Internetgeschwindigkeit.",
                      "ein persistenter Cookie",
                      "ein Hardware-Hersteller",
                      "eine Einheit für digitale Information und besteht aus 8 Bits"],
        "richtig": 3
    },
]

def frage_namen(scores):
    print("Zunächst möchten wir dich bitten, deinen Namen einzugeben. Du kannst auch ein Pseudonym verwenden.\n")
    time.sleep(2)
    print("Dein Name, sowie deine Statistik werden für eine Auswertung gespeichert und ggf. anderen Teilnehmenden gezeigt.")
    print("Solltest du damit nicht einverstanden sein, schreibe: 'ablehnen':\n")
    time.sleep(1)
    while True:
        name = input("Dein Name:")
        if len(name) > 20:
            print("Bitte maximal 20 Zeichen. Kürze ggf. ab oder nutze ein Pseudonym.")
        elif name_bereits_verwendet(name, scores):
            print("Dieser Name wurde bereits verwendet. Bitte wähle einen anderen Namen oder ein Pseudonym.")
        else:
            return name


def make_quiz(name):
    results, scores = load_results()
    richtige_antworten = 0

    for idx, frage_daten in enumerate(quiz):
        print("Frage: "+frage_daten["frage"])
        for i, antwort in enumerate(frage_daten["antworten"]):
            print(f"{i + 1}. {antwort}")

        while True:
            try:
                antwort = int(input("Antwort: ")) - 1
                if antwort not in range(len(frage_daten["antworten"])):
                    raise ValueError
                break
            except ValueError:
                print("Bitte gib die Nummer der entsprechenden Antwort ein.")

        if antwort in range(len(results[idx])):
            results[idx][antwort] += 1

        if antwort == frage_daten["richtig"]:
            print(f"Richtig!\n")
            time.sleep(1)
            richtige_antworten += 1
        else:
            print(f"Leider falsch :-(\n")
            time.sleep(1)

    anteil_richtiger_antworten = richtige_antworten / len(quiz)
    scores.append((name, anteil_richtiger_antworten))

    durchschnitt = sum(score for _, score in scores) / len(scores)
    anzahl_nutzer = len(scores)

    print("Quiz beendet. Deine Auswertung:\n")
    print(f"Richtig beantwortet: {anteil_richtiger_antworten*100:.2f}%")
    print(f"Durchschnitt aller Teilnehmenden: {durchschnitt*100:.2f}% ({anzahl_nutzer} Teilnehmende)")

    save_results(results, scores)
    return anteil_richtiger_antworten


def save_results(results, scores):
    with open("quiz_results.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        for i, row in enumerate(results):
            writer.writerow([i] + row)
        for name, score in scores:
            writer.writerow([name, score])


def load_results():
    results = [[0] * len(q["antworten"]) for q in quiz]
    scores = []
    if os.path.exists("quiz_results.csv"):
        with open("quiz_results.csv", newline="") as csvfile:
            reader = csv.reader(csvfile)
            rows = list(reader)
            for i, row in enumerate(rows[:len(quiz)]):
                try:
                    results[i] = list(map(int, row[1:]))
                except ValueError:
                    print(f"Ungültige Daten in Zeile {i + 1}, werden übersprungen: {row}")
            for row in rows[len(quiz):]:
                try:
                    scores.append((row[0], float(row[1])))
                except ValueError:
                    print(f"Ungültige Daten in Zeile {i + 1}, werden übersprungen: {row}")
    return results, scores




def print_bestenliste(scores, ergebnis, name):
    scores.sort(key=lambda x: x[1], reverse=True)
    top_scores = scores[:10]
    max_score = top_scores[-1][1]
    top_participants = {}

    for name, score in scores:
        if score >= max_score:
            if score not in top_participants:
                top_participants[score] = []
            top_participants[score].append(name)

    print("\nTop 10:")
    for score in sorted(top_participants.keys(), reverse=True)[:3]:
        names = ", ".join(top_participants[score])
        print(f"{score*100:.2f}%: {names}")


def name_bereits_verwendet(name, scores):
    return any(n == name for n, _ in scores)


def bestenlisteHtml(scores, filename="bestenliste.html"):
    # Sortiere die Scores nach dem Ergebnis
    scores.sort(key=lambda x: x[1], reverse=True)
    # Begrenze die Anzeige auf die besten 30 Scores
    top_scores = scores[:30]

    # Erstelle den HTML-Inhalt
    html_content = """
    <!DOCTYPE html>
    <html lang="de">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Bestenliste</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            table { width: 50%; border-collapse: collapse; margin: 0 auto; }
            th, td { padding: 10px; border: 1px solid #ddd; text-align: center; }
            th { background-color: #f4f4f4; }
            h1 { text-align: center; }
        </style>
        <script>
            function reloadPage() {
                setTimeout(function() {
                    window.location.reload();
                }, 10000); // 10000 Millisekunden = 10 Sekunden
            }
        </script>
    </head>
    <body onload="reloadPage()">
        <h1>Bestenliste (Top 30)</h1>
        <table>
            <thead>
                <tr>
                    <th>Platz</th>
                    <th>Name</th>
                    <th>Prozent</th>
                </tr>
            </thead>
            <tbody>
    """

    # Füge die Scores zur Tabelle hinzu
    for i, (name, score) in enumerate(top_scores, start=1):
        html_content += f"""
        <tr>
            <td>{i}</td>
            <td>{name}</td>
            <td>{score * 100:.2f}%</td>
        </tr>
        """

    # Schließe den HTML-Inhalt
    html_content += """
            </tbody>
        </table>
    </body>
    </html>
    """
    with open(filename, "w") as file:
        file.write(html_content)


def main():
    nochmal = ""
    while nochmal != "ende":
        nochmal = input("Drücke Enter, um ein neues Quiz zu starten. Sonst schreibe 'ende'.\n")
        print("Herzlich Willkommen beim Quiz des Stands für \033[32m"+"Informatik in Kultur und Gesundheit \033[0m"+"bei der Langen Nacht Der Wissenschaften 2024!\n")
        _, scores = load_results()
        time.sleep(2)
        name = frage_namen(scores)
        if name != 'ablehnen':
            print(f"\nViel Erfolg bei unserem kleinen Quiz, {name}!\nAnstrengen lohnt sich, es gibt eine Bestenliste!\n")
            ergebnis = make_quiz(name)
            _, scores = load_results()
            print_bestenliste(scores, ergebnis, name)
            bestenlisteHtml(scores)
            print("\n")
        else:
            print("Du hast dich entschieden, das Quiz nicht zu machen.\n")


if __name__ == "__main__":
    main()




















