import pickle
import os

#Constants
MAX_HEALTH = 20
MAX_SANITY = 20
SANITY_PER_TURN = 3
TRAIT = ""
WOODEN_STAKE = "WOODEN STAKE"
SILVER_SICKLE = "SILVER SICKLE"
HOLY_WATER = "HOLY WATER"
CURRENT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
FRAME_FILE = CURRENT_DIRECTORY + "frame.png"
FRAME_INITIAL = CURRENT_DIRECTORY + "frame_initial.png"
REPLACE_COLOR = makeColor(236,0,133)

class frame:
  def __init__(this): #Get resources in file path to create initial frame
    this.timeOfDay = 8
    this.skyColor = makeColor(255,173,160)
    this.initialFrame = makePicture(FRAME_FILE) #TODO
    this.mainFrame = ""
    this.night = False
    #Paint avatar
    this.avatarPicture = makePicture(CURRENT_DIRECTORY + "avatar.jpg")
    
    this.avatarHeight = getHeight(this.avatarPicture)
    this.avatarWidth = getWidth(this.avatarPicture)
    
    this.divideHeight = this.avatarHeight/50
    this.divideWidth = this.avatarWidth/50
    
    this.newAvatarPicture = makeEmptyPicture(50,50)
    for x in range(0,50):
      for y in range(0,50):
        o = getPixel(this.avatarPicture, x * this.divideWidth, y * this.divideHeight)
        setColor(getPixel(this.newAvatarPicture,x,y), getColor(o))
    
    this.placeStartWidth = 16
    this.placeEndWidth = 66
    this.placeStartHeight = 224
    this.placeEndHeight = 274
    
    
    for x in range(16, 66):
      for y in range(224, 274):
        o = getPixel(this.initialFrame, x, y)
        if(distance(REPLACE_COLOR, getColor(o)) < 10):
          setColor(o, getColor(getPixel(this.newAvatarPicture, x - 16, y - 224)))
    
    #Write frame initial to disk, to be used later    
    writePictureTo(this.initialFrame, FRAME_INITIAL)
    this.repaintMainFrame()
    #this.mainFrame = makePicture(FRAME_INITIAL)
    show(this.mainFrame)
    
    
  
    #Initial frame will be the frame to be painted
    #Will paint the frame with everything minus the stats
    #Stats to be painted later
    #Frame to be painted to is the mainFrame
    #MainFrame will always deepcopy the initial frame to copy over the data
    #Possibly cache "new" frames for different times of day for speed effeciency, however loadtime will be rough
  
  def paintPortait(this, frame):
    print("Painting portrait")
    #Replace the pink/purple pixels in the frame in a certain area with the picture given
    return frame
  
  
  def repaintMainFrame(this): #Gets main frame, repaints it
    this.mainFrame = makePicture(FRAME_INITIAL)
    for x in range(0, getWidth(this.mainFrame)):
      for y in range(0, 125):
        o = getPixel(this.mainFrame, x, y)
        if(distance(REPLACE_COLOR, getColor(o)) < 100):
          setColor(o, this.skyColor)
    
    repaint(this.mainFrame)
    
  def paintStats(this): #Should be called whenever sanity or health gets updated
    print("Repainting stats!")
    
   
  
  def updateTimeOfDay(this):
    print("Painting the time of day!")  
    if(this.timeOfDay == 7):
      print("Sun down")
      this.skyColor = makeColor(227,168,87) 
    elif(this.timeOfDay == 5): 
      print("Passing the horizon")
      this.skyColor = makeColor(255, 213, 156)
    elif(this.timeOfDay <= 3 and this.night == False):
      print("Night")
      this.night = True
      this.skyColor = makeColor(38,38,38)
      showInformation("The sun has gone down, Dracula is on his way!")
    this.timeOfDay = this.timeOfDay - 1
   
  def setTimeOfDay(this, time):
    this.timeOfDay = time
  def getTimeOfDay(this):
    return this.timeOfDay

class inventory:

  # Members
  def __init__(this):
    this.contents = list()
  
  # Methods
  def addItem(this, item):
    this.contents.append(item)
        
  def removeItem(this, item):
    this.contents.remove(item)
    
  def hasItem(this, item):
    for i in range(0, len(this.contents)):
      if this.contents[i] == item:
        return true
    return false
    
  def printItems(this):
    printNow("Inventory:")
    for i in range(0, len(this.contents)):
      printNow("   " + this.contents[i])
      
# === ACTION ===
class action:
  
  # Members
  def __init__(this, description):
    this.description = description
    this.callback = 0
  
  # Methods
  def getDescription(this):
    return this.description
  
  def setCallback(this, callback):
    this.callback = callback
      
# === ROOM ===
class room:

  # Members
  def __init__(this, name):
    this.name = name
    this.description = ""
    this.inventory = inventory()
    this.actions = list()
    this.data = 0
  
  # Methods
  def setDescription(this, description):
    this.description = description
    
  def getInventory(this):
    return this.inventory
    
  def addAction(this, action):
    this.actions.append(action)
  
  def removeAction(this, action):
    this.actions.remove(action)  
  
  def takeAction(this, number):
    if(number.isnumeric()):
      number = int(number)
      number = number - 1
      for i in range(0, len(this.actions)):
        if i == number:
          this.actions[i].callback()
          return 1
    showInformation("I don't understand, please make sure you are using a valid number!")
    return 0
    
  def getData(this):
    return this.data
  
  def addData(this):
    this.data = this.data + 1
  #def printActions(this):
  #  for i in range(0, len(this.actions)):
  #    number = this.actions[i].getNumber()
  #    description = this.actions[i].getDescription()
  #    printNow("%s. %s"  % (number,description))  
  def buildActions(this):
    built = this.name + "\n" + this.description + "\n" + "What do you want to do?" + "\n"
    for i in range(0, len(this.actions)):
      number = i + 1
      description = this.actions[i].getDescription()
      built += "%s. %s \n" %(number, description)
    return built
# === PLAYER ===
class player:
  
  # Members
  def __init__(this):
    this.currentRoom = 0
    this.inventory = inventory()
    this.health = MAX_HEALTH
    this.sanity = MAX_SANITY
  
  # Methods
  def setCurrentRoom(this, newRoom):
    this.currentRoom = newRoom
    #this.currentRoom.showDescription()
    
  def getCurrentRoom(this):
    return this.currentRoom

  def getInventory(this):
    return this.inventory
    
  def addHealth(this, healthToAdd):
    this.health += healthToAdd
  
  def getHealth(this):
    return this.health
  
  def damage(this, amount):
    this.health -= amount
    if(this.health <= 0):
      showInformation("Oh dear you are dead")
      global turns
      turns = 0
      #Do death condition
  
  def getSanity(this):
    return this.sanity
  
  def removeSanity(this, sanity):
    this.sanity -= sanity
    if(this.sanity <= 0):
      showInformation("As you break down crying, you become concious and you are inside a holding cell. You hear a faint clicking noise and turn around. Dracula has bitten you...")
      global turns
      turns = 0
      
  def addSanity(this, sanity):
    this.sanity += sanity
      #Do sanity condition
###### Game variables ######
turns = 8
player = player()
end = False
frame = frame()
#TODO Add "fake" room and add actions for different traits
#Traits will effect later game

###### Global Actions ######
#Actions to be added to all rooms besides the fake room

###### Rooms ######

fakeRoom = room("")
fakeRoom.setDescription("There is a murder in your small town of 100 people.")

outsideCastleRoom = room("Dracula's Castle")
outsideCastleRoom.setDescription("You are outside Dracula's castle in Transylvania")

townRoom = room("Old town")
townRoom.setDescription("You are in an old semi-abandoned town you see the remanents of buildings. There are very few people on the street, everyone is heading indoors.")

forestRoom = room("Forest")
forestRoom.setDescription("You are in a heavily dense forest, you feel like something could attack you at any moment. Oddly enough this forest has a trail.\nThere is a fork in the road.")

bottomHillRoom = room("Hill Bottom")
bottomHillRoom.setDescription("You are now at the bottom of the hill, on top of the hill you can see an old church!")

topHillRoom = room("Hill Top")
topHillRoom.setDescription("You are at the top of the hill, the doors to the nearby church are swung open.")

churchRoom = room("Church")
churchRoom.setDescription("The wind is blowing through the church, there is an odd chill. You approach the pulpit.")

churchRoomDracula = room("Church")
churchRoomDracula.setDescription("The doors of the church fly off, Dracula has appeared!")

#Add player to first room
player.setCurrentRoom(outsideCastleRoom)
#player.setCurrentRoom(fakeRoom)
#Set player to fake room instead
#Add actions for fake room
def braveCallBack():
  TRAIT = "BRAVE"
  player.setCurrentRoom(outsideCastleRoom)

def observantCallBack():
  TRAIT = "OBSERVANT"
  player.setCurrentRoom(outsideCastleRoom)

trackDownAction = action("I would track down the killer and report them to the police!")
trackDownAction.setCallback(braveCallBack)
observantAction = action("I would help the police gather information, only a fool would to to find a killer!")
observantAction.setCallback(observantCallBack)
fakeRoom.addAction(trackDownAction)
fakeRoom.addAction(observantAction)

#Add actions for outside castle
def moatCallBack():
  player.damage(10)
  showInformation("As you jump into the moat the current takes you away, you end up in an old town. You seem to be pretty beaten up.")
  player.setCurrentRoom(townRoom)

def forestCallBack():
  showInformation("You gallop into the forest, as you traverse deeper something seems off.")
  player.setCurrentRoom(forestRoom)


moatAction = action("Jump into the moat")
moatAction.setCallback(moatCallBack)
forestAction = action("Go into forest")
forestAction.setCallback(forestCallBack)
outsideCastleRoom.addAction(moatAction)
outsideCastleRoom.addAction(forestAction)

#Add forest actions
def forkLeftCallBack():
  if(player.getCurrentRoom().getData() == 0):
    showInformation("As you go around the fork in the road you notice you are back in the same spot. This is a bit odd....")
    showInformation("You realize that your cognitive skills have taken a hit, you aren't sure what you are doing anymore")
    player.removeSanity(10)
    player.getCurrentRoom().addData()
    player.setCurrentRoom(forestRoom)
  elif(player.getCurrentRoom().getData() == 1):
    frame.setTimeOfDay(3)
    showInformation("You are now on the top of a hill, from here you can see the town.")
    player.setCurrentRoom(topHillRoom)

def forkRightCallBack():
  player.setCurrentRoom(townRoom)

leftForkAction = action("Go left")
leftForkAction.setCallback(forkLeftCallBack)
rightForkAction = action("Go right")
rightForkAction.setCallback(forkRightCallBack)
forestRoom.addAction(leftForkAction)
forestRoom.addAction(rightForkAction)

#Add town actions
bandageAction = action("Find someone who can fix me up")
bottomHillAction = action("Go to the bottom of the hill")

def bandageCallBack():
  if(player.getHealth() < MAX_HEALTH):
    showInformation("You approach a person who seems to run an apothecary. They see how banged up you are and bandage you up. You feel slightly better. The person who bandaged you up walks inside and locks the door")
    halfHealth = (MAX_HEALTH - player.getHealth()) / 2
    player.addHealth(halfHealth)
  else:
    showInformation("You realize it would be pointless for you to get bandaged as you aren't even hurt!")

  player.getCurrentRoom().removeAction(bandageAction)

def bottomHillCallBack():
  showInformation("You slothfully travel through the town, you start going up a slight incline.")
  player.setCurrentRoom(bottomHillRoom)


bandageAction.setCallback(bandageCallBack)
bottomHillAction.setCallback(bottomHillCallBack)

townRoom.addAction(bandageAction)
townRoom.addAction(bottomHillAction)

#Bottom hill actions
def bottomToTopHillCallBack():
  showInformation("You begrudgingly make your way up the hill")
  showInformation("You are starting to lose the will to live, you start thinking that you should have just let Dracula take you.")
  player.removeSanity(8)
  if(player.getSanity() > 0):
    player.setCurrentRoom(topHillRoom)

topHillAction = action("Trek up the hill")
topHillAction.setCallback(bottomToTopHillCallBack)
bottomHillRoom.addAction(topHillAction)

#Top hill actions
def topHillChurchCallBack():
  #If time of day is > 3, set to night time
  showInformation("You enter the old musty church, it seems to have been used just recently.")
  player.setCurrentRoom(churchRoom)

topHillChurchAction = action("Enter the church")
topHillChurchAction.setCallback(topHillChurchCallBack)
topHillRoom.addAction(topHillChurchAction)

#Church actions
# -> Make dracula appear after next action
#Depending on choice made in the church is whether or not the player survives

def grabWoodenStakeCallBack():
  player.getInventory().addItem(WOODEN_STAKE)
  global turns
  turns = 100
  player.setCurrentRoom(churchRoomDracula)
  

def grabSilverSickleCallBack():
  player.getInventory().addItem(SILVER_SICKLE)
  global turns
  turns = 100
  player.setCurrentRoom(churchRoomDracula)

def grabHolyWaterCallBack():
  player.getInventory().addItem(HOLY_WATER) 
  global turns
  turns = 100
  player.setCurrentRoom(churchRoomDracula)
  
  
woodenStakeAction = action("Grab wooden stake")
woodenStakeAction.setCallback(grabWoodenStakeCallBack)

silverSickleAction = action("Grab silver sickle")
silverSickleAction.setCallback(grabSilverSickleCallBack)

holyWaterAction = action("Grab holy water")
holyWaterAction.setCallback(grabHolyWaterCallBack)

churchRoom.addAction(woodenStakeAction)
churchRoom.addAction(silverSickleAction)
churchRoom.addAction(holyWaterAction)

#Church room dracula
def fightDraculaCallback():
  player.addSanity(100)
  showInformation("Dracula flies toward you")
  if(player.getInventory().hasItem(WOODEN_STAKE)):
    global end
    end = True
    showInformation("You stab Dracula with the stake, he withers away and you are free!")
  else:
    showInformation("You have nothing to defend yourself with, Dracula bites you...")
    global turns
    turns = 0

fightAction = action("Fight Dracula")
fightAction.setCallback(fightDraculaCallback)
churchRoomDracula.addAction(fightAction)


#Add resting to all rooms
def restCallBack():
  half = ((MAX_SANITY - player.getSanity()) / 2) + SANITY_PER_TURN
  player.addSanity(half)
  showInformation("You feel rested")
  
rest = action("Rest")
rest.setCallback(restCallBack)
outsideCastleRoom.addAction(rest)
forestRoom.addAction(rest)
townRoom.addAction(rest)
bottomHillRoom.addAction(rest)
topHillRoom.addAction(rest)
churchRoom.addAction(rest)

#BEFORE GAME
#NAME = requestString("Before the game starts, we like to get to know a little about the person who is playing. So lets start off with your name")
#showInformation("This next question is a hypothetical and is not part of the game. Any time during the game if you need help just type HELP in the dialog box to be reminded of how to play the game. Best of luck with Escaping from Transylvania!")

def showHelp():
  printInformation("If at any time you want to stop you can press the STOP button. Input numbers for the given actions. Remember your time, health and well being are all limited! Remember to make use of the rest option!")

while True:
  if(end):
    showInformation("Congratulations you win, play again to find all the secrets!")
    break
  
  if(turns <= 0):
    showInformation("I am sorry but you have lost the game, better luck next time!")
    break
    
  if(player.getSanity() <= 0):
    break
  
  playerInput = requestString(player.getCurrentRoom().buildActions())
  if playerInput.upper() == "HELP":
    showHelp()
  else:
    val = player.getCurrentRoom().takeAction(playerInput)
    if(player.getSanity() <= 0):
      break
    if(val == 1):
      turns -= 1
      player.removeSanity(SANITY_PER_TURN)
      frame.updateTimeOfDay()
      frame.repaintMainFrame()
    else:
      continue
