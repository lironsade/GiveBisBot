#!/usr/bin/python3
# -*- coding: utf-8 -*-

from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler)
import subscribers_db
import logging


s_db = subscribers_db.SubscribersDatabase()


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

FOOD_TYPE, FOOD_NOTE, LOCATION, PAYMENT = range(4)


def start(bot, update):
    reply_keyboard = [['Falafel🥙', 'Pizza🍕', 'Other']]
    chat_id = update.message.chat_id
    update.message.reply_text(
        'Hi! My name is Give Bis Bot. I will try to help you make an order. '
        'Send /cancel to stop talking to me.\n\n'
        'What would you like to order?',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    s_db.insert(chat_id)

    return FOOD_TYPE


def food_type(bot, update):
    user = update.message.from_user
    logger.info("Food type of %s: %s", user.first_name, update.message.text)
    update.message.reply_text('I see! Please send me any note about your order, '
                              'so I know if there is anything special you would like, or send /skip if you don\'t want to.',
                              reply_markup=ReplyKeyboardRemove())

    return FOOD_NOTE


def food_note(bot, update):
    user = update.message.from_user
    logger.info("Food note of %s: %s", user.first_name, update.message.text)
    update.message.reply_text('Nice! Now, send me your location please, '
                              'or send /skip if you don\'t want to.')

    return LOCATION


def skip_food_note(bot, update):
    user = update.message.from_user
    logger.info("User %s did not specify food note.", user.first_name)
    update.message.reply_text('OK! Now, send me your location please, '
                              'or send /skip.')

    return LOCATION


def location(bot, update):
    user = update.message.from_user
    #user_location = update.message.location
    #logger.info("Location of %s: %f / %f", user.first_name, user_location.latitude,
    #            user_location.longitude)
    user = update.message.from_user
    logger.info("Location of %s: %s", user.first_name, update.message.text)

    reply_keyboard = [['Credit Card', 'Cash', 'Other']]
    update.message.reply_text('Maybe I can visit you sometime! '
                              'At last, tell me how you are going to pay.',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
        )

    return PAYMENT


def skip_location(bot, update):
    user = update.message.from_user
    logger.info("User %s did not send a location.", user.first_name)

    reply_keyboard = [['Credit Card', 'Cash', 'Other']]
    update.message.reply_text('You seem a bit paranoid! '
                              'At last, tell me how you are going to pay.',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
        )

    return PAYMENT


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
            FOOD_TYPE: [RegexHandler('^(Falafel🥙|Pizza🍕|Other)$', food_type)],

            FOOD_NOTE: [MessageHandler(Filters.text, food_note),
                    CommandHandler('skip', skip_food_note)],

            LOCATION: [MessageHandler(Filters.text, location),
                       CommandHandler('skip', skip_location)],

            PAYMENT: [MessageHandler(Filters.text, payment)]
        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dp.add_handler(conv_handler)

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print('Please use bot API KEY as an argumnet')
    main(sys.argv[1])
