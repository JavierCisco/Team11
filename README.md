# Team11
Team 11's work for Software Engineering project.


# How to Run Project:
# FIRST please Make sure you have Python and pygame (therefore inferring pip as well) downloaded. Use the following commands.
- sudo apt update
- sudo apt install python3 python3-pip
- pip3 install pygame

# Then open a terminal and type python3 then hit enter. Then use the following commands to verify the installation.
- import pygame
- print(pygame.__version__)

# If there are no errors then the installation was successful.

# Download #Psycopg2 module for the database if your virtual machine does not already have it. Use the following commands.
- sudo apt update
- sudo apt install postgresql postgresql-contrib
- sudo apt install libpq-dev python3-dev
- pip3 install psycopg2
- pip3 install psycopg2-binary **use this if there are issues when compiling the extension**

# Then open a terminal and type python3 then hit enter. Then use the following commands to verify the installation.
- import psycopg2

# If there are no errors then the installation was successful.

# SECOND...
- Download all files in our main branch.
- to initiate program, run the command: 'python3 main.py' in the terminal


# Running the Generator
- To run the generator you will have to run it before running main.py
- Open two terminals and in one type python3 python_trafficgenarator_v2.py
- type in the equipment codes for those 4 players. Please note red team must contain odd number equipment codes and the green team even number equipment codes.
- Then run main.py by typing python3 main.py
- Be sure to type in the same equipment codes you used in the generator for each player.

# Game Start: 
- F3: Starts Game and Countdown timer. It also allows user to move onto game action screen.
- Buttons are on screen, and the keys to do certain actions are also described on the screen.
- Please click back to the game screen to keep interacting with the game.
- On the entry screen, there are two sets of tables, one for each team. For each side, the left box is where the user will enter the player id, and the right box is where they will enter the equipment code. To add player to game first fill out both player id and equipment code. Click on player id box and hit F7. If prompted to enter code name, type code name into box and hit enter. 

Github Names and Real Names:
- JavierCisco = Francisco Hernandez
- ame-0107 = America Cervantes
- ErnestoGalarzaA = Ernesto Galarza
- fjmartin01 = Fernando Martinez
- KadeWas = Kade Wasemiller
