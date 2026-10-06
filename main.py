import discord, os
from discord.ext import commands
from discord import app_commands

TOKEN = os.getenv("TOKEN")
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

class VerifyView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    @discord.ui.button(label="✅ Verifikasi Disini", style=discord.ButtonStyle.green, custom_id="verify_final")
    async def verify_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer(ephemeral=True)
        role = discord.utils.get(interaction.guild.roles, name="Member")
        if not role:
            role = await interaction.guild.create_role(name="Member")
        if role in interaction.user.roles:
            await interaction.followup.send("Udah verif bos!", ephemeral=True)
            return
        await interaction.user.add_roles(role)
        await interaction.followup.send(f"✅ Berhasil {interaction.user.mention}!", ephemeral=True)

@bot.event
async def on_ready():
    bot.add_view(VerifyView())
    await bot.tree.sync()
    print(f"ONLINE 24 JAM: {bot.user}")

@bot.tree.command(name="setup", description="Setup verif")
@app_commands.checks.has_permissions(administrator=True)
async def setup_slash(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=True)
    embed = discord.Embed(title="🔒 VERIFIKASI MEMBER", description="Klik tombol di bawah untuk membuka akses server!", color=discord.Color.green())
    await interaction.channel.send(embed=embed, view=VerifyView())
    await interaction.followup.send("✅ Beres!", ephemeral=True)

bot.run(TOKEN)
