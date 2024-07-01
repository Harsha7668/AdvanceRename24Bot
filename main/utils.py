import math, time
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import heroku3
import os

# Progress bar template
PROGRESS_BAR_TEMPLATE = """<b>\n
╭━━━━❰ᴘʀᴏɢʀᴇss ʙᴀʀ❱━➣
┣⪼ 🗃️ Sɪᴢᴇ: {1} | {2}
┣⪼ ⏳️ Dᴏɴᴇ : {0}%
┣⪼ 🚀 Sᴩᴇᴇᴅ: {3}/s
┣⪼ ⏰️ Eᴛᴀ: {4}
╰━❰@ABOUTSUNRISES24❱━➣ </b>"""

def TimeFormatter(milliseconds: int) -> str:
    seconds, milliseconds = divmod(milliseconds, 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = ((str(days) + "d, ") if days else "") + \
          ((str(hours) + "h, ") if hours else "") + \
          ((str(minutes) + "m, ") if minutes else "") + \
          ((str(seconds) + "s, ") if seconds else "") + \
          ((str(milliseconds) + "ms, ") if milliseconds else "")
    return tmp[:-2]

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

async def progress_message(current, total, ud_type, message, start, user_id, action="#m"):
    now = time.time()
    diff = now - start
    if round(diff % 5.00) == 0 or current == total:
        # Debug statements to check values
        print(f"Current: {current}, Total: {total}, Type: {ud_type}, Start: {start}, User ID: {user_id}, Action: {action}")
        
        if message is None:
            print("Error: message object is None")
            return

        percentage = current * 100 / total
        speed = current / diff
        elapsed_time = round(diff) * 1000
        time_to_completion = round((total - current) / speed) * 1000
        estimated_total_time = elapsed_time + time_to_completion

        elapsed_time = TimeFormatter(milliseconds=elapsed_time)
        estimated_total_time = TimeFormatter(milliseconds=estimated_total_time)

        progress = "{0}{1}".format(
            ''.join(["⬢" for i in range(math.floor(percentage / 8.33))]),
            ''.join(["⬡" for i in range(12 - math.floor(percentage / 8.33))])
        )

        if "Download" in ud_type:
            status = "Downloading"
        else:
            status = "Uploading"
        
        progress_text = (
            f"{ud_type}\n"
            f"┌ {status}...\n"
            f"├ {progress}\n"
            f"├ Progress: {round(percentage, 2)}%\n"
            f"├ Processed: {humanbytes(current)}\n"
            f"├ Total Size: {humanbytes(total)}\n"
            f"├ Speed: {humanbytes(speed)}/s\n"
            f"├ ETA: {estimated_total_time if estimated_total_time != '' else '0 s'}\n"
            f"├ Elapsed: {elapsed_time}\n"
            f"├ By: {user_id}\n"
            f"├ Action: {action}\n"
            f"└ /cancel1 EDEZ4fa6"
        )

        if len(progress_text) > 1024:  # Split message if it exceeds Telegram limit
            progress_text = progress_text[:1020] + "..."

        try:
            await message.edit(
                text=progress_text,
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("✖️ CANCEL ✖️", callback_data="close")]])
            )
        except Exception as e:
            print(f"Error: {e}")

def convert(seconds):
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60      
    return "%d:%02d:%02d" % (hour, minutes, seconds)

# Example usage
async def example_usage():
    current = 500000000  # Current bytes processed
    total = 1000000000  # Total bytes to process
    message = None  # Replace with actual message object
    start = time.time()
    user_id = 12345

    await progress_message(current, total, "Renaming...", message, start, user_id, action="#rename")
    await progress_message(current, total, "Changing Metadata...", message, start, user_id, action="#changemetadata")
    await progress_message(current, total, "Changing Index Audio...", message, start, user_id, action="#changeindexaudio")
    await progress_message(current, total, "Changing Index Sub...", message, start, user_id, action="#changeindexsub")
    await progress_message(current, total, "Attaching Photo...", message, start, user_id, action="#attachphoto")
    await progress_message(current, total, "Leeching...", message, start, user_id, action="#leech")
    await progress_message(current, total, "Multi Task...", message, start, user_id, action="#multitask")
    await progress_message(current, total, "Taking Screenshot...", message, start, user_id, action="#screenshots")
    await progress_message(current, total, "Creating Sample Video...", message, start, user_id, action="#samplevideo")

# To run the example usage, use asyncio.run(example_usage()) if running in a standalone script.

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
            
