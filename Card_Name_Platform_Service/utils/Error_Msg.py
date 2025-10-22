
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

class ProfileMsg:
    build_successful = "Build profile successful"
    build_failed = "Build profile failed"
    update_successful = "Update profile successful"
    get_successful = "Get profile successful"
    get_failed = "Get profile failed"
    failed = "Handle profile failed"
    not_found = "Profile not found"
    get_list_profile_successful = "Get list profile successful"
    get_list_profile_failed = "Get list profile failed"
    profile_list_empty = "Profile list is empty"
    create_new_profile_successful = "Create new profile successful"
    create_new_profile_failed = "Create new profile failed"
    edit_profile_successful = "Edit profile successful"
    edit_profile_failed = "Edit profile failed"

class UsernameLinkMsg:
    is_exists = "Username link is already taken"
    is_found = "OK"
    not_found = "Username link not found"

class CardMsg:
    is_found = "OK"
    not_found = "Card not found"
    is_linked = "Card is already linked to a profile"
    is_unlinked = "Card is already unlinked"
    no_linked_profile = "No linked profile found for this card"
    link_successful = "Link profile to card successful"
    link_failed = "Link profile to card failed"
    unlink_successful = "Unlink profile from card successful"
    unlink_failed = "Unlink profile from card failed"