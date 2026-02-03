# 🚀 HƯỚNG DẪN SETUP NHANH

## ⚡ Setup trong 5 phút

### 1. Cài Python (nếu chưa có)

**Windows:**
- Tải từ: https://www.python.org/downloads/
- Chạy file .exe và **NHỚ TICK "Add Python to PATH"**

**Mac:**
```bash
brew install python3
```

**Linux:**
```bash
sudo apt update
sudo apt install python3 python3-pip
```

### 2. Tạo Bot Discord

1. Vào: https://discord.com/developers/applications
2. Click **"New Application"** → Đặt tên (ví dụ: "Anime Bot")
3. Vào tab **"Bot"** → Click **"Add Bot"**
4. **BẬT CÁC INTENTS** (quan trọng!):
   ```
   ✅ PRESENCE INTENT
   ✅ SERVER MEMBERS INTENT  
   ✅ MESSAGE CONTENT INTENT
   ```
5. Click **"Reset Token"** → Copy token (GIỮ BÍ MẬT!)

### 3. Mời Bot vào Server

1. Vào tab **"OAuth2"** → **"URL Generator"**
2. Chọn **Scopes**: 
   - ✅ bot
   - ✅ applications.commands
3. Chọn **Bot Permissions**:
   - ✅ Read Messages/View Channels
   - ✅ Send Messages
   - ✅ Manage Messages
   - ✅ Embed Links
   - ✅ Attach Files
   - ✅ Read Message History
   - ✅ Add Reactions
   - ✅ Moderate Members
   - ✅ Connect
   - ✅ Speak
4. Copy **GENERATED URL** → Mở trong browser → Chọn server

### 4. Cài đặt Bot

```bash
# Mở Terminal/CMD tại folder bot
cd discord-bot

# Cài thư viện
pip install -r requirements.txt

# Tạo file .env
# Windows:
copy .env.example .env
# Mac/Linux:
cp .env.example .env

# Mở file .env và dán token vào
notepad .env  # Windows
nano .env     # Mac/Linux
```

**File .env phải có dạng:**
```
DISCORD_TOKEN=YOUR_DISCORD_BOT_TOKEN

```

### 5. Chạy Bot

```bash
python bot.py
```

Hoặc dùng script auto-restart:
```bash
./run_bot.sh  # Mac/Linux
bash run_bot.sh  # Windows Git Bash
```

### 6. Test Bot

Trong Discord server của bạn:
```
!rank          → Xem rank của bạn
!top           → Xem bảng xếp hạng
!help          → Xem tất cả lệnh
```

## ✅ Checklist

- [ ] Python đã cài (gõ `python --version` để check)
- [ ] Bot đã tạo trên Discord Developer Portal
- [ ] 3 Intents đã BẬT (PRESENCE, MEMBERS, MESSAGE CONTENT)
- [ ] Bot đã được mời vào server
- [ ] Token đã paste vào file .env
- [ ] Đã chạy `pip install -r requirements.txt`
- [ ] Bot đã chạy thành công (không có lỗi)
- [ ] Bot hiện ONLINE trong server

## 🐛 Lỗi thường gặp

### "discord.py not found"
```bash
pip install discord.py
```

### "Invalid Token"
- Check lại token trong file .env
- Token không có khoảng trắng đầu/cuối
- Token phải là token MỚI NHẤT (nếu đã reset)

### "Missing Intents"
- Vào Discord Developer Portal
- Tab Bot → Bật 3 Intents
- Reset bot và thử lại

### Bot không đọc lệnh
- Check prefix đúng không (mặc định: `!`)
- Bot cần quyền "Read Messages"
- Channel không bị ẩn với bot

## 🌐 Chạy 24/7

### Cách 1: VPS (Tốt nhất)

**Oracle Cloud (FREE):**
1. Đăng ký: https://cloud.oracle.com
2. Tạo VM instance (Ubuntu)
3. SSH vào VPS:
```bash
ssh ubuntu@your-vps-ip
```
4. Upload code:
```bash
git clone your-github-repo
cd discord-bot
pip3 install -r requirements.txt
```
5. Chạy với screen:
```bash
screen -S bot
python3 bot.py
# Nhấn Ctrl+A+D để detach
```

**Quay lại screen:**
```bash
screen -r bot
```

### Cách 2: Replit (Dễ nhất)

1. Tạo account: https://replit.com
2. New Repl → Import from GitHub
3. Thêm Secret `DISCORD_TOKEN` (tab Secrets)
4. Click Run
5. Dùng UptimeRobot để bot không sleep

### Cách 3: Raspberry Pi

Nếu có Pi ở nhà:
```bash
# Setup tương tự VPS
# Thêm autostart:
crontab -e
@reboot cd /home/pi/discord-bot && python3 bot.py
```

## 📱 Lệnh hữu ích

### User commands:
```
!rank              - Xem rank của bạn
!rank @user        - Xem rank của người khác  
!top               - Top 10 server
```

### Moderator commands:
```
!mute @user 5      - Mute 5 phút
!unmute @user      - Unmute
!listwords         - Xem từ cấm
```

### Admin commands:
```
!addword badword   - Thêm từ cấm
!removeword word   - Xóa từ cấm
```

## 🎨 Tùy chỉnh nhanh

### Đổi prefix
`bot.py` dòng 17:
```python
bot = commands.Bot(command_prefix='?', intents=intents)
```

### Đổi XP mỗi tin nhắn
`bot.py` dòng 286:
```python
db.add_xp(message.author.id, 20)  # Đổi 10 → 20
```

### Đổi thời gian mute
`bot.py` dòng 275:
```python
timedelta(minutes=5)  # Đổi 2 → 5
```

## 💡 Tips

1. **Tạo channel "welcome"** trong server để bot gửi welcome card
2. **Tạo role "Moderator"** với quyền "Moderate Members"
3. **Test từ cấm** bằng `!addword test` rồi chat "test"
4. **Backup database.json** thường xuyên
5. **Đọc logs** khi bot lỗi để debug

## 📚 Tài liệu thêm

- Discord.py docs: https://discordpy.readthedocs.io
- Discord Developer Portal: https://discord.com/developers
- Python tutorial: https://www.python.org/about/gettingstarted

## 🆘 Cần trợ giúp?

1. Đọc phần **Troubleshooting** trong README.md
2. Check logs khi chạy bot
3. Google error message
4. Hỏi ChatGPT/Claude về lỗi cụ thể

---

**Good luck! 🎉**
