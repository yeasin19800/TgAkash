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
pip install python-telegram-bot requests beautifulsoup4
        response.raise_for_status() # HTTP ত্রুটির জন্য ব্যতিক্রম তৈরি করুন (যেমন 404, 500)

        soup = BeautifulSoup(response.text, 'html.parser')

        # --- কৌশল 1: <script> ট্যাগের মধ্যে JSON ডেটা (window.share_data) খোঁজা ---
        # TeraBox প্রায়শই ভিডিও লিঙ্ক একটি JavaScript ভেরিয়েবলের মধ্যে JSON হিসাবে রাখে।
        for script in soup.find_all('script'):
            if script.string and 'window.share_data' in script.string:
                try:
                    # 'var share_data = { ... };' প্যাটার্ন থেকে JSON স্ট্রিং এক্সট্র্যাক্ট করুন
                    json_match = re.search(r'var\s+share_data\s*=\s*(\{.*?});', script.string, re.DOTALL)
                    if json_match:
                        share_data_str = json_match.group(1)
                        data = json.loads(share_data_str)

                        # JSON কাঠামোর উপর নির্ভর করে ভিডিও লিঙ্ক খুঁজে বের করুন
                        # এটি প্রায়শই 'list' অ্যারের প্রথম আইটেমের 'dlink' বা 'play_url' এর মধ্যে থাকে।
                        if 'list' in data and data['list']:
                            first_item = data['list'][0]
                            if 'dlink' in first_item:
                                return first_item['dlink']
                            elif 'play_url' in first_item:
                                return first_item['play_url']

                except json.JSONDecodeError as e:
                    logger.warning(f"JSON পার্সিং ত্রুটি: {e}")
                except KeyError as e:
                    logger.warning(f"JSON ডেটাতে অনুপস্থিত কী: {e}")
                except Exception as e:
                    logger.warning(f"JSON ডেটা প্রসেস করার সময় অনাকাঙ্ক্ষিত ত্রুটি: {e}")

        # --- কৌশল 2: <script> ট্যাগের মধ্যে সরাসরি 'play_url' বা 'video_url' খোঁজা ---
        # যদি JSON পদ্ধতি কাজ না করে, তবে সরাসরি URL প্যাটার্ন খোঁজা।
        for script in soup.find_all('script'):
            if script.string:
                # উদাহরণ: var play_url = "https://example.com/video.mp4";
                # বিভিন্ন ভিডিও এক্সটেনশন (.mp4, .m3u8, .avi, ইত্যাদি) সমর্থন করে।
                match_play_url = re.search(
                    r'var\s+(?:play_url|video_url)\s*=\s*\"(https?://[\w./-]+?\.(?:mp4|m3u8|avi|mov|mkv)(?:(?:\?|&)[^"]*)?)\"', 
                    script.string
                )
                if match_play_url:
                    # &amp; কে & এ পরিবর্তন করুন যদি থাকে
                    return match_play_url.group(1).replace('&amp;', '&')

        # --- কৌশল 3: og:video মেটা ট্যাগ খোঁজা (সাধারণত সামাজিক শেয়ারের জন্য ব্যবহৃত) ---
        # এটি সরাসরি ডাউনলোড লিঙ্ক নাও হতে পারে, তবে একটি প্লেয়েবল লিঙ্ক হতে পারে।
        og_video_tag = soup.find('meta', property='og:video')
        if og_video_tag and og_video_tag.get('content'):
            return og_video_tag['content']

        logger.info(f"কোনো সরাসরি লিঙ্ক পাওয়া যায়নি: {terabox_url}")
        return None # কোনো লিঙ্ক না পেলে

    except requests.exceptions.RequestException as e:
        logger.error(f"রিকোয়েস্ট ত্রুটি: {terabox_url}: {e}")
        return None
    except Exception as e:
        logger.error(f"পার্সিং করার সময় অনাকাঙ্ক্ষিত ত্রুটি: {terabox_url}: {e}")
        return None
# মেসেজ হ্যান্ডলার
async def handle_message(update: Update, context):
    """ব্যবহারকারীর পাঠানো মেসেজ গ্রহণ করে এবং TeraBox লিঙ্ক প্রসেস করে।"""
    text = update.message.text

    # TeraBox এবং এর সহযোগী ডোমেইনগুলির জন্য রেগুলার এক্সপ্রেশন
    # এটি terabox.com, nephobox.com, 4funbox.com, ইত্যাদি ডোমেইনগুলিকে শনাক্ত করবে।
