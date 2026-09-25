import re, os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.getenv("8929002817:AAGU3GZaKwqsJaBzc01AuqIEaFBgobxj_EY")

# ===== المنيو الجديد =====
keyboard = [
    ["👁️‍🗨️ فحص الروابط"],
    ["ℹ️ معلومات البوت", "👑 𝑫𝑬𝑽𝑬𝑳𝑶𝑷𝑬𝑹 : 𝑬𝑳 𝑬𝑻𝑺𝑯"]
]
markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

# ===== دومينات خطيرة ومشبوهة =====
DANGEROUS = ["powerv1.site", "grabify", "iplogger", "blasze", "webcam", "whatsapp-hack", "ip-", "camera-hack"]
SUSPICIOUS = ["2no.co", "yip.su", "tinyurl", "bit.ly", "cutt.ly", "shorturl", "free", "gift", "login", "verify"]

def analyze_link(url: str):
    low = url.lower()

    # 1- فحص ضار
    for bad in DANGEROUS:
        if bad in low:
            return "ضار", f"**السبب:** الدومين `{bad}` معروف انه للاختراق والتتبع والكاميرا"

    if "@" in url or re.match(r"https?://\d+\.\d+\.\d+\.\d+", url):
        return "ضار", "**السبب:** اللينك يستخدم طريقة اخفاء بـ @ او IP مباشر للخداع"

    # 2- فحص مشبوه
    for sus in SUSPICIOUS:
        if sus in low:
            return "مشبوه", f"**السبب:** يحتوي على كلمة `{sus}` وهي غالباً لاخفاء الرابط الحقيقي"

    if "http://" in low:
        return "مشبوه", "**السبب:** اللينك غير مشفر ويستخدم http وليس https"

    # 3- آمن
    return "آمن", "**السبب:** لم يتم العثور على علامات تصيد او اختراق معروفة"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "**👑 𝑯𝑬𝑺𝑯𝑨𝑴 𝑬𝑳 𝑬𝑻𝑺𝑯 𝑺𝑬𝑪𝑼𝑹𝑰𝑻𝒀 👑**\n\n"
        "**مرحباً بك في بوت الإتش للحماية**\n"
        "اختار من الأسفل للبدء 👇",
        reply_markup=markup,
        parse_mode="Markdown"
    )

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "👁️‍🗨️ فحص الروابط":
        await update.message.reply_text("**تمام، ابعت اللينك اللي عايز تفحصه الآن 🔗**", parse_mode="Markdown")
        return

    if text == "👑 𝑫𝑬𝑽𝑬𝑳𝑶𝑷𝑬𝑹 : 𝑬𝑳 𝑬𝑻𝑺𝑯":
        await update.message.reply_text(
            "**👑 𝑫𝑬𝑽𝑬𝑳𝑶𝑷𝑬𝑹 : 𝑬𝑳 𝑬𝑻𝑺𝑯 👑**\n\n"
            "**المطور:** هشام الإتش\n"
            "**اليوزر:** @YOUR_USERNAME",
            parse_mode="Markdown"
        )
        return

    if text == "ℹ️ معلومات البوت":
        await update.message.reply_text(
            "**ℹ️ معلومات البوت**\n\n"
            "**تم تطوير هذا البوت بواسطة المطور هشام الإتش منعاً للابتزاز**\n\n"
            "**بوت الإتش لحماية المستخدمين وحرمان المبتزين والمخربين من الوصول الي اهدافهم الخبيثة**",
            parse_mode="Markdown"
        )
        return

    # فحص اللينك
    urls = re.findall(r'https?://\S+', text)
    if not urls:
        await update.message.reply_text("**ابعت لينك صحيح يبدأ بـ https://**", parse_mode="Markdown", reply_markup=markup)
        return

    url = urls[0]
    await update.message.reply_text(f"**🔍 جاري فحص الرابط...**\n`{url}`", parse_mode="Markdown")

    status, reason = analyze_link(url)

    if status == "آمن":
        msg = f"**لينك آمن يمكنك الدخول بكل طمأنينة ✅**\n\n**الرابط:** `{url}`\n\n{reason}"
    elif status == "ضار":
        msg = f"**لينك ضار احذر من الدخول إليه والعبث به 🚫**\n\n**الرابط:** `{url}`\n\n{reason}"
    else: # مشبوه
        msg = f"**لينك مشبوه لم يتم التعرف علي نسبة امانه 👻**\n\n**الرابط:** `{url}`\n\n{reason}"

    await update.message.reply_text(msg, parse_mode="Markdown", reply_markup=markup)

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))
    print("بوت الإتش المية مية اشتغل")
    app.run_polling()

if __name__ == "__main__":
    main()
