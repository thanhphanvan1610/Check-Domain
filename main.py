import requests
import telebot
import tldextract
from telebot import types
import concurrent.futures 
import gzip
import io

TELEGRAM_BOT_TOKEN = '6422001885:AAFP214_o7BKyJBnLT7ISmRZdGjfdMMNtxM'
ADMIN_USER = 5324788170
GODADDY_API_KEY = 'gHpjQ9t97Cbi_XXxwTvgiqrw4TJTUYXNbFZ'
GODADDY_API_SECRET = 'BoptKd8BnZ9hDiZmQjwEJt'
user_language = 'en'  # Set default language


bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

language_texts = {
    'en': {
        'start': "This is a bot that checks domain availability. Send any domain for a lookup!",
        'help': "Available commands:\n/start - Start the bot\n/help - Display this help message",
        'invalid_domain': "Please enter a valid domain name.",
        'available': "{} is available! Register now! 🦤",
        'unavailable': "{} registered.",
        'unknown_response': "Unknown response format from GoDaddy API.",
        'request_error': "This type of LTD is not supported",
        'http_error': "HTTP error occurred: {}",
        'connection_error': "Connection error occurred: {}",
        'value_error': "Value error occurred: {}",
        'generic_error': "An error occurred: {}",
        'err': 'An error has occurred',
        'no_valid_domains': "No valid domain names found. Please enter at least one valid domain.",
        'unauth': "You don't have permission",
        'restart': "Bot is restarting"
    },
    'vi': {
        'start': "Đây là bot kiểm tra tính khả dụng của tên miền. Gửi một tên miền để tra cứu!",
        'help': "Các lệnh có sẵn:\n/start - Bắt đầu bot\n/help - Hiển thị thông điệp trợ giúp này",
        'invalid_domain': "Vui lòng nhập tên miền hợp lệ.",
        'available': "{} Khả dụng! Hãy đăng kí ngay🦤",
        'unavailable': "{} Đã được Đăng kí.",
        'unknown_response': "Định dạng phản hồi từ API GoDaddy không rõ ràng.",
        'request_error': "Không hỗ trợ đăng kí tên Miền có định dạng này",
        'http_error': "Đã xảy ra lỗi HTTP: {}",
        'err': 'Đã có lỗi xảy ra',
        'connection_error': "Đã xảy ra lỗi kết nối: {}",
        'value_error': "Đã xảy ra lỗi giá trị: {}",
        'generic_error': "Đã xảy ra lỗi: {}",
        'no_valid_domains': "Không tìm thấy tên miền hợp lệ. Vui lòng nhập ít nhất một tên miền hợp lệ.",
        'unauth': "Bạn không có quyền truy cập",
        'restart': "Bot đang được khởi động"
    }
}



      
def is_valid_domain(domain_name):
    ext = tldextract.extract(domain_name)
    return ext.domain and ext.suffix

def check_domain_status(domain_name, user_language):
    if not is_valid_domain(domain_name):
        return language_texts[user_language]['invalid_domain']

    url = f'https://api.godaddy.com/v1/domains/available?domain={domain_name}'
    headers = {
        'Authorization': f'sso-key {GODADDY_API_KEY}:{GODADDY_API_SECRET}'
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()

        if 'available' in data:
            available = data['available']
            if available:
                return language_texts[user_language]['available'].format(domain_name)
            else:
                return language_texts[user_language]['unavailable'].format(domain_name)
        else:
            return language_texts[user_language]['unknown_response']

    except requests.exceptions.RequestException as req_exc:
        return language_texts[user_language]['request_error'].format(req_exc)
    except requests.exceptions.HTTPError as http_err:
        return language_texts[user_language]['http_error'].format(http_err)
    except requests.exceptions.ConnectionError as conn_err:
        return language_texts[user_language]['connection_error'].format(conn_err)
    except ValueError as val_err:
        return language_texts[user_language]['value_error'].format(val_err)
    except Exception as e:
        return language_texts[user_language]['generic_error'].format(e)

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    item_en = types.InlineKeyboardButton('English', callback_data='en')
    item_vi = types.InlineKeyboardButton('Tiếng Việt', callback_data='vi')
    markup.add(item_en, item_vi)
    global user_language
    user_language = 'en'  # Reset to default language
    bot.reply_to(message, language_texts[user_language]['start'], reply_markup=markup)

@bot.message_handler(commands=['help'])
def help(message):
    bot.reply_to(message, language_texts[user_language]['help'])



@bot.callback_query_handler(func=lambda call: True)
def language_callback(call):
    global user_language
    user_language = call.data
    bot.send_message(call.message.chat.id, language_texts[user_language]['start'])


@bot.message_handler(func=lambda message: True)
def handle_multiple_domain_lookup(message):
    try:
        domain_names = message.text.strip().split()  # Split message by whitespace
        valid_domains = [domain for domain in domain_names if is_valid_domain(domain)]
        
        if not valid_domains:
            bot.send_message(message.chat.id, language_texts[user_language]['no_valid_domains'])
        else:
            results = []
            with concurrent.futures.ThreadPoolExecutor() as executor:  # Use ThreadPoolExecutor for concurrent domain checks
                futures = [executor.submit(check_domain_status, domain_name, user_language) for domain_name in valid_domains]
                for future in concurrent.futures.as_completed(futures):
                    result = future.result()
                    results.append(result)
            bot.send_message(message.chat.id, "\n".join(results))
    except Exception as e:
        bot.send_message(message.chat.id, language_texts[user_language]['generic_error'].format(e))
  


print("Bot starting!!")
bot.polling()
