# Telegram Watermark Bot

This bot adds watermarks to images sent by users and uploads them to ImgBB. It is deployable on Railway.

## Setup

1. Create a `.env` file with the following content:

    ```
    IMGBB_API_KEY=your_imgbb_api_key
    TELEGRAM_API_KEY=your_telegram_api_key
    ```

2. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Run the bot locally:

    ```bash
    python bot.py
    ```

## Deployment

Deploy to Railway using GitHub Actions.

## Usage

Send an image to the bot and specify the watermark position (top-left, top-right, bottom-left, bottom-right).
