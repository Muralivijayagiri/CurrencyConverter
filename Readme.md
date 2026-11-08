# Currency Converter

A small, interactive Python command-line program that converts a **USDT** amount into **Indian Rupees (INR)** using a live USD-based exchange rate. It prints the result with Indian digit grouping and summarizes large values in **Lakh** or **Crore**.

The whole application lives in [`script.py`](script.py) — there are no command-line arguments, config files, or API keys. Run it, enter an amount, and it does the rest.

## What the script does

1. Prompts for a USDT quantity (commas are accepted).
2. Fetches the current USD → INR rate from [ExchangeRate-API](https://open.er-api.com/) with a 5-second timeout.
3. Converts the amount to INR (USDT is treated at par with USD).
4. Formats values using the Indian numbering system, e.g. `55,00,000` instead of `5,500,000`.
5. Prints the INR result in Crore (≥ 1 crore), Lakh (≥ 1 lakh), or as a plain value.
6. Falls back to a fixed rate of `₹86.50` if the API request fails.

## Features

- Live exchange rate with no API key required
- Accepts comma-separated input such as `5,500,000`
- Indian comma placement for both the input quantity and the INR result
- Human-readable Lakh/Crore summary
- Graceful fallback when the network or API is unavailable

## Requirements

- Python 3.10+
- [`requests`](https://pypi.org/project/requests/) (pinned in `requirements.txt`)

## Setup

```bash
git clone <repository-url>
cd CurrencyConverter
python -m venv .venv

# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
```

Or with [uv](https://docs.astral.sh/uv/):

```bash
uv venv
uv pip install -r requirements.txt
```

> A uv-created virtual environment does not include `pip`; use `uv pip` or run `python -m ensurepip` first.

## Usage

```bash
python script.py
```

```text
=== US USDT to Indian Number System Converter ===
Enter the USDT quantity (e.g., 5500000 or 5.5M as 5500000): 5500000
```

It can also be driven non-interactively by piping input:

```bash
echo 5500000 | python script.py
```

### Example output

```text
✅ Successfully fetched live rate: ₹94.11

--- Conversion Results ---
USDT Input Value: 5,500,000.00
USDT Quantity with Indian Comma System: 55,00,000
Equivalent Value in INR (at ₹94.11/USDT): ₹51,76,29,656
--------------------------
In Indian Words (INR Value): 51.76 Crore
```

The rate changes between runs. If the request fails, the script prints a warning and continues with the `₹86.50` fallback rate.

## Inside `script.py`

| Function | Responsibility |
| --- | --- |
| `convert_us_to_indian()` | Main entry point: reads input, converts the amount, and prints the report. |
| `get_live_usdt_inr()` | Calls `https://open.er-api.com/v6/latest/USD`, extracts the `INR` rate, and returns the fallback rate on any error. |
| `format_indian_currency(number)` | Groups digits using Indian conventions (last three digits, then pairs). |

The script runs `convert_us_to_indian()` only when executed directly, so it can also be imported without starting the interactive prompt.

## Notes

- The API is queried with **USD** as the base currency; USDT is assumed to trade 1:1 with USD.
- `format_indian_currency()` works on the whole-number part, so the Indian-grouped line omits decimals. The standard formatted values still show two decimal places.
- There is no test suite. Verify changes by running the script with a few values, such as `100`, `100000`, and `5500000`.

## Project structure

```text
CurrencyConverter/
├── script.py          # Application logic
├── requirements.txt   # Python dependency
└── Readme.md
```
