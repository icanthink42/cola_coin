from fauna import fql
from fauna.client import Client
from fauna.errors import ServiceError

with open("fauna_token.txt") as f:
    token = f.read()

client = Client(secret=token)

async def create_user(discord_id, account_name):
    try:
        client.query(fql("""
        create_user(${discord_id}, ${account_name})
        """, discord_id=str(discord_id), account_name=account_name))
    except ServiceError:
        return False
    return True

async def balance(discord_id):
    try:
        return client.query(fql("""
        balance(${discord_id})
        """, discord_id=str(discord_id))).data
    except ServiceError:
        return False

async def pay(from_id, to_id, amount):
    try:
        client.query(fql("""
        pay_user(${from_id}, ${to_id}, ${amount})
        """, from_id=str(from_id), to_id=str(to_id), amount=amount)).data
        return None
    except ServiceError as e:
        if e.abort is None:
            return "An internal error occured!"
        return e.abort["message"]
