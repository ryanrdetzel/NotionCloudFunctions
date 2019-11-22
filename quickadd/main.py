import os
from datetime import datetime
from flask import redirect
from google.cloud import pubsub_v1
import json

topic_name = os.environ.get('topic_name', 'Missing topic name')
project_id = os.environ.get('project_id', 'Missing project id')
redirect_page = os.environ.get('redirect', 'Missing redirect page')

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_name)

def quickadd(request):
  title = 'Untitled'
  args = request.args.to_dict(flat=True)
  if args and 'title' in args:
    title = args.get('title')

  data_obj = {
    'title': title
  }
  data = json.dumps(data_obj)
  publisher.publish(
    topic_path, data=data.encode('utf-8')  # data must be a bytestring.
  )
  
  return redirect(redirect_page, code=302)
