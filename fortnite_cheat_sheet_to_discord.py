import requests
from bs4 import BeautifulSoup
import os.path

discordWebhook = ''  # Enter your discord webhook.
filename = 'links_posted.txt'

# Check and see if file has been created. If not, create it.
if os.path.isfile(filename):
    # Read the lines.
    f = open(filename, 'r')
    lines = f.read()
else:
    f = open(filename, 'x')
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
            if link not in lines:
                # Post to discord.
                data = {
                    "username": "Webhook",
                    "avatar_url": "https://i.imgur.com/4M34hi2.png",
                    "content": link
                }
                discord = requests.post(discordWebhook, data=data)

                # Write the link to the file to not post again.
                f = open(filename, 'a')
                f.write(link + '\n')
