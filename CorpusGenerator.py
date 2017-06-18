#!/usr/bin/env python


#commented imports are not necessary now but expected to be
#used as functionality is expanded.

#import sys
#import os
import argparse
#import configparse
import json


class Generator():
    """
    This class handles arguments passed in from the command line
    and contains methods from other modules needed to return a
    language corpus for training a chat bot. Imports of modules
    made exclusively for this script are only called in the functions
    that require them to avoid a large number of unnecessary imports.
    """

    def __init__(self,module, board, filename):
        self.board = board
        self.filename = filename
        self.module = module
        self.mods = {'8chan':self.infchan}

    def writeout(self, corpus):
        """
        Opens a file object for our corpus and writes out a json
        """
        outfile = open(self.filename+'.corpus.json','w')
        outfile.write(json.dumps(corpus))
        outfile.close()
        print('language corpus written to %s.corpus.json' % self.filename)
        return True
    
    def infchan(self):
        """
        Import the 8chan module and use it to construct our corpus
        """
        from InfChanConvo import InfChanConversations as inf
        inf_obj = inf(board=self.board)
        corpus = inf_obj.gen_corpus()
        self.writeout(corpus)
        return True

    def run(self):
        self.mods[self.module]()
        return True


if __name__ == "__main__":

    desc = '-'*40+'Scrape online sources for conversations and produce \
    a language corpus for training compatible with the Chatterbot module.\n'+'-'*40
    parser = argparse.ArgumentParser(prog='Corpus Generator',
                                     description=desc)
    #Set default parameters
    parser.add_argument('-l','--modlist',action='store_true',help='list available modules')
    parser.add_argument('-m','--module',default='8chan',help='module to be used')
    parser.add_argument('-b','--board',default='pol',help='name of board to scrape [optional]')
    parser.add_argument('-w','--write',default='chan',help='filename to write out to')
    args = parser.parse_args()

    if args.modlist:
        modlist = Generator(args.module,args.board,args.write).mods
        for key in modlist:
            print(key)
            quit()
    else:
        G = Generator(args.module,args.board,args.write)
        G.run()
        quit()
        
