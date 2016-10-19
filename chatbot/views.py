#!/usr/bin/env python
# -*- coding: utf-8 -*-


from django.shortcuts import render
from django.http import HttpResponse

from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
import requests , random , re



# Create your views here.


VERIFY_TOKEN = 'emojify'




PAGE_ACCESS_TOKEN = 'EAACkFTCZBIPoBAH2otifAKUl7Bzisq3TrGtMFFQ9FZAKaNouMWejpfYA21YwOS57tlzZBOoVZCKC3fRAUFgZAVXSvIVTUEhuVfMVbvWplpl23v3Hz5nJPhs9OdNdGYymluIZApZBEZCbvWNNQJI9GLa6nRz7CvCJkskbc1hLiwHOKwZDZD'


def set_menu():
    post_message_url = 'https://graph.facebook.com/v2.6/me/thread_settings?access_token=%s'%PAGE_ACCESS_TOKEN
    
    response_object =   {
                          "setting_type" : "call_to_actions",
                          "thread_state" : "existing_thread",
                          "call_to_actions":[
                            {
                              "type":"postback",
                              "title":"Help",
                              "payload":"MENU_LINK"
                            },
                            {
                              "type":"postback",
                              "title":"Our website",
                              "payload":"MENU_OUTPUT"
                            },
                            {
                              "type":"postback",
                              "title":"Our hy",
                              "payload":"MENU_hy"
                            },
                            {
                              "type":"postback",
                              "title":"Why Master Event",
                              "payload":"MENU_WHY"
                            }
                          ]
                        }

    menu_object = json.dumps(response_object)
    status = requests.post(post_message_url,
          headers = {"Content-Type": "application/json"},
          data = menu_object)







def handle_postback(fbid,payload):
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s'%PAGE_ACCESS_TOKEN
    output_text = 'Payload Recieved: ' + payload

    if payload == 'MENU_WHY':
        return post_facebook_message(fbid,'Your vision our creativity')

    elif payload == 'MENU_WHY':
        return post_facebook_message(fbid,'Your vision our creativity')
        

    elif payload == 'MENU_OUTPUT':
        response_object = {
                              "recipient":{
                                "id":"USER_ID"
                              },
                              "message":{
                                "attachment":{
                                  "type":"template",
                                  "payload":{
                                    "template_type":"generic",
                                    "elements":[
                                      {
                                        "title":"Welcome to Peter\'s Hats",
                                        "item_url":"https://petersfancybrownhats.com",
                                        "image_url":"https://petersfancybrownhats.com/company_image.png",
                                        "subtitle":"We\'ve got the right hat for everyone.",
                                        "buttons":[
                                          {
                                            "type":"web_url",
                                            "url":"https://petersfancybrownhats.com",
                                            "title":"View Website"
                                          },
                                          {
                                            "type":"postback",
                                            "title":"Start Chatting",
                                            "payload":"DEVELOPER_DEFINED_PAYLOAD"
                                          }              
                                        ]
                                      }
                                    ]
                                  }
                                }
                              }
                            }

        response_msg = json.dumps(response_object)
        requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
    






def post_facebook_message(fbid, recevied_message):
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s'%PAGE_ACCESS_TOKEN
    
    response_msg3 = json.dumps(
            {"recipient":{"id":fbid}, 
                "message":{
                    "attachment":{
                        "type":"image",
                        "payload":{
                            "url":'http://thecatapi.com/api/images/get?format=src&type=png'
                        }
                    }
                }
         })
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg3)
    return
    
    response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"text":response_text}})
    
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
    pprint(status.json())


class MyChatBotView(generic.View):
    def get(self, request, *args, **kwargs):
        if self.request.GET['hub.verify_token'] == VERIFY_TOKEN:
            return HttpResponse(self.request.GET['hub.challenge'])
        else:
            return HttpResponse('Error, invalid token')
        
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return generic.View.dispatch(self, request, *args, **kwargs)

    
    def post(self, request, *args, **kwargs):
        incoming_message = json.loads(self.request.body.decode('utf-8'))
        for entry in incoming_message['entry']:
            for message in entry['messaging']: 
                if 'message' in message:
                    try:  
                        sender_id = message['sender']['id']
                        message_text = message['message']['text']
                        post_facebook_message(sender_id,message_text) 
                    except Exception as e:
                        print e
                        post_facebook_message(message['sender']['id'], 'Please send a valid text for emoji search.')


                    try:
                        if 'postback' in message:
                            handle_postback(message['sender']['id'],message['postback']['payload'])
                            return HttpResponse()
                        else:
                            pass
                    except Exception as e:
                        pass



        return HttpResponse()    



def index(request):
    set_menu()
    handle_postback('fbid','MENU_CALL')
    return HttpResponse('Hello world')

















