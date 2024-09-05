import telebot
import requests
import threading

TOKEN = '7224364066:AAHJW6j0mLKGfrWOI4jeC11aJFwv97SeOpM'
bot = telebot.TeleBot(TOKEN)

ALLOWED_USERS = [6204580535, 7306675136, 6162561053, 6783750964, 7321197230]

def is_user_allowed(user_id):
    return user_id in ALLOWED_USERS

@bot.message_handler(commands=['start'])
def send_phone(message):
    if not is_user_allowed(message.from_user.id):
        #bot.reply_to(message, "انت غير مشترك في هذا البوت يرجى تحدث مع المطور من اجل الاشتراك @ZO_RO_40 والرجاء الانضمام هنا للحصول على كل شي جديد https://t.me/bdjdidksjdbdn.")
        return

    bot.reply_to(message, "بوت 𝗡𝗔𝗦𝗥𝗢 𝗔𝗟𝗘𝗫 يرحب بك في اي وقت يرجى الانضمام هنا https://t.me/YOONESXYOOZ وايضا اشترك هنا فضلا وليس امرا https://t.me/YOONESYOOZ ")
    bot.send_message(message.chat.id, "مرحبا بك!  أرسل رقمك للتحقق, و لا تنسى الدعاء لأخوتنا في فلسطين 🇵🇸 ")
    bot.register_next_step_handler(message, send_verification_code)

def send_verification_code(message):
    phone_number = message.text
    url = "https://ibiza.ooredoo.dz/auth/realms/ibiza/protocol/openid-connect/token"
    payload = {
        "client_id": "ibiza-app",
        "grant_type": "password",
        "mobile-number": phone_number,
        "language": "AR"
    }
    headers = {
        "User-Agent": "okhttp/4.9.3",
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    try:
        response = requests.post(url, data=payload, headers=headers)
        if "ROOGY" in response.text:
            bot.send_message(message.chat.id, "حط الرمز لي وصلك وستغفر في طريق 💬✅")
            bot.register_next_step_handler(message, verify_code, phone_number)
        else:
            bot.send_message(message.chat.id, "هناك خطأ ما اعد التشغيل بعد قليل ")
    except Exception as e:
        bot.send_message(message.chat.id, f"حدث خطأ في إرسال رمز التحقق: {e}")

def verify_code(message, phone_number):
    otp_code = message.text
    url = "https://ibiza.ooredoo.dz/auth/realms/ibiza/protocol/openid-connect/token"
    payload = {
        "client_id": "ibiza-app",
        "grant_type": "password",
        "mobile-number": phone_number,
        "language": "AR",
        "otp": otp_code
    }
    headers = {
        "User-Agent": "okhttp/4.9.3",
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    try:
        response = requests.post(url, data=payload, headers=headers)
        response_json = response.json()
        if "access_token" in response_json:
            bot.send_message(message.chat.id, "تم التحقق من الرمز... سيتم ارسال الانترنت بعد كل 20 دقيقة بشكل تلقائي 🌹")
            access_token = response_json["access_token"]
            # إرسال الطلبات 6 مرات عند التحقق
            send_requests_six_times(message, access_token)
            # بدء عملية التكرار كل 20 دقيقة
            threading.Timer(20 * 60, repeat_requests, args=[message, access_token]).start()
        else:
            bot.send_message(message.chat.id, "هناك خطأ ما اثناء الارسال 💔")
    except Exception as e:
        bot.send_message(message.chat.id, f"حدث خطأ في التحقق من الرمز: {e}")

def send_requests_six_times(message, access_token):
    # إرسال 6 طلبات مع فواصل زمنية قصيرة
    for i in range(6):
        threading.Timer(i * 2, send_final_request, args=[message, access_token]).start()

def send_final_request(message, access_token):
    url = 'https://ibiza.ooredoo.dz/api/v1/mobile-bff/users/mgm/info/apply'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'language': 'AR',
        'request-id': 'ed66ca07-7aee-4b97-952c-f0fcbc7eee0f',
        'flavour-type': 'gms',
        'Content-Type': 'application/json; charset=utf-8',
        'Host': 'ibiza.ooredoo.dz',
        'Connection': 'Keep-Alive',
        'User-Agent': 'okhttp/4.9.3',
    }
    data = '{"skipMgm":false,"mgmValue":"5.5GB"}'

    try:
        response = requests.post(url, headers=headers, data=data)
        bot.send_message(message.chat.id, "استغفر الله... سيتم إرسال لك انترنت  ")
        balance = check_balance(access_token)
        if balance is not None:
            bot.send_message(message.chat.id, f"رصيد الانترنت الحالي هو: {balance}")
        else:
            bot.send_message(message.chat.id, "لم يتم استرجاع الرصيد.")
    except Exception as e:
        bot.send_message(message.chat.id, f"حدث خطأ في إرسال الطلب النهائي: {e}")

def check_balance(access_token):
    url = "https://ibiza.ooredoo.dz/api/v1/mobile-bff/users/balance"
    
    headers = {
        'Authorization': f'Bearer {access_token}',
        'User-Agent': "okhttp/4.9.3",
        'Connection': "Keep-Alive",
        'Accept-Encoding': "gzip",
        'language': "AR",
        'request-id': "995fd8a7-853c-481d-b9c6-0a24295df76a",
        'flavour-type': "gms"
    }

    try:
        response = requests.get(url, headers=headers)
        response_json = response.json()
        accounts = response_json.get('accounts', [])

        for account in accounts:
            if account.get('label') == 'رصيد التكفل المهدى':
                return account.get('value', None)
    except Exception as e:
        bot.send_message(message.chat.id, f"حدث خطأ في التحقق من الرصيد: {e}")

    return None

# تكرار الطلبات كل 20 دقيقة
def repeat_requests(message, access_token):
    send_final_request(message, access_token)
    threading.Timer(20 * 60, repeat_requests, args=[message, access_token]).start()

# تشغيل البوت
bot.polling(none_stop=True)