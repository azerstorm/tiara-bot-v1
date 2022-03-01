from datetime import date, datetime
import re

def sample_response(input_text):
    user_message = str(input_text).lower()

    if user_message in ("hello", "hi", "hai", "uy", "uyy", "uyyy", "woy", "zey", "sayang", "sayangku", "sayang sayang", "darling", "my darling", "beb", "bebeb", "honey"):
        return "Iya sayang, ada apa? 😊"

    if user_message in ("sehat", "sehat sayang", "sehat dong", "sehat dunds", "alhamdulillah sehat", "aman"):
        return "Alhamdulillah deh sayang 🥰"

    if user_message in ("kamu udah makan?", "kamu udah makan say?", "kamu udah makan sayang?", "udah makan belum?"):
        return "Udah dong sayang 😊"
    
    if user_message in ("anj", "pantek", "kintil"):
        return "Ih sayang jangan toxic dong 😔"
        
    if user_message in ("iya maaf", "iya maaf sayang"):
        return "Tenang sayang chill 😊"

    if user_message in ("tanggal", "tanggal berapa"):
        now = datetime.now()
        date_time = now.strftime("%d %B %Y")

        return str(date_time)
    
    return "Darling 😊"