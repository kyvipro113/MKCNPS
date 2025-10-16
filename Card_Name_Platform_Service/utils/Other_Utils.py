
def mask_phone(phone: str)->str:
    mask = phone[:4] + "******" + phone[-2:]
    return mask