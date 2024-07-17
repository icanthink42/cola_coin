import discord
import api

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


with open("discord_token.txt") as f:
    token = f.read()

bot.run(token)
