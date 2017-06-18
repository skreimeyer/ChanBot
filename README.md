# ChanBot
ChanBot scrapes popular image boards for conversations to create corpora compatible with the Chatterbot module.
Chatterbot is a retrieval-based chat-bot, which is the most simple implementation, but lacks the ability to
respond with statements that have not been used for training. Over time this may evolve into a text processor
for more flexible chatbot implementations, like RNN. The corpora may be useful to a user interested in
exploring conversation patterns on image boards, as each list constitutes a complete conversation (albeit
between an unknown number of persons) within a discussion thread.

Support
==========


The following imageboards are supported at this time:

8ch.net

More to follow.


Usage
==========

Run the CorpusGenerator script to create a .json file that can be used as a Chatterbot corpus. A corpus is an array of conversations that the Chatterbot instance will use to select appropriate responses for a given text input.
Chatterbot includes multiple comparisons from the NLTK module, but, broadly speaking, all are statistical models of text similarity. In order to create a functional bot, you will need to write a
Chatterbot script tailored to your desired application.

examples
----------
#Create a language corpus with all default parameters

python CorpusGenerator.py

#Specify which scraper to use, which board and the output filename

python CorpusGenerator.py -m 8chan -b a -w my_file

