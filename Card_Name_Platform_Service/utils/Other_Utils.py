
def mask_phone(phone: str)->str:
    mask = phone[:4] + "******" + phone[-2:]
    return mask

def get_bucket_object_from_url(url: str, get_location=False)->tuple[str, str]:
    parts = url.split("?X-Amz-Algorithm=")
    path = parts[0].split("/")
    if get_location:
        return path[-2] + "/" + path[-1]
    return path[-2], path[-1]
