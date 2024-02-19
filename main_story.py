# All the imports to be used in the program
import os
import re
import time
import random
from json import JSONDecodeError
from typing import Optional
from stdiomask import getpass
import hashlib
import json
import csv


import pygame
import math
from pygame.locals import *

from classes import user, Room, Item, HitlerSubordinates, Allies, Team, Hitler
from caesarcipher import CaesarCipher
from random import randint

# Instantiation
# Creating Objects to assign to characters or rooms
Room_Key = Item('broadcast room key')
knife = Item('knife')
Gun = Item('gun')
poison_vial = Item('poison vial')
revolver = Item('revolver')
cyanide = Item('cyanide')
pistol = Item('pistol')
poison_dart = Item('poison dart')
dagger = Item('dagger')
sheriff_deagle = Item('deagle')
dual_pistols = Item('dual pistols')
arsenic_injections = Item('arsenic injections')

# Room Declarations
main_hall = Room("Main Hall", "This the enthralling main hallway of the the Fuhrer himself, proceed with caution", None)
generals_room = Room("Generals' Room", 'This is where all the strategic plans are laid out', Room_Key)
broadcast_room = Room("The Broadcast Room", "The department that makes sure Germans get their daily dose of propaganda",
                      None)
dining_hall = Room("Dining Hall", "A communal place for all the soldiers to meet, greet and eat", cyanide)
shooting_range = Room("The Shooting Range", "The range where soldiers are required to practice their aim", None)
main_hall.link_room(generals_room, "east")
generals_room.link_room(main_hall, "west")
main_hall.link_room(dining_hall, 'west')
dining_hall.link_room(main_hall, 'east')
dining_hall.link_room(broadcast_room, 'north')
broadcast_room.link_room(dining_hall, 'south')
generals_room.link_room(shooting_range, "south")
shooting_range.link_room(generals_room, "north")

# Character Declarations
General_Aladeen = HitlerSubordinates('Aladeen', 'General', 'In charge of ammunition and organized sieges', 2,
                                     'knife', 2, 4, 'kids')
Dining_Hall_Soldier = HitlerSubordinates('Sawcon', 'Private', 'In charge of the dining hall mess', 1, 'gun', 3, 3,
                                         'body')
hitler = Hitler('Adolf Hitler', 'Fuhrer', 'The Fuhrer of the Reich', None, 'cyanide', None, 15)

# Assigning objects to Characters
Dining_Hall_Soldier.change_inventory(Room_Key, True)
General_Aladeen.change_inventory(Gun, True)
hitler.add_items(poison_vial, revolver, pistol, poison_dart)

# Variable Declarations for Global Variables
team_lst = []
user1: Optional[user] = None
Team1: Optional[Team] = None
General_Aladeen_Combat: Optional[Allies] = None
Guard_Gorbachev: Optional[Allies] = None
Private_Sawcon: Optional[Allies] = None
Camp_Officer: Optional[Allies] = None

# Data Set Declaration
data = {
    'Username': None,
    'Password': None,
    'Name': None,
    'Attributes': None,
    'Dining Hall Speech': None,
    'Inventory': None,
    'Score from Brick Game': None,
    'Shooting range score': None,

}


def updateUserObject(user_data: dict):  # replaces user data to update the file (searches for same username)
    if 'Username' not in user_data:
        return

    with open('My record.json', 'r') as file:
        lines = file.readlines()

        for i in range(len(lines)):
            try:
                obj = json.loads(lines[i])
                if obj['Username'] == user_data['Username']:
                    lines[i] = json.dumps(user_data) + '\n'
                    break
            except JSONDecodeError:
                continue

    with open('My record.json', 'w') as file:
        file.writelines(lines)


def Add_Value_to_Data(name_, field, value):  # replaces specific field in user's data
    with open('My record.json', 'r') as file:
        lines = file.readlines()

        for i in range(len(lines)):
            try:
                obj = json.loads(lines[i])
                if obj['Username'] == name_:
                    obj[field] = value
                    lines[i] = json.dumps(obj) + '\n'
                    break
            except JSONDecodeError:
                continue

    with open('My record.json', 'w') as file:
        file.writelines(lines)


# General subroutines
def intro():
    print('You find yourself walking down a very familiar path, wishing you could alter history in anyway possible, '
          'after a long day at school of memorizing dates for important events in Nazi Regime you just wish you could '
          'really live it! Suddenly you fall into a hole and find yourself in all to familiar setting in 1945')


def login_system():
    # Helps clear the screen
    def clear_screen():
        # for mac and linux(here, os.name is 'posix')
        if os.name == 'posix':
            _ = os.system('clear')
        else:
            # for windows platform
            _ = os.system('cls')

    def Main_Menu():
        clear_screen()
        print('This is the main menu')
        print("---------")
        print()
        print('Choose: ')
        print('1 - Register')
        print('2 - Login')
        print('3 - Exit')
        choice = None
        while True:
            choice = input('> ').strip()
            if choice == '1':
                temp = Register()
                return temp
            if choice == '2':
                Login()
                break
            if choice == '3':
                exit()

    def Register():
        clear_screen()
        print('Register')
        print()
        print("---------")
        username = None
        while True:
            username = input('Enter username: ').strip()
            if username != '':
                break
        if check_for_user(username):
            displayUserAlreadyExistMessage()
        else:
            while True:
                password = getpass('Enter password: ')
                if password != '':
                    break
            while True:
                check_password = getpass('Re-enter your password: ')
                if check_password == password:
                    break
                else:
                    print('Password does not match')
                    print()
            # After username and password validation call subroutine to add to data file
            Add_User_Info(username, hash_password(password))
            return username

    def Login():
        clear_screen()
        print("LOGIN")
        print("-----")
        print()
        username = input('Enter your Username: ').strip()
        # Subroutine returns boolean value thus displays details or asks for password again
        if check_for_user(username):
            while True:
                password = getpass('Enter your password: ').strip()
                if CheckPassword(username, hash_password(password)):
                    print('You are in the system!')
                    with open('My record.json', 'r') as f:
                        for line in f.readlines():
                            try:
                                if line == '':
                                    continue
                                temp = json.loads(line)
                                if temp['Username'] == username:
                                    print('These are your details')
                                    print('Username:', temp['Username'])
                                    print('Name:', temp['Name'])
                                    print('Attributes:', temp['Attributes'])
                                    print('Dining Hall Speech:', temp['Dining Hall Speech'])
                                    print('Inventory:', temp['Inventory'])
                                    print('Score from Brick Game:', temp['Score from Brick Game'])
                                    print('Shooting range score:', temp['Shooting range score'])
                                    input('Press enter to quit\n>')
                                else:
                                    continue
                            except JSONDecodeError:
                                continue
                    quit()
                else:
                    print('Wrong password')
                    continue
        else:
            print('You are not Registered!')
            time.sleep(1)
            Main_Menu()

    def Add_User_Info(username, password):
        d = {'Username': username}
        d1 = {'Password': password}
        data.update(d)
        data.update(d1)
        j = json.dumps(data)
        with open('My record.json', 'a') as f:
            f.write(j)
            f.write('\n')
            f.close()

    def Add_New_Field(field, element):
        new = {field: element}
        data.update(new)

    # Returns boolean Values for checking
    def check_for_user(username):
        with open('My record.json', 'r') as f:
            for line in f.readlines():
                try:
                    if line == '':
                        continue
                    temp = json.loads(line)
                    if temp['Username'] == username:
                        return True
                    else:
                        continue
                except JSONDecodeError:
                    continue

    # Returns boolean Values for checking
    def CheckPassword(username, password):
        with open('My record.json', 'r') as f:
            for line in f.readlines():
                try:
                    if line == '':
                        continue
                    temp = json.loads(line)
                    if not temp['Username'] == username:
                        continue
                    elif temp['Password'] == password:
                        return True
                    else:
                        return False
                except JSONDecodeError:
                    continue

    def displayUserAlreadyExistMessage():
        while True:
            print()
            error = input("You Are Already Registered.\n\nPress (T) To Try Again:\nPress (L) To Login: ").lower()
            if error == 't':
                Register()
                break
            elif error == 'l':
                Login()
                break

    # Hashing module used to hash password
    def hash_password(password):
        return hashlib.sha256(str.encode(password)).hexdigest()

    m = Main_Menu()
    return m


def screen_clear():
    # for mac and linux(here, os.name is 'posix')
    if os.name == 'posix':
        _ = os.system('clear')
    else:
        # for windows platform
        _ = os.system('cls')


def assign_points():
    total = 8
    x1, x2, x3, x4, x5 = 0, 0, 0, 0, 0

    while total != 0:

        try:
            # abs makes sure the value is positive to avoid negative entries
            x1 = abs(int(input("charisma: ")))
            x2 = abs(int(input("passion: ")))
            x3 = abs(int(input("skill: ")))
            x4 = abs(int(input("charm: ")))
            x5 = abs(int(input("fame: ")))

            total -= x1 + x2 + x3 + x4 + x5

        except Exception:

            print("invalid input try again")
            # returns the function again
            return assign_points()

        if total < 0:
            x1 = 0
            x2 = 0
            x3 = 0
            x4 = 0
            x5 = 0
            print("u have exceeded the limit, try again ")
            return assign_points()

    # Adds the attributes and their values to json files to save
    Add_Value_to_Data(user_username, 'Attributes',
                      {'Charisma': x1, 'Passion': x2, 'Skill': x3, 'Charm': x4, 'Fame': x5})
    return x1, x2, x3, x4, x5


def user_setup():
    screen_clear()
    print("customize your character, you have 8 points to assign to your characters attributes, these points would be "
          "distributed between passion, charisma, skill, fame and charm. Any negative inputs would be taken as absolute"
          " positive values")
    charisma, passion, skill, charm, fame = assign_points()
    # Uses regular expressions to validate name to make sure to avoid numbers or blank spaces
    pattern = "[A-Za-z]+"
    name = input("name: ")
    while not re.fullmatch(pattern, name):
        name = input("invalid name try again: ")
    global user1
    # Creates user object using attributes from user input
    user1 = user(name, charisma, passion, skill, charm, fame)
    print("your charisma is:", user1.charisma)
    print("your passion is:", user1.passion)
    print("your skill is:", user1.skill)
    print("your charm is:", user1.charm)
    print('your fame is:', user1.fame)
    print("your name is :", user1.name)
    Add_Value_to_Data(user_username, 'Name', name)


def current_user_stats():
    print("your charisma is:", user1.charisma)
    print("your passion is:", user1.passion)
    print("your skill is:", user1.skill)
    print("your charm is:", user1.charm)
    print('your current hp is:', user1.hp)
    # So that the object itself isn’t printed
    lst = []
    for i in user1.inventory:
        temp = i.name
        lst.append(temp)
    print('your current inventory is:', lst)


def menu(character, room):
    # Passing character and room objects into menu subroutine to call their methods and alter their attributes
    # accordingly
    selection = 0
    tries = 0
    while selection != '6' and tries < 5:
        print("you have between 6 options:\n1) Steal from", character.name, "\n2) Search",
              room.name, "\n3) Salute", character.name, "\n4) Fight", character.name, '\n5) Compliment',
              character.name, "\n6) Exit Menu")
        selection = input("> ")
        if selection == "1":
            character.steal(user1)
            current_user_stats()
            tries += 1
            selection = 0
        elif selection == "2":
            room.search_room(user1)
            current_user_stats()
            tries += 1
            selection = 0
        elif selection == "3":
            character.salute(user1)
            current_user_stats()
            tries += 1
            selection = 0
        elif selection == "4":
            character.fight(user1)
            current_user_stats()
            tries += 1
            selection = 0
        elif selection == '5':
            character.compliment(user1)
            current_user_stats()
            tries += 1
            selection = 0
        elif selection == '6':
            current_user_stats()
            break
        else:
            continue


def binary_decision_function(expression, fn1, fn2):
    selection = 0
    print(expression)
    while selection not in ('1', '2'):
        try:
            selection = input("> ")
            if selection == '1':
                fn1()
            elif selection == '2':
                fn2()
        except Exception:
            pass


def binary_decision_general(user_defined_input, input1, input2):
    selection = 0
    while selection not in ('1', '2'):
        try:
            selection = int(input(user_defined_input))
            if selection == '1':
                print(input1)
            elif selection == '2':
                print(input2)
                pass
        except Exception:
            pass


def validation():
    temp = False
    input1 = 0
    while not temp:
        try:
            input1 = int(input("Enter (integer): "))
            temp = True
        except Exception:
            pass
        print("try again")
    return input1


# Using the caesar cipher module to encode messages
def level1(time_):
    cipher1 = CaesarCipher('Fuhrer', offset=14)
    cipher2 = CaesarCipher('War', offset=14)
    cipher3 = CaesarCipher('Rations', offset=14)
    cipher4 = CaesarCipher('Revolution', offset=14)
    cipher5 = CaesarCipher('Economy', offset=14)

    print('your offset is 14')
    print(cipher1.encoded, cipher2.encoded, cipher3.encoded, cipher4.encoded, cipher5.encoded)
    timer(time_)
    screen_clear()


def level2(time_):
    lst = []
    for x in range(5):
        lst.append(random.randint(1, 25))

    cipher1 = CaesarCipher('Fuhrer', offset=lst[0])
    cipher2 = CaesarCipher('War', offset=lst[1])
    cipher3 = CaesarCipher('Rations', offset=lst[2])
    cipher4 = CaesarCipher('Revolution', offset=lst[3])
    cipher5 = CaesarCipher('Economy', offset=lst[4])

    for x in range(len(lst)):
        print('your offset is:', lst[x])

    print(cipher1.encoded, cipher2.encoded, cipher3.encoded, cipher4.encoded, cipher5.encoded)
    timer(time_)
    screen_clear()


def level3(time_):
    lst = []
    for x in range(5):
        lst.append(random.randint(1, 25))

    cipher1 = CaesarCipher('Fuhrer', offset=lst[0])
    cipher2 = CaesarCipher('War', offset=lst[1])
    cipher3 = CaesarCipher('Rations', offset=lst[2])
    cipher4 = CaesarCipher('Revolution', offset=lst[3])
    cipher5 = CaesarCipher('Economy', offset=lst[4])
    print("a = 1 and ' = 0")

    for x in range(len(lst)):
        z = lst[x] // 10
        y = lst[x] % 10
        print('your offset is:', chr(z + 96), chr(y + 96))

    print(cipher1.encoded, cipher2.encoded, cipher3.encoded, cipher4.encoded, cipher5.encoded)
    timer(time_)
    screen_clear()


# subroutine that keeps track of active time on terminal
def timer(amount_of_time):
    t = amount_of_time
    temp = True
    while temp:
        while t != 0:
            mins = t // 60
            secs = t % 60
            timer_ = '{:02d}:{:02d}'.format(mins, secs)
            print(f"\r{timer_}", end="", flush=True)
            time.sleep(1)
            t -= 1
        temp = False


# Subroutine to transition between rooms by passing the room objects and room subroutines
def room_transition(rt_input1, rt_input2, rt_input3, rt_function1, rt_function2):
    current_state = True
    while current_state:
        print("\n")
        rt_input3.get_details()
        print("Where do you want to go: ")
        command = input("> ")
        current_room = rt_input3.move(command.lower().strip())
        if current_room == rt_input1:
            rt_function1()
            current_state = False
        elif current_room == rt_input2:
            rt_function2()
            current_state = False


# Mini-Game subroutines
def aimTrainer(time_limit):
    pygame.init()
    # Constants to be set
    WIDTH = 900
    HEIGHT = 600
    SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
    text_x = 10
    text_y = 10
    time_limit = time_limit

    # Colors
    black = (0, 0, 0)
    white = (255, 255, 255)
    purple = (128, 0, 128)
    grey = (128, 128, 128)
    sky = (0, 0, 220)
    blue = (85, 206, 255)
    orange = (255, 127, 80)
    red = (200, 0, 0)
    light_red = (255, 0, 0)
    green = (0, 200, 0)
    light_green = (0, 255, 0)
    colors = [white, grey, purple, sky, blue, orange, red, light_red, green, light_green]

    clock = pygame.time.Clock()  # To set the frame rate

    # Changing variables

    score = 0
    start_time = time.time()

    # Setting up screen and circles
    font = pygame.font.SysFont('verdana', 32)
    cx = random.randint(100, WIDTH - 100)
    cy = random.randint(100, HEIGHT - 100)
    width_of_circle = random.randint(14, 20)
    pygame.draw.circle(SCREEN, random.choice(colors), (cx, cy), width_of_circle)

    # Function to show score
    def show_score(z, y):
        score_value = font.render('Score: ' + str(score), True, (255, 255, 255))
        SCREEN.blit(score_value, (z, y))

    # Main loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return score
        # Keep a check of time elapsed since start of game
        elapsed_time = time.time() - start_time
        # check if time is over, then finish the subroutine and return the score
        if elapsed_time > time_limit:
            print('game over')
            pygame.quit()
            return score

        x = pygame.mouse.get_pos()[0]
        y = pygame.mouse.get_pos()[1]
        click = pygame.mouse.get_pressed()
        # Using maths to keep track of circle and mouse collision

        sqx = (x - cx) ** 2
        sqy = (y - cy) ** 2

        if math.sqrt(sqx + sqy) < width_of_circle and click[0] == 1:
            SCREEN.fill(black)  # Reset the screen
            cx = random.randint(20, WIDTH - 20)
            cy = random.randint(20, HEIGHT - 20)
            width_of_circle = random.randint(14, 20)
            pygame.draw.circle(SCREEN, random.choice(colors), (cx, cy), width_of_circle)
            score += 1

        show_score(text_x, text_y)
        pygame.display.update()
        clock.tick()


def breakout(user_lives, speed):
    pygame.init()
    # Setting constants
    SCREEN_WIDTH = 600
    SCREEN_HEIGHT = 600

    SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    pygame.display.set_caption('BreakMe')

    font = pygame.font.SysFont('Constantia', 30)
    # background color
    bg = (234, 218, 184)

    # brick colors
    brick_red = (242, 85, 96)
    brick_green = (86, 174, 87)
    brick_blue = (89, 177, 232)
    # paddle colors
    paddle_color = (142, 135, 123)
    paddle_outline = (100, 100, 100)
    text_colour = (78, 81, 139)

    # game variables
    COLS = 6
    ROWS = 6
    clock = pygame.time.Clock()
    FPS = 60
    live_ball = False
    game_over = 0
    lives = user_lives
    ball_speed = speed

    def write_text(text, _font, text_col, x, y):
        image = _font.render(text, True, text_col)
        SCREEN.blit(image, (x, y))

    # classes
    class Wall:
        def __init__(self):
            self.brick = None
            self.width = SCREEN_WIDTH // COLS
            self.height = 50

        def create_wall(self):
            self.brick = []
            strength = None
            # empty list for single block
            brick_individual = []
            for row in range(ROWS):
                # reset the block row list
                brick_row = []
                # iterate through each col in the row
                for col in range(COLS):
                    # produce x and y positions and create rectangle from these positions
                    brick_x = col * self.width
                    brick_y = row * self.height
                    rect = pygame.Rect(brick_x, brick_y, self.width, self.height)
                    # assign brick strength based on the rows:
                    if row < 2:
                        strength = 3
                    elif row < 4:
                        strength = 2
                    elif row < 6:
                        strength = 1
                    # creating list to store rectangle and its color
                    brick_individual = [rect, strength]
                    # appending individual brick to the brick row
                    brick_row.append(brick_individual)
                # adding row to the whole list of the blocks
                self.brick.append(brick_row)

        def draw_wall(self):
            brick_color = None
            for row in self.brick:
                for brick in row:
                    # set a color based on brick level strength
                    if brick[1] == 3:
                        brick_color = brick_blue
                    elif brick[1] == 2:
                        brick_color = brick_green
                    elif brick[1] == 1:
                        brick_color = brick_red
                    # drawing the bricks
                    pygame.draw.rect(SCREEN, brick_color, brick[0])
                    # to draw a border for each brick to be differentiated
                    pygame.draw.rect(SCREEN, bg, (brick[0]), 1)

    class Paddle:
        def __init__(self):
            # setting paddle variables
            self.height = 20
            self.width = int(SCREEN_WIDTH / COLS)
            self.x = int((SCREEN_WIDTH / 2) - (self.width / 2))
            self.y = SCREEN_HEIGHT - (self.height * 2)
            self.speed = 10
            self.rect = Rect(self.x, self.y, self.width, self.height)
            self.direction = 0

        def move(self):
            # resets the direction of the movement
            self.direction = 0
            key = pygame.key.get_pressed()
            if key[pygame.K_LEFT] and self.rect.left > 0:
                self.rect.x -= self.speed
                self.direction = -1
            if key[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
                self.rect.x += self.speed
                self.direction = 1

        def draw(self):
            pygame.draw.rect(SCREEN, paddle_color, self.rect)
            pygame.draw.rect(SCREEN, paddle_outline, self.rect, 3)

        def reset(self):
            # to reset the paddle to original dimensions and positions for game reset
            self.height = 20
            self.width = int(SCREEN_WIDTH / COLS)
            self.x = int((SCREEN_WIDTH / 2) - (self.width / 2))
            self.y = SCREEN_HEIGHT - (self.height * 2)
            self.speed = 10
            self.rect = Rect(self.x, self.y, self.width, self.height)
            self.direction = 0

    class Ball:
        def __init__(self, x, y, _speed):
            self.radius = 10
            self.x = x - self.radius
            self.y = y
            self.rect = Rect(self.x, self.y, self.radius * 2, self.radius * 2)
            self.speed_x = _speed
            self.speed_y = -_speed
            self.max_speed = _speed + 1
            self.game_over = 0

        def move(self, _lives):
            collision_threshold = 5
            player_lives = _lives

            # checking for collision with walls - assuming wall has been destroyed completely
            wall_destroyed = 1
            row_counter = 0
            for row in wall.brick:
                item_counter = 0
                for item in row:
                    # checking for collision
                    if self.rect.colliderect(item[0]):
                        # collision from above
                        if abs(self.rect.bottom - item[0].top) < collision_threshold and self.speed_y > 0:
                            self.speed_y *= -1
                        # collision from below
                        if abs(self.rect.top - item[0].bottom) < collision_threshold and self.speed_y < 0:
                            self.speed_y *= -1
                        # collision from the right
                        if abs(self.rect.right - item[0].left) < collision_threshold and self.speed_x > 0:
                            self.speed_x *= -1
                        # collision from the left
                        if abs(self.rect.left - item[0].right) < collision_threshold and self.speed_x < 0:
                            self.speed_x *= -1
                        # reducing brick strength
                        if wall.brick[row_counter][item_counter][1] > 1:
                            wall.brick[row_counter][item_counter][1] -= 1
                        else:
                            wall.brick[row_counter][item_counter][0] = (0, 0, 0, 0)
                    # check if any brick exists
                    if wall.brick[row_counter][item_counter][0] != (0, 0, 0, 0):
                        wall_destroyed = 0
                    # increment item counter
                    item_counter += 1
                # increment row counter
                row_counter += 1
            # checking if wall is destroyed after going through all bricks
            if wall_destroyed == 1:
                self.game_over = 1

            if self.rect.left < 0 or self.rect.right > SCREEN_WIDTH:
                self.speed_x *= -1
            if self.rect.top < 0:
                self.speed_y *= -1
            if self.rect.bottom > SCREEN_HEIGHT:
                self.game_over = -1
                player_lives -= 1
            # collision with paddle
            if self.rect.colliderect(user_paddle):
                # check for only collisions from top:
                if (abs(self.rect.bottom - user_paddle.rect.top) < collision_threshold) and (self.speed_y > 0):
                    self.speed_y *= -1
                    self.speed_x += user_paddle.direction
                    if self.speed_x > self.max_speed:
                        self.speed_x = self.max_speed
                    elif self.speed_x < 0 and self.speed_x < - self.max_speed:
                        self.speed_x = - self.max_speed
                else:
                    self.speed_x *= -1

            self.rect.x += self.speed_x
            self.rect.y += self.speed_y

            return self.game_over, player_lives

        def draw(self):
            pygame.draw.circle(SCREEN, paddle_color, ((self.rect.x + self.radius), (self.rect.y + self.radius)),
                               self.radius)
            pygame.draw.circle(SCREEN, paddle_outline, ((self.rect.x + self.radius), (self.rect.y + self.radius)),
                               self.radius, 3)

        def reset(self, x, y, _speed):
            self.radius = 10
            self.x = x - self.radius
            self.y = y
            self.rect = Rect(self.x, self.y, self.radius * 2, self.radius * 2)
            self.speed_x = _speed
            self.speed_y = -_speed
            self.max_speed = _speed + 1
            self.game_over = 0

    # creating objects
    wall = Wall()
    wall.create_wall()
    user_paddle = Paddle()
    ball = Ball(user_paddle.x + (user_paddle.width // 2), user_paddle.y - user_paddle.height, ball_speed)

    run = True

    while run and lives > 0:
        clock.tick(FPS)
        SCREEN.fill(bg)

        # drawing the wall
        wall.draw_wall()
        user_paddle.draw()
        ball.draw()
        if live_ball:
            user_paddle.move()
            game_over, lives = ball.move(lives)
            if game_over != 0:
                live_ball = False

        # player instructions
        if not live_ball:
            if game_over == 0:
                write_text('Click anywhere to start', font, text_colour, 150, SCREEN_HEIGHT // 2 + 100)
            elif game_over == 1:
                write_text('You won', font, text_colour, 250, SCREEN_HEIGHT // 2 + 50)
                pygame.quit()
                return lives
            elif game_over == -1:
                write_text('You lost', font, text_colour, 250, SCREEN_HEIGHT // 2)
                write_text(('You have ' + str(lives) + ' try(s) left'), font, text_colour, 165, SCREEN_HEIGHT // 2 + 50)
                write_text('Click anywhere to start', font, text_colour, 150, SCREEN_HEIGHT // 2 + 100)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                #lives = 0
                run = False
                pygame.quit()
                return lives
            if event.type == pygame.MOUSEBUTTONDOWN and live_ball is False:
                live_ball = True
                ball.reset(user_paddle.x + (user_paddle.width // 2), user_paddle.y - user_paddle.height, ball_speed)
                user_paddle.reset()
                wall.create_wall()

        pygame.display.update()

    pygame.quit()
    return lives


# Story Subroutines

def rallying_speech():
    time_amount = 180
    print('as you make up your mind to give the speech a small envelope is shoved into your pocket')
    print('it contains the following words: ')
    print('decrypt this message to find out what stirs soldiers towards rebellion and include it in your speech')
    if user1.skill <= 0:
        time_amount = 160
    elif user1.skill > 2:
        time_amount = 200

    if user1.passion <= 0:
        level3(time_amount)

    elif user1.passion > 2:
        level1(time_amount)

    else:
        level2(time_amount)

    temp = 0
    user_speech = input('enter your speech:\n> ')
    user_speech.split(' ')
    # Uses list operations to validate user input to given words
    lst = ['fuhrer', 'war', 'revolution', 'rations', 'economy']
    for x in range(len(lst)):
        if lst[x] in user_speech:
            temp += 1
    if temp == 5:
        user1.change_charisma(True)
        user1.change_fame(True)
        user1.change_charm(True)
        print('your speech caused the whole infantry to erupt in applause, you are carried on their soldiers as a'
              ' messiah')
    elif 3 <= temp < 5:
        user1.change_fame(True)
        user1.change_charisma(True)
        print('your speech caused a disturbance among most soldiers as they nod their head in agreement')

    elif 1 <= temp < 3:
        user1.change_fame(True)
        print('your speech arouses a few suspicious looks around but you also see a few approving looks')
    else:
        user1.change_charisma(False)
        user1.change_fame(False)
        print('you are booed off the stage for your speech and you look for an escape before anyone reports your name')
    # Adds to speech to the json file
    Add_Value_to_Data(user_username, 'Dining Hall Speech', user_speech)


def class_creation(name):
    # Creates characters for final boss battle
    global General_Aladeen_Combat, Private_Sawcon, Guard_Gorbachev
    if name == 'general aladeen':
        General_Aladeen_Combat = Allies('general aladeen', 'The General in charge of forming strategies',
                                        'revolver', 'was never given any credit')
        General_Aladeen_Combat.add_items(dagger)
    elif name == 'private sawcon':
        Private_Sawcon = Allies('private sawcon', 'The soldier in charge of rations and motivation',
                                'pistol', "feels like the reich would be better off in someone else's hands")
        Private_Sawcon.add_items(sheriff_deagle)
    elif name == 'guard gorbachev':
        Guard_Gorbachev = Allies('guard gorbachev', 'Guard in charge of the shooting range and ammunition',
                                 'poison vial', 'has been part of the reich for 20 years now and never gotten above the'
                                                'rank of a guard')
        Guard_Gorbachev.add_items(dual_pistols)

    return General_Aladeen_Combat, Private_Sawcon, Guard_Gorbachev


def Broadcast_Room():
    while Room_Key in user1.inventory:
        while not broadcast_room.room_visited:
            print('You find the Broadcast Room deserted and empty, and you find this as your opportunity '
                  'to put the final nail in the coffin')
            print('For every life you conserve you get to make an ally from within the regime, anyone memorable you '
                  'have met throughout the game such as "general x"...provided you remember their name and you have '
                  'left an impressionable mark upon them')
            time.sleep(2)
            number_of_lives = 4
            if user1.skill < 0:
                number_of_lives = 3
            elif user1.skill > 2:
                number_of_lives = 5
            speed = 3
            if user1.charisma < 0:
                speed = 4
            elif user1.charisma > 2:
                speed = 2
            score = breakout(number_of_lives, speed)
            print('your score:', score)
            global team_lst, Camp_Officer, Team1
            if score == 5:
                print('You get to urge 3 comrades of yours to join your resistance against the fuhrer, however get 4 '
                      'tries broadcast their name on media and they will be on your side however get their name wrong '
                      'and it would be very hard to convince them after')
                broadcast1 = input("Broadcast Name 1: \n>").lower().strip()
                broadcast2 = input("Broadcast Name 2: \n>").lower().strip()
                broadcast3 = input("Broadcast Name 3: \n>").lower().strip()
                broadcast4 = input("Broadcast Name 4: \n>").lower().strip()
                ally_list = ['general aladeen', 'private sawcon', 'guard gorbachev']
                if broadcast1 in ally_list:
                    ally_list.remove(broadcast1)
                    a, b, c = class_creation(broadcast1)
                else:
                    continue
                if broadcast2 in ally_list:
                    ally_list.remove(broadcast2)
                    a, b, c = class_creation(broadcast2)
                else:
                    continue
                if broadcast3 in ally_list:
                    ally_list.remove(broadcast3)
                    a, b, c = class_creation(broadcast3)
                else:
                    continue
                run = True
                if len(ally_list) == 0:
                    run = False
                while run:
                    if broadcast4 in ally_list:
                        ally_list.remove(broadcast4)
                        class_creation(broadcast4)
                        a, b, c = class_creation(broadcast4)
                        run = False
                    else:
                        run = False
                print("For being exceptional at this task you also awarded with an opportunity to name a person you "
                      "hope would join your rebellion, a person in control of the camps for you don't agree with the "
                      'practice and hope to free them')
                special = input("> ").strip().lower()
                if special == 'rudolf höss' or special == 'theodor eicke' or special == 'heinrich himmler' \
                        or special == 'rudolf hoess':
                    print('You have chosen the right man for this job')
                    Camp_Officer = Allies(special, 'camp officer in charge of the camps', 'poison dart',
                                          "does not agree with the practices but has to his job")
                    Camp_Officer.add_items(arsenic_injections)
                else:
                    print('Unfortunately that is a person who would not be able to help')
                Team1 = Team(a, b, c, Camp_Officer)
            elif score == 4:
                print('You get to urge 3 comrades of yours to join your resistance against the fuhrer, however get 4 '
                      'tries broadcast their name on media and they will be on your side however get their name wrong '
                      'and it would be very hard to convince them after')
                broadcast1 = input("Broadcast Name 1: \n>").lower().strip()
                broadcast2 = input("Broadcast Name 2: \n>").lower().strip()
                broadcast3 = input("Broadcast Name 3: \n>").lower().strip()
                broadcast4 = input("Broadcast Name 4: \n>").lower().strip()
                ally_list = ['general aladeen', 'private sawcon', 'guard gorbachev']
                if broadcast1 in ally_list:
                    ally_list.remove(broadcast1)
                    a, b, c = class_creation(broadcast1)
                else:
                    continue
                if broadcast2 in ally_list:
                    ally_list.remove(broadcast2)
                    a, b, c = class_creation(broadcast2)
                else:
                    continue
                if broadcast3 in ally_list:
                    ally_list.remove(broadcast3)
                    a, b, c = class_creation(broadcast3)
                else:
                    continue
                run = True
                if len(ally_list) == 0:
                    run = False
                while run:
                    if broadcast4 in ally_list:
                        ally_list.remove(broadcast4)
                        a, b, c = class_creation(broadcast4)
                        run = False
                    else:
                        run = False
                Team1 = Team(a, b, c)
            elif score == 3:
                print('You get to urge 3 comrades of yours to join your resistance against the fuhrer, get 3 tries to'
                      ' broadcast their name on media and they will be on your side however get their name wrong and '
                      'it would be very hard to convince them after')
                broadcast1 = input("Broadcast Name 1: \n>").lower().strip()
                broadcast2 = input("Broadcast Name 2: \n>").lower().strip()
                broadcast3 = input("Broadcast Name 3: \n>").lower().strip()
                ally_list = ['general aladeen', 'private sawcon', 'guard gorbachev']
                if broadcast1 in ally_list:
                    ally_list.remove(broadcast1)
                    a, b, c = class_creation(broadcast1)
                else:
                    continue
                if broadcast2 in ally_list:
                    ally_list.remove(broadcast2)
                    a, b, c = class_creation(broadcast2)
                else:
                    continue
                if broadcast3 in ally_list:
                    ally_list.remove(broadcast3)
                    a, b, c = class_creation(broadcast3)
                else:
                    continue
                Team1 = Team(a, b, c)
            elif score == 2:
                print('You get to urge 2 comrades of yours to join your resistance against the fuhrer, get 2 tries to '
                      'broadcast their name on media and they will be on your side however get their name wrong'
                      'and it would be very hard to convince them after')
                broadcast1 = input("Broadcast Name 1: \n>").lower().strip()
                broadcast2 = input("Broadcast Name 2: \n>").lower().strip()
                ally_list = ['general aladeen', 'private sawcon', 'guard gorbachev']
                if broadcast1 in ally_list:
                    ally_list.remove(broadcast1)
                    a, b, c = class_creation(broadcast1)
                else:
                    continue
                if broadcast2 in ally_list:
                    ally_list.remove(broadcast2)
                    a, b, c = class_creation(broadcast2)
                else:
                    continue
                Team1 = Team(a, b, c)
            elif score == 1:
                print('You get to urge a comrade of yours to join your resistance against the fuhrer, get a '
                      'try to broadcast their name on media and they will be on your side however get their name wrong'
                      'and it would be very hard to convince them after')
                broadcast1 = input("Broadcast Name 1: \n>").lower().strip()
                ally_list = ['general aladeen', 'private sawcon', 'guard gorbachev']
                if broadcast1 in ally_list:
                    ally_list.remove(broadcast1)
                    a, b, c = class_creation(broadcast1)
                else:
                    continue
                Team1 = Team(a, b, c)
            else:
                print('You could not complete the game ')
                print('Thus you will now face the Fuhrer alone')
                Team1 = Team(General_Aladeen_Combat, Guard_Gorbachev, Private_Sawcon)
            team_lst = [General_Aladeen_Combat, Private_Sawcon, Camp_Officer, Guard_Gorbachev]
            Add_Value_to_Data(user_username, 'Score from Brick Game', score)
            broadcast_room.change_room_status()
            room_transition(dining_hall, None, broadcast_room, Dining_Hall, None)
            user1.change_inventory(Room_Key, False)
        print('You have been here before')
        room_transition(dining_hall, None, broadcast_room, Dining_Hall, None)
    print('You do not have the key to this room')
    room_transition(dining_hall, None, broadcast_room, Dining_Hall, None)


def Main__Hall():
    global main_hall
    while True:
        while not main_hall.room_visited:
            print('You are walking down the path when a soldier in a stunning black uniform walks up to u and says:'
                  '"Ah', user1.name, 'what are you doing here, General Aladeen is waiting for you"')
            print('While the soldier accompanies along you decide to engage in small talk. The soldier is unaware and '
                  'is about to reveal crucial information about the general however you notice a scintillating object')
            print('You have to make a choice if you would rather \n1) choose to pickpocket the mysterious object '
                  '\n2) listen to the crucial information')
            selection = 0
            while selection not in ('1', '2'):
                try:
                    selection = input("> ")
                    if selection == '1':
                        print('You decide to pickpocket the item and quickly escape the conversation to avoid'
                              ' being detected')
                        user1.change_inventory(knife, True)
                    elif selection == '2':
                        print('[Soldier]: I have heard he has an absurd fear when it comes to knives, however if you do'
                              ' want to please him do mention his kids. I have also heard he has a gun ')
                except Exception:
                    pass
            main_hall.change_room_status()
            room_transition(generals_room, dining_hall, main_hall, Generals_Room, Dining_Hall)
        print('You are back in the main hall where would u want go now')
        if generals_room.room_visited and shooting_range.room_visited and dining_hall.room_visited and \
                broadcast_room.room_visited:
            print('You have visited all rooms and are confronted by Hitler')
            print('He has finally caught up to you and confronts you about all of your shenanigans')
            for item in team_lst:
                if item is not None:
                    item.introduction()
                else:
                    continue
            user1.change_inventory(Room_Key, False)
            while hitler.is_alive():
                print('Time to battle!')
                decision = None
                if Team1.team_is_alive():
                    while decision not in ['y', 'a']:
                        decision = input(
                            'Do you want to battle Hitler or do you want your ally to battle:\n1)y-you\n2)a-ally\n>') \
                            .strip().lower()
                    if decision == 'y':
                        hit = user1.combat()
                        hitler.got_hit(hit)
                    elif decision == 'a':
                        hit = Team1.team_combat()
                        hitler.got_hit(hit)
                    hitler.combat(user1, team_lst[0], team_lst[1], team_lst[2], team_lst[3])
                    if not user1.is_alive():
                        print('You die game over')
                        print('Hitler defeats you')
                        input('Press enter to exit\n>')
                        exit()
                else:
                    print('You do not have any allies left')
                    hit = user1.combat()
                    hitler.got_hit(hit)
                    hitler.combat(user1)
                    if not user1.is_alive():
                        print('You die game over')
                        print('Hitler defeats you')
                        input('Press enter to exit\n>')
                        exit()

            hitler_maze_run()
            print('Game Over You Win')
            exit()
        else:
            room_transition(generals_room, dining_hall, main_hall, Generals_Room, Dining_Hall)


def Generals_Room():
    while not generals_room.room_visited:
        print("You enter the room and are greeted by everyone")
        print("u say... greetings general...")
        user_test1 = input("> ")
        if user_test1.lower() == General_Aladeen.name.lower():
            print("[General]: I see you respect me")
        else:
            user1.change_charisma(False)
            print("[General]: That's not my name soldier")
        print('[General]: Anyways moving on... we need to decide which ally to send aid to')
        user_test2 = input("> ")
        allies = ['italy', 'japan']
        if user_test2.lower() in allies:
            print("[General]: Good decision")
            user1.change_passion(True)
        else:
            print("[General]: They not our ally...")
            user1.change_passion(False)
        print("[General]: Finally the topic to discuss we need a plan to attack a country...")
        user_decision1 = input("> ")
        if user_decision1.lower() == "russia":
            print("[General]: That might be interesting provided russia winters have just passed")
            user1.change_charisma(True)
        elif user_decision1.lower() == "belgium":
            print("[General]: Ah as per the original plan one would say")
            user1.change_passion(True)
        else:
            print('[General]: Why would you attack them??')
            user1.change_passion(False)
        print("[General]: Is there any particular way you would like to lay siege?")
        user_test3 = input("> ")
        if user_test3.lower() == 'blitzkrieg':
            user1.change_passion(True)
            print('[General]: Original to the plan')
        else:
            print('[General]: Hmm i really doubt that would work but thank you for your input regardless')
        print('[General]: You are free to go soldier however you might soon want to head to the shooting range to the '
              'right for daily practice')
        current_user_stats()
        print('You need to search the room till you find a key to progress')
        menu(General_Aladeen, generals_room)
        generals_room.change_room_status()
        room_transition(main_hall, shooting_range, generals_room, Main__Hall, Shooting_Range)
    print('You have been here before')
    room_transition(main_hall, shooting_range, generals_room, Main__Hall, Shooting_Range)


def Dining_Hall():
    while not dining_hall.room_visited:
        if not generals_room.room_visited:
            print('You enter into a rather quiet room ')
            print('Yet another soldier reminds you that the general is waiting for you')
            room_transition(main_hall, broadcast_room, dining_hall, Main__Hall, Broadcast_Room)
        if not shooting_range.room_visited:
            print('The general has informed you to go practice at the shooting range first it is recommended '
                  'you proceed accordingly')
            room_transition(main_hall, broadcast_room, dining_hall, Main__Hall, Broadcast_Room)
        else:
            print('[Private Sawcon]: Oye', user1.name, 'we be hearing')
            print('[Private Sawcon]: That you had a meeting with good ol Aladeen')
            print('[Private Sawcon]: you think you are better than us?')
            print('You are given a choice')
            print('Either:\n1) Bad mouth the general or \n2) stand up for yourself')
            binary_decision_function("choose an option:", user1.change_charisma, user1.change_passion)
            print('[Private Sawcon]: "I-')
            print("As the  soldier is about to reply to you, there is an announcement about daily rations for "
                  "soldiers which causes a commotion")
            print("do you take this opportunity to \n1) make a rallying speech or \n2) use it as an distraction to "
                  "find an essential tool next to the kitchen")
            selection = 0
            print("make a choice: ")
            while selection not in ('1', '2'):
                try:
                    selection = input("> ")
                    if selection == '1':
                        rallying_speech()
                    elif selection == '2':
                        user1.change_inventory(knife, True)
                        print('you scour the room and successfully find a mini knife')
                except Exception:
                    pass
            current_user_stats()
            menu(Dining_Hall_Soldier, dining_hall)
            dining_hall.change_room_status()
            room_transition(main_hall, broadcast_room, dining_hall, Main__Hall, Broadcast_Room)
    print('You have been here already')
    room_transition(main_hall, broadcast_room, dining_hall, Main__Hall, Broadcast_Room)


def word_check(num):
    word = None
    pattern = "[A-Za-z]+"
    for x in range(num):
        while not re.fullmatch(pattern, word):
            word = input("Is this your input to the masses? Pathetic, invalid input try again: ")


def Shooting_Range():
    if shooting_range.room_visited:
        user1.change_skill(False)
    print("[Guard Gorbachev]: Welcome to the shooting range")
    print("The guard at the shooting range seems bored, he has decided to play a game with you")
    print('Since he despises the soldier in charge of the dining hall because he bullies everyone the guard '
          'decides to share vital information about him, the twist being the higher the score you get the more'
          ' information he dispels')
    print('If you get above the score of 75 u will get the key to the broad cast room')
    time.sleep(5)
    time_limit = 60
    if user1.skill < 0:
        time_limit = 45
    elif user1.skill > 2:
        time_limit = 75
    score = aimTrainer(time_limit)
    print('Your score is:', score)
    time.sleep(1)
    if score == 69:
        print('[Guard Gorbachev]: Nice')
        print('[Guard Gorbachev]: Private Sawcon always has the key to the broad cast room in his pocket')
        user1.skill += 2
    elif score > 100:
        print('[Guard Gorbachev]: Officer you are cracked')
        print('[Guard Gorbachev]: Private Sawcon is really obsessed with his body, if you want to woo him mention his '
              'body')
        print('[Guard Gorbachev]: Private Sawcon has always been scared of guns')
        print('Here is your promised key')
        if not Room_Key in user1.inventory:
            user1.change_inventory(Room_Key, True)
        user1.skill += 3
    elif score > 75:
        print('[Guard Gorbachev]: You are quite the sharpshooter, but always remember switching to your pistol is '
              'faster than reloading')
        print('[Guard Gorbachev]: Private Sawcon has always been scared of guns')
        print('Here is your promised key')
        user1.change_inventory(Room_Key, True)
        user1.skill += 2
    elif score > 60:
        print('[Guard Gorbachev]: Well done officer, looks like you are still in form to go the battlefield')
        print('[Guard Gorbachev]: Private Sawcon always has the key to the broad cast room in his pocket')
        user1.skill += 1

    else:
        print('[Guard Gorbachev]: Officer your performance has been subpar to the standards I recommend coming back in'
              ' a few hours, I have no information to give you due to such abysmal performance')
    shooting_range.change_room_status()
    Add_Value_to_Data(user_username, 'Shooting range score', score)
    room_transition(generals_room, None, shooting_range, Generals_Room, None)


def hitler_maze_run():
    # Constants to be set
    SCREEN_WIDTH = 1000
    SCREEN_HEIGHT = 800
    wall_image = pygame.image.load('pygame2.jpg')
    square_image = pygame.image.load('white_square.jpg')
    empty_image = pygame.image.load('black_square.jpg')
    dot_image = pygame.image.load('dot.jpg')
    clock = pygame.time.Clock()  # To set the frame rate
    SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    def create(_maze, path):
        clock.tick(120)
        SCREEN.fill((0, 0, 0))
        m2 = _maze[:]  # creates a copy

        for item in path:
            m2[item[0]][item[1]] = '.'

        m2[path[-1][0]][path[-1][1]] = 'M'

        for y in range(len(_maze)):
            row = _maze[y]
            for x in range(len(row)):
                item = row[x]
                if item == '1':
                    SCREEN.blit(wall_image, (46 * x, 45 * y))
                elif item == 'M':
                    SCREEN.blit(square_image, (46 * x, 45 * y))
                elif item == '.':
                    SCREEN.blit(dot_image, ((46 * x) + 23, (45 * y) + 22))
                elif item == '2':
                    SCREEN.blit(empty_image, (46 * x, 45 * y))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

    def get_maze(file):
        f = open(file, 'r')
        reader = csv.reader(f)
        maze = []
        for line in reader:
            maze.append(line)
        return maze

    def navigate(path):
        time.sleep(0.3)
        clock.tick(120)
        cur = path[-1]
        create(maze, path)
        poss = [(cur[0], cur[1] + 1), (cur[0], cur[1] - 1), (cur[0] + 1, cur[1]), (cur[0] - 1, cur[1])]
        choice = randint(0, 2)
        # Randomly chooses desired path of traversal
        if choice == 1:
            # random traversal
            random.shuffle(poss)
        elif choice == 2:
            # breadth first tree traversal
            poss = [(cur[0] + 1, cur[1]), (cur[0] - 1, cur[1]), (cur[0], cur[1] + 1), (cur[0], cur[1] - 1)]
        elif choice == 3:
            # depth first tree traversal
            poss = [(cur[0], cur[1] + 1), (cur[0], cur[1] - 1), (cur[0] + 1, cur[1]), (cur[0] - 1, cur[1])]

        # This is the recursive algorithm that call itself till the end of the maze is reached
        for item in poss:
            # to keep in check so that algorithm doesn't go off the maze
            if item[0] < 0 or item[1] < 0 or item[0] > len(maze) or item[1] > len(maze[0]):
                continue
            # to avoid colliding into walls
            elif maze[item[0]][item[1]] in ['1', '2']:
                continue
            # to avoid retracing the path
            elif item in path:
                continue
            # if user reaches end of the maze
            elif maze[item[0]][item[1]] == 'B':
                path = path + (item,)
                create(maze, path)
                input('Hitler enters the Mysterious Room and you hear a gunshot, you realize the rein of'
                      ' the Third Reich is all but over\nPress Enter to finish the Game\n>')
                exit()
                pygame.quit()


            else:
                new_path = path + (item,)
                # once the path is updated the algorithm calls upon itself
                navigate(new_path)
                maze[item[0]][item[1]] = '2'
                create(maze, path)
                time.sleep(0.3)
                pygame.display.update()

    maze = get_maze('maze.csv')
    run = True
    start = ((1, 0),)
    while run:
        navigate(start)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()


user_username = login_system()
user_setup()
intro()
Main__Hall()
