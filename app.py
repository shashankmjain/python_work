from kafka import SimpleProducer, SimpleClient

# To send messages asynchronously
client = SimpleClient('192.168.27.185:9092')
producer = SimpleProducer(client, async=True)
producer.send_messages('demo-topic', b'async message')

# To send messages in batch. You can use any of the available
# producers for doing this. The following producer will collect
# messages in batch and send them to Kafka after 20 messages are
# collected or every 60 seconds
# Notes:
# * If the producer dies before the messages are sent, there will be losses
# * Call producer.stop() to send the messages and cleanup
producer = SimpleProducer(client,
                          async=True,
                          batch_send_every_n=20,
                          batch_send_every_t=60)
						  
						client = SimpleClient('192.168.27.185:9092')
consumer = SimpleConsumer(client, "my-group", "demo-topic")
for message in consumer:
    # message is raw byte string -- decode if necessary!
    # e.g., for unicode: `message.decode('utf-8')`
    print(message)


# Use multiprocessing for parallel consumers
from kafka import MultiProcessConsumer

# This will split the number of partitions among two processes
consumer = MultiProcessConsumer(client, "my-group", "demo-topic", num_procs=2)

# This will spawn processes such that each handles 2 partitions max


for message in consumer:
    print(message)

for message in consumer.get_messages(count=5, block=True, timeout=4):
    print(message)

client.close()