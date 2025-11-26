from .models import CURRENCY_SYMBOLS

def user_currency(request):
    if request.user.is_authenticated and hasattr(request.user, "profile"):
        code = request.user.profile.currency
        symbol = request.user.profile.currency_symbol
    else:
        code = "PLN"
        symbol = CURRENCY_SYMBOLS.get("PLN", "zł")

    return {
        "USER_CURRENCY": code,
        "USER_CURRENCY_SYMBOL": symbol,
    }
