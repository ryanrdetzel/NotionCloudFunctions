import os
import json

from google.cloud import pubsub_v1

topic_name = os.environ.get('topic_name', 'Missing topic name')
project_id = os.environ.get('project_id', 'Missing project id')

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_name)

def addFromEmail(request):
  args = request.form.to_dict()
  fromAddress = args.get('from')
  subject = args.get('subject')
  text = args.get('text')

  data_obj = {
    'subject': subject,
    'text': text,
    'from': fromAddress
  }
  data = json.dumps(data_obj)
  publisher.publish(
    topic_path, data=data.encode('utf-8')  # data must be a bytestring.
  )
 
  return 'done' 
