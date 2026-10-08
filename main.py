import discord, os, json, random, math
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# --- DATABASE ---
try:
    with open("levels.json", "r") as f:
        levels = json.load(f)
except:
    levels = {}
def save_levels():
    with open("levels.json", "w") as f:
        json.dump(levels, f, indent=4)
def get_level(xp):
    return int(math.sqrt(xp / 100))

LEVEL_ROLES = {
    5: "🌱 Active",
    10: "💎 Sapphire",
    15: "🔥 Elite",
    20: "👑 Legend",
    30: "💀 Immortal"
}
LEVEL_UP_ID = 1556686604632989717

# --- VIEW VERIFIKASI (FIX TIMEOUT) ---
class Verif(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    @discord.ui.button(label="✅ Verifikasi Disini", style=discord.ButtonStyle.green, custom_id="verif_daf_final")
    async def btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        role = discord.utils.get(interaction.guild.roles, name="Member")
        if not role:
            role = await interaction.guild.create_role(name="Member")
        if role in interaction.user.roles:
            await interaction.response.send_message("Kamu udah Member bos!", ephemeral=True)
        else:
            await interaction.user.add_roles(role)
            await interaction.response.send_message("✅ Verif DAF berhasil! Welcome!", ephemeral=True)

# --- VIEW SELF ROLE ---
class SelfRoleView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    @discord.ui.select(
        custom_id="selfrole_final",
        placeholder="💎 Pilih role kamu...",
        min_values=1, max_values=3,
        options=[
            discord.SelectOption(label="Valorant", emoji="🎮"),
            discord.SelectOption(label="Mobile Legends", emoji="⚔️"),
            discord.SelectOption(label="Roblox", emoji="🧱"),
            discord.SelectOption(label="Chill", emoji="💎"),
            discord.SelectOption(label="Ngobrol", emoji="💬"),
            discord.SelectOption(label="Cewek", emoji="👩"),
            discord.SelectOption(label="Cowok", emoji="👨"),
        ]
    )
    async def select_callback(self, interaction: discord.Interaction, select: discord.ui.Select):
        added = []
        for role_name in select.values:
            role = discord.utils.get(interaction.guild.roles, name=role_name)
            if not role:
                role = await interaction.guild.create_role(name=role_name, color=discord.Color.blue())
            if role in interaction.user.roles:
                await interaction.user.remove_roles(role)
                added.append(f"❌ {role_name} dihapus")
            else:
                await interaction.user.add_roles(role)
                added.append(f"✅ {role_name} ditambah")
        await interaction.response.send_message("\n".join(added), ephemeral=True)

@bot.event
async def on_ready():
    print(f"ONLINE {bot.user} ✅")
    bot.add_view(Verif())
    bot.add_view(SelfRoleView())
    await bot.tree.sync()

@bot.event
async def on_member_join(member):
    ch = discord.utils.get(member.guild.text_channels, name="welcome")
    if ch:
        emb = discord.Embed(title="💎 WELCOME TO DAF", description=f"Hai {member.mention} Welcome! Verif di #verif ya! 💙", color=0x00bfff)
        emb.set_thumbnail(url=member.display_avatar.url)
        await ch.send(embed=emb)

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    uid = str(message.author.id)
    if uid not in levels:
        levels[uid] = {"xp": 0, "level": 0}
    levels[uid]["xp"] += random.randint(5, 15)
    old = levels[uid]["level"]
    new = get_level(levels[uid]["xp"])
    if new > old:
        levels[uid]["level"] = new
        level_ch = bot.get_channel(LEVEL_UP_ID)
        if not level_ch:
            try:
                level_ch = await bot.fetch_channel(LEVEL_UP_ID)
            except:
                level_ch = message.channel
        reward = ""
        for lvl_need, rname in LEVEL_ROLES.items():
            if new >= lvl_need and old < lvl_need:
                r = discord.utils.get(message.guild.roles, name=rname)
                if not r:
                    r = await message.guild.create_role(name=rname, color=discord.Color.gold())
                if r not in message.author.roles:
                    await message.author.add_roles(r)
                    reward += f"\n🎁 Reward: **{rname}**"
        emb = discord.Embed(title="🎉 LEVEL UP!", description=f"GG {message.author.mention} naik ke **Level {new}**! 🔥{reward}", color=0x00bfff)
        emb.set_thumbnail(url=message.author.display_avatar.url)
        emb.set_footer(text=f"DAF Community • XP: {levels[uid]['xp']}")
        await level_ch.send(embed=emb)
    save_levels()
    await bot.process_commands(message)

# --- COMMAND FIX ANTI "DIDN'T RESPOND IN TIME" ---
@bot.tree.command(name="setup", description="Setup verifikasi DAF")
@discord.app_commands.default_permissions(administrator=True)
async def setup(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=True) # INI KUNCINYA BIAR GA MERAH
    emb = discord.Embed(
        title="📜 VERIFIKASI MEMBER",
        description="Klik tombol di bawah untuk membuka akses server!\n\n✅ Klik **Verifikasi Disini** buat dapet role Member",
        color=0x2bff00
    )
    if interaction.guild.icon:
        emb.set_thumbnail(url=interaction.guild.icon.url)
    await interaction.channel.send(embed=emb, view=Verif())
    await interaction.followup.send("✅ Panel verifikasi dikirim!", ephemeral=True)

@bot.tree.command(name="selfrole", description="Kirim panel self-role")
@discord.app_commands.default_permissions(administrator=True)
async def selfrole(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=True)
    emb = discord.Embed(title="💎 SELF ROLE - DAF", description="Pilih role kamu dibawah! Bisa pilih 3 sekaligus. Klik lagi buat hapus.", color=0x00bfff)
    await interaction.channel.send(embed=emb, view=SelfRoleView())
    await interaction.followup.send("✅ Panel Self Role dikirim!", ephemeral=True)

@bot.tree.command(name="level", description="Cek level")
async def level_cmd(interaction: discord.Interaction, member: discord.Member = None):
    member = member or interaction.user
    data = levels.get(str(member.id), {"xp":0, "level":0})
    await interaction.response.send_message(f"{member.mention} Level **{data['level']}** | XP {data['xp']}")

@bot.tree.command(name="leaderboard", description="Top level")
async def lb(interaction: discord.Interaction):
    top = sorted(levels.items(), key=lambda x: x[1]['xp'], reverse=True)[:10]
    txt = "\n".join([f"**{i+1}.** <@{uid}> - Lv {d['level']}" for i, (uid,d) in enumerate(top)])
    await interaction.response.send_message(embed=discord.Embed(title="🏆 LEADERBOARD DAF", description=txt or "Belum ada", color=0xffd700))

# --- EMBED CUSTOM + FOTO ---
@bot.tree.command(name="embed", description="Bikin embed custom + foto")
@discord.app_commands.default_permissions(administrator=True)
async def custom_embed(
    interaction: discord.Interaction,
    title: str,
    description: str,
    channel: discord.TextChannel = None,
    color: str = "#00bfff",
    image: discord.Attachment = None,
    thumbnail: discord.Attachment = None,
    footer: str = None
):
    await interaction.response.defer(ephemeral=True)
    try:
        hex_color = int(color.replace("#",""), 16)
    except:
        hex_color = 0x00bfff
    emb = discord.Embed(title=title, description=description.replace("\\n", "\n"), color=hex_color)
    if image:
        emb.set_image(url=image.url)
    if thumbnail:
        emb.set_thumbnail(url=thumbnail.url)
    if footer:
        emb.set_footer(text=footer)
    target = channel or interaction.channel
    await target.send(embed=emb)
    await interaction.followup.send(f"✅ Embed dikirim ke {target.mention}!", ephemeral=True)

bot.run(os.getenv("TOKEN"))
