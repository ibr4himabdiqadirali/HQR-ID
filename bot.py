# ... (Koodhkaagii hore ee ID-ga, magaca, iwm lagusoo saarayay) ...

        # 1. Raadi sawirka Profile-ka (User, Bot ama Channel)
        photo_id = None
        photo_status = "🔒 Hidden"
        
        try:
            # Isku day inuu kasoo qaado xogta Chat-ka (Sida Channels iyo Bots)
            chat_info = bot.get_chat(target_id)
            if chat_info.photo:
                photo_id = chat_info.photo.big_file_id
                photo_status = "🖼 1 Photo"
            else:
                # Haddii uusan ahayn channel/bot, ka raadi sawirada User-ka
                photos = bot.get_user_profile_photos(target_id)
                if photos.total_count > 0:
                    photo_id = photos.photos[0][-1].file_id
                    photo_status = f"🖼 {photos.total_count} Photo(s)"
        except Exception as e:
            pass # Haddii cilad timaado ama sawirku qarsoon yahay, iska dhaaf.

        # 2. Habaynta Qoraalka (Caption-ka)
        caption = f"""🔎 TELEGRAM ID CHECK

👤 Name: {name}
🔗 Username: {username}
🆔 <code>{target_id}</code> | {len(str(target_id))} digits

🌐 Language/Region: {lang}
🖼 Profile Picture: {photo_status}
📝 Bio/Desc: {bio}
🎂 Birthday: {birthday}

<blockquote>This data helps you:
• understand the real age of the account
• assess profile reliability
• avoid risks in deals and communication</blockquote>"""

        # 3. Dirista Fariinta (Sawir + Qoraal) ama (Qoraal kaliya)
        if photo_id:
            # Haddii sawir la helo, sawirka raaci
            bot.send_photo(message.chat.id, photo=photo_id, caption=caption, parse_mode="HTML", reply_markup=your_markup_buttons)
        else:
            # Haddii sawirku qarsoon yahay, qoraal kaliya dir
            bot.reply_to(message, caption, parse_mode="HTML", reply_markup=your_markup_buttons)

# ... (Inta kale ee koodhkaaga) ...
