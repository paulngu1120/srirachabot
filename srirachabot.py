#!/usr/bin/python

import socket, re, subprocess, os, time, threading, sys

server = "kukki.asuscomm.com" # Server
channel = "#general" # Channel
botnick = "SrirachaBot" 
exitcode = botnick + "Cha"
lines = 0

ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ircsock.connect((server, 6667)) # Here we connect to the server using the port 6667
ircsock.send("USER "+ botnick +" "+ botnick +" "+ botnick + " " + botnick + "\n") # user authentication
ircsock.send("NICK "+ botnick +"\n") # assign the nick to the bot

def ping(): # respond to server Pings.
  ircsock.send("PONG :pingis\n")  

def sendmsg(msg): # sends messages to the channel.
  ircsock.send("PRIVMSG "+ channel +" :"+ msg +"\n") 

def joinchan(chan): # join channel(s).
  ircsock.send("JOIN "+ chan +"\n")

def whisper(msg, user): # whisper a user 
  ircsock.send("PRIVMSG " + user + ' :' + msg.strip('\n\r') + '\n')

# log chat messages
def logger(name, msg):
  # loop through the content of the chat log and reduce to 100 lines, starting with oldest. --Definitely a better way to do this, needs improvement.
  irclog = open("ircchat.log", 'r')
  content = irclog.readlines()
  irclog.close()
  # loop through the content of the chat log and reduce to 100 lines, starting with oldest. --Definitely a better way to do this, needs improvement.
  irclog = open("ircchat.log", "w")
  while len(content) > 100:
    content.remove(content[0])
  if len(content) > 0:
    for i in content:
      irclog.write(i.strip('\n\r') + '\n')
  # write newest messge to log.
  irclog.write(name + ':' + msg.strip('\n\r'))
  irclog.close()

def help(name,topic=''):
  message = ''
  # if no help topic is specified, send general help message about the bot.
  if topic == '':
    message = "Hi! I am SrirachaBot, made by pieceOniece. I can't do anything yet."
  # if a help message is specified, let the user know it's not coded yet.
  else:
    message = "Feature not yet implemented, sorry. Please see the main help (message me with \'.help\')"
  print(topic)
  # send help message in whisper to user.
  sendmsg(message)

def main():
  joinchan(channel)
  with open("ircchat.log", "w") as temp:
    temp.write("")
  while 1: 
    ircmsg = ""
    ircmsg = ircsock.recv(2048)
    ircmsg = ircmsg.strip('\n\r') 
    # For debugging
    print(ircmsg) 
    if ircmsg.find("PING :") != -1: 
      ping()
    # look for PRIVMSG lines as these are messages in the channel or sent to the bot
    if ircmsg.find("PRIVMSG") != -1:
      # save user name into name variable
      name = ircmsg.split('!',1)[0][1:]
      print('name: ' + name)
      # get the message to look for commands
      message = ircmsg.split('PRIVMSG',1)[1].split(':',1)[1]
      print(message)
      # look for commands and send to appropriate function.
      if message[:17] == '.' + botnick + ' ' +'find':
	sendmsg("Find what!?")
      elif message[:19] == '.' + botnick + ' ' + 'tellme':
	sendmsg("Tell you a joke?")
      elif message[:5] == '.help':
        help(name,message[5:])
      else:
      # if no command found, get 
        if len(name) < 17:
          logger(name, message)
          # if the final message is from me and says ' [bot]' stop the bot and exit. Needs adjustment so it works for main user account and not hardcoded username.
          if name.lower() == "piece" and message.rstrip() == exitcode:
            sendmsg("Heroes never die!")
            ircsock.send("PART " + channel + "\r\n")
            sys.exit()

main()

