import base64
import os
import json

from datetime import datetime

from notion.client import NotionClient
from notion.block import TextBlock, PageBlock

token = os.environ.get('token', 'Missing notion login token')
page_url = os.environ.get('page', 'Missing notion page url')
page_email = os.environ.get('page_email', 'Missing notion email inbox url')

client = NotionClient(token_v2=token)

def processInbox(event, context):
  message_raw = base64.b64decode(event['data']).decode('utf-8')
  message = json.loads(message_raw)

  if 'subject' in message:
    # email
    subject = message.get('subject')
    text = message.get('text')

    parent_page = client.get_block(page_email)
    page = parent_page.children.add_new(
      PageBlock,
      title=subject,
    )

    page.children.add_new(TextBlock, title=text)
  else:
    # Quick add
    title = message.get('title', 'Untitled')

    parent_page = client.get_block(page_url)
    page = parent_page.children.add_new(
      TextBlock,
      title=title,
    )