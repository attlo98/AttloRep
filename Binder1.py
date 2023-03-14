import telegram
import random
from telegram.ext import Updater, CommandHandler
from datetime import datetime
import csv
import requests
from bs4 import BeautifulSoup
import tabulate

# Token del bot ottenuto dal BotFather di Telegram
TOKEN = "6245665853:AAHqRqtsuE-lc1xytYkz6hvxJWQEjjZVrj8"

# Funzione che gestisce il comando /bora
def bora(update, context):
    # URL dell'immagine da inviare con un parametro di query casuale
    image_url = f"https://profiwetter.ch/wind_bora_it.png?{random.randint(1, 100000)}"
    # Testo del messaggio da inviare
    caption = "Ecco il *Diagramma della Bora!* \nIl grafico mostra la differenza di pressione fra Trieste e Marburgo: \n- Se la curva scende al di sotto della linea tratteggiata (-4hPa), *si attiva la Bora* \n- Se la curva scende al di sotto della linea indicata dalla freccia (-8hPa), *la Bora può risultare particolarmente violenta*"
    # Invia il messaggio con l'immagine e la didascalia
    context.bot.send_photo(chat_id=update.effective_chat.id, photo=image_url, caption=caption, parse_mode="Markdown")

def compleanno(update, context):
    today = datetime.now().strftime('%d-%m')
    print(f"Data corrente: {today}")  # stampa di debug
    with open('/Users/attiliosica/Desktop/tabella.csv') as file:
        reader = csv.reader(file, delimiter=',')
        compleanni = []
        for row in reader:
            if row[1] == today:
                compleanni.append(row[0] + " " + row[2])
        if compleanni:
            message = f"Buon Compleanno a {' e a '.join(compleanni)}!"
        else:
            message = "Oggi nessuno Spec invecchia!"
        context.bot.send_message(chat_id=update.effective_chat.id, text=message)

bot = telegram.Bot(TOKEN)

def lezioni(update, context):
    # Lettura del file CSV
    with open('/Users/attiliosica/Desktop/Bot/Lezioni.csv', 'r') as file:
        reader = csv.DictReader(file, delimiter=';')
        lezioni = [row for row in reader]
        
    # Creazione del messaggio
    message = 'Ciao! Ecco le prossime lezioni:\n\n'
    for i, lezione in enumerate(lezioni):
        print(lezione)
        message += f'*{i+1}) {lezione["Lezione"]} - {lezione["Relatore"]}* \n- {lezione["Data"]}\n- {lezione["Ora inizio"]} - {lezione["Ora fine"]}\n- {lezione["Sede"]}\n\n'

    # Invio del messaggio
    chat_id = update.effective_chat.id
    bot.send_message(chat_id=chat_id, text=message, parse_mode=telegram.ParseMode.MARKDOWN)

# Definiamo la funzione per il comando /Osmize
def osmize(update, context):
    # Estraiamo la prima tabella dalla pagina web
    url = 'https://www.osmize.com/'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    tables = soup.find_all('table')
    table = tables[0]

    # Estraiamo i dati dalla tabella
    rows = [[td.get_text().strip() for td in tr.find_all('td')] for tr in table.find_all('tr')[1:]]
    data = []
    for row in rows:
        if len(row) >= 4:
            item = {'nome': row[0], 'localita': row[1], 'telefono': row[2], 'data': row[3]}
            data.append(item)

    # Convertiamo i dati in formato Markdown
    text = 'Ecco le *Osmize* aperte oggi!\n\n'
    for i, item in enumerate(data):
        text += f"*{i+1}) {item['nome']}* \n"
        text += f"- Località: {item['localita']}\n"
        text += f"- Telefono: {item['telefono']}\n"
        text += f"- Aperta fino al: {item['data']}\n\n"

    text += "Mappa delle Osmize aperte: https://www.osmize.com/mappa"
    # Inviamo il messaggio di testo
    context.bot.send_message(chat_id=update.effective_chat.id, text=text, parse_mode=telegram.ParseMode.MARKDOWN)

# Crea l'oggetto Updater e passa il token del bot
updater = Updater(TOKEN, use_context=True)

# Ottieni il dispatcher per registrare i gestori di comandi
dp = updater.dispatcher

# Aggiungi un gestore per il comando /bora
dp.add_handler(CommandHandler("bora", bora))
dp.add_handler(CommandHandler("compleanno", compleanno))
dp.add_handler(CommandHandler("lezioni", lezioni))
dp.add_handler(CommandHandler("Osmize", osmize))

# Avvia il bot
updater.start_polling()

# Fai eseguire il bot finché non viene interrotto
updater.idle()





