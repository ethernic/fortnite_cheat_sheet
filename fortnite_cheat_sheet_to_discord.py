import requests
from bs4 import BeautifulSoup
import os.path
import json

discordWebhook = ''  # Enter your discord webhook.
filename = 'links_posted.txt'

# Check and see if file has been created. If not, create it.
if os.path.isfile(filename):
    # Read the lines.
    with open(filename, 'r') as f:
        lines = f.read()
else:
    with open(filename, 'x') as f:
        lines = []

# Get all stories from fortniteinsider.
r = requests.get(
    'https://fortniteinsider.com/?s=cheat')
parsed_html = BeautifulSoup(r.text, 'html.parser')

h3s = parsed_html.findAll('h3', {'class': 'entry-title'})

for h3 in h3s:
    if 'cheat' in h3.text.lower():
        for a in h3.contents:
            link = a.attrs['href']
            cheat_sheet = requests.get(link)
            parsed_cheat = BeautifulSoup(cheat_sheet.text, 'html.parser')
            imgs = parsed_cheat.findAll('img', {'class': 'entry-thumb'})
            for img in imgs:
                if "Fortnite-Cheat-Sheet-Map" in img['src']:
                    cheat_link = img['src']
            if cheat_link not in lines:
                data = {
                    "username": "Webhook",
                    "avatar_url": "https://i.imgur.com/4M34hi2.png",
                }
                # Get the image
                file = requests.get(cheat_link).content
                headers = {}
                payload = {'payload_json': json.dumps(data)}
                multipart = {'file': ('cheat_sheet.png', file)}

                # Post to discord.
                discord = requests.post(discordWebhook, data=payload, headers=headers, files=multipart)

                # Write the link to the file to not post again.
                with open(filename, 'a') as f:
                    f.write(link + '\n')
