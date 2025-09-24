
class AuthMsg:
    successful = "Successful"
    unauthorized = "Unauthorized"
    forbidden = "Forbidden"
    invalid_refresh_token = "Invalid refresh token"
    token_invalid = "Token is invalid or has expired"
    token_can_not_decode = "Token can not decode"

class  RegisterMsg:
    successful = "Register successful"
    failed = "Register failed"
    email_exist = "Email already exists"
    handle_error = "Handle error"
    verify_code_invalid = "Verify code is invalid or expired"

class LoginMsg:
    successful = "Login successful"
    failed = "Login failed"
    user_not_found = "Invalid email/phone number or password"
    cms_not_found = "Invalid username or password cms"
    handle_error = "Handle error"

class MinIOMsg:
    failed = "Get presigned url failed"
    successful = "Get presigned url successful"
