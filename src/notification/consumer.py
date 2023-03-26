import pika,sys,os,time
from send import email
def main():
    connection= pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
    channel=connection.channel()
    def callback(ch,method,properties,body):
        print("Received in consumer")
        print(body)
        err= email.notification(body)
        if err:
            ch.basic_nack(delivery_tag=method.delivery_tag)
            print("Error in converting")
        else:
            ch.basic_ack(delivery_tag=method.delivery_tag)
            print("Converted")
    channel.basic_consume(queue='mp3',on_message_callback=callback)

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