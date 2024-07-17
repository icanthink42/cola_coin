from fauna import fql
from fauna.client import Client
from fauna.errors import ServiceError

with open("fauna_token.txt") as f:
    token = f.read()

client = Client(secret=token)

async def create_user(discord_id, account_name):
    discord_id = str(discord_id)
    try:
        client.query(fql("""
        create_user(${discord_id}, ${account_name})
        """, discord_id=discord_id, account_name=account_name))
    except ServiceError:
        return False
    return True
