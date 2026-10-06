import discord, os
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

# --- VIEW VERIFIKASI ---
class Verif(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    @discord.ui.button(label="✅ Verifikasi Disini", style=discord.ButtonStyle.green, custom_id="daf_verif_123")
    async def btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        role = discord.utils.get(interaction.guild.roles, name="Member")
        if not role:
            role = await interaction.guild.create_role(name="Member")
        if role in interaction.user.roles:
            await interaction.response.send_message("Lu udah Member bos!", ephemeral=True)
        else:
            await interaction.user.add_roles(role)
            await interaction.response.send_message(f"✅ Berhasil! Role Member dikasih!", ephemeral=True)

@bot.event
async def on_ready():
    print(f"ONLINE {bot.user}")
    bot.add_view(Verif())
    await bot.tree.sync()
    print("Semua command synced!")

# --- COMMAND 1: SETUP VERIF ---
@bot.tree.command(name="setup", description="Setup verifikasi DAF")
async def setup(interaction: discord.Interaction):
    emb = discord.Embed(title="📜 VERIFIKASI MEMBER", description="Klik tombol di bawah untuk buka akses server!\n\n✅ Klik **Verifikasi Disini**", color=0x00ff00)
    await interaction.response.send_message(embed=emb, view=Verif())

# --- COMMAND 2: EMBED CUSTOM (PISAH) ---
@bot.tree.command(name="embed", description="Bikin embed custom DAF")
@discord.app_commands.describe(title="Judul", description="Isi text", warna="green/red/blue/yellow", channel="Kirim ke mana")
async def embed_custom(interaction: discord.Interaction, title: str, description: str, warna: str = "green", channel: discord.TextChannel = None):
    colors = {"green":0x00ff00,"red":0xff0000,"blue":0x0000ff,"yellow":0xffff00,"purple":0x9b59b6}
    color = colors.get(warna.lower(), 0x00ff00)
    emb = discord.Embed(title=title, description=description, color=color)
    emb.set_footer(text=f"By {interaction.user.name}")
    target = channel if channel else interaction.channel
    await interaction.response.send_message(f"✅ Dikirim ke {target.mention}", ephemeral=True)
    await target.send(embed=emb)

# --- COMMAND 3: SAY (BOT NGOMONG) ---
@bot.tree.command(name="say", description="Bot ngomongin pesan lu")
async def say(interaction: discord.Interaction, pesan: str, channel: discord.TextChannel = None):
    target = channel if channel else interaction.channel
    await interaction.response.send_message(f"✅ Dikirim ke {target.mention}", ephemeral=True)
    await target.send(pesan)

bot.run(os.getenv("TOKEN"))
