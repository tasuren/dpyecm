# dpyecm - Test

from os import environ

import discord

from dpyecm import ExtendContextMenu


pguild = discord.Object(777430548951728149)


client = discord.Client(intents=discord.Intents.default())
tree = discord.app_commands.CommandTree(client)
ecm_message = ExtendContextMenu(tree, discord.AppCommandType.message, guild=pguild)
ecm_user = ExtendContextMenu(tree, discord.AppCommandType.user, guild=pguild)


@tree.error
async def on_error(interaction: discord.Interaction, error):
    print(1, error)


@client.event
async def on_ready():
    print("Connected")
    await tree.sync(guild=pguild)
    print("Synced")


async def test1(interaction: discord.Interaction, obj: discord.Message):
    await interaction.response.send_message(f"Hi: {obj}", ephemeral=True)
ecm_message.add_context(discord.app_commands.ContextMenu(name="test1", callback=test1))
ecm_user.add_context(discord.app_commands.ContextMenu(name="test1", callback=test1))
async def test2(interaction: discord.Interaction, obj: discord.Message):
    await interaction.response.send_message(f"Hi: {obj}", ephemeral=True)
    raise ValueError("test")
ecm_message.add_context(discord.app_commands.ContextMenu(name="test2", callback=test2))


@discord.app_commands.context_menu()
@discord.app_commands.checks.cooldown(1, 30)
async def show_id(interaction: discord.Interaction, member: discord.Member):
    await interaction.response.send_message(
        f"This member's id is `{member.id}`.", ephemeral=True
    )
ecm_user.add_context(show_id)


client.run(environ["TOKEN"])