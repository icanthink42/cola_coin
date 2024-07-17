import discord
from pandas import DataFrame
import api
from discord.ui import InputText, Item

class OrderListType(discord.ui.View):
    def __init__(self, *items: Item, timeout: float | None = 180, disable_on_timeout: bool = False, company: str):
        super().__init__(*items, timeout=timeout, disable_on_timeout=disable_on_timeout)
        self.company = company

    @discord.ui.button(label="Sell", style=discord.ButtonStyle.primary, emoji="📉")
    async def sell(self, _, interaction):
        await respond_list_orders(interaction, company_name=self.company, list_type="sell")

    @discord.ui.button(label="Buy", style=discord.ButtonStyle.green, emoji="📈")
    async def buy(self, _, interaction):
        await respond_list_orders(interaction, company_name=self.company, list_type="buy")

    @discord.ui.button(label="All", style=discord.ButtonStyle.danger, emoji="📊")
    async def all(self, _, interaction):
        await respond_list_orders(interaction, company_name=self.company, list_type="all")

async def respond_list_orders(interaction, company_name, list_type):
    orders_list, error_message = await api.list_orders(company_name)
    if error_message is None and orders_list is not None:
        order_types = []
        share_numbers = []
        share_prices = []
        for order in orders_list:
            kind = order["kind"]
            if  list_type == "sell" and kind != "sell":
                continue
            elif  list_type == "buy" and kind != "buy":
                continue
            order_types.append(kind)
            share_numbers.append(order["amount"])
            share_prices.append(order["price"])
        dict_dataframe = {
            "Order Type": order_types,
            "Number of Shares": share_numbers,
            "Price Per Share": share_prices,
        }
        if list_type != "all":
            del dict_dataframe["Order Type"]
        text_table = str(DataFrame(dict_dataframe))
        await interaction.respond(f"```\n{text_table}\n```", ephemeral=True)
    else:
        await interaction.respond(error_message, ephemeral=True)

class ShareholderCompanyView(discord.ui.View):
    def __init__(self, *items: Item, timeout: float | None = 180, disable_on_timeout: bool = False, company: str):
        super().__init__(*items, timeout=timeout, disable_on_timeout=disable_on_timeout)
        self.company = company

    @discord.ui.button(label="View Share Orders", style=discord.ButtonStyle.primary, emoji="📈")
    async def view_share_orders(self, _, interaction):
        await interaction.respond(f"# {self.company}", ephemeral=True, view=OrderListType(company=self.company))

    @discord.ui.button(label="Notify Shareholders", style=discord.ButtonStyle.secondary, emoji="📢")
    async def notify_shareholders(self, _, interaction):
        await interaction.response.send_modal(NotifyShareholdersModal(title=f"{self.company} Notify", company=self.company))

    @discord.ui.button(label="Edit Products", style=discord.ButtonStyle.green, emoji="✏️")
    async def edit_products(self, _, interaction):
        await interaction.response.send_message(f"# {self.company}'s Products", ephemeral=True, view=EditProducts(company=self.company))

    @discord.ui.button(label="Dissolve Company", style=discord.ButtonStyle.danger, emoji="🔥")
    async def dissolve_company(self, _, interaction):
        await interaction.response.send_message("You clicked the button!", ephemeral=True)

class CompanyView(discord.ui.View):
    def __init__(self, *items: Item, timeout: float | None = 180, disable_on_timeout: bool = False, company: str):
        super().__init__(*items, timeout=timeout, disable_on_timeout=disable_on_timeout)
        self.company = company

    @discord.ui.button(label="View Share Orders", style=discord.ButtonStyle.primary, emoji="📈")
    async def view_share_orders(self, _, interaction):
        await interaction.respond(f"# {self.company}", ephemeral=True, view=OrderListType(company=self.company))

    @discord.ui.button(label="View Products", style=discord.ButtonStyle.green, emoji="📦")
    async def view_products(self, _, interaction):
        await interaction.response.send_message(f"# {self.company}'s Products", ephemeral=True, view=EditProducts(company=self.company))


class NotifyShareholdersModal(discord.ui.Modal):
    def __init__(self, *children: InputText, title: str, custom_id: str | None = None, timeout: float | None = None, company) -> None:
        super().__init__(*children, title=title, custom_id=custom_id, timeout=timeout)
        self.company = company

        self.add_item(discord.ui.InputText(label="Message Title"))
        self.add_item(discord.ui.InputText(label="Message", style=discord.InputTextStyle.long))

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message("Big", ephemeral=True)

class EditProducts(discord.ui.View):
    def __init__(self, *items: Item, timeout: float | None = 180, disable_on_timeout: bool = False, company: str):
        super().__init__(*items, timeout=timeout, disable_on_timeout=disable_on_timeout)
        self.company = company

    @discord.ui.select(
        placeholder = "Delete a Product",
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
    async def delete_product_callback(self, select, interaction):
        await interaction.response.send_modal(CreateProductModal(title=select.values[0], company=self.company))

    @discord.ui.button(label="Add New Product", style=discord.ButtonStyle.green, emoji="➕")
    async def add_new_product(self, _, interaction):
        await interaction.response.send_modal(CreateProductModal(title="Create New Product", company=self.company))

class CreateProductModal(discord.ui.Modal):
    def __init__(self, *children: InputText, title: str, custom_id: str | None = None, timeout: float | None = None, company) -> None:
        super().__init__(*children, title=title, custom_id=custom_id, timeout=timeout)
        self.company = company

        self.add_item(discord.ui.InputText(label="Product Name"))
        self.add_item(discord.ui.InputText(label="Product Description", style=discord.InputTextStyle.long))
        self.add_item(discord.ui.InputText(label="Product Price"))

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message("This will display the new product", ephemeral=True)
