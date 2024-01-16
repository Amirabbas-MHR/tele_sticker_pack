import requests
import json
import os
import glob
from PIL import Image
from core import S_BOT

print("Welcome to telegram sticker pack generator.\n")

print("Your bot api key(If you don't have one, get it from @BotFather bot in telegram): ")
API_KEY = input("< ")

bot = S_BOT(API_KEY=API_KEY)

print("Your user_id to own the pack. should be the id of bot owner. (if you don't know it, get it from @userinfobot bot in telegram):")
USER_ID = input("< ")

print("Folder name containing you images: ")
path = input("< ")

print("Channel name to use as a container to upload files(Should be in this format @channel_name). if you don't have it, create one in the app!")
container = input("< ")

print("Emojies to use for pack, comma seperated. example: 🐸,🦀")
emojies = input("< ").split(',')

print("keywords to use for pack, comma seperated. example: bar,foo")
keywords = input("< ").split(',')

stickers = bot.load_stickers(path, container, emojies, keywords)

print("name to your sticker pack? in the future it will be available in t.me/addstickers/pack_name ")
name = input("< ")

print("title to your sticker pack? in the future it will be shown on top of sticker pack in telegram app ")
title = input("< ")

bot.createNewStickerSet(USER_ID, name, title, stickers)

print('\n Finished. terminating...')