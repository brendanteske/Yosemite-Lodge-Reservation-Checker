# Yosemite Lodging Snagger 🌲

A Python-based automation tool designed to monitor Yosemite National Park reservation availability in real-time. This script uses Selenium to navigate the booking engine, bypasses UI obstructions, and pings your Discord server the moment a room is found.

## Features

- **Automated Search**: Continuously loops through availability checks based on your preferred interval.
- **Discord Integration**: Sends a notification to your Discord server via Webhooks with the specific check-in date.
- **Visible Takeover**: Runs in visible mode, allowing you to manually finalize the payment and booking once a room is located.
- **Deep Configuration**: Manage guest counts, lodge types, dates, and even website element IDs through a single JSON file.
- **Stealth UI Handling**: Uses JavaScript injection to set dropdown values and handles stubborn datepicker overlays automatically.

## Prerequisites

- **Python 3.x**
- **Google Chrome**
- **ChromeDriver** (Matched to your Chrome version)
- Python Libraries:
  ```bash
  pip install selenium requests
Configuration
The script is entirely driven by config.json. Ensure this file is in the same directory as the script.

discord_settings
webhook_url: Your unique Discord Webhook URL.

check_interval_minutes: How long to wait between checks (recommended: 5).

search_settings
checkin_date / checkout_date: Dates in MM/DD/YYYY format.

lodging_type: Use codes like _ALLPROPS_ (All), D (Curry Village), M (Ahwahnee), etc.

rooms / adults / children: Guest and room counts (1–9).

website_locators
Internal IDs used by the script to find elements on the page. Do not change these unless the website updates its code.

Usage
Update config.json with your desired dates and guest counts.

Run the script:

Bash
python snag_yosemite_reservation.py
Minimize the window: Use a third-party tool or simply move the window out of view. The script will close the window and restart it automatically every loop unless a reservation is found.

⚠️ Security Note
Never commit your config.json to a public repository if it contains your live Discord Webhook URL. Use a placeholder in your public version and keep your local credentials in a .gitignore file.

Happy Camping!
