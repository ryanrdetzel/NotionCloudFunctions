import os

from datetime import datetime

from notion.client import NotionClient
from notion.block import TextBlock

token = os.environ.get('token', 'Missing notion login token')
page_url = os.environ.get('page', 'Missing notion page url')
api_key = os.environ.get('api_key', 'Missing api key')

client = NotionClient(token_v2=token)

def quickadd(request):
  args = request.args.to_dict(flat=True)
  if not args:
    return 'missing args', 500
  if 'api' not in args:
    return 'missing api key', 500
  if args.get('api') != api_key:
    return 'api key is incorrect'

  title = args.get('title', 'Untitled')

  parent_page = client.get_block(page_url)
  page = parent_page.children.add_new(
    TextBlock,
    title=title,
  )
  return page.id
