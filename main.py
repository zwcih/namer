#!/usr/bin/env python
# coding: utf-8

import os
import json
import re
import random
from http.server import BaseHTTPRequestHandler, HTTPServer
from os import path
from urllib.parse import urlparse
import json



fulllist = []

for root, dirs, files in os.walk('json'):
    for file in files:
        with open(os.path.join(root, file), 'r', encoding = 'utf-8') as f:
            d = json.loads(f.read())
        for l in d:
            if l['content'] == None:
                continue
            l['content'] = re.sub(r'<.*?>','',l['content'])
            l['content'] = l['content'].replace('\u3000', '')
            
            fulllist.append(l)
            
print(len(fulllist))

def getname(fulllist):
    sentence_list = []
    #print('start')
    while len(sentence_list) < 2:
        article = random.choice(fulllist)
        content = re.sub(r'[（(].+[)）]', '', article['content'])
        sentence_list = re.split(r'[。？！\s]', content)
        #print(sentence_list)
    sentence = ''
    while len(sentence) < 3:
        sentence = random.choice(sentence_list)
    #print(sentence)
    b_list = range(0,len(sentence))
    #print(b_list)
    name = ''
    while len(name) != 2:
        l = random.sample(b_list,2)
        l = sorted(l)
        for i in l:
            c = sentence[i]
            if c.isalpha():
                name += c
        if len(name) != 2:
            name=''

    return {'name' : name, 'index':l, 'sentence':sentence, 'book' : article['book'], 'title' : article['title'], 'author' :article['author']}

curdir = path.dirname(path.realpath(__file__))
sep = '/'


class testHTTPServer_RequestHandler(BaseHTTPRequestHandler):
    # GET
    def do_GET(self):
        sendReply = False
        querypath = urlparse(self.path)
        filepath, query = querypath.path, querypath.query
        
        if filepath.endswith('/'):
            filepath += 'index.html'
            try:
                with open(path.realpath(curdir + sep + filepath),'rb') as f:
                    content = f.read()
                    self.send_response(200)
                    self.send_header('Content-type','text/html')
                    self.end_headers()
                    self.wfile.write(content)
            except IOError:
                self.send_error(404,'File Not Found: %s' % self.path)
        elif filepath.endswith('/get-name'):
            self.send_response(200)
            self.send_header('Content-type','application/json')
            self.end_headers()
            content = json.dumps(getname(fulllist))
            self.wfile.write(content.encode('utf-8'))

            
def run():
    port = 8000
    print('starting server, port', port)

    # Server settings
    server_address = ('', port)
    httpd = HTTPServer(server_address, testHTTPServer_RequestHandler)
    print('running server...')
    httpd.serve_forever()

if __name__ == '__main__':
    run()


