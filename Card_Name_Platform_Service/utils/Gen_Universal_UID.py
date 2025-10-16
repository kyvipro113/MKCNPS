import uuid
import datetime
import string
import random

def genUniversalUID(num_character=6):
    '''Default use Universal UID version 4.0'''
    # universalUID = uuid.uuid4().hex[:num_character]
    # return universalUID

    while True:
        uid = uuid.uuid4().hex[:num_character]
        # Đếm số ký tự là chữ cái (a-f)
        num_letters = sum(1 for c in uid if c in string.ascii_letters)
        if num_letters >= 2:
            return uid

def genUIDHex():
    return uuid.uuid4().hex

def genUserUID(num_character=12):
    time_gen = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    _uuid = uuid.uuid4().hex[:num_character]
    uidUser = _uuid + time_gen
    return uidUser

def genUserUIDNoTime(num_character=12):
    _uuid = uuid.uuid4().hex[:num_character]
    return _uuid

def genUidWithTime(num_character=8):
    time_gen = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    _uuid = uuid.uuid4().hex[:num_character]
    return (_uuid + time_gen)

def genUniversalUID_PIN(num_character=6):
    '''Generate UID with at least 2 letters (a-f) from UUID4 hex'''
    while True:
        uid = uuid.uuid4().hex[:num_character]
        # Đếm số ký tự là chữ cái (a-f)
        num_letters = sum(1 for c in uid if c in string.ascii_letters)
        if num_letters >= 2:
            return uid
        
def genOTP(num_character=6):
    uuid_hex = uuid.uuid4().hex
    uuid_dec = int(uuid_hex, 16)
    otp = str(uuid_dec)[0:num_character]
    return otp

def genOTP_rnd():
    return str(random.randint(100000, 999999))