import os
import struct
import threading
import time
from datetime import datetime, timezone

class ObjectIdGenerator:
    """
    Tạo ObjectId theo cấu trúc:
    [4B timestamp seconds][5B random per-process][3B counter]
    - timestamp: big-endian
    - counter: 24-bit, quay vòng
    Cấu trúc này tương thích định dạng với MongoDB drivers hiện đại.
    """
    _lock = threading.Lock()
    _rand5 = os.urandom(5)                 # 5 byte ngẫu nhiên cố định cho mỗi process
    _counter = int.from_bytes(os.urandom(3), "big")  # 24-bit counter khởi tạo ngẫu nhiên

    @classmethod
    def generate_bytes(cls) -> bytes:
        ts = int(time.time())
        with cls._lock:
            cls._counter = (cls._counter + 1) & 0xFFFFFF  # giữ 24-bit
            counter_bytes = cls._counter.to_bytes(3, "big")

        ts_bytes = struct.pack(">I", ts)  # 4 byte big-endian
        return ts_bytes + cls._rand5 + counter_bytes

    @classmethod
    def generate(cls) -> str:
        """Trả về 24 ký tự hex (chuỗi) giống Mongo ObjectId."""
        return cls.generate_bytes().hex()

def decode_oid_hex(oid_hex: str):
    """
    Giải mã OID hex (24 hex) -> dict: timestamp, random5, counter
    """
    b = bytes.fromhex(oid_hex)
    if len(b) != 12:
        raise ValueError("ObjectId phải dài 12 byte (24 hex).")
    ts = struct.unpack(">I", b[0:4])[0]
    rand5 = b[4:9]
    counter = int.from_bytes(b[9:12], "big")
    return {
        "timestamp": ts,
        "datetime_utc": datetime.fromtimestamp(ts, tz=timezone.utc),
        "random5_hex": rand5.hex(),
        "counter": counter,
    }

# if __name__ == "__main__":
#     for _ in range(3):
#         oid = ObjectIdGenerator.generate()
#         print(oid, decode_oid_hex(oid))
#     print("68b1241c91b161bf70c9cf35", decode_oid_hex("68b1241c91b161bf70c9cf35"))
