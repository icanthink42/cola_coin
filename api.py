from fauna import fql
from fauna.client import Client
from fauna.errors import ServiceError

with open("fauna_token.txt") as f:
    token = f.read()

client = Client(secret=token)

async def create_user(discord_id, name):
    try:
        client.query(fql("""
        create_user(${discord_id}, ${name})
        """, discord_id=str(discord_id), name=name))
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
            print(e)
            return "An internal error occured!"
        return e.abort["message"]

async def create_company(owner, name, shares):
    try:
        client.query(fql("""
        create_company(${owner}, ${name}, ${shares})
        """, owner=str(owner), name=str(name), shares=shares)).data
        return None
    except ServiceError as e:
        if e.abort is None:
            print(e)
            return "An internal error occured!"
        return e.abort["message"]

async def sell_shares(owner, company_name, shares, price):
    try:
        client.query(fql("""
        sell_shares(${owner}, ${company_name}, ${shares}, ${price})
        """, owner=str(owner), company_name=str(company_name), shares=shares, price=price)).data
        return None
    except ServiceError as e:
        if e.abort is None:
            print(e)
            return "An internal error occured!"
        return e.abort["message"]

async def buy_shares(owner, company_name, shares, price):
    try:
        client.query(fql("""
        buy_shares(${owner}, ${company_name}, ${shares}, ${price})
        """, owner=str(owner), company_name=str(company_name), shares=shares, price=price)).data
        return None
    except ServiceError as e:
        if e.abort is None:
            print(e)
            return "An internal error occured!"
        return e.abort["message"]

async def list_orders(company_name):
    try:
        return client.query(fql("""
        list_orders(${company_name})
        """, company_name=str(company_name))).data, None
    except ServiceError as e:
        if e.abort is None:
            print(e)
            return None, "An internal error occured!"
        return None, e.abort["message"]

async def create_token(discord_id):
    try:
        return client.query(fql("""
        create_token(${discord_id})
        """, discord_id=str(discord_id))).data, None
    except ServiceError as e:
        if e.abort is None:
            print(e)
            return None, "An internal error occured!"
        return None, e.abort["message"]
