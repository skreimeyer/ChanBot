#!/usr/bin/env python

from chatterbot import ChatBot
import logging
import time

bot = ChatBot("Terminal-chan",
              storage_adapter="chatterbot.storage.MongoDatabaseAdapter",
              logic_adapters=[
                  "chatterbot.logic.BestMatch"
                  ],
              trainer="chatterbot.trainers.ChatterBotCorpusTrainer",
              input_adapter="chatterbot.input.TerminalAdapter",
              output_adapter="chatterbot.output.TerminalAdapter",
              database='chatterbot-database'
              )
print('TRAIN TO BECOME STRONG!')

start = time.time()

bot.train('chatterbot.corpus.english.greetings',
          './8chan.corpus.json'
          )
end = time.time()
traintime = end-start

print('TRAINING TOOK %10.2f seconds' % traintime)

print('GOOD LUCK BOT-CHAN!')

while True:
    try:
        start = time.time()
        bot_input = bot.get_response(raw_input('>'))
        end = time.time()
        response_time = end-start
        print('RESPONSE TOOK %10.2f seconds' % response_time)
    except (KeyboardInterrupt, EOFError, SystemExit):
        break
