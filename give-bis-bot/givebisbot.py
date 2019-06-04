#/usr/bin/python3
# -*- coding: utf-8 -*-

from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler)

import logging

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

MENU_PICK, PHONE, INITIAL_BOARD, MENU, FOOD_NOTE, NAME, LOCATION, PAYMENT = range(8)


def start(bot, update):
    reply_keyboard = [['Order', 'Check Status']]

    update.message.reply_text(
        'Hi! My name is Give Bis Bot. I will try to help you make an order. '
        'Send /cancel to stop talking to me.\n\n'
        'What would you like to do?',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    return INITIAL_BOARD

menu_items = ['Falafel', 'Pizza']

def menu(bot, update):
    reply_keyboard = [menu_items]
    update.message.reply_text(
        'What would you like to order?'
        'Send /close_order if you ordered everything you want.',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    return MENU_PICK

def menu_pick(bot, update, user_data):
    user = update.message.from_user
    user_data['type'] = update.message.text
    logger.info("Food type of %s: %s", user.first_name, update.message.text)
    update.message.reply_text('Any notes about this order?')

    return FOOD_NOTE

def food_note(bot, update, user_data):
    user = update.message.from_user
    user_data['note'] = update.message.text
    update.message.reply_text('What is your name?')
    logger.info("Food type of %s: %s", user.first_name, update.message.text)

    return NAME


def name(bot, update, user_data):
    user = update.message.from_user
    user_data['name'] = update.message.text
    logger.info("User %s is called: %s", user.first_name, update.message.text)
    update.message.reply_text('What is your location?')

    return LOCATION
    

def location(bot, update, user_data):
    user = update.message.from_user
    user_data['location'] = update.message.text
    logger.info("Name of %s: %s", user.first_name, update.message.text)
    update.message.reply_text('What is your phone number?')

    return PHONE

def phone(bot, update, user_data):
    user = update.message.from_user
    user_data['phone'] = update.message.text
    logger.info("Phone of %s: %s", user.first_name, update.message.text)
    update.message.reply_text('Your order is:\n' + d_to_str(user_data) + '\nThank you for ordering!')

    return ConversationHandler.END

def d_to_str(d):
    return f"{d['name']} ordered {d['type']} with note {d['note']} and to location {d['location']} with phone {d['phone']}"

    


def payment(bot, update):
    user = update.message.from_user
    logger.info("Payment of %s: %s", user.first_name, update.message.text)
    update.message.reply_text('Thank you! I hope we can talk again some day.',
            reply_markup=ReplyKeyboardRemove()
            )

    return ConversationHandler.END


def cancel(bot, update):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text('Bye! I hope we can talk again some day.',
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def main(api_token):
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(api_token)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler with the states FOOD_TYPE, FOOD_NOTE, LOCATION and PAYMENT.
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            INITIAL_BOARD: [RegexHandler('^Order$', menu)],

            MENU_PICK: [MessageHandler(Filters.text, menu_pick, pass_user_data=True),
                    CommandHandler('close_order', location, pass_user_data=True)],

            FOOD_NOTE: [MessageHandler(Filters.text, food_note, pass_user_data=True)],

            NAME: [MessageHandler(Filters.text, name, pass_user_data=True)],

            LOCATION: [MessageHandler(Filters.text, location, pass_user_data=True)],

            PHONE: [MessageHandler(Filters.text, phone, pass_user_data=True)]


            #FOOD_TYPE: [RegexHandler('^(Falafel🥙|Pizza🍕|Other)$', food_type)],

            #FOOD_NOTE: [MessageHandler(Filters.text, food_note),
            #        CommandHandler('skip', skip_food_note)],

            #LOCATION: [MessageHandler(Filters.text, location),
            #           CommandHandler('skip', skip_location)],

            #PAYMENT: [MessageHandler(Filters.text, payment)]
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
    if len(sys.argv) < 2:
        print('Please use bot API KEY as an argumnet')
    main(sys.argv[1])