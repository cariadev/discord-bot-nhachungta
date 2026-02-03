import discord
from discord.ext import commands
import aiohttp
import json
import os
from datetime import datetime, timedelta
import asyncio
from collections import defaultdict

# Cấu hình intents
intents = discord.Intents.all()
intents.message_content = True
intents.members = True
intents.voice_states = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Database đơn giản (dùng JSON)
class Database:
    def __init__(self):
        self.data = {
            'users': {},  # {user_id: {text_xp, voice_time, level, warnings}}
            'muted_users': {},  # {user_id: unmute_time}
            'banned_words': []
        }
        self.load_data()
    
    def load_data(self):
        if os.path.exists('database.json'):
            with open('database.json', 'r', encoding='utf-8') as f:
                self.data = json.load(f)
    
    def save_data(self):
        with open('database.json', 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=4, ensure_ascii=False)
    
    def get_user(self, user_id):
        user_id = str(user_id)
        if user_id not in self.data['users']:
            self.data['users'][user_id] = {
                'text_xp': 0,
                'voice_time': 0,
                'level': 1,
                'warnings': 0,
                'last_message': None
            }
        return self.data['users'][user_id]
    
    def add_xp(self, user_id, xp):
        user = self.get_user(user_id)
        user['text_xp'] += xp
        
        # Tính level (100 XP cho mỗi level)
        new_level = user['text_xp'] // 100 + 1
        leveled_up = new_level > user['level']
        user['level'] = new_level
        
        self.save_data()
        return leveled_up, user['level']
    
    def add_voice_time(self, user_id, minutes):
        user = self.get_user(user_id)
        user['voice_time'] += minutes
        self.save_data()
    
    def add_warning(self, user_id):
        user = self.get_user(user_id)
        user['warnings'] += 1
        self.save_data()
        return user['warnings']
    
    def reset_warnings(self, user_id):
        user = self.get_user(user_id)
        user['warnings'] = 0
        self.save_data()

db = Database()

# Theo dõi người dùng trong voice channel
voice_users = {}  # {user_id: join_time}

# Welcome/Goodbye Card Generator
async def create_welcome_card(member, card_type="welcome"):
    """Tạo welcome/goodbye card với theme anime"""
    try:
        async with aiohttp.ClientSession() as session:
            # Sử dụng API tạo card (có thể thay bằng API khác)
            avatar_url = str(member.display_avatar.url)
            
            # Tạo embed card đẹp với theme anime
            if card_type == "welcome":
                embed = discord.Embed(
                    title="🌸 WELCOME TO THE SERVER 🌸",
                    description=f"Chào mừng {member.mention} đã đến với **{member.guild.name}**!",
                    color=0xFF69B4,
                    timestamp=datetime.now()
                )
                embed.set_thumbnail(url=avatar_url)
                embed.add_field(name="👤 Thành viên", value=f"#{member.guild.member_count}", inline=True)
                embed.add_field(name="📅 Tham gia Discord", value=member.created_at.strftime("%d/%m/%Y"), inline=True)
                embed.set_image(url="https://i.imgur.com/AfFp7pu.png")  # Anime welcome banner
                embed.set_footer(text=f"ID: {member.id}", icon_url=member.guild.icon.url if member.guild.icon else None)
            else:  # goodbye
                embed = discord.Embed(
                    title="💔 GOODBYE 💔",
                    description=f"**{member.name}** đã rời khỏi server...",
                    color=0x808080,
                    timestamp=datetime.now()
                )
                embed.set_thumbnail(url=avatar_url)
                embed.add_field(name="Thành viên còn lại", value=f"{member.guild.member_count}", inline=True)
                embed.set_footer(text=f"Hẹn gặp lại!", icon_url=member.guild.icon.url if member.guild.icon else None)
            
            return embed
    except Exception as e:
        print(f"Lỗi tạo card: {e}")
        return None

@bot.event
async def on_ready():
    print(f'Bot đã đăng nhập: {bot.user.name}')
    print(f'Bot ID: {bot.user.id}')
    await bot.change_presence(activity=discord.Game(name="!help | Anime Server"))
    
    # Bắt đầu theo dõi voice time
    bot.loop.create_task(track_voice_time())

@bot.event
async def on_member_join(member):
    """Gửi welcome card khi có người join"""
    # Tìm channel welcome (tên channel có thể tùy chỉnh)
    welcome_channel = discord.utils.get(member.guild.text_channels, name='welcome') or \
                     discord.utils.get(member.guild.text_channels, name='general')
    
    if welcome_channel:
        embed = await create_welcome_card(member, "welcome")
        if embed:
            await welcome_channel.send(embed=embed)

@bot.event
async def on_member_remove(member):
    """Gửi goodbye card khi có người rời server"""
    goodbye_channel = discord.utils.get(member.guild.text_channels, name='goodbye') or \
                     discord.utils.get(member.guild.text_channels, name='general')
    
    if goodbye_channel:
        embed = await create_welcome_card(member, "goodbye")
        if embed:
            await goodbye_channel.send(embed=embed)

@bot.event
async def on_voice_state_update(member, before, after):
    """Theo dõi join/leave voice channel"""
    # Người join vào voice channel
    if before.channel is None and after.channel is not None:
        voice_users[member.id] = datetime.now()
        
        # Gửi thông báo trong text channel của voice room đó
        if after.channel.category:
            # Tìm text channel cùng category
            text_channel = None
            for channel in after.channel.category.text_channels:
                if channel.permissions_for(member.guild.me).send_messages:
                    text_channel = channel
                    break
            
            if text_channel:
                embed = discord.Embed(
                    description=f"🎤 {member.mention} đã tham gia **{after.channel.name}**",
                    color=0x00FF00,
                    timestamp=datetime.now()
                )
                embed.set_thumbnail(url=member.display_avatar.url)
                await text_channel.send(embed=embed, delete_after=30)
    
    # Người rời khỏi voice channel
    elif before.channel is not None and after.channel is None:
        if member.id in voice_users:
            join_time = voice_users[member.id]
            duration = datetime.now() - join_time
            minutes = int(duration.total_seconds() / 60)
            
            # Cộng voice time
            db.add_voice_time(member.id, minutes)
            
            del voice_users[member.id]
            
            # Gửi thông báo
            if before.channel.category:
                text_channel = None
                for channel in before.channel.category.text_channels:
                    if channel.permissions_for(member.guild.me).send_messages:
                        text_channel = channel
                        break
                
                if text_channel:
                    embed = discord.Embed(
                        description=f"👋 {member.mention} đã rời **{before.channel.name}** (Thời gian: {minutes} phút)",
                        color=0xFF0000,
                        timestamp=datetime.now()
                    )
                    embed.set_thumbnail(url=member.display_avatar.url)
                    await text_channel.send(embed=embed, delete_after=30)

async def track_voice_time():
    """Cập nhật voice time mỗi phút"""
    await bot.wait_until_ready()
    while not bot.is_closed():
        await asyncio.sleep(60)  # Mỗi phút
        for user_id in list(voice_users.keys()):
            db.add_voice_time(user_id, 1)

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    
    # Kiểm tra nếu user đang bị mute
    user_id = str(message.author.id)
    if user_id in db.data['muted_users']:
        unmute_time = datetime.fromisoformat(db.data['muted_users'][user_id])
        if datetime.now() < unmute_time:
            await message.delete()
            remaining = (unmute_time - datetime.now()).seconds
            await message.channel.send(
                f"{message.author.mention} Bạn đang bị cấm chat! Còn {remaining}s",
                delete_after=5
            )
            return
        else:
            del db.data['muted_users'][user_id]
            db.save_data()
    
    # Kiểm tra từ cấm
    user = db.get_user(message.author.id)
    for word in db.data['banned_words']:
        if word.lower() in message.content.lower():
            warnings = db.add_warning(message.author.id)
            await message.delete()
            
            if warnings == 1:
                embed = discord.Embed(
                    title="⚠️ CẢNH BÁO",
                    description=f"{message.author.mention} Bạn đã sử dụng từ ngữ không phù hợp!\n**Cảnh báo lần 1/2**",
                    color=0xFFA500
                )
                await message.channel.send(embed=embed, delete_after=10)
            elif warnings >= 2:
                # Mute 2 phút
                unmute_time = datetime.now() + timedelta(minutes=2)
                db.data['muted_users'][user_id] = unmute_time.isoformat()
                db.save_data()
                
                embed = discord.Embed(
                    title="🔇 BỊ CẤM CHAT",
                    description=f"{message.author.mention} đã bị cấm chat 2 phút do vi phạm quy định!",
                    color=0xFF0000
                )
                await message.channel.send(embed=embed, delete_after=10)
                db.reset_warnings(message.author.id)
            return
    
    # Cộng XP (tránh spam: giới hạn 1 message/phút để được XP)
    if user['last_message'] is None or \
       datetime.now() - datetime.fromisoformat(user['last_message']) > timedelta(seconds=60):
        leveled_up, level = db.add_xp(message.author.id, 10)
        user['last_message'] = datetime.now().isoformat()
        db.save_data()
        
        if leveled_up:
            embed = discord.Embed(
                title="🎉 LEVEL UP!",
                description=f"Chúc mừng {message.author.mention} đã lên **Level {level}**!",
                color=0xFFD700
            )
            embed.set_thumbnail(url=message.author.display_avatar.url)
            await message.channel.send(embed=embed)
    
    await bot.process_commands(message)

# Commands
@bot.command(name='rank')
async def rank(ctx, member: discord.Member = None):
    """Xem rank của bản thân hoặc người khác"""
    member = member or ctx.author
    user_data = db.get_user(member.id)
    
    embed = discord.Embed(
        title=f"📊 Thông tin của {member.name}",
        color=0x00FFFF
    )
    embed.set_thumbnail(url=member.display_avatar.url)
    embed.add_field(name="Level", value=user_data['level'], inline=True)
    embed.add_field(name="XP", value=f"{user_data['text_xp']}/100", inline=True)
    embed.add_field(name="Voice Time", value=f"{user_data['voice_time']} phút", inline=True)
    
    await ctx.send(embed=embed)

@bot.command(name='top')
async def leaderboard(ctx):
    """Xem bảng xếp hạng server"""
    # Sắp xếp theo level và XP
    sorted_users = sorted(
        db.data['users'].items(),
        key=lambda x: (x[1]['level'], x[1]['text_xp']),
        reverse=True
    )[:10]
    
    embed = discord.Embed(
        title="🏆 TOP 10 SERVER RANKING",
        color=0xFFD700,
        timestamp=datetime.now()
    )
    
    description = ""
    for i, (user_id, data) in enumerate(sorted_users, 1):
        try:
            member = await bot.fetch_user(int(user_id))
            medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"**#{i}**"
            description += f"{medal} {member.name} - Level {data['level']} ({data['text_xp']} XP)\n"
        except:
            continue
    
    embed.description = description or "Chưa có dữ liệu"
    await ctx.send(embed=embed)

@bot.command(name='mute')
@commands.has_permissions(moderate_members=True)
async def mute(ctx, member: discord.Member, minutes: int = 5):
    """Cấm chat thành viên (phút)"""
    unmute_time = datetime.now() + timedelta(minutes=minutes)
    db.data['muted_users'][str(member.id)] = unmute_time.isoformat()
    db.save_data()
    
    embed = discord.Embed(
        title="🔇 MUTED",
        description=f"{member.mention} đã bị cấm chat trong {minutes} phút!",
        color=0xFF0000
    )
    await ctx.send(embed=embed)

@bot.command(name='unmute')
@commands.has_permissions(moderate_members=True)
async def unmute(ctx, member: discord.Member):
    """Bỏ cấm chat thành viên"""
    user_id = str(member.id)
    if user_id in db.data['muted_users']:
        del db.data['muted_users'][user_id]
        db.save_data()
        await ctx.send(f"✅ {member.mention} đã được bỏ cấm chat!")
    else:
        await ctx.send(f"{member.mention} không bị cấm chat!")

@bot.command(name='addword')
@commands.has_permissions(administrator=True)
async def add_banned_word(ctx, *, word):
    """Thêm từ cấm"""
    if word not in db.data['banned_words']:
        db.data['banned_words'].append(word)
        db.save_data()
        await ctx.send(f"✅ Đã thêm từ cấm: **{word}**")
    else:
        await ctx.send(f"Từ **{word}** đã có trong danh sách!")

@bot.command(name='removeword')
@commands.has_permissions(administrator=True)
async def remove_banned_word(ctx, *, word):
    """Xóa từ cấm"""
    if word in db.data['banned_words']:
        db.data['banned_words'].remove(word)
        db.save_data()
        await ctx.send(f"✅ Đã xóa từ cấm: **{word}**")
    else:
        await ctx.send(f"Từ **{word}** không có trong danh sách!")

@bot.command(name='listwords')
@commands.has_permissions(moderate_members=True)
async def list_banned_words(ctx):
    """Xem danh sách từ cấm"""
    if db.data['banned_words']:
        words = ", ".join(f"**{w}**" for w in db.data['banned_words'])
        embed = discord.Embed(
            title="📋 Danh sách từ cấm",
            description=words,
            color=0xFF0000
        )
        await ctx.send(embed=embed)
    else:
        await ctx.send("Chưa có từ cấm nào!")

# Chạy bot
if __name__ == "__main__":
    TOKEN = os.getenv("DISCORD_TOKEN") 
    bot.run(TOKEN)
