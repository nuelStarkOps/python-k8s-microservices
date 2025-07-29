import pika, json

# Upload Fn uploads the file to MongoDB using GridFs
#   put message in RabbitMQ queue to allow downstream service pull ID from queue
#   Queue allows asynch btw Gateway and Vid~>mp3 svc


def upload(f, fs, channel, access):
    try:
        fid = fs.put(f) # file id
    except Exception as err:
        return "internal serveer error", 500
    
    # file id object is returned as string if successful
    message = {
        "video_fid": str(fid),
        "mp3_fid": None,
        "Username": access["username"],
    }
    
    #try to add message to queue
    try: 
        channel.basic_publish(
            exchange="", # default exchange (empty string "") - every queue created is bound to default exchange with routing key same as queue name.
            routing_key="video", # routing key will be name of queue
            body=json.dumps(message), # converts python object into json string - gives converter svc all the info needed for the conversion
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSITENT_DELIVERY_MODE # message is persistent so that messages stay even if pod fails and restarts
            ),
        )
    except:
        fs.delete(fid) # delete file from MongoDB in case of failure | since without message, it never gets processed
        return "internal server error", 500