import pygame
from pygame.locals import *
from sys import exit
from random import randint

WIDTH = 1900
HEIGHT = 1000
pygame.init()
SCREEN_SIZE = (WIDTH,HEIGHT)
clock = pygame.time.Clock()
screen = pygame.display.set_mode(SCREEN_SIZE, 0, 32)

import game_functions2 as f

genetic_table = {
    'rabbit': {
        'hunger_threshold' : {True: 375, False: 500},
        'starvation_threshold' : {True: 2000, False: 2500},
        'horny_threshold' : {True: 900, False: 750},
        'vision' : {True: 100, False: 150},
        'roam_speed' : {True: 15, False: 24},
        'sprint_speed' : {True: 25, False:30}
        },
    'wolf': {
        'hunger_threshold' : {True: 900, False: 1100},
        'starvation_threshold' : {True: 4000, False: 4500},
        'horny_threshold' : {True: 3800, False: 3000},
        'vision' : {True: 100, False: 150},
        'roam_speed' : {True: 15, False: 24},
        'sprint_speed' : {True: 25, False:30}
        }
    }

class Animal():
    def __init__(self, world, name, coord = f.Vector2(randint(0,WIDTH), randint(0,HEIGHT)), destination = f.Vector2(randint(0,WIDTH), randint(0,HEIGHT)), genes = 'default'):
        self.world = world
        self.name = name
        self.coord = coord
        self.coord_int = self.coord.int_()
        self.destination = destination
        self.vel = f.Vector2(0,0)
        self.color = (255,255,255)
        self.hungry = False
        self.horny = False
        self.pregnant = False
        self.prey = None
        self.mate = None
        self.prey_name = None
        self.frames_since_eaten = 150
        self.frames_since_mated = 0
        self.offspring_genes = 'default'
        if genes == 'default':
            self.genes = {
                'hunger_threshold' : [True, False],
                'starvation_threshold' : [True, False],
                'horny_threshold' : [True, False],
                'vision' : [True, False],
                'roam_speed' : [True, False],
                'sprint_speed' : [True, False],
                }
        else:
            self.genes = genes
        self.phenotype = self.get_phenotype()
        self.initiate_genetics()
        self.pixels_per_second = self.genes['roam_speed']
        
    def initiate_genetics(self):
        for gene in self.genes:
            attribute = genetic_table[self.name][gene][self.phenotype[gene]]
            setattr(self,gene,attribute)
    
    def hunt(self):
        if self.prey == None or self.prey.id not in self.world.entities:
            self.prey = self.world.get_close_entity(self.prey_name,self.coord, self.vision)
        if self.prey == None:
            self.roam()
        else:
            self.destination = self.prey.coord
            self.pixels_per_second = self.sprint_speed
            distance_to_prey = self.coord.get_distance_from_point(self.prey.coord)
            if distance_to_prey < 5:
                self.hungry = False
                self.frames_since_eaten = 0
                self.prey.die()
                self.prey = None

    def seek_mate(self):
        if self.mate == None or self.mate.id not in self.world.entities:
            self.mate = self.world.get_close_entity(self.name,self.coord, self.vision)
        if self.mate == None:
            self.roam()
        else:
            self.destination = self.mate.coord
            self.pixels_per_second = self.sprint_speed
            distance_to_mate = self.coord.get_distance_from_point(self.mate.coord)
            if distance_to_mate < 5:
                self.have_sex()

    def give_birth(self):
        if randint(1,200) == 1:
            self.world.entity_add_list.add(self.__class__(self.world, coord = self.coord, genes = self.offspring_genes))
        

    def have_sex(self):
        self.horny = False
        self.frames_since_mated = 0
        if randint(1,5) == 1:
            self.pregnant = True
            self.offspring_genes = self.get_child_genes()
        self.mate.horny = False
        self.mate.frames_since_mated = 0

    def get_child_genes(self):
        child_genes = {}
        for gene in self.genes:
            gene1_passed = self.genes[gene][randint(0,1)]
            gene2_passed = self.mate.genes[gene][randint(0,1)]
            child_genotype = [gene1_passed, gene2_passed]
            child_genotype.sort(reverse = True)
            child_genes[gene] = child_genotype
        return child_genes

    def get_phenotype(self):
        phenotypes = {}
        for gene in self.genes:
            phenotypes[gene] = (self.genes[gene][0] or self.genes[gene][1])
        return phenotypes


    def check_needs(self):
        if self.frames_since_eaten > self.hunger_threshold:
            self.hungry = True
        if self.frames_since_eaten > self.starvation_threshold:
            self.die()
        if self.frames_since_mated > self.horny_threshold:
            self.horny = True

    def die(self):
        self.world.entity_remove_list.add(self)
        

    def roam(self):
        self.pixels_per_second = self.roam_speed
        if self.coord == self.destination:
            self.destination = f.Vector2(randint(0,WIDTH), randint(0,HEIGHT))
        if randint(1,300) == 1:
            self.destination = f.Vector2(randint(0,WIDTH), randint(0,HEIGHT))
        
    def move(self, time_passed_seconds):
        if self.coord == self.destination:
            return None
        heading = self.coord.get_heading(self.destination)
        heading.normalize()
        distance = self.pixels_per_second*time_passed_seconds
        self.coord += heading*distance
        self.coord_int = self.coord.int_()

    def process(self, time_passed_seconds):
        self.frames_since_eaten += 1
        self.frames_since_mated += 1

        self.check_needs()
        
        if self.hungry:
            self.hunt()
        elif self.horny:
            self.seek_mate()
        elif self.pregnant:
            self.give_birth()
            self.roam()
        else:
            self.roam()
        
        self.move(time_passed_seconds)

    def render(self, screen):
        pygame.draw.circle(screen, self.color, (self.coord_int.x, self.coord_int.y), 3)

class Wolf(Animal):
    def __init__(self, world, coord = f.Vector2(randint(0,WIDTH), randint(0,HEIGHT)), destination = f.Vector2(randint(0,WIDTH), randint(0,HEIGHT)), genes = 'default'):
        Animal.__init__(self, world, name = 'wolf', coord = coord, destination = destination, genes = genes)
        self.color = (50,50,50)
        self.prey_name = 'rabbit'
    
        
class Rabbit(Animal):
    def __init__(self, world, coord = f.Vector2(randint(0,WIDTH), randint(0,HEIGHT)), destination = f.Vector2(randint(0,WIDTH), randint(0,HEIGHT)), genes = 'default'):
        Animal.__init__(self, world, name = 'rabbit', coord = coord, destination = destination, genes = genes)
        self.color = (255,255,255)
        self.prey_name = 'lettuce'

class Lettuce():
    def __init__(self, world, coord = f.Vector2(randint(0,WIDTH), randint(0,HEIGHT))):
        self.world = world
        self.coord = coord

        if self.coord.x > WIDTH: self.coord.x = WIDTH
        if self.coord.x < 0: self.coord.x = 0
        if self.coord.y > HEIGHT: self.coord.y = HEIGHT
        if self.coord.y < 0: self.coord.y = 0
        
        self.coord_int = self.coord.int_()
        self.color = (50,150,50)
        self.name = 'lettuce'
        

    def die(self):
        Animal.die(self)

    def reproduce(self):
        if randint(1,5000) == 1:
            self.world.entity_add_list.add(self.__class__(self.world, coord = self.coord + f.Vector2(randint(-50,50), randint(-50,50))))

    def process(self, time_passed_seconds):
        self.reproduce()

    def render(self, screen):
        pygame.draw.circle(screen, self.color, (self.coord_int.x, self.coord_int.y), 3)
        

pixels_per_second = 10
world = f.World()

for i in range(10):
    world.add_entity(Wolf(world, coord = f.Vector2(randint(0,WIDTH), randint(0,HEIGHT))))
for i in range(35):
    world.add_entity(Rabbit(world, coord = f.Vector2(randint(0,WIDTH), randint(0,HEIGHT))))
for i in range(255):
    world.add_entity(Lettuce(world, coord = f.Vector2(randint(0,WIDTH), randint(0,HEIGHT))))

data = {
    'horny_rabbits': [],
    'wolf vision' : [],
    'wolf hunger_threshold' : [],
    'horny_wolves' : [],
    'wolf horny_threshold' : [],
    'hungry_rabbits' : [],
    'horny_rabbits' : [],
    'rabbit sprint_speed' : [],
    'wolf starvation_threshold' : [],
    'hungry_wolves' : [],
    'rabbit starvation_threshold' : [],
    'wolf sprint_speed' : [],
    'wolf roam_speed' : [],
    'rabbit vision' : [],
    'rabbit roam_speed' : [],
    'num_lettuce' : [],
    'num_rabbits' : [],
    'rabbit hunger_threshold' : [],
    'num_wolves' : [],
    'rabbit horny_threshold' : [],
    }

def write_data(data, filename = 'Wolf Rabbit Data.txt'):
    keys = list(data.keys())
    with open(filename,'w') as g:
        for key in keys:
            g.write('%s\t' %key)
        g.write('\n')
        for i in range(len(data[keys[0]])):
            for key in keys:
                g.write('%s\t' %data[key][i])
            g.write('\n')
        

frame_num = 500
while True:    
    for event in pygame.event.get():
        if event.type == QUIT:
            write_data(data)
            exit()

    #MAIN GAME LOOP GOES HERE
    
    screen.fill((0,150,20))
    time_passed = clock.tick(70)
    time_passed_seconds = time_passed/1000

    world.process(time_passed_seconds)
    world.render(screen)
    
    frame_num += 1
    if frame_num >= 500:
        data['num_wolves'].append(len([1 for entity in world.entities.values() if entity.name == 'wolf']))
        data['num_rabbits'].append(len([1 for entity in world.entities.values() if entity.name == 'rabbit']))
        data['num_lettuce'].append(len([1 for entity in world.entities.values() if entity.name == 'lettuce']))
        data['hungry_wolves'].append(len([1 for entity in world.entities.values() if (entity.name == 'wolf' and entity.hungry)]))
        data['hungry_rabbits'].append(len([1 for entity in world.entities.values() if (entity.name == 'rabbit' and entity.hungry)]))
        data['horny_wolves'].append(len([1 for entity in world.entities.values() if (entity.name == 'wolf' and entity.horny)]))
        data['horny_rabbits'].append(len([1 for entity in world.entities.values() if (entity.name == 'rabbit' and entity.horny)]))
        rabbits = [entity for entity in world.entities.values() if entity.name == 'rabbit']
        wolves = [entity for entity in world.entities.values() if entity.name == 'wolf']
        for item in rabbits[0].phenotype:
            data['rabbit ' + str(item)].append(len([rabbit for rabbit in rabbits if rabbit.phenotype[item] == False])/len(rabbits))
            data['wolf ' + str(item)].append(len([wolf for wolf in wolves if wolf.phenotype[item] == False])/len(wolves))
        print('500 more frames...')
        frame_num = 0
    
    
    
    if randint(0,400) == 1:
        world.add_entity(Lettuce(world))

    
    
    pygame.display.update()
