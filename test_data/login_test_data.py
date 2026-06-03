INVENTORY_URL_PATTERN = "inventory.html"

INVALID_CREDENTIALS_ERROR = (
    "Epic sadface: Username and password do not match any user in this service"
)
LOCKED_OUT_USER_ERROR = "Epic sadface: Sorry, this user has been locked out."
USERNAME_REQUIRED_ERROR = "Epic sadface: Username is required"
PASSWORD_REQUIRED_ERROR = "Epic sadface: Password is required"
ACCESS_DENIED_ERROR = "Epic sadface: You can only access '/inventory.html' when you are logged in."


VALID_USER_CASES = [
    {"case_id": "TC-LOGIN-001", "username": "standard_user", "password": "secret_sauce"}
]

LOCKED_OUT_USER_CASES = [
    {
        "case_id": "TC-LOGIN-007",
        "username": "locked_out_user",
        "password": "secret_sauce",
        "expected_error": LOCKED_OUT_USER_ERROR,
    }
]

INVALID_LOGIN_CASES = [
    {
        "case_id": "TC-LOGIN-002",
        "username": "invalid_user",
        "password": "secret_sauce",
        "expected_error": INVALID_CREDENTIALS_ERROR,
    },
    {
        "case_id": "TC-LOGIN-003",
        "username": "standard_user",
        "password": "invalid_password",
        "expected_error": INVALID_CREDENTIALS_ERROR,
    },
    {
        "case_id": "TC-LOGIN-008",
        "username": "invalid_user",
        "password": "invalid_sauce",
        "expected_error": INVALID_CREDENTIALS_ERROR,
    },
]

EMPTY_LOGIN_CASES = [
    {
        "case_id": "TC-LOGIN-004",
        "username": "",
        "password": "secret_sauce",
        "expected_error": USERNAME_REQUIRED_ERROR,
    },
    {
        "case_id": "TC-LOGIN-005",
        "username": "standard_user",
        "password": "",
        "expected_error": PASSWORD_REQUIRED_ERROR,
    },
    {
        "case_id": "TC-LOGIN-006",
        "username": "",
        "password": "",
        "expected_error": USERNAME_REQUIRED_ERROR,
    },
]
