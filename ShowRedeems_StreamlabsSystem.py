# -*- coding: utf-8 -*-

# ShowRedeems by luissanchezdev
#   Show all rewards redeemed on Twitch using channel
#   points directly on your Streamlabs Chatbot Console.
# 
# Versions
#   1.0.0 - Release

import os
import sys
import clr
import time
import json
import codecs
import System

# Include the assembly with the name AnkhBotR2
clr.AddReference([asbly for asbly in System.AppDomain.CurrentDomain.GetAssemblies() if "AnkhBotR2" in str(asbly)][0])
import AnkhBotR2

# Twitch PubSub library and dependencies
lib_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "Lib")
clr.AddReferenceToFileAndPath(os.path.join(lib_path, "Microsoft.Extensions.Logging.Abstractions.dll"))
clr.AddReferenceToFileAndPath(os.path.join(lib_path, "TwitchLib.Communication.dll"))
clr.AddReferenceToFileAndPath(os.path.join(lib_path, "TwitchLib.PubSub.dll"))
from TwitchLib.PubSub import *
from TwitchLib.PubSub.Events import *

# I wasn't able to use Parent.GetRequest :( so I used this instead
clr.AddReference("System.Net.Http")
from System.Net.Http import HttpClient

# Simple message box fordebugging
clr.AddReference("System.Windows.Forms")
from System.Windows.Forms.MessageBox import Show
msgbox = lambda obj: Show(str(obj))

# Script Information
Creator = "LuisSanchezDev"
Description = "Show all rewards redeemed on Twitch using channel points directly on your Streamlabs Chatbot Console"
ScriptName = "ShowRedeems"
Version = "1.0"
Website = "https://www.fiverr.com/luissanchezdev"

# Define Global Variables
path = os.path.dirname(os.path.realpath(__file__))
client = None

# Initialize Data (Only called on load)
def Init():
  # Get OAuth token
  # vmloc = AnkhBotR2.Managers.GlobalManager.Instance.VMLocator
  oauth = GetOAuth()
  
  # .Net Get request to get streamer's ID
  auth = 'OAuth ' + oauth.replace("oauth:", "")
  httpclient = HttpClient()
  httpclient.DefaultRequestHeaders.Add("Authorization", auth)
  t = httpclient.GetStringAsync("https://id.twitch.tv/oauth2/validate")
  data = ""
  try:
    t.Wait()
    data = t.Result
  except:
    msgbox("There was an error while authenticating\nPlease reload the scripts to try again\n\n" + str(t.Exception))
    return
  casterid = json.loads(data)['user_id']

  # Create a Twitch.PubSub client and register to listen to reward redeems
  client = TwitchPubSub();
  def connected(s, e):
    client.SendTopics()
  def reward(s, e):
    message = "👉 " + e.DisplayName + " redeemed " + e.RewardTitle
    message += " - " + e.RewardPrompt
    _print(message)
    if e.Message:
      _print("📧 Message: " + e.Message)
  
  client.OnPubSubServiceConnected += connected
  client.OnRewardRedeemed += reward
  client.ListenToRewards(casterid)
  client.Connect()

# Execute Data / Process messages
def Execute(data):
  pass

# Tick method (Gets called during every iteration even when there is no incoming data)
def Tick():
  pass

def GetOAuth():
  vmloc = AnkhBotR2.Managers.GlobalManager.Instance.VMLocator
  return vmloc.StreamerLogin.Token

def _print(msg):
  g_manager = AnkhBotR2.Managers.GlobalManager.Instance
  handler = g_manager.SystemHandler
  handler.StreamerClient.PrintServerMessage(msg)
  #public void PrintMessage(string user = "", string message = "", IncTwitchMessage ircMessage = null)
  handler.StreamerClient.WriteTextToUI()

def donate():
  os.startfile("https://streamlabs.com/luissanchezdev/tip")