import urllib.request as request
from urllib.error import HTTPError
from http.client import HTTPResponse
from typing import Dict, Union
import json
from datetime import datetime
import signal
import os
from telegram import Update
from telegram.ext import Application,CommandHandler,MessageHandler,filters,ContextTypes
from typing import Final
import requests
import openpyxl

signal.signal(signal.SIGINT, signal.SIG_DFL)
workbook = openpyxl.load_workbook("C:/Users/HP/Desktop/FOREX/Copy of Customer Details.xlsx")
sheet = workbook["Sheet1"] 
chat_ids = []  

for row in sheet.iter_rows(min_row=2): 
    chat_id = row[7].value  
    if chat_id:
        chat_ids.append(chat_id)
TOKEN : Final='6599628479:AAEH5OFwkEmjuMopAAMuC8JeRiak5htjItE'
BOT_USERNAME="@Forex13_bot"
async def start_command(update:Update,context:ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("hello thanks for chatting i am a bot")
async def help_command(update:Update,context:ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("for help contact the administrator")
async def custom_command(update:Update,context:ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("As a tele bot i have limitations so i cant understand your message")
async def trigger_message(update:Update,context:ContextTypes.DEFAULT_TYPE):
    for i in chat_ids:
        base_url = f"https://api.telegram.org/bot6599628479:AAEH5OFwkEmjuMopAAMuC8JeRiak5htjItE/sendMessage?chat_id={i}&text=test from nidun"
        response = requests.get(base_url)
    
        if response.status_code == 200:
            print(f"Message sent to chat ID: {chat_id}")
        else:
            print(f"Failed to send message to chat ID: {chat_id}. Status code: {response.status_code}")
async def handle_response(text: str, context: ContextTypes.DEFAULT_TYPE) -> str:
    message_text = text.message.text
    processed: str = message_text.lower()
    if 'hello' in processed:
        return 'Hey there whatchu doin'
    if 'how are you' in processed:
        return 'I am fine, what about you?'
    if 'good' in processed:
        return 'Thanks for your feedback'
    else:
        return 'As a tele bot, I have limitations so I can\'t understand your message'
    
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text
    print(f'User({update.message.chat.id}) in {message_type}: "{text}"')

    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '').strip()
            response: str = handle_response(text)
        else:
            return
    else:
        response: str = handle_response(text)
        print('BOT', response)

        try:
            await update.message.reply_text(response)
        except Exception as e:
            print(f"Error sending message: {e}")
if __name__=='__main__':
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('custom', custom_command)) 
    app.add_handler(CommandHandler('trigger',trigger_message))
    app.add_handler(MessageHandler(filters.TEXT, handle_response))
    
    # app.add_error_handler(error)
    print("running....")
    app.run_polling(poll_interval=3)
