from os import environ
import aiohttp
import re
import requests
from pyrogram import Client, filters
from pyrogram.handlers import MessageHandler

API_ID = environ.get('API_ID')
API_HASH = environ.get('API_HASH')
BOT_TOKEN = environ.get('BOT_TOKEN')
API_KEY = environ.get('API_KEY', '3494ad69b7c32aa52e71adf0da498357')

bot = Client('pdiskshortner bot',
             api_id=API_ID,
             api_hash=API_HASH,
             bot_token=BOT_TOKEN,
             workers=50,
             sleep_threshold=10)


@bot.on_message(filters.command('start') & filters.private)
async def start(bot, message):
    await message.reply(
        f"**Hi {message.chat.first_name}!**\n\n"
        "I'm Pdisk link converter bot. Just send me link and get converted link of pdisk.\n\n Created By @Tamil_Rulzz")

@bot.on_message(filters.command('help') & filters.private)
async def help(bot, message):
    await message.reply(
        f"**This is our Help Page {message.chat.first_name}!**\n\n"
        "**Just Simply send Any Lisk**\n\n"
        "if PDISK Site Says **The File is not Available Now** Click The Link again in few minutes\n"
        "[Because PDISK Takes few Minute to Upload your video]")

@bot.on_message(filters.private)
async def link_handler(bot, message):
    stringliteral = message.text
    Link = (re.search("(?P<url>https?://[^\s]+)", stringliteral).group("url"))
    session = requests.Session()
    resp = session.head(Link, allow_redirects=True)
    short_link = await post_shortlink(resp.url)
    shortlink = ('https://www.cofilink.com/share-video?videoid='+short_link)
    txt = stringliteral.replace(Link, shortlink)
    try:
        await message.reply(f'{txt}', quote=True)
    except Exception as e:
        await message.reply(f'Error: {e}', quote=True)


async def post_shortlink(Link):
    url = 'http://linkapi.net/open/create_item'
    params = {'api_key': API_KEY, 'content_src': Link, 'link_type': 'link', 'cover_url' : '/steallootdeal.jpeg'}
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params, raise_for_status=True) as response:
            data = await response.json()
            print(data["data"].get("item_id"))
            return data["data"].get("item_id")
 

bot.run()
