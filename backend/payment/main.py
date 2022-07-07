from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.background import BackgroundTasks
from redis_om import get_redis_connection, HashModel
from starlette.requests import Request
import requests, time

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000'],
    allow_methods=['*'],
    allow_headers=['*'],
)

redis_url = "redis://default:yH8qVetKSdR8gySrZOse1U91DJ62NE7J@redis-12578.c276.us-east-1-2.ec2.cloud.redislabs.com:12578"
#This should be a different database
# redis3 = get_redis_connection(
#     url=redis_url,
#     decode_responses=True
# )


redis = get_redis_connection(
    host="redis-12578.c276.us-east-1-2.ec2.cloud.redislabs.com",
    port="12578",
    password="yH8qVetKSdR8gySrZOse1U91DJ62NE7J",
    decode_responses=True
)


class Order(HashModel):
    product_id: str
    price: float
    fee: float
    total: float
    quantity: int
    status: str # pending, completed, refunded

    class Meta:
        database = redis


@app.get('/orders/{pk}')
def get(pk: str):
    return Order.get(pk)



@app.post('/orders')
async def create(request: Request, background_tasks: BackgroundTasks): #id, quantity
    body = await request.json()

    url = f"http://localhost:8000/products/{body['id']}"
    print(url)
    req = requests.get(url)
    product = req.json()
    

    order = Order(
        product_id = body['id'],
        price = product['price'],
        fee = 0.2 * product['price'],
        total = 1.2 * product['price'],
        quantity = body['quantity'],
        status = 'pending'
    )

    order.save()
    
    background_tasks.add_task(order_completed, order)
    
    # redis.xadd('refund_order', order.dict(), '*')
    return order
    
def order_completed(order: Order):
    time.sleep(5)
    order.status = 'completed'
    order.save()
    redis.xadd('order_completed', order.dict(), '*')