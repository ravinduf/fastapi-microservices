from base64 import decode
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from redis_om import get_redis_connection, HashModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000'],
    allow_methods=['*'],
    allow_headers=['*'],
)

redis = get_redis_connection(
    host="redis-12578.c276.us-east-1-2.ec2.cloud.redislabs.com",
    port="12578",
    password="yH8qVetKSdR8gySrZOse1U91DJ62NE7J",
    decode_responses=True
)

class Product(HashModel):
    name: str
    price: float
    quantity: int

    class Meta:
        database = redis


@app.get('/products')
async def all():
    return [format(pk) for pk in Product.all_pks()]

def format(pk: str):
    product = Product.get(pk)

    return {
        'id': product.pk,
        'name': product.name,
        'price': product.price,
        'quantity': product.quantity,
    }

@app.post('/products')
def create(product: Product):
    return product.save()

@app.get('/products/{pk}')
def get(pk: str):
    print(Product.get(pk))
    return Product.get(pk)

@app.delete('/products/{pk}')
def delete(pk: str):
    return Product.delete(pk)

@app.get("/")
async def root():
    return {"message": "Hello World"}


