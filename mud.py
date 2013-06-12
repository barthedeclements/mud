import sys
import dung
import time

def RunMud(username):
  start_room = dung.Room()
  player = dung.Person(username)
  #player.inventory['torch']=[dung.Item('torch', 'bla', 'bla')]
  path01 = dung.Room()
  path02 = dung.Room()
  path03 = dung.Room()
  tree_room = dung.Room()
  tree_top = dung.Room()
  
  start_room.description = 'A dead-end road.'
  start_room.exits['north'] = path01
  start_room.contents['shovel'] = [dung.Item('shovel', 'A shovel', 'A shovel you could dig with')]
  start_room.internal_contents['road'] = [dung.Item('road', 'A dead-end road. Pretty boring, really.', 'A dead-end road. Pretty boring, really.')]

  path01.description = 'You are standing on a grassy path.'
  path01.exits['south'] = start_room
  path01.exits['north'] = path02
  path01.internal_contents['path'] = [dung.Item('path', 'A well-tread path with matted grass.', 'A well-tread path with matted grass.')]
  path01.internal_contents['grass']  = [dung.Item('grass', 'Matted grass... what are you looking for exactly?', 'Matted grass... what are you looking for exactly?')]

  path02.description = 'You are standing on a path. Some bushes grow by the side of the road.'
  path02.exits['south'] = path01
  path02.exits['north'] = path03
  path02.internal_contents['bushes'] = [dung.Item('bushes', 'Some bushes', 'Some thick bushes growing by the side of the road... was that a glint of metal you saw?')]
  path02.hidden_contents['hook'] = [dung.HiddenItem('hook', 'A grappling hook', 'A grappling hook that could be useful in climbing a tree.', 'bushes')]

  path03.description = 'You are standing on a path.'
  path03.exits['south'] = path02
  path03.exits['west'] = tree_room
  
  tree_room.description = 'You are standing next to a large tree.'
  tree_room.exits['east'] = path03
  tree_room.hidden_exits['tree'] = tree_top
  tree_room.internal_contents['tree'] = [dung.Item('tree', 'A tall tree. Perhaps you can climb it?', 'A tall tree. Perhaps you can climb it?')]
  #tree_room.commands['climb'] = Climb
  
  tree_top.description = 'The top of a tall tree. Congratulations, you won the game.'
  tree_top.exits['down'] = tree_room

  RunLoop(player, start_room)

def IntroSequence():
  sys.stdout.write('\n \n   Welcome!     \n \n \n')
  sys.stdout.write('Please enter your name: ')
  u_input = sys.stdin.readline()
  user_name = u_input[:-1]
  user_name = user_name.title()
  sys.stdout.write('\n'+ 'Hello, %s. Please have a look around! \n' % user_name)
  sys.stdout.write('Valid commands include: look, exa, search, get, drop, i...\n\n')
  return user_name

def PrintRoom(room):
  obvious_exits = []
  for x in room.exits:
    if len(obvious_exits)==0:
      obvious_exits.append(x)
    elif len(obvious_exits)>0:
      obvious_exits.append(', ' + x)
  contents_descriptions = []
  for x in room.contents.values():
    for item in x:
      if len(contents_descriptions)==0:
        contents_descriptions.append(item.description)
      elif len(contents_descriptions)>0:
        contents_descriptions.append(', ' + item.description.lower())
  sys.stdout.write(room.description)
  if len(contents_descriptions)>0:
    sys.stdout.write('\n'+''.join(contents_descriptions) + '.')
  sys.stdout.write('\nThe only obvious exits are: '+''.join(obvious_exits)+'.\n')
  return room 
  
def TryToGo(room, direction):
  if direction in room.exits:
    sys.stdout.write('You leave %s.\n' %direction)
    PrintRoom(room.exits[direction])
    return room.exits[direction]
  else:
    sys.stdout.write('There is no obvious exit %s.\n' %direction)
    return room



def RunLoop(player, room):
  PrintRoom(room)
  player.room=room
  
  while True:
   sys.stdout.write('> ')
   user_input = sys.stdin.readline()
   user_words = user_input[:-1].split(' ')
   
   if user_words[0] == 'quit':
      sys.stdout.write('You quit the game.\n')
      break
   
   if user_words[0] == 'n':
     user_words[0] = 'north'
   if user_words[0] == 's':
     user_words[0] = 'south'
   if user_words[0] == 'e':
     user_words[0] = 'east'
   if user_words[0] == 'w':
     user_words[0] = 'west'
   if user_words[0] == 'u':
     user_words[0] = 'up'
   if user_words[0] == 'd':
     user_words[0] = 'down'
       
   if user_words[0] in ['north', 'south', 'east', 'west', 'up', 'down']:
     room=TryToGo(room, user_words[0])
     player.room = room
     
   if user_words[0] in room.commands:
     room = room.commands[user_words[0]](room, *user_words[1:])
     player.room=room
       
   if user_words[0] in player.commands:
     player = player.commands[user_words[0]](player, *user_words[1:])     
     room = player.room

if __name__ == '__main__':
  RunMud(IntroSequence())
  
  
  
