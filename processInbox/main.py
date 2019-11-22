import base64
import os
import json

from datetime import datetime

from notion.client import NotionClient
from notion.block import TextBlock

token = os.environ.get('token', 'Missing notion login token')
page_url = os.environ.get('page', 'Missing notion page url')

client = NotionClient(token_v2=token)

def process_inbox(event, context):
  message_raw = base64.b64decode(event['data']).decode('utf-8')
  print(message_raw)
  message = json.loads(message_raw)

  title = message.get('title', 'Untitled')

  parent_page = client.get_block(page_url)
  page = parent_page.children.add_new(
    TextBlock,
    title=title,
  )
  print("Added page: " + page.id)
