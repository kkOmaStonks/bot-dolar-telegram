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
    url = 'https://api.dolarito.ar/api/frontend/quotations/dolar'
    try:

        headers = {
    'Auth-client':'eb72699e60745f9cd000e0af740092ee'
        } # validador

        r = requests.get(url, timeout=10,headers=headers)
        data = r.json()
    except:
        return None  # fallas

    mensaje = "💵 *Cotización actual:*\n\n"

    tipos = {
        "informal": ("💸", "BLUE"),
        "oficial": ("🏦", "OFICIAL"),
        "mep": ("📊", "MEP"),
        "ccl": ("🔌", "CCL")
    }

    alguno = False
    for key, (emoji, nombre) in tipos.items():
        if key in data:
            valores = data.get(key)
            compra_raw = valores.get("buy")
            venta_raw = valores.get("sell")

            if not venta_raw:  # si no hay precio de venta, no mostramos nada
                continue

            compra = format_precio(compra_raw) if compra_raw else None
            venta = format_precio(venta_raw)

            mensaje += f"{emoji} *{nombre}*\n"
            if compra:
                mensaje += f"Compra: ${compra} | "
            mensaje += f"Venta: ${venta}\n\n"
            alguno = True


    return mensaje.strip() if alguno else None

async def enviar():
    mensaje = obtener_dolares()
    if mensaje:
        await bot.send_message(chat_id=CHAT_ID, text=mensaje, parse_mode='Markdown')

def run_async():
    asyncio.run(enviar())

run_async()

# Horarios programados
schedule.every().day.at("12:00").do(run_async)
schedule.every().day.at("15:00").do(run_async)
schedule.every().day.at("17:00").do(run_async)

while True:
    schedule.run_pending()
    time.sleep(30)

