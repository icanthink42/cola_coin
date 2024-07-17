from itertools import product
from discord.ui import InputText, Item
from numpy._core.defchararray import title
from pandas import DataFrame
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
    if await api.create_user(ctx.user.id):
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

@bot.slash_command(guild_ids=guild_ids)
async def create_company(ctx, name: str, shares: int):
    error_message = await api.create_company(ctx.user.id, name, shares)
    if error_message is None:
        await ctx.respond(f"{name} has been created and {shares} shares have been issued.", ephemeral=True)
    else:
        await ctx.respond(error_message, ephemeral=True)

@bot.slash_command(guild_ids=guild_ids)
async def sell_shares(ctx, company_name: str, shares: int, price: float):
    error_message = await api.sell_shares(ctx.user.id, company_name, shares, price)
    if error_message is None:
        await ctx.respond(f"{shares} shares of {company_name} have been put up for sale for {price}cc", ephemeral=True)
    else:
        await ctx.respond(error_message, ephemeral=True)

@bot.slash_command(guild_ids=guild_ids)
async def list_orders(ctx, company_name: str):
    orders_list, error_message = await api.list_orders(company_name)
    if error_message is None and orders_list is not None:
        order_types = []
        share_numbers = []
        share_prices = []
        for order in orders_list:
            order_types.append(order["kind"])
            share_numbers.append(order["amount"])
            share_prices.append(order["price"])
        text_table = str(DataFrame({
            "Order Type": order_types,
            "Number of Shares": share_numbers,
            "Price Per Share": share_prices,
        }))
        await ctx.respond(f"```\n{text_table}\n```", ephemeral=True)
    else:
        await ctx.respond(error_message, ephemeral=True)

class ShareholderCompanyView(discord.ui.View):
    def __init__(self, *items: Item, timeout: float | None = 180, disable_on_timeout: bool = False, company: str):
        super().__init__(*items, timeout=timeout, disable_on_timeout=disable_on_timeout)
        self.company = company

    @discord.ui.button(label="Notify Shareholders", style=discord.ButtonStyle.primary, emoji="📢")
    async def notify_shareholders(self, _, interaction):
        await interaction.response.send_message("You clicked the button!", ephemeral=True)

    @discord.ui.button(label="Edit Products", style=discord.ButtonStyle.green, emoji="✏️")
    async def edit_products(self, _, interaction):
        await interaction.response.send_message(f"# {self.company}'s Products", ephemeral=True, view=EditProducts(company=self.company))

    @discord.ui.button(label="Dissolve Company", style=discord.ButtonStyle.danger, emoji="🔥")
    async def dissolve_company(self, _, interaction):
        await interaction.response.send_message("You clicked the button!", ephemeral=True)

class EditProducts(discord.ui.View):
    def __init__(self, *items: Item, timeout: float | None = 180, disable_on_timeout: bool = False, company: str):
        super().__init__(*items, timeout=timeout, disable_on_timeout=disable_on_timeout)
        self.company = company

    @discord.ui.select(
        placeholder = "Edit a Product",
        min_values = 1,
        max_values = 1,
        options = [
            discord.SelectOption(
                label="Example Product 1",
                description="Neil Macneale I"
            ),
            discord.SelectOption(
                label="Example Product 2",
                description="Neil Macneale II"
            ),
            discord.SelectOption(
                label="Example Product 3",
                description="Neil Macneale III"
            )
        ]
    )
    async def select_callback(self, select, interaction):
        await interaction.response.send_modal(EditProductModal(title=select.values[0], company=company, product=select.values[0]))

    @discord.ui.button(label="Add New Product", style=discord.ButtonStyle.green, emoji="➕")
    async def add_new_product(self, _, interaction):
        await interaction.response.send_message("You clicked the button!", ephemeral=True)

class EditProductModal(discord.ui.Modal):
    def __init__(self, *children: InputText, title: str, custom_id: str | None = None, timeout: float | None = None, company, product) -> None:
        super().__init__(*children, title=title, custom_id=custom_id, timeout=timeout)
        self.company = company
        self.product = product

        self.add_item(discord.ui.InputText(label="Product Name"))
        self.add_item(discord.ui.InputText(label="Product Description", style=discord.InputTextStyle.long))
        self.add_item(discord.ui.InputText(label="Product Price"))

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message("This will display the new product", ephemeral=True)

@bot.slash_command(guild_ids=guild_ids)
async def company(ctx, company_name: str):
    if True: # Check a user is a share holder
        await ctx.respond(f"# {company_name}", ephemeral=True, view=ShareholderCompanyView(company=company_name))
    else:
        await ctx.respond(f"# {company_name}", ephemeral=True, view=CompanyView)

with open("discord_token.txt") as f:
    token = f.read()

bot.run(token)
