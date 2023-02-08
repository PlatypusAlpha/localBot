import json
import discord
from discord import app_commands
from discord.ext import commands


TOKEN = ""
intents = discord.Intents.all()
intents.members = True
intents.message_content = True
client = commands.Bot(command_prefix="/", intents=intents)

@client.event
async def on_ready():
    print("Bot is Up and Ready!")
    try:
        synced = await client.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)

js_data = {}


@client.tree.command(name="register")
@app_commands.describe(addr="Register your wallet address.")
async def wallet(interaction: discord.Interaction, addr: str = None):

    if addr.startswith("addr1"):
        if interaction.user.id in js_data:
            await interaction.response.send_message("Already Registered.")
        else:
            with open("wallet_list.json", 'w', encoding='utf-8') as f:
                js_data[interaction.user.id] = {"name": interaction.user.name, "wallet": addr}
                json.dump(js_data, f, ensure_ascii=False, indent=4)
            await interaction.response.send_message(f"Address ending in {addr[-5:]} has been registered.")

    elif addr.startswith("$"):
        await interaction.response.send_message(f"We do not support adaHandles at this time.")
    else:
        await interaction.response.send_message(f"Wallet entry of {addr}"
                                                f"doesn't match any known Cardano address patterns.")

    print(js_data)

client.run(TOKEN)