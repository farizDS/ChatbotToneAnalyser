import re
import json
import os
import time
from slackclient import SlackClient

from pprint import pprint


class CaringBot:
  ########################################################################################################################
  # Variable initialisation
  ######################################################################################################################## 
  
  def __init__(self,slack_client, conversation_client, workspace, tone_analyser, discovery_client):
    
    self.slack_client = slack_client
    self.conversation_client = conversation_client
    self.delay = 0.5 #second
    self.workspace_id = workspace
    self.bot_id = self.slack_client.api_call("auth.test")['user_id']
    
    self.tone_analyser = tone_analyser
    self.discovery = discovery_client
   
  ########################################################################################################################
  # Slack Commands for receiving and sending text from and to user in slack
  ######################################################################################################################## 
  def parse_slack_output(self, slack_rtm_output):
    """
    Get message from user
    message = text from user
    """
    def parse_direct_mention(message_text):
      """
        Finds a direct mention (a mention that is at the beginning) in message text
        and returns the user ID which was mentioned. If there is no direct mention, returns None
      """
      MENTION_REGEX = "^<@(|[WU].+?)>(.*)"
      matches = re.search(MENTION_REGEX, message_text)
       
      # the first group contains the username, the second group contains the remaining message
      return (matches.group(1), matches.group(2).strip()) if matches else (None, None)

    slack_events = slack_rtm_output
    for event in slack_events:
        if event["type"] == "message" and not "subtype" in event:
            user_id, message = parse_direct_mention(event["text"])
            if user_id == self.bot_id:
                channel = event['channel']
                return message,channel
    return None, None
    
  def post_to_slack(self, response, channel):
    """
    post reponse from Watson Asistant to Slack 
    """
    print("Sending response from Watson Assistant to Slack......")   
    self.slack_client.api_call("chat.postMessage", 
                          channel=channel,
                          text=response, as_user=True)
  
  ########################################################################################################################
  # Configuration about how to handle any input from user
  ######################################################################################################################## 
  
   
  def assistant_send_text(self, message=None, emotion=None):
  ########################################################################################################################
  # a function to send text/message to assistant from User
  ######################################################################################################################## 
    if emotion == None:
      return self.conversation_client.message(workspace_id=self.workspace_id, 
    input={"text": message}).get_result()
    else:
      return self.conversation_client.message(workspace_id=self.workspace_id, 
      context={"emotion": emotion}).get_result()

  
  
  def handle_message(self, message, channel):
    print("Message, received!")
    
  ########################################################################################################################
  # a function to control what should Watson Assistant send to User
  ######################################################################################################################## 


    #get the tone from Tone Analyser
    tone_response= self.tone_analyser.tone(tone_input = message, content_type='text/plain').get_result()
    
    #if there is emotion
    if tone_response['document_tone']['tones'] != []:
      #get response from Watson Assistant based on the tone
      user_tone = tone_response['document_tone']['tones'][0]['tone_id']
      watson_response = self.assistant_send_text(emotion = user_tone)
      
      if 'output' in watson_response:
        response = watson_response['output']['text'][0]
    
    else:

      #We assume user does not send a message with a tone
      watson_response = self.assistant_send_text(message)
      if 'output' in watson_response:
        response = watson_response['output']['text'][0]
      
      
      
      #in Watson Assistant, topic is a context variable for set up the query in Watson Discovery
      if 'topic' in watson_response['context']:
        self.post_to_slack("Ok let me search that topic", channel)
        discovery_response = self.discovery.query(
          environment_id="system", #get the environment id from collection
          collection_id="news-en", # get the collection id from collection
          query=watson_response['context']['topic'], 
          return_fields='text').get_result()
        response = discovery_response['results']
    
    
    #send the response from Watson Assistant to Slack
    self.post_to_slack(response, channel)
       

  def run(self):
    if self.slack_client.rtm_connect():
      print("Caring Bot is connected and running!")
      while True:
        slack_output = self.slack_client.rtm_read() #read
        message, channel= self.parse_slack_output(slack_output) 
        
        if message and channel:
          self.handle_message(message, channel)
        
        time.sleep(self.delay)
    else:
      print("Connection failed. Invalid Slack token or bot ID?")
