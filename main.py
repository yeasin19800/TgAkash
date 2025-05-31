# main.py

import logging
import re
import json  # JSON ডেটা পার্স করার জন্য
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
import requests
from bs4 import BeautifulSoup

# BotFather থেকে প্রাপ্ত আপনার API Token এখানে বসান
# এটিকে আপনার গোপন রাখা উচিত!
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE" 

# লগিং সেটআপ: বটের কার্যকলাপ এবং ত্রুটিগুলো দেখতে সাহায্য করবে
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)
# /start কমান্ড হ্যান্ডলার
async def start(update: Update, context):
    """বট চালু হলে /start কমান্ডের প্রতিক্রিয়া জানায়।"""
    await update.message.reply_text("নমস্কার! আমাকে একটি TeraBox লিঙ্ক পাঠান, আমি চেষ্টা করব এটিকে সরাসরি ভিডিও লিঙ্কে রূপান্তর করতে।")
# TeraBox লিঙ্ক পার্স করার ফাংশন
def get_terabox_direct_link(terabox_url):
    """
    TeraBox শেয়ার লিঙ্ক থেকে সরাসরি ভিডিও লিঙ্ক বের করার চেষ্টা করে।
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
    }

    try:
        # TeraBox পেজ রিকোয়েস্ট করুন
        # allow_redirects=True যাতে রিডাইরেক্ট ফলো করে
        # timeout=15 যাতে রিকোয়েস্ট খুব বেশি সময় না নেয়
        response = requests.get(terabox_url, headers=headers, allow_redirects=True, timeout=15)
      # মূল ফাংশন
def main():
    """বট সেটআপ করে এবং পোলিং শুরু করে।"""
    # Application তৈরি করুন এবং আপনার বটের টোকেন দিন।
    application = Application.builder().token(BOT_TOKEN).build()

    # কমান্ড হ্যান্ডলার যোগ করুন
    application.add_handler(CommandHandler("start", start))

    # মেসেজ হ্যান্ডলার যোগ করুন (সব টেক্সট মেসেজের জন্য যা কমান্ড নয়)
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # বট শুরু করুন এবং নতুন আপডেটগুলি শুনতে থাকুন
    logger.info("বট চালু হচ্ছে...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)
    logger.info("বট বন্ধ হচ্ছে।")

# যখন স্ক্রিপ্টটি সরাসরি চালানো হয়, তখন main() ফাংশনটি কল করুন
if __name__ == '__main__':
    main()
