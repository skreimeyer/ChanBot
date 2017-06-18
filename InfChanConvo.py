#!/usr/bin/env python

import requests
import bs4
import json
import re
from fake_useragent import UserAgent
##import pdb

class InfChanConversations():
    """
    This class contains all methods necessary to query the 8ch.net website
    for a list of threads, request every thread and produce nested lists of
    all conversations for use as a language training corpus. The board
    should be specified as a keyword argument.
    """

    def __init__(self,**kwargs):
        self.board = kwargs.get('board','pol')
        self.board.strip('/')
        self.threads_url = 'http://8ch.net/'+self.board+'/threads.json'
        self.base_thread = 'http://8ch.net/'+self.board+'/res/'
        #spoof the user agent because we're sneaky
        self.ua = UserAgent()
        self.headers = {'User-Agent':self.ua.random}

    def fetch_thread_ids(self):
        """
        Request the threads.json page, then loop through each row (thread)
        on each page and append the thread number to a master list.
        """
        req = requests.get(self.threads_url, headers=self.headers)
        if req.status_code != 200:
            print('FAILED TO LOAD %s !\n Exiting' % self.threads_url)
            quit()
        data = json.loads(req.text)
        thread_ids = list()
        for page in data:
            for row in page['threads']:
                thread_ids.append(row['no'])
        print('>>Found %s threads' % len(thread_ids))
        return thread_ids

    def fetch_thread(self,thread_id):
        """
        Request an individual thread in JSON format and return a dictionary
        object of post number and post text pairs.
        """
        status_flag = False
        req = requests.get(self.base_thread+str(thread_id)+'.json', headers = self.headers)
        if req.status_code != 200:
            print('Request for page %s%s failed!' % (self.base_thread,thread_id))
            status_flag = True
        posts = {}
        op = tuple()
        if not status_flag:
            data = json.loads(req.text)
            #exclude OP because we need to handle it differently when
            #we extract our statements
            for post in data['posts'][1:]:
                key = post['no']
                text = post['com']
                re.sub('</p>','\n</p>',text)
                #Use BS4 to reliably remove HTML tags
                soup = bs4.BeautifulSoup(text,'lxml')
                clr_text = soup.get_text()
                posts[key]=clr_text
            #make a tuple for OP to use later
            op_text = data['posts'][0]['com']
            #add newlines at paragraph tags to avoid concatenation
            re.sub('</p>',' \n</p>',op_text)
            op_soup = bs4.BeautifulSoup(op_text,'lxml')
            op_clr = op_soup.get_text()
            op = (data['posts'][0]['no'],op_clr)
                  
        return posts,op,status_flag

    def extract_statements(self,posts,op):
        """
        This method takes the dictionary object from the fetch_thread method
        and returns a list of tuples of statements and the post ID they refer to.
        By convention, replies have a preamble of a link to the post being
        repsoned to, like ">>12345". This is achieved by splitting a post's text
        by regex matches for post IDs

        This method maps ids to corresponding statements,
        and assigns the id of the first thread post where a post id is not given.
        """
        #Make OP the first tuple
        statement_tuples = [(op[0],'',op[1])]
        for post_num in posts:
            refs = re.findall('\>\>[\d]+',posts[post_num])
            refs = [x.strip('>>') for x in refs]
            #So in the unlikely scenario that a post refers to its own post id
            #the conversation constructor will get stuck in an infinite loop
            #so we'll just test for this ridiculous edge case and rewrite any
            #self-referential post ids to the OP-id for simplicity.
            if str(post_num) in refs:
                for i,x in enumerate(refs):
                    if x == str(post_num):
                        refs[i] = op[0]
            #re.split will not always consume the search string after a large number
            #of iterations. Use a while loop to validate our output.
            regex_flag = True
            regex_counter = 0
            while regex_flag:
                statements = re.split('\>\>[\d]+',posts[post_num])
                if True not in ['>>' in x for x in statements]:
                    regex_flag = False
                else:
                    regex_counter += 1
                if regex_counter == 2:
                    regex_flag = False
            #instantiate a list to hold many-to-one mappings of ids to
            #statements
            holder = []
            if statements[0] != '':
                    statement_tuples.append((post_num,op[0],statements[0].strip()))
            for statement in statements[1:]:
                #Cast reference number as int to avoid type-mismatch later
                holder.append(int(refs.pop(0)))
                if statement != '':
                    for i in holder:
                        statement_tuples.append((post_num,holder.pop(0),statement))
                if len(refs) == 0:       
                    for i in holder:
                        statement_tuples.append((post_num,holder.pop(0),statement))
        return statement_tuples

    def construct_conversations(self,statement_tuples,op):
        """
        This method reconstructs conversation streams by linking statements
        with the post id they refer to. This method creates an array to hold each
        converstion stream. The stream loops over our tuples and finds those
        statements with post IDs which are not referenced by any other statement.
        The remaining statements are traced by following reference IDs in the
        newly formed array to work back toward the original post.
        """
        array = []
        #Determine endpoints of our array and pop them from list
        for i,statement in enumerate(statement_tuples):
            if statement[0] not in [x[1] for x in statement_tuples]:
                array.append([(statement[1],statement[2])])
        #Trace each conversation back to its source
        while False in [x[0][0] == '' for x in array]:
            #create a flag to avoid an infinite loop
            loop_flag = True
            for x in array:
                #search statements for an ID matching our reference
                for y in statement_tuples:
                    if x[0][0] == y[0]:
                        x.insert(0,(y[1],y[2]))
                        loop_flag = False
            if loop_flag:
                #This should only return true after looping every statement
                #for every list object in our array.
                break

        #Create a final array (list of lists) now that we no longer
        #need id reference number
        out_array = [[y[1] for y in x] for x in array]
        return out_array

    def gen_corpus(self):
        """
        This method executes the previously defined methods to generate
        a language corpus JSON compatible with chatterbot.
        """
        #continer for our JSON output
        corpus = {}
        #container for conversational arrays to tie into the corpus
        #object
        conv_arrays = []
        threads = self.fetch_thread_ids()
        for i,thread in enumerate(threads):
            print('PROCESSING THREAD %s OF %s\t[ID:%s]' % (i,len(threads),thread))
            try:
                (posts,op,status_flag) = self.fetch_thread(thread)
                if status_flag:
                    continue
                statements = self.extract_statements(posts,op)
                array = self.construct_conversations(statements,op)
                conv_arrays += array
            except:
                continue
        corpus[self.board]=conv_arrays
        return corpus
