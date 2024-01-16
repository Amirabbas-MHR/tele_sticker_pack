import requests
import json
import os
import glob
from PIL import Image
from time import sleep

class S_BOT:

    def __init__(self, API_KEY:str):
        '''
        Use this object to initialize the bot usage and start the sticker creation process

		before starting, consider doing theese 3 steps in telegram app:

		1. get a bot api key from @BotFather bot in telegram. we call this API_KEY
		2. create a channel to be used as a container for your images to upload, then using them to create stickers, we call this channel CONTAINER
		3. get your user id from @userinfobot. we call this USER_ID

		arguments:
			API_KEY (str) : Your bot api key. You should get it from @BotFather bot in telegram.

		returns:
			None

		params:
			S_BOT.API_KEY : the api key used to initialize object
			S_BOT.root : the root url for telegram requests. here, https://api.telegram.org/bot{API_KEY}/
			S_BOT.id: bot id
			S_BOT.name: bot name
			S_BOT.username: bot username
        '''

        self.API_KEY = API_KEY
        self.root = f'https://api.telegram.org/bot{API_KEY}/'

		# sending getMe request, to check the properties of bot and connection
        getMe_response = requests.get(self.root + 'getMe').json()

        if not getMe_response['ok']:
            print(f'Error code:{getMe_response["error_code"]}, Message: {getMe_response["description"]}.')
            raise Exception('Trouble calling the bot api... Check the internet connection and API_KEY.')
            quit()
        else:
            print('Bot api response: ok. initiating...\n')
            result = getMe_response['result']
            self.id = result['id']
            self.name = result['first_name']
            self.username = result['username']
        return

    def createNewStickerSet(self, user_id:int, name:str, title:str, stickers:json, sticker_format:str ='static'):
        
        '''
		Method to create a new sticker set

		arguments:
			user_id (int): Your user id to own the sticker pack(NECESSARILY owner of the bot). if you don't know your user id, send a message to @userinfobot
			name (str): sticker pack name. used in the add sticker link t.me/addsticker/name
			title (str): sticker pack title. shown on the top of pack in telegram app
			path (str): the path which contains the pictures you want to create stickers from them.
			sticker_format (str): only static format is supported in telegram api, so don't change it.

		returns:
			None
        '''

        method = 'createNewStickerSet'
        # sticker packs created by bots, must be named with the format: 'botname_by_bot-userneme'
        params = {"user_id": user_id, 
                    "name": f"{name}_by_{self.username}",
                    "title": title,
                    "stickers": stickers,
                    "sticker_format": sticker_format}
        link = self.root + method
        response = requests.get(link, data=params)

        if response.status_code == 200:
            print(f"Sticker pack {name} created successfully and is available in https://t.me/addstickers/{params['name']}")
        else:
            print("Sticker pack creaion failed:", response.text)

    
    def load_stickers(self, path:str, container:str, emojies:list, keywords:list):
        '''
        Use this method to load stickers of a path, to use in S_BOT.createNewStickerSet method.

		arguments:
			path (str) : folder which contains the pictures you want to turn thm into stickers.
                         if in the same folder as this file, only pass folder name. but you can pass absolute paths too.
            container (str): channel used to store the pictures which are going to be used to make stickers from them
            emojies (list): a single emoji list for all the pack. example: ['🦕', '🐸']
            keywords (list): a single keyword list for all the pack. example: ['foo', 'bar', 'boo']

		returns:
			json list of stickers.

        '''
        #TODO seperating emojies for each sticker
        #TODO seperating keywords for each sticker

        def find_images(path:str):
            image_extensions = ["*.jpg", "*.png"]  # Add more extensions if needed

            image_paths = []
            for extension in image_extensions:
                pattern = os.path.join(path, extension)
                image_paths.extend(glob.glob(pattern))

            return image_paths

        image_paths = find_images(path)

        if not os.path.exists(path):
            print("Folder does not exist. Please provide a valid path.")
            raise Exception('Folder does not exist')
            
        if not image_paths:
            print("No images found in the specified folder.")
            raise Exception('No images found')
        

        sticker_list = []
        t = 1
        for image_path in image_paths:
            img = Image.open(image_path)
            x, y = img.size
            if (x>512 or y>512) or (x!=512 and y!=512):
                raise Exception(ValueError, "Images should have size (512, x) or (x, 512) with x<512")
            else:
                if t%10 == 0:
                    print("Sleeping for 30s to prevent ip ban.")
                    sleep(32)
                image_id = self._photo_uploader(image_path, container)
                t+=1
                sticker_object = {"sticker": image_id, "emoji_list": emojies, "keywords": keywords}
                sticker_list.append(sticker_object)
            img.close()
        return json.dumps(sticker_list)


    def _photo_uploader(self, file_path:str, container:str):
        '''
		Method to upload sticker pictures to container channel

		arguments:
			file_path (str): file path to desired image to be uploaded
			container (str): channel username which is used as a container. MUST BE IN FORMAT @channel_user_name

		returns:
			file_id (str): id to that file in telegram servers for future uses

        '''
        with open(file_path, 'rb') as file:
            files = {'document': file}
            response = requests.post(f'{self.root}sendDocument', files=files, data={'chat_id': container})

            if response.status_code == 200:
                file_id = response.json()['result']['document']['file_id']
                print(f'Photo {file_path} uploaded successfully.')
                return file_id
            else:
                print(f'Failed to upload photo {file_path}:', response.text)