import os
import io
from PIL import Image, ImageDraw, ImageFont
from telegram import Update, InputMediaPhoto
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import requests

# Load your API key from the environment variable
IMGBB_API_KEY = os.getenv('IMGBB_API_KEY')

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Send me an image and specify the watermark position (top-left, top-right, bottom-left, bottom-right).')

def watermark_image(image: io.BytesIO, position: str) -> io.BytesIO:
    # Open image
    img = Image.open(image)
    watermark = Image.new('RGBA', img.size, (0, 0, 0, 0))
    
    # Add watermark text
    draw = ImageDraw.Draw(watermark)
    text = "Watermark"
    font = ImageFont.load_default()
    
    # Position based on user input
    if position == 'top-left':
        xy = (10, 10)
    elif position == 'top-right':
        xy = (img.width - 100, 10)
    elif position == 'bottom-left':
        xy = (10, img.height - 20)
    elif position == 'bottom-right':
        xy = (img.width - 100, img.height - 20)
    else:
        xy = (10, 10)  # Default to top-left

    draw.text(xy, text, fill=(255, 255, 255, 128), font=font)
    
    # Combine watermark with the original image
    watermarked = Image.alpha_composite(img.convert('RGBA'), watermark)
    
    # Save to a BytesIO object
    output = io.BytesIO()
    watermarked.save(output, format='PNG')
    output.seek(0)
    
    return output

def upload_to_imgbb(image: io.BytesIO) -> str:
    response = requests.post(
        'https://api.imgbb.com/1/upload',
        data={
            'key': IMGBB_API_KEY,
            'image': image.read()
        }
    )
    response_data = response.json()
    return response_data['data']['url']

def handle_photo(update: Update, context: CallbackContext) -> None:
    photo_file = update.message.photo[-1].get_file()
    photo_file.download('photo.jpg')
    
    position = context.args[0] if context.args else 'top-left'
    with open('photo.jpg', 'rb') as image_file:
        watermarked_image = watermark_image(io.BytesIO(image_file.read()), position)
        
        img_link = upload_to_imgbb(watermarked_image)
        
        update.message.reply_photo(photo=watermarked_image)
        update.message.reply_text(f'Here is your image with a watermark: {img_link}')

def main() -> None:
    # Load your Telegram Bot API key from the environment variable
    TELEGRAM_API_KEY = os.getenv('TELEGRAM_API_KEY')
    
    updater = Updater(TELEGRAM_API_KEY)
    
    dispatcher = updater.dispatcher
    
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.photo, handle_photo))
    
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
