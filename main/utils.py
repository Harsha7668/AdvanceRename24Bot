import math, time
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import heroku3
import os

PROGRESS_BAR = """
┏🏷️ 
┠[■■■■■■■■▤□□□□] {0:.2f}%
┠🔄 Process: {1} of {2} | ETA: {3}
┠📶 Speed: {4}/s | Elapsed: {5}
"""

import time
import math
from pyrogram import Client
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def TimeFormatter(milliseconds: int) -> str:
    seconds, milliseconds = divmod(milliseconds, 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return f"{hours}:{minutes}:{seconds}"

def humanbytes(size):    
    if not size:
        return ""
    power = 2**10
    n = 0
    Dic_powerN = {0: ' ', 1: 'K', 2: 'M', 3: 'G', 4: 'T'}
    while size > power:
        size /= power
        n += 1
    return str(round(size, 2)) + " " + Dic_powerN[n] + 'B'

async def progress_message(current, total, ud_type, message, start):
    now = time.time()
    diff = now - start
    if round(diff % 5.00) == 0 or current == total:        
        percentage = current * 100 / total
        speed = current / diff
        elapsed_time = round(diff) * 1000
        time_to_completion = round((total - current) / speed) * 1000
        estimated_total_time = elapsed_time + time_to_completion

        elapsed_time = TimeFormatter(milliseconds=elapsed_time)
        estimated_total_time = TimeFormatter(milliseconds=estimated_total_time)

        progress = "[{0}{1}] {2:.2f}%".format(
            ''.join(["■" for _ in range(math.floor(percentage / 10))]),
            ''.join(["□" for _ in range(10 - math.floor(percentage / 10))]),
            percentage
        )

        try:
            await message.edit(
                text=PROGRESS_BAR.format(
                    percentage,
                    humanbytes(current), 
                    humanbytes(total), 
                    estimated_total_time if estimated_total_time != '' else '0 s',
                    humanbytes(speed),
                    elapsed_time
                ),               
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("✖️ CANCEL ✖️", callback_data="close")]])                                               
            )
        except Exception as e:
            print(f"Error editing message: {e}")



# Define heroku_restart function
async def heroku_restart():
    HEROKU_API = "HRKU-987b360b-e27e-43bf-b4e8-026e4c07521e"
    HEROKU_APP_NAME = "infinitystartrename24bot"
    x = None
    if not HEROKU_API or not HEROKU_APP_NAME:
        x = None
    else:
        try:
            acc = heroku3.from_key(HEROKU_API)
            bot = acc.apps()[HEROKU_APP_NAME]
            bot.restart()
            x = True
        except Exception as e:
            print(e)
            x = False
    return x

#for merging downloading media
async def download_media(msg, sts):
    c_time = time.time()
    try:
        file_path = await msg.download(progress=progress_message, progress_args=("🚀 Downloading media... ⚡", sts, c_time))
        await msg.reply_text(f"✅ Media downloaded successfully: {os.path.basename(file_path)}")
        return file_path
    except Exception as e:
        await sts.edit(f"❌ Error downloading media: {e}")
        raise

        
# Recursive function to upload files
async def upload_files(bot, chat_id, directory, base_path=""):
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        if os.path.isfile(item_path):
            try:
                await bot.send_document(chat_id, document=item_path, caption=item)
            except Exception as e:
                print(f"Error uploading {item}: {e}")
        elif os.path.isdir(item_path):
            await upload_files(bot, chat_id, item_path, base_path=os.path.join(base_path, item))
            
