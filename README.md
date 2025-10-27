# Discord Server Messenger

A modern Discord webhook message sender for automating notifications and announcements on your Discord server.

## Features

- **Modern UI**: Clean, Discord-themed interface with dark mode styling
- **Real-time Statistics**: Track sent messages, failures, and success rates
- **Custom Messages**: Send personalized messages to your server
- **Multi-threading**: Send messages using multiple threads for efficiency
- **Stop/Start Controls**: Full control over message sending with start and stop buttons
- **Activity Log**: Detailed timestamped log with color-coded status messages
- **Input Validation**: Comprehensive validation to prevent errors
- **Webhook Verification**: Automatically checks if URLs are valid Discord webhooks

## Requirements

- Python 3.6 or higher
- Required packages:
  - tkinter (usually comes with Python)
  - requests

## Installation

1. Clone or download this repository
2. Install required packages:
   ```bash
   pip install requests
   ```

## Usage

1. Run the application:
   ```bash
   python main.py
   ```

2. Enter your Discord webhook URL
3. Customize your message
4. Configure settings:
   - **Threads**: Number of concurrent sending threads (1-10)
   - **Messages per thread**: How many messages each thread should send (1-1000)
   - **Delay**: Time in seconds between messages

5. Click "Start Sending" to begin

## Configuration

- **Webhook URL**: Your Discord server webhook URL (get this from Server Settings > Integrations > Webhooks)
- **Custom Message**: The message text to send
- **Threads**: Number of parallel threads (recommended: 1-2 for regular use)
- **Messages per thread**: Total messages each thread will send
- **Delay**: Time delay between messages in seconds (recommended: 2+ seconds)

## Use Cases

- Automated server announcements
- Scheduled notifications
- Warning broadcasts to moderators
- Bulk message testing for your own webhooks
- Server status updates

## Notes

- This tool is intended for use on your own Discord servers where you have proper authorization
- Respect Discord's rate limits and terms of service
- Recommended to use delays of 2+ seconds between messages
- Limited to 10 threads maximum to prevent abuse

## Version

**v2.0** - Complete UI overhaul with modern design and enhanced features

## License

This project is provided as-is for educational and personal server management purposes.
