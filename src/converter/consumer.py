import pika,sys,os,time
from pymongo import MongoClient
import gridfs
from convert import to_mp3

def main():
    client=MongoClient('host.minikube.internal',27017)
    db_videos=client.videos
    db_mp3s=client.mp3s

    fs_videos=gridfs.GridFS(db_videos)
    fs_mp3s=gridfs.GridFS(db_mp3s) 
    connection= pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
    channel=connection.channel()
    def callback(ch,method,properties,body):
        print("Received in consumer")
        print(body)
        err= to_mp3.start(body,fs_videos,fs_mp3s,ch)
        if err:
            ch.basic_nack(delivery_tag=method.delivery_tag)
            print("Error in converting")
        else:
            ch.basic_ack(delivery_tag=method.delivery_tag)
            print("Converted")
    channel.basic_consume(queue='video',on_message_callback=callback)

    print("waiting for messages.To exit presss CTR+C")

    channel.start_consuming()
if __name__=='__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)




