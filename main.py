import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

class VerifView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="✅ Verifikasi Disini", style=discord.ButtonStyle.green, custom_id="verif_btn")
    async def verif(self, interaction: discord.Interaction, button: discord.ui.Button):
        role = discord.utils.get(interaction.guild.roles, name="Member")
        if not role:
            role = await interaction.guild.create_role(name="Member")
        if role in interaction.user.roles:
            await interaction.response.send_message("Lu udah terverifikasi bos!", ephemeral=True)
        else:
            await interaction.user.add_roles(role)
            await interaction.response.send_message(f"Berhasil verifikasi! Welcome {interaction.user.mention} dapet role {role.mention}", ephemeral=True)

@bot.event
async def on_ready():
    print(f"ONLINE 24 JAM - {bot.user}")
    bot.add_view(VerifView())
    try:
        synced = await bot.tree.sync()
        print(f"Sync {len(synced)} command")
    except Exception as e:
        print(e)

@bot.tree.command(name="setup", description="Setup verifikasi DAF")
async def setup(interaction: discord.Interaction):
    embed = discord.Embed(
        title="📜 VERIFIKASI MEMBER",
        description="Klik tombol di bawah untuk membuka akses server!\n\n✅ Klik **Verifikasi Disini** buat dapet role Member",
        color=0x00ff00
    )
    await interaction.response.send_message(embed=embed, view=VerifView())
    
TOKEN = os.getenv("TOKEN")
bot.run(TOKEN)
