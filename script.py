import requests

def get_live_usdt_inr():
    """
    Fetches the live exchange rate using ExchangeRate-API open access engine.
    This works reliably without API keys and bypasses bot-blocking firewalls.
    """
    url = "https://open.er-api.com/v6/latest/USD"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        
        # Extract INR rate from the base USD response
        live_rate = float(data["rates"]["INR"])
        print(f"✅ Successfully fetched live rate: ₹{live_rate:.2f}")
        return live_rate
    except Exception as e:
        fallback_rate = 86.50
        print(f"⚠️ Could not fetch live rate. Reason: {e}")
        print(f"   Using fallback rate: ₹{fallback_rate:.2f}")
        return fallback_rate

def format_indian_currency(number):
    """Formats a number into the Indian numbering system with correct comma placement."""
    str_num = str(int(number))
    if len(str_num) <= 3:
        return str_num
    
    last_three = str_num[-3:]
    remaining = str_num[:-3]
    
    pairs = []
    while len(remaining) > 0:
        pairs.append(remaining[-2:])
        remaining = remaining[:-2]
    
    pairs.reverse()
    return ",".join(pairs) + "," + last_three

def convert_us_to_indian():
    print("=== US USDT to Indian Number System Converter ===")
    
    # 1. Prompt user for the numerical value
    try:
        user_input = input("Enter the USDT quantity (e.g., 5500000 or 5.5M as 5500000): ")
        clean_input = user_input.replace(",", "")
        us_value = float(clean_input)
    except ValueError:
        print("❌ Invalid input! Please enter a valid number without text or letters.")
        return

    # 2. Fetch live USDT to INR exchange rate
    exchange_rate = get_live_usdt_inr()

    # 3. Calculate INR value
    inr_value = us_value * exchange_rate
    
    # 4. Format numbers with Indian comma placement
    indian_comma_count = format_indian_currency(us_value)
    indian_comma_inr = format_indian_currency(inr_value)
    
    # 5. Print the formatted output
    print(f"\n--- Conversion Results ---")
    print(f"USDT Input Value: {us_value:,.2f}")
    print(f"USDT Quantity with Indian Comma System: {indian_comma_count}")
    print(f"Equivalent Value in INR (at ₹{exchange_rate:.2f}/USDT): ₹{indian_comma_inr}")
    print(f"--------------------------")
    
    # 6. Break down into words (Lakhs and Crores) using the final conversion result
    if inr_value >= 10_000_000:
        crores = inr_value / 10_000_000
        print(f"In Indian Words (INR Value): {crores:.2f} Crore")
    elif inr_value >= 100_000:
        lakhs = inr_value / 100_000
        print(f"In Indian Words (INR Value): {lakhs:.2f} Lakh")
    else:
        print(f"In Indian Words (INR Value): {inr_value:.2f} (Less than 1 Lakh)")

# Run the program
if __name__ == "__main__":
    convert_us_to_indian()
