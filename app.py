from kafka import KafkaProducer
from kafka import KafkaConsumer
from kafka.errors import KafkaError

producer = KafkaProducer(bootstrap_servers=['192.168.27.185:9092'])

# Asynchronous by default
future = producer.send('demo-topic', b'raw_bytes')

## Block for 'synchronous' sends
try:
    record_metadata = future.get(timeout=10)
except KafkaError:
    # Decide what to do if produce request failed...
    log.exception()
    pass

# Successful result returns assigned partition and offset
print (record_metadata.topic)
print (record_metadata.partition)
print (record_metadata.offset)

# produce keyed messages to enable hashed partitioning
producer.send('demo-topic', key=b'foo', value=b'bar')

# encode objects via msgpack
#producer = KafkaProducer(value_serializer=msgpack.dumps)
#producer.send('msgpack-topic', {'key': 'value'})

# produce json messages
#producer = KafkaProducer(value_serializer=lambda m: json.dumps(m).encode('ascii'))
#producer.send('json-topic', {'key': 'value'})

# produce asynchronously
for _ in range(100):
    producer.send('demo-topic', b'msg')

# block until all async messages are sent
producer.flush()

# configure multiple retries
#producer = KafkaProducer(retries=5)
print ('message produced')
consumer = KafkaConsumer('demo-topic',
                         group_id='my-group',
                         bootstrap_servers=['192.168.27.185:9092'])
for message in consumer:
    # message value and key are raw bytes -- decode if necessary!
    # e.g., for unicode: `message.value.decode('utf-8')`
    print ("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,
                                          message.offset, message.key,
                                          message.value))
