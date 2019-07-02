import re
import json
import os
import time
from slackclient import SlackClient

from pprint import pprint

class CaringBot:
  def __init__(self,slack_client, conversation_client, workspace, tone_analyser):
    bot_id = slack_client.api_call("auth.test")["user_id"]
    self.slack_client = slack_client
    self.conversation_client = conversation_client
    self.delay = 0.5 #second
    self.workspace_id = workspace
    self.bot_id = bot_id
    self.context = {}
    self.tone_analyser = tone_analyser
    
  
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
    print("now running post_to_slack")   
    self.slack_client.api_call("chat.postMessage", 
                          channel=channel,
                          text=response, as_user=True)
  
  ########################################################################################################################
  # Configuration about how to handle any input from user
  ######################################################################################################################## 

  def handle_message(self, message, channel):
    print("now running handle_message")
    
    #get the tone from Tone Analyser
    tone_response= self.tone_analyser.tone(tone_input = message, content_type='text/plain').get_result()
    if tone_response['document_tone']['tones'] == []:
      user_tone = None
      watson_response = self.conversation_client.message(workspace_id=self.workspace_id, 
      input={'text': message}).get_result()
    else:
      #get response from Watson Assistant based on the tone
      user_tone = tone_response['document_tone']['tones'][0]['tone_id']
      watson_response = self.conversation_client.message(workspace_id=self.workspace_id, 
      context={"emotion": str(user_tone)}).get_result()
      
        
    if 'output' in watson_response:
      response = watson_response['output']['text'][0]

    #send the response from Watson Assistant to Slack
    self.post_to_slack(response, channel)
       

  def run(self):
    if self.slack_client.rtm_connect():
      print("Caring Bot is connected and running!")
      while True:
        slack_output = self.slack_client.rtm_read()
        message, channel = self.parse_slack_output(slack_output)
        print(message)
        if message and channel:
          self.handle_message(message, channel)
        time.sleep(self.delay)
    else:
      print("Connection failed. Invalid Slack token or bot ID?")
