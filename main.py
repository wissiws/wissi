import os
from threading import Thread
import discord
from discord import app_commands
from discord.ext import commands
from flask import Flask

# 1. Render의 포트 바인딩 및 상시 구동을 위한 가벼운 Flask 웹 서버 설정
app = Flask('')

@app.route('/')
def home():
    return "봇이 정상적으로 작동 중입니다!"

def run_web_server():
    # Render는 포트를 환경 변수('PORT')로 지정하므로 이를 읽어와야 합니다. (기본값 8080)
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run_web_server)
    t.start()


# 2. 디스코드 봇 설정
intents = discord.Intents.default()

class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=intents)

    async def on_ready(self):
        print(f'로그인 성공: {self.user.name}')
        try:
            synced = await self.tree.sync()
            print(f'동기화 성공: {len(synced)}개의 슬래시 명령어를 동기화했습니다.')
        except Exception as e:
            print(f'동기화 실패: {e}')

bot = MyBot()

# /웹사이트 명령어
@bot.tree.command(name="웹사이트", description="클릭하면 이동할 수 있는 웹사이트 링크 임베드를 보냅니다.")
async def website_command(interaction: discord.Interaction):
    site_name = "Wissi Offcial Website"
    site_url = "https://www.google.com"
    
    embed = discord.Embed(
        title="🌐 추천 웹사이트 안내",
        description=f"아래 링크를 클릭하면 해당 사이트로 이동합니다:\n\n👉 **[{site_name}]({site_url})**",
        color=discord.Color.blue()
    )
    embed.add_field(name="바로가기", value=f"[여기 주소를 클릭하세요]({site_url})", inline=False)
    embed.set_footer(text="Wissi KR Bot • 안내 메시지")

    await interaction.response.send_message(embed=embed)


# 3. 봇 실행 플로우
if __name__ == "__main__":
    # 웹 서버 먼저 실행 (Render가 포트를 체크할 수 있도록)
    keep_alive()
    
    # ⚠️ 코드가 아닌 Render 환경변수(Environment Variables)에서 토큰을 가져옵니다.
    token = os.environ.get("DISCORD_TOKEN")
    
    if token:
        bot.run(token)
    else:
        print("에러: 환경변수에 'DISCORD_TOKEN'이 설정되지 않았습니다.")
