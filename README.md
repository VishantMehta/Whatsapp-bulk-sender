# WhatsApp Bulk Message Sender
<p>Comments are there in Code for more clarity</p>

This project automates the process of sending messages to multiple WhatsApp contacts using Python and Playwright. It opens WhatsApp Web, waits for the user to scan the QR code, and then sends a specified message to each contact listed in a file.

## Features
- Automatically sends a custom message to multiple WhatsApp contacts.
- Uses Playwright for browser automation.
- Easy-to-use script with phone numbers read from a `numbers.txt` file.

## Prerequisites
- Python 3.7+
- Node.js (required by Playwright)

## Installation

### 1. Clone the repository
```bash
git clone https://github.com/VishantMehta/Whatsapp-bulk-sender.git
cd whatsapp-bulk-message-sender
```
### 2. Install dependencies
Use the following command to install required dependencies:
```bash
pip install -r requirements.txt
```
Playwright also requires some browser binaries to be installed. Run this command to set them up:
```bash
playwright install
```
## Usage
1. Add the list of phone numbers (one per line) in a file named numbers.txt. Each number should include the country code (e.g., +1234567890).
2. Run the script:
```bash
python script.py
```
3. When prompted, enter the message you want to send.
4. Scan the QR code in the browser window to log in to WhatsApp Web.
5. The script will automatically send the message to each number listed in numbers.txt.

## Files
- script.py: The main script for sending bulk messages.
- numbers.txt: A file containing the phone numbers of recipients.
- requirements.txt: Dependencies required for this script.

## Dependencies
- playwright: For browser automation.

## Why Playwright rather than Selenium
- More faster , reliable than Selenium .
- Our previous version was on Selenium itself which was not very reliable.

## License
- This project is licensed under the MIT License.
