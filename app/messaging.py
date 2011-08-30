from celery.messaging import establish_connection
from kombu.compat import Publisher, Consumer
from bjj.app.models import Post 
from kombu import Exchange, Queue, Producer


def send_increment_upvotes(for_post_id):
    """Send a message for incrementing the click count for an URL."""
    exchange = Exchange("test", type="direct")
    queue = Queue("test", exchange, routing_key="test")
    connection = establish_connection()
    channel = connection.channel()
    producer = Producer(channel, exchange, routing_key="test")
    producer.publish(str(for_post_id))
    connection.close()

def process_upvotes():
    """Process all currently gathered clicks by saving them to the
    database."""
    connection = establish_connection()
    consumer = Consumer(connection=connection,
                        queue="test",
                        exchange="test",
                        routing_key="test",
                        exchange_type="direct")
    # First process the messages: save the number of clicks
    # for every URL.
    upvotes_for_post = {}
    messages_for_post = {}
    for message in consumer.iterqueue():
        id = message.body
        upvotes_for_post[id] = upvotes_for_post.get(id, 0) + 1
        # We also need to keep the message objects so we can ack the
        # messages as processed when we are finished with them.
        if id in messages_for_post:
            messages_for_post[id].append(message)
        else:
            messages_for_post[id] = [message]

    # Then increment the clicks in the database so we only need
    # one UPDATE/INSERT for each URL.
    for id, vote_count in upvotes_for_post.items():
        p=Post.objects.get(id=int(id)) # is id a string or int?
        p.upvotes += vote_count
        p.save()
        # Now that the clicks has been registered for this URL we can
        # acknowledge the messages
        [message.ack() for message in messages_for_post[id]]

    consumer.close()
    connection.close()


