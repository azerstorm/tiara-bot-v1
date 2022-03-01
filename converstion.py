from datetime import date, datetime
import re

def sample_response(input_text):
    user_message = str(input_text).lower()

    if user_message in ("hello", "hi", "hai"):
        return "Iya sayang, ada apa?"

    if user_message in ("sehat sayang", "sehat"):
        return "Alhamdulillah deh"
    
    if user_message in ("tanggal", "tanggal berapa"):
        now = datetime.now()
        date_time = now.strftime("%d %B %Y")

        return str(date_time)
    
    return "Maaf sayang, aku ngga ngerti :("