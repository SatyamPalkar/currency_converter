def format_conversion_text(rate, inverse_rate, amount, currency_from, currency_to, date=None):
    if date:
        date_str = date.strftime("%Y-%m-%d")
        return (
            f"The conversion rate on {date_str} from {currency_from} to {currency_to} was {rate}. "
            f"So {amount} in {currency_from} correspond to {amount * rate} in {currency_to}. "
            f"The inverse rate was {inverse_rate}."
        )
    else:
        return (
            f"The conversion rate from {currency_from} to {currency_to} is {rate}. "
            f"So {amount} in {currency_from} correspond to {amount * rate} in {currency_to}. "
            f"The inverse rate is {inverse_rate}."
        )
