from datetime import datetime
import re


def sample_response(input_text):
    user_message = str(input_text).lower()

    badWordList = ["anj", "tai", "anjing", "pantek", "bangsat"]

    for word in badWordList:
        if re.findall(word, user_message):
            return "Sayang, jangan dibiasain toxic 😠"

    if user_message in ("hello", "hi", "hai", "uy", "uyy", "uyyy", "woy", "zey", "sayang", "sayangku", "sayang sayang", "darling", "my darling", "beb", "bebeb", "honey"):
        return "Iya sayang, ada apa? 😊"

    if user_message in ("sehat", "sehat sayang", "sehat dong", "sehat dunds", "alhamdulillah sehat", "aman"):
        return "Alhamdulillah deh sayang 🥰"

    if user_message in ("kamu udah makan?", "kamu udah makan say?", "kamu udah makan sayang?", "udah makan belum?"):
        return "Udah dong sayang 😊"
    
    if user_message in ("iya maaf", "iya maaf sayang", "eh iya maaf sayang"):
        return "Chill sayang chill 🤗"

    if user_message in ("kamu dimana?", "kamu dimana sayang?"):
        return "Aku udah di rumah, kamu masih di tempat kerja?"

    if user_message in ("masih sayang"):
        return "Hari ini mendung kan? kamu mau aku jemput ngga? kan lumayan deket dari rumah"

    if user_message in ("jalan kaki deket", "jalan kaki deket kok hehe"):
        return "Ishh kan sekalian ke shelter nanti sayy"
    
    if user_message in ("nanti aku pulangnya kemaleman sayang"):
        return "Makanya kan nanti aku anter pulang 🤭"

    if user_message in ("kamu kenapa deh say?"):
        return "Pengen ngobrol langsung lahh, kalau lewat chat kan bosen sayanggg"

    if user_message in ("tanggal", "tanggal berapa"):
        now = datetime.now()
        date_time = now.strftime("%d %B %Y")
        return str(date_time)
    
    return "Darling 😊"