import os
import pytz

from datetime import datetime
from pytz import timezone

from notion.collection import NotionDate
from notion.client import NotionClient
from notion.block import TextBlock

token = os.environ.get('token', 'Missing notion login token')
page_url = os.environ.get('page', 'Missing notion page url')
api_key = os.environ.get('api_key', 'Missing api key')

client = NotionClient(token_v2=token)
cv = client.get_collection_view(page_url, force_refresh=True)

def updateLastSeen(reference, row=None):
    if row is None:
        row = getRowByReference(reference)

    if row:
        tz = pytz.timezone('America/New_York')
        east_now = datetime.now(tz)
        dd = NotionDate(east_now, None, "America/New_York")
        row.last_seen = dd
        return row
    else:
        print("Failed to find reference " + reference)
        return None

def getRowByReference(reference):
    filter_params = [{
        "property": "reference",
        "comparator": "string_is",
        "value": reference,
    }]
    result = cv.build_query(filter=filter_params).execute()
    if len(result) == 1:
        return result[0]
    else:
        return None

def updateTable(request):
  args = request.args.to_dict(flat=True)
  if not args:
    return 'missing args', 500
  if 'api' not in args:
    return 'missing api key', 500
  if args.get('api') != api_key:
    return 'api key is incorrect', 500

  if not args.get('entity_id'):
    return 'missing entity id', 500

  entity_id = request.args.get('entity_id')
  result = updateLastSeen(entity_id)
  if (result):
    return 'Okay'
  else:
    return 'Fail'
