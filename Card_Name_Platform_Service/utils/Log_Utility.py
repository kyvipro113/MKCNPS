# from functools import wraps
# from Card_Name_Platform_Service.logger.Logger import *

# def trace_log(ip: str):
#     def decorator(func):
#         @wraps(func)
#         async def wrapper(*args, **kwargs):
#             logger = Logger(folder_name="Log", file_name=ip, name_logger=ip, file_mode="a")
#             try:
#                 result = await func(*args, **kwargs)
#             except Exception as e:
#                 await logger.trace(f"Exception in {func.__name__}: {str(e)}")

                     
