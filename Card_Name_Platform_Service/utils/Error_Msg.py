
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
    handle_error = "Handle error"
    already_exists = "The username link already exists."
    update_successful = "Username link updated successfully."
    update_failed = "Failed to update username link."

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
    get_list_card_failed = "Get list card failed"
    get_list_card_successful = "Get list card successful"

class SetPrimaryProfileMsg:
    set_primary_successful = "Set primary profile successful"
    set_primary_failed = "Set primary profile failed"

class ForgotPasswordMsg:
    email_not_found = "Email not found"
    send_email_failed = "Send reset password email failed"
    send_email_successful = "Send reset password email successful"

class ResetPasswordMsg:
    invalid_verify_code = "Invalid verification code"
    reset_password_successful = "Reset password successful"
    reset_password_failed = "Reset password failed"

class DeleteProfileMsg:
    delete_profile_successful = "Delete profile successful"
    delete_profile_failed = "Delete profile failed"
    cannot_delete_primary = "Cannot delete primary profile"
    no_permission = "No permission to delete profile"

class AccountSettingsMsg:
    get_account_setting_successful = "Get account settings successful"
    get_account_setting_failed = "Get account settings failed"
    not_found = "Account not found"
    handle_error = "Handle error"
    update_account_successful = "Update successful"
    reset_setting_successful = "Reset setting successful"
    reset_setting_failed = "Reset setting failed"
    reset_setting_invalid_phone_number = "Invalid phone number"
    reset_setting_invalid_email = "Invalid email"
    reset_setting_invalid_password = "Invalid password"
    invalid_flag = "Invalid flag for resetting settings"
    send_verify_code_successful = "Send verification code successful"
    send_verify_code_failed = "Send verification code failed"

