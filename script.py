import asyncio
from playwright.async_api import async_playwright

async def send_bulk_messages(numbers, message):
    async with async_playwright() as p:
        # Launch the browser
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        # Go to WhatsApp Web
        await page.goto("https://web.whatsapp.com")

        # Wait for user to scan the QR code
        print("Please scan the QR code to log in.")
        await page.wait_for_selector("div[aria-label='Chat list']", timeout=120000)  # Updated selector

        # Loop through each number and send the message
        for number in numbers:
            print(f"Sending message to {number}...")
            await page.goto(f"https://web.whatsapp.com/send?phone={number}")
            
            # Wait for the chat input box to load
            await page.wait_for_selector("div[contenteditable='true'][data-tab='10']", timeout=20000)
            message_box = await page.query_selector("div[contenteditable='true'][data-tab='10']")
            
            # Clear any existing text in the message box
            await message_box.evaluate("node => node.innerText = ''")

            # Type the message
            await message_box.type(message)
            
            # Press Enter to send the message
            await page.keyboard.press("Enter")
            await asyncio.sleep(1)  # Small delay to ensure message is sent

            # Confirm message sent and wait before moving to the next
            print(f"Message sent to {number}!")
            await asyncio.sleep(2)

        print("All messages have been sent successfully!")
        await browser.close()

# Read numbers from 'numbers.txt' and clean the list
def load_numbers(file_path="numbers.txt"):
    with open(file_path, "r") as file:
        numbers = [line.strip() for line in file if line.strip()]
    return numbers

if __name__ == "__main__":
    # Load phone numbers from file
    numbers = load_numbers("numbers.txt")
    if not numbers:
        print("No numbers found in numbers.txt. Please add phone numbers (one per line) and try again.")
        exit()
    
    # Get the message from the user
    message = input("Enter the message you want to send: ")
    
    # Run the async function
    asyncio.run(send_bulk_messages(numbers, message))
