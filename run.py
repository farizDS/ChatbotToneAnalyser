import json
import os
import time
#from dotenv import load_dotenv
from slackclient import SlackClient
import ibm_watson
from caring.caring import CaringBot

if __name__ == "__main__":
   
   
  ########################################################################################################################
  # Start Watson Assistant service using your credentials
  ########################################################################################################################
  conversation_client = ibm_watson.AssistantV1(
    iam_apikey = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx', # replace with apikey
    url = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx', # replace with Watson Assistant's Credentials - URL
    version = '2018-09-20'
  )
  workspace_id = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx' # replace with Skill ID
  
  ########################################################################################################################
  # Start Watson Tone Analyser service using your credentials
  ########################################################################################################################
  tone_analyser = ibm_watson.ToneAnalyzerV3(
    version='2017-09-21',
    url='xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx', #replace with gateway URL
    iam_apikey='xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'  #replace with apikey
  )

  ########################################################################################################################
  # Start Watson Discovery service using your credentials
  ########################################################################################################################
  discovery_client = ibm_watson.DiscoveryV1(
        version='2018-08-01',
        url='https://gateway-syd.watsonplatform.net/discovery/api', #replace with gateway URL
        iam_apikey='xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'#replace with apikey
  )


  ########################################################################################################################
  # Start Slack service using Bot Token
  ########################################################################################################################
  SLACK_BOT_TOKEN='xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx' #replace with Bot token
  slack_client = SlackClient(SLACK_BOT_TOKEN)
  
  ########################################################################################################################
  # Start the program
  ########################################################################################################################
  caring_bot = CaringBot(slack_client, 
                      conversation_client,
                      workspace_id,
                      tone_analyser,
                      discovery_client
                      )
  caring_bot.run()
