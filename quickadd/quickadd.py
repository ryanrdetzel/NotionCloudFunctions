import os

from datetime import datetime

from notion.client import NotionClient
from notion.block import TextBlock

token = os.environ.get('token', 'Missing notion login token')
page_url = os.environ.get('page', 'Missing notion page url')

client = NotionClient(token_v2=token)

def quickadd(request):
  title = 'Untitled'
  args = request.args.to_dict(flat=True)
  if args and 'title' in args:
    title = args.get('title')

  parent_page = client.get_block(page_url)
  page = parent_page.children.add_new(
    TextBlock,
    title=title,
  )
  return 'done'
