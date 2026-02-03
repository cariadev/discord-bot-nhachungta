# 🤖 Discord Bot Anime - Hướng dẫn đầy đủ

Bot Discord đa chức năng với theme anime, bao gồm:
- ✅ Welcome/Goodbye cards anime đẹp mắt
- ✅ Thông báo join/leave voice channel
- ✅ Hệ thống kiểm duyệt nội dung (từ cấm, mute)
- ✅ Level & XP cho chat và voice
- ✅ Bảng xếp hạng server
- ✅ Chạy 24/7

## 📋 Yêu cầu

- Python 3.8 trở lên
- Tài khoản Discord
- Bot Discord đã tạo

## 🚀 Cài đặt

### Bước 1: Tạo Bot trên Discord Developer Portal

1. Truy cập: https://discord.com/developers/applications
2. Click "New Application" → Đặt tên bot
3. Vào tab "Bot" → Click "Add Bot"
4. Bật các **Privileged Gateway Intents**:
   - ✅ PRESENCE INTENT
   - ✅ SERVER MEMBERS INTENT
   - ✅ MESSAGE CONTENT INTENT
5. Copy **Token** (giữ bí mật!)

### Bước 2: Mời Bot vào Server

1. Vào tab "OAuth2" → "URL Generator"
2. Chọn **Scopes**: `bot`, `applications.commands`
3. Chọn **Bot Permissions**:
   - ✅ Read Messages/View Channels
   - ✅ Send Messages
   - ✅ Manage Messages
   - ✅ Embed Links
   - ✅ Attach Files
   - ✅ Read Message History
   - ✅ Add Reactions
   - ✅ Moderate Members
   - ✅ Connect (Voice)
   - ✅ Speak (Voice)
4. Copy URL sinh ra và mở trong browser để mời bot

### Bước 3: Cài đặt Bot trên máy

```bash
# Clone hoặc tải code về
cd discord-bot

# Cài đặt thư viện
pip install -r requirements.txt

# Tạo file .env và thêm token
cp .env.example .env
nano .env  # Hoặc dùng editor khác
```

**Nội dung file .env:**
```env
DISCORD_TOKEN=YOUR_ACTUAL_BOT_TOKEN_HERE
```

### Bước 4: Chạy Bot

```bash
python bot.py
```

Khi thấy "Bot đã đăng nhập: [Tên Bot]" → Bot đã hoạt động! ✅

## 🎮 Các lệnh Bot

### 👤 Lệnh người dùng

| Lệnh | Mô tả | Ví dụ |
|------|-------|-------|
| `!help` | Xem hướng dẫn sử dụng bot | `!help` |
| `!rank` | Xem rank của bạn | `!rank` |
| `!rank @user` | Xem rank của người khác | `!rank @John` |
| `!top` | Xem top 10 server | `!top` |

> 💡 **Tip:** Gõ `!help` để xem menu hướng dẫn đẹp mắt với đầy đủ thông tin chi tiết!

### 🛡️ Lệnh Moderator (Cần quyền "Moderate Members")

| Lệnh | Mô tả | Ví dụ |
|------|-------|-------|
| `!mute @user [phút]` | Cấm chat thành viên | `!mute @John 5` |
| `!unmute @user` | Bỏ cấm chat | `!unmute @John` |
| `!listwords` | Xem danh sách từ cấm | `!listwords` |

### 👑 Lệnh Admin (Cần quyền "Administrator")

| Lệnh | Mô tả | Ví dụ |
|------|-------|-------|
| `!addword [từ]` | Thêm từ cấm | `!addword badword` |
| `!removeword [từ]` | Xóa từ cấm | `!removeword badword` |

## ⚙️ Tính năng chi tiết

### 🎨 Welcome/Goodbye Cards

- **Tự động gửi card** khi có người join/leave server
- Theme anime đẹp mắt
- Hiển thị avatar, thông tin thành viên
- Card sẽ gửi vào channel tên "welcome" hoặc "general"

**Tùy chỉnh:**
- Đổi hình ảnh banner trong code tại dòng `embed.set_image(url="...")`
- Tìm anime banner tại: imgur.com, pinterest.com

### 🎤 Voice Channel Notifications

- **Tự động thông báo** khi ai đó join/leave voice
- Thông báo sẽ gửi trong **text channel cùng category** với voice channel
- Hiển thị thời gian ở trong voice
- Tin nhắn tự xóa sau 30 giây

### 🔒 Hệ thống kiểm duyệt

**Từ cấm:**
1. Lần vi phạm đầu: **Cảnh báo**
2. Lần vi phạm thứ 2: **Mute 2 phút**
3. Tin nhắn chứa từ cấm bị xóa ngay lập tức

**Mute thủ công:**
- Mod có thể mute người dùng với thời gian tùy chỉnh
- Người bị mute không thể gửi tin nhắn
- Tin nhắn của họ sẽ bị xóa tự động

### 📈 Level & XP System

**Chat XP:**
- +10 XP mỗi tin nhắn (giới hạn 1 tin/phút tránh spam)
- 100 XP = 1 Level
- Thông báo level up tự động

**Voice XP:**
- Tự động ghi nhận thời gian trong voice
- Tích lũy theo phút
- Hiển thị trong lệnh `!rank`

### 🏆 Bảng xếp hạng

- Top 10 thành viên có level cao nhất
- Sắp xếp theo level và XP
- Medal cho top 3: 🥇🥈🥉
- Cập nhật real-time

## 🌐 Chạy Bot 24/7

### Option 1: Sử dụng VPS (Khuyên dùng)

**Các dịch vụ VPS rẻ:**
- [Oracle Cloud](https://cloud.oracle.com) - **FREE** forever
- [Google Cloud](https://cloud.google.com) - Free 90 ngày
- [DigitalOcean](https://digitalocean.com) - $6/tháng
- [Vultr](https://vultr.com) - $3.5/tháng

**Hướng dẫn chạy trên VPS:**

```bash
# 1. SSH vào VPS
ssh user@your-vps-ip

# 2. Cài Python
sudo apt update
sudo apt install python3 python3-pip

# 3. Upload code lên VPS (dùng git hoặc scp)
git clone your-repo-url
cd discord-bot

# 4. Cài đặt
pip3 install -r requirements.txt

# 5. Chạy với screen (không bị tắt khi đóng SSH)
screen -S discord-bot
python3 bot.py

# Nhấn Ctrl+A+D để detach
# Để quay lại: screen -r discord-bot
```

### Option 2: Sử dụng Replit (Dễ nhất)

1. Tạo tài khoản tại [Replit.com](https://replit.com)
2. Tạo Repl mới → Import từ GitHub
3. Thêm Secret `DISCORD_TOKEN` trong tab Secrets
4. Click Run

**Giữ bot online 24/7 trên Replit:**
- Sử dụng [UptimeRobot](https://uptimerobot.com) để ping bot
- Hoặc nâng cấp Replit (có phí)

### Option 3: Sử dụng Raspberry Pi

Nếu có Raspberry Pi tại nhà:
```bash
# Cài đặt giống như trên VPS
# Chạy lệnh này để tự khởi động khi reboot
crontab -e
# Thêm dòng:
@reboot cd /home/pi/discord-bot && python3 bot.py
```

## 📁 Cấu trúc File

```
discord-bot/
├── bot.py              # Code chính của bot
├── requirements.txt    # Thư viện cần thiết
├── .env               # Token và cấu hình (không share!)
├── .env.example       # Template cho .env
├── database.json      # Database lưu data (tự tạo)
└── README.md          # File này
```

## 🔧 Tùy chỉnh Bot

### Đổi Prefix (mặc định: !)

```python
# Trong bot.py, dòng 17:
bot = commands.Bot(command_prefix='!', intents=intents)
# Đổi thành:
bot = commands.Bot(command_prefix='?', intents=intents)
```

### Đổi XP mỗi tin nhắn

```python
# Dòng 286:
leveled_up, level = db.add_xp(message.author.id, 10)
# Đổi 10 thành số XP bạn muốn
```

### Đổi thời gian mute khi vi phạm

```python
# Dòng 275:
unmute_time = datetime.now() + timedelta(minutes=2)
# Đổi minutes=2 thành số phút bạn muốn
```

### Thay đổi hình ảnh Welcome Card

```python
# Dòng 62:
embed.set_image(url="https://i.imgur.com/AfFp7pu.png")
# Thay URL bằng link ảnh anime của bạn
```

**Nguồn ảnh anime miễn phí:**
- https://imgur.com
- https://wallhaven.cc
- https://www.pinterest.com

### Tùy chỉnh màu Embed

```python
# Màu hiện tại:
color=0xFF69B4  # Pink
color=0x00FF00  # Xanh lá
color=0xFF0000  # Đỏ
color=0xFFD700  # Vàng

# Tìm mã màu tại: https://htmlcolorcodes.com
```

## ❓ Troubleshooting

### Bot không online?

1. Kiểm tra token trong file `.env`
2. Kiểm tra bot đã được mời vào server chưa
3. Kiểm tra đã bật đủ Intents chưa (xem Bước 1)

### Bot không nhận tin nhắn?

- Bật **MESSAGE CONTENT INTENT** trong Developer Portal
- Kiểm tra quyền bot trong server (Read Messages)

### Lỗi "Missing Permissions"?

- Kiểm tra quyền bot trong Server Settings → Roles
- Bot cần quyền: Send Messages, Manage Messages, Moderate Members

### Database.json không tạo?

- Bot sẽ tự tạo file này khi chạy lần đầu
- Nếu lỗi, tạo thủ công: `touch database.json`

### Lệnh không hoạt động?

- Kiểm tra prefix đúng chưa (mặc định: `!`)
- Kiểm tra quyền của role bạn

## 📊 Database Structure

File `database.json` lưu trữ:

```json
{
  "users": {
    "user_id": {
      "text_xp": 100,
      "voice_time": 50,
      "level": 2,
      "warnings": 0,
      "last_message": "2024-01-01T10:00:00"
    }
  },
  "muted_users": {
    "user_id": "2024-01-01T10:10:00"
  },
  "banned_words": ["badword1", "badword2"]
}
```

## 🎯 Roadmap / Tính năng tương lai

- [ ] Slash commands support
- [ ] Web dashboard để quản lý
- [ ] Music player
- [ ] Mini games (quiz, đoán chữ)
- [ ] Economy system (tiền ảo)
- [ ] Custom welcome images API
- [ ] Backup database tự động

## 🤝 Đóng góp

Bạn có thể cải thiện bot bằng cách:
1. Fork repo
2. Tạo branch mới (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Tạo Pull Request

## 📞 Hỗ trợ

Nếu gặp vấn đề:
1. Đọc phần Troubleshooting
2. Kiểm tra logs khi chạy bot
3. Google error message

## 📝 License

MIT License - Sử dụng tự do cho mục đích cá nhân và thương mại.



