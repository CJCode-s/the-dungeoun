import random
import os
class Enemy(): #Enemy Object Class
    """Enemy stats"""
    def __init__(self,health=0,type=0): #Default enemy is a goblin with 1 health
        self.health = health
        self.type = type
    enemy_types = ['Gobelin','Slyme','Kobold','Beeste','Barbarian','Corrupten Knight','Ogre','Dragoun']
    health_values = [2,3,4,5,6,9,12,15,20,25,35]
    def __str__(self): #str returns the enemy type
        return '%s' %(Enemy.enemy_types[self.type])
class Item(): #Item Object Class
    def __init__(self,name=0,health=0,maxhealth=0,damage=0,fire=0): #Item is a potion that gives no health, no health upgrade, fire upgrade, or damage upgrade
        self.name = name
        self.health = health
        self.maxhealth = maxhealth
        self.damage = damage
        self.fire = fire
    name_types = ['Pocioun','Whetston','Enchauntement','Turpentyne','Stew']
    health_values = [0,2,4,6,8,10]
    maxhealth_values = [0,2,4]
    damage_values = [0,2,3,4]
    fire_types = ['No fire','Fire']
    def __str__(self): #str returns item attributes
        return '%s, gives %s health, %s max health, boosts damage by %s, and gives %s' %(Item.name_types[self.name],Item.health_values[self.health],Item.maxhealth_values[self.maxhealth],Item.damage_values[self.damage],Item.fire_types[self.fire])
    def __repr__(self): #repr returns item attributes
        return '%s, gives %s health, %s max health, boosts damage by %s, and gives %s' %(Item.name_types[self.name],Item.health_values[self.health],Item.maxhealth_values[self.maxhealth],Item.damage_values[self.damage],Item.fire_types[self.fire])
    def use(self): #Function for using items
        global player_health
        global player_maxhealth
        global player_damage
        global player_fire
        if player_health == player_maxhealth and self.maxhealth + self.damage + self.fire == 0: #Item can't be used
                return "Did not use %s, health is full and no upgrades are possible" %(Item.name_types[self.name])
        else: #Item can be used
            inventory.remove(self)
            player_maxhealth = player_maxhealth + Item.maxhealth_values[self.maxhealth]
            player_damage = player_damage + Item.damage_values[self.damage]
            if self.fire == 1:
                player_fire = 1
            if player_health + Item.health_values[self.health] <= player_maxhealth:
                player_health = player_health + Item.health_values[self.health]
            else:
                player_health = player_maxhealth
            return "%s was used" %(Item.name_types[self.name])
        
def espawnlow(): #Spawn weak enemies
    global enemy
    global enemy_health
    global enemy_damage
    enemy = Enemy(random.randint(0,4),random.randint(0,2))
    enemy_health = Enemy.health_values[enemy.health]
    enemy_t = Enemy.enemy_types.index(Enemy.enemy_types[enemy.type])
    enemy_damage = enemy_t+1

def espawnmed(): #Spawn medium enemies
    global enemy
    global enemy_health
    global enemy_damage
    enemy = Enemy(random.randint(4,7),random.randint(3,5))
    enemy_health = Enemy.health_values[enemy.health]
    enemy_t = Enemy.enemy_types.index(Enemy.enemy_types[enemy.type])
    enemy_damage = enemy_t+1

def espawnhi(): #Spawn strong enemies
    global enemy
    global enemy_health
    global enemy_damage
    enemy = Enemy(random.randint(8,10),random.randint(5,7))
    enemy_health = Enemy.health_values[enemy.health]
    enemy_t = Enemy.enemy_types.index(Enemy.enemy_types[enemy.type])
    enemy_damage = enemy_t+1

def attack(): #Player attacks
    global player_fire
    global enemy_health
    global player_damage
    global enemy_maxhealth
    crit = random.choice(crits) #Critical hits
    if crit == 3: 
        print('\n'"LUKKY STRICHE!"'\n')
    if (enemy.type == 1 and player_fire == 1) == True: #Checks for fire weakness on slimes
        enemy_health = 0
        player_fire = 0
        return        
    if (enemy.type == 5 and player_fire == 1) == True: #Checks for fire weakness on corrupted knights
        enemy_health = 0
        player_fire = 0
        return
    if enemy_maxhealth <= player_damage: #Instakill check
        enemy_health = 0
        print('\n'"ANNIHILATUS!"'\n')
        return
    if (enemy.type == 1 and player_fire == 1) == True: #Checks for fire weakness on slimes
        enemy_health = 0
        player_fire = 0
        return        
    if (enemy.type == 5 and player_fire == 1) == True: #Checks for fire weakness on corrupted knights
        enemy_health = 0
        player_fire = 0
        return
    else:
        enemy_health = enemy_health - player_damage * crit
        return

def defend(): #Enemy attacks
    global player_health
    global enemy_damage
    if player_health <= enemy_damage:
        player_health = 0
        return
    else:
        player_health = player_health - enemy_damage
        return

def itemspawn(): #Item spawning and placement in chest
    name = random.randint(0,4)
    if name == 0:
        damage = random.randint(0,2)
        health = random.randint(1,4)
        maxhealth = random.randint(0,2)
        fire = 0
    elif name == 1:
        damage = random.randint(1,3)
        health = 0
        maxhealth = 0
        fire = 0
    elif name == 3:
        fire = 1
        damage = random.randint(0,1)
        maxhealth = 0
        health = 0
    elif name == 4:
        damage = 0
        fire = 0
        maxhealth = random.randint(0,1)
        health = random.randint(1,5)
    else:
        damage = random.randint(1,2)
        health = 0
        maxhealth = random.randint(0,1)
        fire = random.randint(0,1)
    item = Item(name,health,maxhealth,damage,fire)
    chest.append(item)

def layer(): #Announces the layer and increments the depth counter
    global depth
    depth += 1
    g = f'Leyer {depth}'
    print(g.center(terminal_width),'\n')

def inv(): #Governs inventory control
    global inventory
    global inventorytext
    c = ' '
    q = ' '
    while q != 'q':
        print('\n', f'{inventorytext.center(terminal_width)}','\n',inventory,'\n')
        q = input('Picke a noumbre to chese thy item (list order), or use q to exit' '\n')
        try:
            q = int(q)-1
            choice = inventory[q]
            c=Item.use(choice)
            print(c)
        except:
            continue
        
def combat(): #Governs combat
    global enemy_health
    global player_health
    global enemy_maxhealth
    enemy_maxhealth = enemy_health
    fire = ' '
    while enemy_health or player_health > 0:
        if player_fire == 1:
            fire = '🔥'
        else:
            fire = ' '
        if enemy_health <= 0:
            print('Scoundrel Defeten!' '\n')
            return
        if player_health <=0:
            return
        print('\n',f"{enemy}'s Health: {enemy_health}",'\n',f'Thy Health: {player_health}/{player_maxhealth} ',f'Thy Strengthe: {player_damage}',f'Fyr:{fire}')
        choice = input('Use a to assaile or use i to vewe thy inventorie' '\n')
        choice = choice.lower()

        if choice == 'a':
            attack()
            if enemy_health <= 0:
                continue
            else:
                defend()
                continue
        elif choice == 'i':
            inv()
            continue

def loot(): #Governs looting at the end of a layer
    global chest
    global inventory
    itemspawn()
    itemspawn()
    while len(chest) > 1:
        ch = str(chest[0])
        ch2 = str(chest[1])
        print("Thou hast found a chest.",'\n',"Chest", '\n', f'{ch}; {ch2}')
        choice = input('\n''Picke a noumbre to chese one item (list order)' '\n')
        try:
            choice = int(choice) -1
            s = chest.pop(choice)
            inventory.append(s)
            chest = []
            return
        except:
            continue
            
quit_game = ' '
depth = 0
crits=[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,3,1,1,1,1,1,1,1] #4% default crit chance
chest = []
enemy = Enemy()
enemy_maxhealth = 1
enemy_health = 1
enemy_damage = 1
healing_potion = Item(0,3,0,0,0)
inventory = [healing_potion]
player_maxhealth = 10
player_health = 10
player_damage = 1
player_fire = 0 #Fire upgrade is a modifier for enemies weak to fire, instakills vulnerable enemies if 1
menu = 'The Dungeoun' #Menu text
inventorytext = "Inventorie"
congratulations = 'Congratulations! Thou hast founden the tresor!' #Victory text
terminal_width = os.get_terminal_size().columns #Finds width of terminal for centering
while 'q' not in quit_game:
    print(menu.center(terminal_width),'\n')
    cont = hash(input('Use any key''\n')) #Initial input will be used to seed crit chance
    if cont % 10 == 0:
        crits = [1,1,1,1,1,3,1,1,1,1] #10% crit chance if last digit of cont is 0
    depth = 0
    chest = []
    enemy = Enemy()
    enemy_health = 1
    enemy_damage = 1
    healing_potion = Item(0,3,0,0,0)
    inventory = [healing_potion]
    player_maxhealth = 10
    player_health = 10
    player_damage = 1
    player_fire = 0 
    while depth <= 12:
        if depth < 4: #If elif chain used for determining what enemies to spawn at each depth
            layer()
            espawnlow()
            combat()
            if player_health <= 0: #Allows player to continue or quit upon death, repeated in elif chain
                quit_game = input("Woldest thou like to assaye agayne? Use any key to assaye agayne, use q to quit" '\n')
                quit_game = quit_game.lower()
                if 'q' in quit_game:
                    quit()
                else:
                    depth = 0
                    enemy = Enemy()
                    enemy_health = 1
                    enemy_damage = 1
                    healing_potion = Item(0,3,0,0,0)
                    inventory = [healing_potion]
                    player_maxhealth = 10
                    player_health = 10
                    player_damage = 1
                    player_fire = 0 
                    continue
            else:
                loot()
        elif depth <= 8:
            layer()
            espawnmed()
            combat()
            if player_health <= 0:
                quit_game = input("Woldest thou like to assaye agayne? Use any key to assaye agayne, use q to quit" '\n')
                quit_game = quit_game.lower()
                if 'q' in quit_game:
                    quit()
                else:
                    depth = 0
                    enemy = Enemy()
                    enemy_health = 1
                    enemy_damage = 1
                    healing_potion = Item(0,3,0,0,0)
                    inventory = [healing_potion]
                    player_maxhealth = 10
                    player_health = 10
                    player_damage = 1
                    player_fire = 0 
                    continue
            else:
                loot()
        elif depth < 12:
            layer()
            espawnhi()
            combat()
            if player_health <= 0:
                quit_game = input("Woldest thou like to assaye agayne? Use any key to assaye agayne, use q to quit" '\n')
                quit_game = quit_game.lower()
                if 'q' in quit_game:
                    quit()
                else:
                    depth = 0
                    enemy = Enemy()
                    enemy_health = 1
                    enemy_damage = 1
                    healing_potion = Item(0,3,0,0,0)
                    inventory = [healing_potion]
                    player_maxhealth = 10
                    player_health = 10
                    player_damage = 1
                    player_fire = 0 
                    continue
            else:
                if depth < 12:
                    loot()
                else:
                    print(congratulations.center(terminal_width),'\n')