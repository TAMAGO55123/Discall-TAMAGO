import discord
from dotenv import load_dotenv
from discord.ext import commands
from discord import app_commands
from datetime import datetime, timedelta
from keep_alive import keep_alive
from os import getenv
import asyncio

load_dotenv()
TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True

bot = commands.Bot(command_prefix="/", intents=intents)

latest_bump_time = None

ROLE_ID =getenv("Admin_id")  # 特定のロールID
TOKEN = getenv("TOKEN")  # TOKENの取得
RUNNER_NAME = getenv("PC_NAME")
terminal_id = getenv("Log_id")
update_id = getenv("Server_log_id")


@bot.event
async def on_ready():
    # 起動したらターミナルにログイン通知が表示される
    log(f'{bot.user} としてログインしました^o^')
    try:
        synced = await bot.tree.sync()
        log(f'Synced {len(synced)} commands')
    except Exception as e:
        log(f'Error syncing commands: {e}')
    # 起動したことを送信
    await send_update_message()

async def log(message):
    print(message)
    # ターミナルの代わりを作ったまで
    log = await bot.fetch_channel(terminal_id)
    await log.send(message)


async def handle_bump_notification(message):
    master = datetime.now() + timedelta(hours=1)
    notice_embed = discord.Embed(
        title="UPを検知しました",
        description=f"<t:{int(master.timestamp())}:f> 頃に通知します",
        color=0x00BFFF,
        timestamp=datetime.now()
    )
    await message.channel.send(embed=notice_embed)
    await asyncio.sleep(3600)
    #await asyncio.sleep(3)
    notice_embed = discord.Embed(
        title="UPが可能です！",
        description="</up:935190259111706754> でUPできます",
        color=0x3FFB3A,
        timestamp=datetime.now()
    )
    await message.channel.send(embed=notice_embed)

@bot.event
async def on_message(message):
    global channel_pairs, user_word_counts, respond_words
    global latest_bump_time
    if message.author == bot.user:
        return

    embeds = message.embeds
    data1=""
    if embeds is not None and len(embeds) != 0:
        for item in embeds:
            print(item.description)
            data1=data1+item.description
        if "サーバーは上部に表示されます。" in data1:
            latest_bump_time = datetime.now()  # 最新のBUMPの時刻を記録
            await handle_bump_notification(message)

@bot.tree.command(name="status",description="ステータスを設定するコマンドです")
@app_commands.describe(text="ステータスを設定します")
async def text(interaction: discord.Interaction, text: str):
    if ROLE_ID in [role.id for role in interaction.user.roles]:
        await bot.change_presence(status=discord.Status.online, activity=discord.CustomActivity(name=f'{text}'))
        await interaction.response.send_message(f'ステータスを「{text}」に設定しました。',ephemeral=True)
    else:
        await interaction.response.send_message('このコマンドを実行する権限がありません。', ephemeral=True)
    
async def send_update_message():
    update = await bot.fetch_channel(update_id)
    embed = discord.Embed(title='BOTが起動しました^o^',description=f"{RUNNER_NAME}を使用してBOTが起動されました",color=0x0004ff,timestamp=datetime.utcnow())
    await update.send(embed=embed)

try:
    keep_alive()
    bot.run(TOKEN)
except Exception as e:
    print(f'エラーが発生しました: {e}')
