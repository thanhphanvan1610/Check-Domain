import telebot
import random
import sqlite3
from datetime import datetime

#Thông tin BOT
API_TOKEN = '6004381298:AAGqT8s0pCxQp7hys-webxxH2RCg1VfAc9I'
bot = telebot.TeleBot(API_TOKEN)
#Thông tin Admin
ADMIN =5324788170 #Thay 1234 thành ID của bạn
#Tạo bảng nếu chưa tồn tại
conn = sqlite3.connect('cltx.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        ID INTEGER PRIMARY KEY,
        Tien INT
    )
''')
conn.commit()
conn.close()

def xemtien(ID):
    conn = sqlite3.connect('cltx.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE ID = ?", (ID,))
    tien = cursor.fetchone()
    return tien[1]

def themtien(ID, tien):
    conn = sqlite3.connect('cltx.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE ID = ?", (ID,))
    tiencu = cursor.fetchone()
    tienmoi = tiencu[1] + tien
    cursor.execute("UPDATE users SET tien = ? WHERE ID = ?", (tienmoi, ID))
    conn.commit()
    conn.close()
    return tienmoi

def trutien(ID, tien):
    conn = sqlite3.connect('cltx.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE ID = ?", (ID,))
    tiencu = cursor.fetchone()
    tienmoi = tiencu[1] - tien
    cursor.execute("UPDATE users SET tien = ? WHERE ID = ?", (tienmoi, ID))
    conn.commit()
    conn.close()
    return tienmoi

def checkID(ID):
    conn = sqlite3.connect('cltx.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE ID = ?", (ID,))
    user = cursor.fetchone()
    if user is None:
        cursor.execute('INSERT INTO users (ID,tien) VALUES (?, 1000)', (ID,))
        conn.commit()
        text = "Bạn đã tạo tài khoản thành công và nhận được 1000 vnd !\n"
    else:
        text = f"Chào mừng ID: {ID} trở lại.\n"
    conn.close()
    return text

def testtien(ID, tien):
    db = sqlite3.connect('cltx.db')
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE ID = ?", (ID,))
    tiencu = cursor.fetchone()
    new_coin = tiencu[1] - tien
    if new_coin < 0:
        return False
    else:
        return True

def chanle():
    now = datetime.now()
    microsecond = now.microsecond
    so = random.randint(1, 1000)
    a = microsecond * 1000 + so
    return a

def gameTX(ID, nd):
    def generate_message(is_win):
        result = "thắng" if is_win else "thua"
        operation = "+" if is_win else "-"
        tiendatcuoc = int(nd[1])
        tong = themtien(ID, tiendatcuoc) if is_win else trutien(ID, tiendatcuoc)
        bet_type = "Tài" if bot_reply == 't' else "Xỉu"
        cuoc = "Tài" if nd[0] == 't' else "Xỉu"
        return f"""
Bạn đã {result} {operation}{tiendatcuoc} vnd
Bạn đặt cược [{cuoc}] với số tiền {tiendatcuoc} vnd.
Kết quả của hệ thống là [ {XS_1}-{XS_2}-{XS_3}] => {T_X} [{bet_type}]
Tổng số tiền của bạn là {tong} vnd
"""

    XS_1 = random.randint(1, 6)
    XS_2 = random.randint(1, 6)
    XS_3 = random.randint(1, 6)
    T_X = XS_1 + XS_2 + XS_3
    bot_reply = 't' if T_X >= 10 else 'x'

    tiendatcuoc = int(nd[1])
    if testtien(ID, tiendatcuoc) == False:
        return "Bạn không đủ tiền để đặt cược"
    elif (bot_reply == "t" and nd[0] == 't') or (bot_reply == "x" and nd[0] == 'x'):
        return generate_message(True)
    else:
        return generate_message(False)
   
def gameCL(ID, nd):
    def generate_message(is_win):
        result = "thắng" if is_win else "thua"
        operation = "+" if is_win else "-"
        tiendatcuoc = int(nd[1])
        tong = themtien(ID, tiendatcuoc) if is_win else trutien(ID, tiendatcuoc)
        bet_type = "CHẴN" if bot_reply == 'c' else "LẺ"
        cuoc = "CHẴN" if nd[0] == 'c' else "LẺ"
        return f"""
Bạn đã {result} {operation}{tiendatcuoc} vnd
Bạn đặt cược [{cuoc}] với số tiền {tiendatcuoc} vnd.
Kết quả của hệ thống là [ {so} [{bet_type}]
Tổng số tiền của bạn là {tong} vnd
"""

    so = chanle()
    bot_reply = 'c' if so % 2 == 0 else 'l'
    tiendatcuoc = int(nd[1])
    if testtien(ID, tiendatcuoc) == False:
        return "Bạn không đủ tiền để đặt cược"
    if (bot_reply == "c" and nd[0] == 'c') or (bot_reply == "l" and nd[0] == 'l'):
        return generate_message(True)
    else:
        return generate_message(False)
    

@bot.message_handler(commands=['start'])
def handler_start(message):
    ID = message.from_user.id
    text = checkID(ID)
    text += "Hướng dẫn sử dụng:\n"
    text += "Chọn số 1 => Chẵn Lẻ.\n"
    text += "Chọn số 2 => Tài Xỉu.\n"
    text += "Chọn số 3 => Nạp | Rút.\n"
    text += "Chọn số 4 => Kiểm Tra Tiền.\n\n"
    text += "Bạn vui lòng gửi số tương ứng:"
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['them'])
def handler_themtien(message):
    user_id = message.from_user.id
    if user_id != ADMIN:
        bot.reply_to(message, 'Bạn không phải là Admin')
        return
    command = message.text.split()
    if len(command) == 3 and command[1].isdigit() and command[2].isdigit():
        ID = int(command[1])
        tien = int(command[2])
        themtien(ID, tien)
        bot.reply_to(message, f"Đã cộng {tien} vnd cho ID {ID}")
    else:
        bot.reply_to(message, "Lệnh không hợp lệ !\n Command: /them {ID} {tien}")

@bot.message_handler(commands=['xem'])
def handler_xemtien_admin(message):
    user_id = message.from_user.id
    if user_id != ADMIN:
        bot.reply_to(message, 'Bạn không phải là Admin')
        return
    command = message.text.split()
    if len(command) == 2 and command[1].isdigit():
        ID = int(command[1])
        tien = xemtien(ID)
        bot.reply_to(message, f"{ID} đang có tổng số tiền là {tien} vnd")
    else:
        bot.reply_to(message, f"Command: /xem {ID}")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    ID = message.from_user.id
    text = getmsg(ID, message.text)
    bot.send_message(message.chat.id, text)

def getmsg(ID,message):
    nd = message.lower().split(" ")

    if nd[0] == "t" or nd[0] == "x":
        text = gameTX(ID,nd)
        return text
    
    elif nd[0] == "c" or nd[0] == "l":
        text = gameCL(ID, nd)
        return text
    elif nd[0] == "1" :
        return f"""
        [Chẵn Lẻ]
Luật chơi: Hệ thống sẽ chọn ngẫu nhiên dãy số. Bạn phải đoán xem kết quả là [Chẵn] hay [Lẻ]
Cách chơi: Nhập "C" hoặc "L" khoảng cách <số tiền cược>
Ví dụ: C 1000 (Đặt cược "Chẵn" với số tiền cược là 1000 vnd)
Nếu thắng hệ thống sẽ cộng tiền bằng với số tiền cược, ngược lại mất số tiền cược
Chúc bạn giàu to
"""
    elif nd[0] == "2" :
        return f"""
        [Tài Xỉu]
Luật chơi: Hệ thống sẽ tung 3 xúc sắc.
Tổng số 3 xúc sắc từ 4-10 => Tài | 11-17 là => Xỉu.
Bạn phải đoán xem kết quả là 'Tài' hay 'Xỉu'
Cách chơi: Nhập "T" hoặc "X" khoảng cách <số tiền cược>
Ví dụ: T 1000 (Đặt cược "Tài" với số tiền cược 1000 vnd)
Nếu thắng hệ thống sẽ cộng tiền bằng với số tiền cược, ngược lại mất số tiền cược
Chúc bạn giàu to
"""
    elif nd[0] == "3" :
        return f"""
        [Nạp/Rút]
Bạn vui lòng liên hệ Admin @ để nạp/rút
"""
    elif nd[0] == "4" :
        tien = xemtien(ID)
        return f"""
Bạn đang có {tien} vnd
"""
    else: return """
Cú pháp không hợp lệ
Đây là hướng dẫn sử dụng:
Chọn số 1 => Chẵn Lẻ.
Chọn số 2 => Tài Xỉu.
Chọn số 3 => Nạp | Rút.
Chọn số 4 => Kiểm Tra Tiền.\n
Bạn vui lòng gửi số tương ứng:
"""

if __name__ == '__main__':
    bot.infinity_polling()
