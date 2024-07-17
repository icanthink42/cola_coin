import discord
import api
from discord.commands import Option

bot = discord.Bot()

guild_ids = [
    1262923658679287939
]

@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")

@bot.slash_command(guild_ids=guild_ids)
async def register(ctx):
    if await api.create_user(ctx.user.id, ctx.user.name):
        await ctx.respond("Account created!", ephemeral=True)
    else:
        await ctx.respond("You've already created an account!", ephemeral=True)

@bot.slash_command(guild_ids=guild_ids)
async def bal(ctx, user: Option(discord.User, required=False)):
    if user is None:
        user = ctx.user
    balance = await api.balance(user.id)
    if balance is False:
        await ctx.respond(f"{user.mention} has not created registered their account. Tell them to run /register to get started!", ephemeral=True)
    else:
        await ctx.respond(f"{user.mention} has {balance}cc.", ephemeral=True)

@bot.slash_command(guild_ids=guild_ids)
async def pay(ctx, user: discord.User, amount: float):
    error_message = await api.pay(ctx.user.id, user.id, amount)
    if error_message is None:
        await ctx.respond(f"Paid {user.mention} {amount}cc.", ephemeral=True)
        try:
            await user.send(f"{ctx.user.mention} paid you {amount}cc!") # TODO: Error handling
        except discord.errors.Forbidden:
            pass
    else:
        await ctx.respond(error_message, ephemeral=True)

with open("discord_token.txt") as f:
    token = f.read()

bot.run(token)
