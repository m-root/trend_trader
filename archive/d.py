import telegram
# from config import telegram_token_news

# use token generated in first step
bot = telegram.Bot(token='620369180:AAF58K-FUyB1E5L-AwEdp6D7GFciRNxEYJw')
status = bot.send_message(chat_id="@crypto_signals_int", text='Buy BTCUSD at 7996.45 \nSell BTCUSD at 8160.15\nBuy BTCUSD at 8108.00 \nSell BTCUSD at 8118.15 \nBuy BTCUSD at 7739.33 \nSell BTCUSD at 7753.23 \nBuy BTCUSD at 7728.23 \nSell BTCUSD at 7734.34'
, parse_mode=telegram.ParseMode.HTML)

print(status)


# https://t.me/joinchat/AAAAAEwSdkaEUS0gO6Z_MQ