#!/usr/bin/python
from __future__ import print_function
from httplib2 import Http
from json import dumps
import ast

retry_timeout=7
retry_max_count=3

def post_to_data_google_chat(gcmsg):
    """Send Notification to Google chat rooms"""
    message_headers = { 'Content-Type': 'application/json; charset=UTF-8'}
    http_obj = Http()
    for i in range(0,retry_max_count):
       try:
           response = http_obj.request(
               uri=notification_url,
               method='POST',
               headers=message_headers,
               body=dumps(gcmsg),
           )
           return ast.literal_eval(response[1])['thread']

       except Exception,e:
           print ('Not able to post message to google chat API')
           print ("Retrying after " + str(retry_timeout) + " Seconds")
           time.sleep(retry_timeout)
           if i < retry_max_count-1:
               continue
           else:
               print ("Failing after " + str(retry_max_count) + " retries")
               print ('Not able to post message to google chat API')
               sys.exit(1)
        break



def google_chat_notify(msg):
    if len(msg) < 4096:
        get_my_chat_thread=post_to_data_google_chat(gcmsg={'text':'@all','thread':{'name':''}})
        post_to_data_google_chat(gcmsg={'text':msg,'thread':get_my_chat_thread})
    else:
        get_my_chat_thread=post_to_data_google_chat(gcmsg={'text':'@all','thread':{'name':''}})
        total_size=len(msg)
        max_chunks=total_size/4096
        start_pos=0
        end_pos=4096
        for i in range(max_chunks+1):
            msg_chunk=''
            for j in range(start_pos,end_pos):
                msg_chunk=msg_chunk+msg[j]
            start_pos=end_pos
            if i == max_chunks-1:
                end_pos=total_size
            else:
                end_pos=end_pos+4096
            post_to_data_google_chat(gcmsg={'text':msg_chunk,'thread':get_my_chat_thread})

