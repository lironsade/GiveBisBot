# /usr/bin/python3
# -*- coding: utf-8 -*-

from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler)
import csv
import logging
import constants
import menu
from config import ORDERS_BROADCAST_CHANNEL_ID
from order import Order

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

STATUS, MENU_PICK, PHONE, INITIAL_BOARD, MENU, FOOD_NOTE, NAME, LOCATION, PAYMENT = range(9)

rest_menu = menu.Menu()

start_keyboard = [['Order', 'Check Status']]

with open('orders.csv', 'w', newline='') as outcsv:
    writer = csv.writer(outcsv)
    writer.writerow(['chat_id', 'type', 'note', 'name', 'location', 'phone', 'order description'])


def start(bot, update):

    update.message.reply_text(
        constants.START_MSG,
        reply_markup=ReplyKeyboardMarkup(start_keyboard, one_time_keyboard=True))

    return INITIAL_BOARD


def menu(bot, update):
    reply_keyboard = [rest_menu.AllText()]
    update.message.reply_text(
        constants.MENU_MSG,
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    return MENU_PICK


def menu_pick(bot, update, user_data):
    # user_data['order'] = Order()
    if 'chat_id' not in user_data:
        user_data['chat_id'] = []
    user_data['chat_id'].append(update.message.chat_id)
    user = update.message.from_user
    if 'type' not in user_data:
        user_data['type'] = []
    user_data['type'].append(update.message.text)
    logger.info("Food type of %s: %s", user.first_name, update.message.text)
    update.message.reply_text('Any notes about this order? /skip if you don\'t have one')

    return FOOD_NOTE


def food_note(bot, update, user_data):
    reply_keyboard = [rest_menu.AllText()]
    user = update.message.from_user
    if 'note' not in user_data:
        user_data['note'] = []
    user_data['note'].append(update.message.text)
    logger.info("Food type of %s: %s", user.first_name, update.message.text)
    update.message.reply_text(
        'Anything else, or /close_order ?',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    return MENU_PICK


def skip_food_note(bot, update, user_data):
    user = update.message.from_user
    if 'note' not in user_data:
        user_data['note'] = []
    user_data['note'].append('no note')
    logger.info("%s skipped food note", user.first_name)
    reply_keyboard = [rest_menu.AllText()]
    update.message.reply_text(
        'Anything else, or /close_order ?',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    return MENU_PICK


def close_order(bot, update, user_data):
    user = update.message.from_user
    update.message.reply_text('Thank you for ordering! What is your name?', reply_markup=ReplyKeyboardRemove())
    return NAME


def name(bot, update, user_data):
    user = update.message.from_user
    user_data['name'] = update.message.text
    logger.info("User %s is called: %s", user.first_name, update.message.text)
    update.message.reply_text(constants.LOC_MSG)

    return LOCATION


def location(bot, update, user_data):
    user = update.message.from_user
    user_data['location'] = update.message.text
    logger.info("Name of %s: %s", user.first_name, update.message.text)
    update.message.reply_text(constants.PHIE_NUM_MSG)

    return PHONE


def phone(bot, update, user_data):
    user = update.message.from_user
    user_data['phone'] = update.message.text
    logger.info("Phone of %s: %s", user.first_name, update.message.text)
    user_data['order'] = CreateOrderFromData(user_data)
    order_desc = repr(user_data['order'])
    update.message.reply_text('Your order is:\n' + order_desc + '\nThank you for ordering!',
        reply_markup=ReplyKeyboardMarkup(start_keyboard, one_time_keyboard=True))
    bot.send_message(chat_id=ORDERS_BROADCAST_CHANNEL_ID,
                     text=f'New order:\n{order_desc}')

    with open('orders.csv', 'a', newline='') as outcsv2:
        writer2 = csv.writer(outcsv2)
        writer2.writerow(
            [user_data['chat_id'], user_data['type'], user_data['note'], user_data['name'], user_data['location'],
             user_data['phone'], user_data['order']])
    return INITIAL_BOARD



def d_to_str(d):
    return \
        f"{d['name']} ordered {d['type']} with note {d['note']} and to location {d['location']} with phone {d['phone']}"


def CreateOrderFromData(data):
    order = Order(data['name'], data['location'], data['phone'])
    for item_type, item_note in zip(data['type'], data['note']):
        order.place_order(rest_menu.GetItem(item_type), item_note)
    return order


def payment(bot, update):
    user = update.message.from_user
    logger.info("Payment of %s: %s", user.first_name, update.message.text)
    update.message.reply_text(constants.PAYMENT_MSG,
                              reply_markup=ReplyKeyboardRemove()
                              )

    return ConversationHandler.END


def cancel(bot, update):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text(constants.AFTER_CANCEL_MSG,
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)

def check_status(bot, update, user_data):
    order_text = 'You have\'t placed an order.'
    if 'order' in user_data:
        order_text = repr(user_data['order'])
    update.message.reply_text(order_text,
        reply_markup=ReplyKeyboardMarkup(start_keyboard, one_time_keyboard=True)
    )

    return INITIAL_BOARD
    

def main(api_token):

    with open('menu.csv', 'r', newline='') as menucsv:
        csv_reader = csv.reader(menucsv, delimiter=',', quotechar='|')
        rest_menu.crete_menu_from_csv_file(csv_reader)
    menu_items = rest_menu.AllText()

    # Create the EventHandler and pass it your bot's token.
    updater = Updater(api_token)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler with the states FOOD_TYPE, FOOD_NOTE, LOCATION and PAYMENT.
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            INITIAL_BOARD: [
                    RegexHandler('^Order$', menu),
                    RegexHandler('^Check Status$', check_status, pass_user_data=True)
                ],

            MENU_PICK: [
                    MessageHandler(Filters.text, menu_pick, pass_user_data=True),
                    CommandHandler('close_order', close_order, pass_user_data=True)
                ],

            FOOD_NOTE: [
                    MessageHandler(Filters.text, food_note, pass_user_data=True),
                    CommandHandler('skip', skip_food_note, pass_user_data=True)
                ],

            NAME: [MessageHandler(Filters.text, name, pass_user_data=True)],

            LOCATION: [MessageHandler(Filters.text, location, pass_user_data=True)],
			
	    PHONE: [RegexHandler('^0([57]\d|[23489])\d{7}$', phone, pass_user_data=True)]

            },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dp.add_handler(conv_handler)

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    print('Starting GiveBisBot...')
    updater.start_polling()
    print('GiveBisBot started!')

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    import sys
    logging.info("starting server")
    if len(sys.argv) < 2:
        print('Please use bot API KEY as an argumnet')
    main(sys.argv[1])
