import discord
from discord.ui import InputText, Item

class ShareholderCompanyView(discord.ui.View):
    def __init__(self, *items: Item, timeout: float | None = 180, disable_on_timeout: bool = False, company: str):
        super().__init__(*items, timeout=timeout, disable_on_timeout=disable_on_timeout)
        self.company = company

    @discord.ui.button(label="Notify Shareholders", style=discord.ButtonStyle.primary, emoji="📢")
    async def notify_shareholders(self, _, interaction):
        await interaction.response.send_modal(NotifyShareholdersModal(title=f"{self.company} Notify", company=self.company))

    @discord.ui.button(label="Edit Products", style=discord.ButtonStyle.green, emoji="✏️")
    async def edit_products(self, _, interaction):
        await interaction.response.send_message(f"# {self.company}'s Products", ephemeral=True, view=EditProducts(company=self.company))

    @discord.ui.button(label="Dissolve Company", style=discord.ButtonStyle.danger, emoji="🔥")
    async def dissolve_company(self, _, interaction):
        await interaction.response.send_message("You clicked the button!", ephemeral=True)

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
