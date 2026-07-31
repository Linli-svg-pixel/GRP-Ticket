import os
import discord
from discord.ext import commands

TOKEN = os.getenv("MTUzMjgyMDY1ODA5NzIyOTk4NQ.GLY7br.9OQNO6QuO5oI3O2gdIGFCYewtOpvapjVz5VCzM")
SUPPORT_ROLE = "|———Server Team——-|"

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

class CloseView(discord.ui.View):
    @discord.ui.button(label="🔒 Ticket schließen", style=discord.ButtonStyle.red)
    async def close(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("Ticket wird geschlossen...", ephemeral=True)
        await interaction.channel.delete()

class TicketView(discord.ui.View):
    @discord.ui.button(label="🎫 Ticket erstellen", style=discord.ButtonStyle.green)
    async def ticket(self, interaction: discord.Interaction, button: discord.ui.Button):

        guild = interaction.guild

        category = discord.utils.get(guild.categories, name="Tickets")
        if category is None:
            category = await guild.create_category("Tickets")

        channel = await guild.create_text_channel(
            f"ticket-{interaction.user.name}",
            category=category
        )

        await channel.set_permissions(guild.default_role, view_channel=False)
        await channel.set_permissions(interaction.user, view_channel=True, send_messages=True)

        support = discord.utils.get(guild.roles, name=SUPPORT_ROLE)
        if support:
            await channel.set_permissions(support, view_channel=True, send_messages=True)

        await channel.send(
            f"Willkommen {interaction.user.mention}!\nBeschreibe dein Problem.",
            view=CloseView()
        )

        await interaction.response.send_message(
            f"Dein Ticket wurde erstellt: {channel.mention}",
            ephemeral=True
        )

@bot.event
async def on_ready():
    print(f"{bot.user} ist online.")
    bot.add_view(TicketView())
    bot.add_view(CloseView())

@bot.command()
async def ticket(ctx):
    await ctx.send(
        "Klicke auf den Button, um ein Ticket zu erstellen.",
        view=TicketView()
    )

bot.run(TOKEN)
