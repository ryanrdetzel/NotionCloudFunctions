import base64
import os
import json

from notion.client import NotionClient
from notion.block import PageBlock, TextBlock

token = 'a9bd0ca17acd386b4f41c7dcb6c04615099b743d064b18efa29d6bd3640e9d68ecede9f19b3b723bbae6416eb1d8f030fc1203293f68884c86bbbbd63b8e472f8b735d1ab5a0099cd2b7362bb1f8'
#page_url = 'https://www.notion.so/ryandetzel/Quick-Add-7a8658ff0a25492dbdc69d09b0c23b67'
page_url = 'https://www.notion.so/ryandetzel/Emails-da4b60ac354343839213ece3f0d00a33'

client = NotionClient(token_v2=token)

def processInbox(event, context):
  #message_raw = base64.b64decode(event['data']).decode('utf-8')
  message_obj = {
    'subject': "This is my subbject",
    'text': 'this is the contents of the email'
  }
  message_raw = json.dumps(message_obj)
  message = json.loads(message_raw)

  title = message.get('subject', 'Untitled Subject')

  parent_page = client.get_block(page_url)
  page = parent_page.children.add_new(
    PageBlock,
    title=title,
  )

  newchild = page.children.add_new(TextBlock, title=message.get('text'))

  print("Added page: " + page.id)

print("here")
processInbox(None, None)

