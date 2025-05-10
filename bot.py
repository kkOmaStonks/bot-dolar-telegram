import requests
from telegram import Bot
import asyncio
import schedule
import time
import datetime

def run_async():
    hoy = datetime.datetime.today().weekday()
    if hoy < 5:  # 0 = lunes, 4 = viernes
        asyncio.run(enviar())


TOKEN = '1681401638:AAFubTtxjsAW1v3KBT8ECbOpCDrhFcZioG4'
CHAT_ID = '-1001536238091'
bot = Bot(token=TOKEN)

def format_precio(valor):
    return int(valor) if valor == int(valor) else round(valor, 2)

def obtener_dolares():
    url = 'https://api.bluelytics.com.ar/v2/latest'
    try:
        r = requests.get(url, timeout=10)
        data = r.json()
    except:
        return None  # si falla la conexión, no manda nada

    mensaje = "💵 *Cotización actual:*\n\n"

    tipos = {
        "blue": ("💸", "BLUE"),
        "oficial": ("🏦", "OFICIAL"),
        "mep": ("📊", "MEP"),
        "ccl": ("🔌", "CCL")
    }

    alguno = False
    for key, (emoji, nombre) in tipos.items():
        if key in data:
            valores = data.get(key)
            compra = format_precio(valores.get("value_buy", 0))
            venta = format_precio(valores.get("value_sell", 0))
            mensaje += f"{emoji} *{nombre}*\nCompra: ${compra} | Venta: ${venta}\n\n"
            alguno = True

    return mensaje.strip() if alguno else None

async def enviar():
    mensaje = obtener_dolares()
    if mensaje:
        await bot.send_message(chat_id=CHAT_ID, text=mensaje, parse_mode='Markdown')

def run_async():
    asyncio.run(enviar())

# 🕒 Horarios programados
schedule.every().day.at("12:00").do(run_async)
schedule.every().day.at("15:00").do(run_async)
schedule.every().day.at("17:00").do(run_async)

while True:
    schedule.run_pending()
    time.sleep(30)
