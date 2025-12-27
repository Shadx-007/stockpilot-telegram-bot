from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
import yfinance as yf

# 🔐 PUT YOUR BOT TOKEN HERE
BOT_TOKEN = "8215890603:AAGgL__UhX1Nf-JOBrlrd3MJsv5MJ_bsKmI"



# Known NSE symbols (expand later)
SYMBOL_MAP = {
    "tcs": "TCS.NS",
    "reliance": "RELIANCE.NS",
    "infosys": "INFY.NS",
    "itc": "ITC.NS",
    "sbin": "SBIN.NS",
    "hdfc bank": "HDFCBANK.NS",
    "icici bank": "ICICIBANK.NS",
    "lt": "LT.NS",
    "l&t": "LT.NS",
    "adanient": "ADANIENT.NS",
    "adani enterprises": "ADANIENT.NS"
}


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower().strip()

    # -------- UPGRADE INTENT --------
    if "upgrade" in text or "premium" in text:
        await update.message.reply_text(
            "🚀 Early Access\n\n"
            "Portfolio tracking & alerts are coming soon.\n"
            "Free for early users 🙂"
        )
        return

    # -------- EDUCATION QUESTIONS --------
    if "what is pe" in text or "pe ratio" in text:
        await update.message.reply_text(
            "📘 P/E (Price to Earnings) shows how much investors pay for ₹1 of profit.\n\n"
            "Lower P/E → cheaper\n"
            "Higher P/E → expensive\n\n"
            "You can ask:\nITC price"
        )
        return

    if "what is market cap" in text:
        await update.message.reply_text(
            "📘 Market Cap is the total value of a company.\n\n"
            "Market Cap = Share Price × Total Shares\n\n"
            "Large cap = stable\n"
            "Small cap = risky but high growth"
        )
        return

    # -------- STOCK PRICE / ANALYSIS --------
    if "price" in text or "good" in text or "invest" in text:
        stock_text = text.replace("price", "").replace("is", "").replace("good", "").replace("invest", "").strip()

        symbol = None
        display_name = stock_text.upper()

        # Try known mapping
        for name, sym in SYMBOL_MAP.items():
            if name in stock_text:
                symbol = sym
                display_name = name.upper()
                break

        # Fallback auto symbol
        if not symbol and stock_text:
            symbol = stock_text.upper().replace(" ", "") + ".NS"

        if not symbol:
            await update.message.reply_text(
                "🤖 Tell me the stock name.\nExample:\nTCS price"
            )
            return

        ticker = yf.Ticker(symbol)
        info = ticker.info

        price_raw = info.get("currentPrice")
        if not price_raw:
            await update.message.reply_text(
                "❌ I couldn’t find this stock.\nTry popular names like:\nTCS, ITC, SBIN"
            )
            return

        price = f"{price_raw:,.2f}"

        pe = info.get("trailingPE")
        pe_text = f"{pe:.1f}x" if pe else "N/A"

        rev = info.get("revenueGrowth")
        rev_text = f"{rev * 100:.1f}%" if rev else "N/A"

        # Simple AI-like view
        if pe and pe < 25:
            view = "Reasonably valued stock, suitable for long-term investors."
        elif pe and pe > 35:
            view = "Expensive valuation. Better to wait for correction."
        else:
            view = "Stable company with moderate valuation."

        await update.message.reply_text(
            f"📊 {display_name}\n\n"
            f"Price: ₹{price}\n"
            f"P/E Ratio: {pe_text}\n"
            f"Revenue Growth (YoY): {rev_text}\n\n"
            f"🧠 StockPilot View:\n{view}\n\n"
            "🔔 Want portfolio tracking & alerts?\n"
            "Type UPGRADE (Free for early users)\n\n"
            "⚠️ Not investment advice"
        )
        return

    # -------- FALLBACK (AI STYLE) --------
    await update.message.reply_text(
        "🤖 I can help you with:\n\n"
        "• Stock prices & fundamentals\n"
        "• Simple stock insights\n"
        "• Investing basics\n\n"
        "Try asking:\n"
        "TCS price\n"
        "Is ITC good?\n"
        "What is P/E ratio?"
    )


def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # ONE handler only → command-less AI
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🤖 StockPilot AI is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
