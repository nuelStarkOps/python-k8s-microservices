import pika, json, tempfile, os
from bson.objectid import ObjectId
import moviepy.editor

def start(message, fs_videos, fs_mp3s, channel):
    message = json.loads(message)
    
    # empty temp. file
    tf = tempfile.NamedTemporaryFile()
    
    # video contents
    out = fs_videos.get(ObjectId(message["video_fid"]))
    
    # add video content to empty file
    tf.write(out.read())
    
    # convert video ~> audio
    audio = moviepy.editor.VideoFileClip(tf.name).audio
    tf.close()
    
    # write audio to file
    tf_path = tempfile.gettempdir() + f"/{message['video_fid']}.mp3"
    audio.write_audiofile(tf_path)
    
    # save file to Mongo
    f = open(tf_path, "rb")
    data = f.read()
    fid = fs_mp3s.put(data)
    f.close()
    os.remove(tf_path)
    
    # update message
    message["mp3_fid"] = str(fid)
    try:
        channel.basic_publish(
            exchange="",
            routing_key=os.environ.get("MP3_QUEUE"),
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            ),
        )
    except Exception as err:
        fs_mp3s.delete(fid)
        return "Failed to publish message"