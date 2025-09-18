import os
import struct
import threading
import time
from datetime import datetime, timezone

class ObjectIdGenerator:
    """
    Creaate ObjectId with structure:
    [4B timestamp seconds][5B random per-process][3B counter]
    - timestamp: big-endian
    - counter: 24-bit, rollover
    This structure is compatible with modern MongoDB drivers.
    """
    _lock = threading.Lock()
    _rand5 = os.urandom(5)                 # 5 bytes random fixed per process
    _counter = int.from_bytes(os.urandom(3), "big")  # 24-bit counter initialized randomly

    @classmethod
    def generate_bytes(cls) -> bytes:
        ts = int(time.time())
        with cls._lock:
            cls._counter = (cls._counter + 1) & 0xFFFFFF  # keep 24-bit
            counter_bytes = cls._counter.to_bytes(3, "big")

        ts_bytes = struct.pack(">I", ts)  # 4 byte big-endian
        return ts_bytes + cls._rand5 + counter_bytes

    @classmethod
    def generate(cls) -> str:
        """Return 24 hex string like Mongo ObjectId."""
        return cls.generate_bytes().hex()

def decode_oid_hex(oid_hex: str):
    """
    Decode OID hex (24 hex) -> dict: timestamp, random5, counter
    """
    b = bytes.fromhex(oid_hex)
    if len(b) != 12:
        raise ValueError("ObjectId must be 12 bytes (24 hex).")
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
