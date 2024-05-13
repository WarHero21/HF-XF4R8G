import pika
from data import Data

def alert_admins(data: Data, RABBITMQ_CONTAINER_NAME):
    # Use plain credentials for authentication
    mq_creds  = pika.PlainCredentials(username = "guest", password = "guest")
    
    # Use localhost
    mq_params = pika.ConnectionParameters(
        RABBITMQ_CONTAINER_NAME,
        5672,
        '/',
        mq_creds
    )
 
    # Anyone subscribing to topic "gallery" receives our messages
    mq_exchange    = "amq.topic"
    mq_routing_key = "gallery"
    
    # This a connection object
    mq_conn = pika.BlockingConnection(mq_params)
    
    # This is one channel inside the connection
    mq_chan = mq_conn.channel()
    

    message = {
        "username": str(data.username),
        "date": str(data.date),
        "number_of_detection": str(data.number_of_detection),
        "filename": str(data.filename),
        "description": str(data.description)
    }
    
    # Switch the ' and " characters to be compatible with javascript JSON.parse()
    message = str(message).replace("\"", "\"\"").replace("\'", "\"").replace("\"\"", "\'")
    
    mq_chan.basic_publish(
        exchange    = mq_exchange,
        routing_key = mq_routing_key,
        body        = message
    )