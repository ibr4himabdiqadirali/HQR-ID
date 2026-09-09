# 1. XALKA CILADDA PYTHON 3.14 EVENT LOOP:
import asyncio
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

# 2. KOODHKA CAADIGA AH (USERBOT)
import sqlite3
from pyrogram import Client, filters
from pyrogram.enums import UserStatus

c = sqlite3.connect("u.db", check_same_thread=False)
x = c.cursor()
x.execute("CREATE TABLE IF NOT EXISTS u(id INTEGER PRIMARY KEY, un TEXT, fn TEXT)")
c.commit()

# Halkani waa Userbot (Account caadi ah), Bot Token looma baahna!
app = Client(
    "my_acc_session", 
    api_id=36675058, 
    api_hash="0fe7b4572c49cbd5a49eb58975fcabef"
)

@app.on_message(filters.private)
async def h(c_obj, m):
    u = m.forward_from or m.from_user
    if not u: return
    
    try:
        x.execute("INSERT OR IGNORE INTO u VALUES(?,?,?)", (u.id, u.username, u.first_name))
        c.commit()
    except: pass
    
    t = m.text
    i = m.from_user.id
    
    if i == 6903972630 and t:
        if t == "👥 Xogta":
            x.execute("SELECT * FROM u")
            o = "👥 Xogta:\n\n"
            for j in x.fetchall():
                o += f"<code>{j[0]}</code> | @{j[1]}\n"
            return await m.reply(o[:4000])
        
        if str(t).startswith(".post "):
            x.execute("SELECT id FROM u")
            s = 0
            for r in x.fetchall():
                try:
                    await c_obj.copy_message(r[0], m.chat.id, m.id)
                    s += 1
                except: pass
            return await m.reply(f"✅ Fariinta waxaa loo diray {s} qof.")
            
    un = f"@{u.username}" if u.username else "Qariyan"
    ti = u.id
    hp = False
    fi = None
    
    async for p in c_obj.get_chat_photos(ti, limit=1):
        hp = True
        fi = p.file_id
        break
        
    ps = "🖼️ 1 Photo Found" if hp else "🔒 Hidden"
    bi = "🔒 Hidden"
    
    try:
        ci = await c_obj.get_chat(ti)
        if getattr(ci, "bio", None):
            bi = f"<code>{ci.bio}</code>"
    except: pass

    # Nidaamka "Last Seen" ee Userbot-ka
    ls = "🔒 Hidden"
    if u.status:
        if u.status == UserStatus.ONLINE:
            ls = "🟢 Online"
        elif u.status == UserStatus.OFFLINE:
            if u.last_online_date:
                ls = f"🕒 {u.last_online_date.strftime('%Y-%m-%d %H:%M')}"
            else:
                ls = "⚪ Offline"
        elif u.status == UserStatus.RECENTLY:
            ls = "🕓 Recently (Last seen recently)"
        elif u.status == UserStatus.LAST_WEEK:
            ls = "📅 Last week"
        elif u.status == UserStatus.LAST_MONTH:
            ls = "🗓️ Last month"

    # Nidaamka "Country Code" 
    cc = "🔒 Hidden"
    if getattr(u, 'phone_number', None):
        cc = f"📱 +{u.phone_number}"
        if u.phone_number.startswith("252"):
            cc += " (🇸🇴 Somalia)"
    elif getattr(u, 'language_code', None):
        cc = f"🌐 {u.language_code.upper()} (Language Region)"
    
    # Maadaama badhamada aan la ogolayn, linkiga Check Another qoraalka ayaan ku daray
    mt = f"""🔎 TELEGRAM ID CHECK

👤 Username: {un}
🆔 <code>{ti}</code> | {len(str(ti))} digits
🏆 Account Rating: 1 level

▪︎ 🌐 Country/Phone: {cc}
▪︎ 🖼️ Profile Picture: {ps}
▪︎ ⏳ Last seen: {ls}
▪︎ 📝 Bio: {bi}
▪︎ 🎂 Birthday: 🔒 Hidden

<blockquote>This data helps you:
• understand the real age of the account
• assess profile reliability
• avoid risks in deals and communication</blockquote>

🔎 <b>Check Another:</b> @HQR_ID"""

    if hp:
        await m.reply_photo(fi, caption=mt)
    else:
        await m.reply(mt)

print("✅ Koodhku waa sax! Wuxuu isku xirayaa Telegram Userbot...")
app.run()
