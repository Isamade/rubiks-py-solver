import asyncio
import aio_pika
import json
import os

RABBITMQ_URL = os.getenv('RABBITMQ_URL', 'amqp://rabbitmq-app')
QUEUE_NAME = 'rubiks_solutions'

async def process_message(message: aio_pika.IncomingMessage):
    async with message.process():
        try:
            body = message.body.decode()
            data = json.loads(body)
            print(f" [x] Received solution:")
            print(f"     Moves: {data.get('moves')}")
            # In a real scenario, you would save this to a database here
        except Exception as e:
            print(f" [!] Error processing message: {e}")

async def consume():
    while True:
        try:
            print(f" [*] Connecting to RabbitMQ at {RABBITMQ_URL}...")
            connection = await aio_pika.connect_robust(RABBITMQ_URL)
            
            async with connection:
                channel = await connection.channel()
                await channel.set_qos(prefetch_count=1)
                
                queue = await channel.declare_queue(QUEUE_NAME, durable=True)
                
                print(f" [*] Waiting for messages in {QUEUE_NAME}. To exit press CTRL+C")
                
                await queue.consume(process_message)
                
                # Wait until the connection is closed
                await asyncio.Future()
        except Exception as e:
            print(f" [!] RabbitMQ Consumer connection failed: {e}. Retrying in 5 seconds...")
            await asyncio.sleep(5)

def start_consumer():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(consume())
