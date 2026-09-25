import os, re, requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.getenv("
8929002817:AAGU3GZaKwqsJaBzc01AuqIEaFBgobxj_EY")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN مش موجود في Environment Variables")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👑 HESHAM EL ETSH SECURITY شغال 🔥\nابعت لينك افحصهولك")

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    urls = re.findall(r https?://\S+ , text)
    if urls:
        await update.message.reply_text(f"🔍 بفحص: {urls[0]}\nبفك الاختصار...")
        try:
            r = requests.head(urls[0], allow_redirects=True, timeout=10, headers={"User-Agent":"Mozilla/5.0"})
            await update.message.reply_text(f"🎯 اللينك الأصلي:\n{r.url}")
        except:
            await update.message.reply_text("مقدرتش اوصل للينك")
    else:
        await update.message.reply_text("ابعت لينك")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))
    app.run_polling()

if __name__ == "__main__":
    main()
