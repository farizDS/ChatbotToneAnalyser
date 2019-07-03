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
    iam_apikey = 'lHAJzMnAM5YXYlM46pLcmWEpY0wO4PvUaAxpPbLbTRAu', # replace with apikey
    url = 'https://gateway.watsonplatform.net/assistant/api/', # replace with Watson Assistant's Credentials - URL
    #iam_apikey = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx', # replace with apikey
    #url = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx', # replace with Watson Assistant's Credentials - URL
    version = '2018-09-20'
  )
  workspace_id = '4135b1d0-1370-41ac-a762-bdb0dd843e2f' # replace with Skill ID
  #workspace_id = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx' # replace with Skill ID
  
  ########################################################################################################################
  # Start Watson Tone Analyser service using your credentials
  ########################################################################################################################
  tone_analyser = ibm_watson.ToneAnalyzerV3(
    version='2017-09-21',
    url='https://gateway.watsonplatform.net/tone-analyzer/api', #replace with gateway URL
    iam_apikey='tzqIsKTxNCPNUUzi-UAf7J_LwQxpKs9rapS4RyTUaNsU'  #replace with apikey
    #url='xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx', #replace with gateway URL
    #iam_apikey='xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'  #replace with apikey
  )

  ########################################################################################################################
  # Start Watson Discovery service using your credentials
  ########################################################################################################################
  discovery_client = ibm_watson.DiscoveryV1(
        version='2018-08-01',
        url='https://gateway-syd.watsonplatform.net/discovery/api', #replace with gateway URL
        iam_apikey='CP_6rqFSuH4gwOuM2GyTbO9yFOylC904-y1T0UnSK42m'#replace with apikey
        #iam_apikey='xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'#replace with apikey
  )


  ########################################################################################################################
  # Start Slack service using Bot Token
  ########################################################################################################################
  SLACK_BOT_TOKEN='xoxb-597388589376-680868079936-b5e0pWZUd3xMFauqJLJjCIey'
  #SLACK_BOT_TOKEN='xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx' #replace with Bot token
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