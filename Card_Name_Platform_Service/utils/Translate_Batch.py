import requests
import base64

# Tạo separator đảm bảo Google không dịch
SEPARATOR = "__SEP_b64_9f86d081884c7d659a2feaa0c55ad015__"

def translate_batch(texts: list[str], source_language: str="auto", target_language: str="en"):
    # Ghép chuỗi bằng separator an toàn
    q = SEPARATOR.join(texts)

    url = "https://translate.googleapis.com/translate_a/single"
    params = {
        "client": "gtx",
        "sl": source_language,
        "tl": target_language,
        "dt": "t",
        "q": q
    }

    r = requests.get(url, params=params)
    data = r.json()[0]

    # Ghép full câu từ Google (nó trả theo block fragment)
    translated_full = "".join(block[0] for block in data)

    # Split theo separator (Google sẽ giữ nguyên separator)
    parts = translated_full.split(SEPARATOR)

    # Trim
    return [p.strip() for p in parts]
