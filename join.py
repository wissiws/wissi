import os
from datetime import datetime
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
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run_web_server)
    t.start()


# 2. 디스코드 봇 설정 (⚠️ 멤버 이벤트를 감지하기 위해 members 인텐트 활성화 필수)
intents = discord.Intents.default()
intents.members = True # 유저 입장/퇴장 감지를 위해 필수 설정!

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

    # ✨ [새로 추가된 부분] 유저가 서버에 입장했을 때 작동하는 이벤트
    async def on_member_join(self, member: discord.Member):
        # ⚠️ 환영 메시지를 보낼 채널 ID를 여기에 적어주세요 (숫자만 입력)
        # 예: WELCOME_CHANNEL_ID = 123456789012345678
        WELCOME_CHANNEL_ID = 0 
        
        channel = self.get_channel(WELCOME_CHANNEL_ID)
        if channel is None:
            print(f"에러: ID가 {WELCOME_CHANNEL_ID}인 채널을 찾을 수 없습니다.")
            return

        # 현재 시간 가져오기 및 포맷팅 (YYYY년 MM월 DD일 HH:MM:SS)
        now = datetime.now().strftime("%Y년 %m월 %d일 %H:%M:%S")

        # 이미지와 동일한 임베드 구성
        embed = discord.Embed(
            title=f"!! {member.display_name}님이 입장했습니다.",
            description=f"**환영합니다!**\n<@{member.id}>님,\nZERO CLOUD에 오신걸\n환영합니다.",
            color=discord.Color.from_rgb(46, 204, 113) # 이미지와 유사한 초록색 바
        )
        
        # 하단 입장 시간 및 ID 안내
        embed.set_footer(text=f"입장 시간: {now} | ID: {member.id}")
        
        # 우측 상단에 유저의 프로필 사진(아바타) 배치
        if member.avatar:
            embed.set_thumbnail(url=member.avatar.url)
        else:
            embed.set_thumbnail(url=member.default_avatar.url)

        # 메시지 전송
        await channel.send(embed=embed)

bot = MyBot()

# /웹사이트 명령어
@bot.tree.command(name="웹사이트", description="Wissi KR 공식 웹사이트 링크를 보냅니다.")
async def website_command(interaction: discord.Interaction):
    site_url = "https://www.google.com"
    
    embed = discord.Embed(
        title="Wissi KR 공식 웹사이트",
        url=site_url,
        color=discord.Color.blue()
    )
    embed.description = site_url 

    await interaction.response.send_message(embed=embed)


# 3. 봇 실행 플로우
if __name__ == "__main__":
    keep_alive()
    token = os.environ.get("DISCORD_TOKEN")
    
    if token:
        bot.run(token)
    else:
        print("에러: 환경변수에 'DISCORD_TOKEN'이 설정되지 않았습니다.")
