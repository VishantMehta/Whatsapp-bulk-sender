from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementClickInterceptedException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import logging
import os

# Configuration
numbers_file = 'number.txt'
sent_numbers_file = 'sent_numbers.txt'
message_body = "YOUR MESSAGE"
max_retries = 2
retry_delay = 5  # Seconds to wait before retrying

# Set up logging
logging.basicConfig(filename='whatsapp_bot.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def setup_driver():
    try:
        driver = webdriver.Chrome()
        driver.get('https://web.whatsapp.com')
        return driver
    except Exception as e:
        logging.error(f"Failed to set up WebDriver: {e}")
        raise


def check_message_sent(driver):
    try:
        # Locate the latest message sent with the double tick (delivered) icon
        delivered_tick = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//span[contains(@aria-label, ' Delivered')]"))
        )
        return delivered_tick is not None  # If found, the message has been delivered
    except TimeoutException:
        logging.warning("Message delivery confirmation not found.")
        return False


def send_message(driver, phone_number):
    url = f"https://web.whatsapp.com/send?phone={phone_number}&text={message_body}"

    # Attempt to send the message
    try:
        driver.get(url)
        time.sleep(10)  # Wait for the page to load

        # Locate the send button and wait for it to become clickable
        send_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Send']"))
        )
        send_button.click()

        time.sleep(5)  # Give some time for the message to be sent

        # Check if the message has been delivered (using double tick confirmation)
        if check_message_sent(driver):
            logging.info(f"Message successfully sent to {phone_number}")
            return True  # Success, move to the next number
        else:
            logging.warning(f"Message not confirmed for {phone_number}. Retrying...")
    except (NoSuchElementException, ElementClickInterceptedException) as e:
        logging.warning(f"Element issue for {phone_number}: {e}. Entering retry mechanism...")
    except TimeoutException as e:
        logging.error(f"Timeout occurred for {phone_number}: {e}. Entering retry mechanism...")
    except Exception as e:
        logging.error(f"Error occurred for {phone_number}: {e}. Entering retry mechanism...")

    # Retry mechanism
    for attempt in range(max_retries):
        try:
            driver.get(url)
            time.sleep(10)  # Wait for the page to load

            send_button = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Send']"))
            )
            send_button.click()

            time.sleep(5)  # Give some time for the message to be sent

            if check_message_sent(driver):
                logging.info(f"Message successfully sent to {phone_number} after {attempt + 1} retries")
                return True  # Success, move to the next number
            else:
                logging.warning(f"Message not confirmed for {phone_number}. Retrying...")
        except (NoSuchElementException, ElementClickInterceptedException) as e:
            logging.warning(f"Element issue for {phone_number}: {e}. Retrying...")
        except TimeoutException as e:
            logging.error(f"Timeout occurred for {phone_number}: {e}. Retrying...")
        except Exception as e:
            logging.error(f"Error occurred for {phone_number}: {e}. Retrying...")

        time.sleep(retry_delay)  # Wait before retrying

    logging.error(f"Failed to send message to {phone_number} after {max_retries} retries.")
    return False  # Failed to send message


def load_sent_numbers():
    """Load already sent numbers from the file to avoid duplicates."""
    if os.path.exists(sent_numbers_file):
        with open(sent_numbers_file, 'r') as f:
            return {line.strip() for line in f if line.strip()}
    return set()


def save_sent_number(phone_number):
    """Save a successfully sent phone number to a file."""
    with open(sent_numbers_file, 'a') as f:
        f.write(f"{phone_number}\n")


def main():
    driver = setup_driver()

    input("Press Enter after scanning QR code")

    # Load already sent numbers to avoid sending again
    sent_numbers = load_sent_numbers()

    # Read the list of phone numbers from the file
    with open(numbers_file, 'r') as file:
        phone_numbers = [line.strip() for line in file if line.strip()]

    # Iterate over the phone numbers
    for phone_number in phone_numbers:
        if phone_number in sent_numbers:
            logging.info(f"Skipping {phone_number} as message was already sent.")
            continue

        success = send_message(driver, phone_number)
        if success:
            logging.info(f"Moving to next contact after {phone_number}")
            sent_numbers.add(phone_number)  # Add to in-memory set
            save_sent_number(phone_number)  # Save to file to persist the state
            driver.get('https://web.whatsapp.com')  # Navigate to the main page to reset state
            time.sleep(10)  # Delay to ensure the page is ready
        else:
            logging.error(f"Skipping {phone_number} after retries failed.")
            driver.get('https://web.whatsapp.com')  # Navigate to the main page to reset state
            time.sleep(10)  # Delay to ensure the page is ready

    driver.quit()
    logging.info("All messages sent and browser closed.")


if __name__ == "__main__":
    main()
