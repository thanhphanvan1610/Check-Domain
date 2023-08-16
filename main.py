import telebot
import hashlib
import speedtest
import requests




API_TOKEN = '6234199632:AAF103EWI-fbOVv1Ar9BnUmo9JpSzYyNRsI'
bot = telebot.TeleBot(API_TOKEN)




def Info(message):
    usr = message.from_user.username
    chatid = message.chat.id
    id = message.from_user.id
    return usr, id, chatid


def get_public_ip():
    try:
        response = requests.get('https://api.ipify.org?format=json')
        data = response.json()
        public_ip = data['ip']
        return public_ip
    except Exception as e:
        return str(e)





@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message, "OpenSwift Hash được vận hành và phát triển bởi OpenSwift")


@bot.message_handler(commands=['info'])
def info(message):
    usr, id, chatid = Info(message)
    bot.send_message(message.chat.id, text="*User: *{}\n *ID: *`{}`\n *ChatID: *`{}` ".format(usr, id, chatid
), parse_mode='markdown')
    

@bot.message_handler(commands=['hash'])
def hash(message):
    try:
        _, content = message.text.split(" ")
        if len(content) > 1:
            string = " ".join(content[1:])
            md5_hash = hashlib.md5(string.encode()).hexdigest()
            bot.send_message(message.chat.id, text="'_{}_' sau khi mã hóa: `{}`".format(string, md5_hash), parse_mode = 'markdown')
        else:
            bot.send_message(message,"Vui lòng cung cấp chuỗi để mã hóa")
    except ValueError:
        bot.reply_to(message, "Sử dụng /hash [văn bản mã hóa] để mã hóa thông tin.")


@bot.message_handler(commands=['speed'])
def get_network_speed(message):
   bot.reply_to(message, "Đang tiến hành kiểm tra tốc độ mạng! Vui lòng chờ")
   st = speedtest.Speedtest()
   st.get_best_server()
   download_speed = st.download() / (1024 * 1024)  # Chuyển đổi từ bytes/s sang Mbps
   upload_speed = st.upload() / (1024 * 1024)  # Chuyển đổi từ bytes/s sang Mbps
   ping = st.results.ping
   bot.send_message(message.chat.id, f"Tốc độ tải xuống: {download_speed:.2f} Mb/s" )
   bot.send_message(message.chat.id, f"Tốc độ tải lên: {upload_speed:.2f} Mb/s" )
   bot.send_message(message.chat.id, f"Ping: {ping:.1f} ms" )


@bot.message_handler(commands=['ip'])
def ip(message):
    public_ip = get_public_ip()
    bot.reply_to(message, "*IP:* `{}`".format(public_ip), parse_mode="markdown")


@bot.message_handler(func=lambda message: True)
def Err(message):
    bot.reply_to(message,"Tôi không hiểu bạn nói gì")




print("successfull !!")
bot.infinity_polling()
