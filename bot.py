import logging
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Define a few command handlers
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Hi! I am your test bot for BlumCryptoBot.')

def play_game(driver) -> None:
    while True:
        try:
            # Click the "Play" button
            play_button = driver.find_element(By.XPATH, '//button[text()="Play"]')
            play_button.click()

            # Wait for the game to start
            time.sleep(5)

            # Tap on green snowflakes until the timer expires
            end_time = time.time() + 60  # Assuming the timer is 60 seconds
            while time.time() < end_time:
                green_snowflakes = driver.find_elements(By.CLASS_NAME, 'green-snowflake')
                for snowflake in green_snowflakes:
                    snowflake.click()
                time.sleep(1)  # Adjust the sleep time as needed

            # Wait for the game to end and the "Play" button to reappear
            time.sleep(5)
        except Exception as e:
            logger.error(f"An error occurred: {e}")
            break

def setup_driver(account_url):
    driver = webdriver.Chrome()  # Ensure chromedriver is in your PATH
    driver.get(account_url)

    # Log in to Telegram Web and navigate to BlumCryptoBot
    # This part requires manual login for the first time
    time.sleep(30)  # Wait for manual login
    return driver

def play_games(update: Update, context: CallbackContext) -> None:
    account_urls = [
        'https://web.telegram.org/#/im?p=@BlumCryptoBot1',
        'https://web.telegram.org/#/im?p=@BlumCryptoBot2',
        # Add more account URLs as needed
    ]

    drivers = [setup_driver(url) for url in account_urls]

    for driver in drivers:
        play_game(driver)
        driver.quit()

def main() -> None:
    # Get the bot token from the environment variable
    bot_token = os.getenv('BOT_TOKEN')

    updater = Updater(bot_token)

    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("play_games", play_games))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT, SIGTERM or SIGABRT
    updater.idle()

if __name__ == '__main__':
    main()
