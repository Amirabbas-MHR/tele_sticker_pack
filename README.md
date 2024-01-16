# Telegram sticker pack creator

## Introduction
tele-sticker-pack is a Python library that allows you to easily create and upload sticker packs to Telegram using the Telegram Bot API. With just a few simple steps, you can transform a collection of images from your local machine into a personalized sticker pack.

## Getting Started
Before using tele-sticker-pack, make sure to perform the following steps in the Telegram app:
1. Obtain a bot API key from [@BotFather](https://t.me/BotFather).
2. Create a channel to be used as a container for your images. This channel will store the pictures used to create stickers.
3. Get your user ID from [@userinfobot](https://t.me/userinfobot).

## Installation
To use tele-sticker-pack, you need to have Python installed. Install the required packages by running:
```bash
pip install requests Pillow
```

## Example Usage

```python
from core import S_BOT

# Initialize the bot with your API key
bot = S_BOT(API_KEY='AAAAAAAAAAAAAA')

# Load stickers from a folder and create a sticker pack
sticker_data = bot.load_stickers(path='sticker_images', container='@mytestcontainer', emojies=['🦕', '🐸'], keywords=['foo', 'bar'])
bot.createNewStickerSet(user_id=1111111, name='mystickerpack', title='sticker pack title', stickers=sticker_data)

-> will create a sticker pack in link https://t.me/addstickers/mystickerpack_by_{bot.username}
```

## Contribution
Feel free to contribute to the project by opening issues or submitting pull requests.
