import time
import random
import neat
import os
import pygame
# import visualize
import pickle
pygame.font.init()

WIN_HEIGHT = 800
WIN_WIDTH = 500

B_IMGS = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird1.png"))),pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird2.png"))),pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird3.png")))]
P_IMGS = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "pipe.png")))
BASE_IMGS = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "base.png")))
BG_IMGS = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bg.png")))

STAT_FONT = pygame.font.SysFont("Arial",50)

GEN = 0

class Bird:
    IMGS = B_IMGS
    MAX_ROT = 25 # bird move up and down
    ROT_VEL = 15 # speed of bird movement
    ANI_TIME = 3 # how long animation lasts

    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_count = 0
        self.vel = 0
        self.height = self.y
        self.img_count = 0
        self.img = self.IMGS[0] 

    def jump(self):
        self.vel = -10
        self.tick_count = 0
        self.height = self.y
    
    def move(self):
        self.tick_count+=1

        dis = self.vel*self.tick_count + 1.5*self.tick_count**2

        if dis >=15:
            dis = 15

        if dis<0:
            dis-=2
        
        self.y = self.y + dis

        if dis<0 or self.height + 50 >self.y:
            if self.tilt < self.MAX_ROT:
                self.tilt = self.MAX_ROT
        
        else:
            if self.tilt>-90:
                self.tilt -= self.ROT_VEL
    def draw(self,win):
        self.img_count +=1

        if(self.img_count < self.ANI_TIME):
            self.img = self.IMGS[0]
        
        elif self.img_count<self.ANI_TIME*2:
            self.img = self.IMGS[1]

        elif self.img_count<self.ANI_TIME*3:
            self.img = self.IMGS[2]

        elif self.img_count<self.ANI_TIME*4:
            self.img = self.IMGS[1]

        elif self.img_count<self.ANI_TIME*4+1:
            self.img = self.IMGS[0]
            self.img_count = 0
        
        if self.tilt <=-80:
            self.img = self.IMGS[1]
            self.img_count = self.ANI_TIME*2

        rotate_img = pygame.transform.rotate(self.img,self.tilt)
        new_rect = rotate_img.get_rect(center = self.img.get_rect(topleft = (self.x,self.y)).center)
        win.blit(rotate_img,new_rect.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.img)
    

class Pipe:
    GAP = 200
    VEL = 5

    def __init__(self,x):
        self.x = x
        self.height = 0
        self.gap =100

        self.top = 0
        self.bottom = 0
        self.PIPE_TOP = pygame.transform.flip(P_IMGS,False,True) #function) def flip(    surface: Surface,    flip_x: bool | Literal[0, 1],   flip_y: bool | Literal[0, 1]) -> Surface
        self.PIPE_BOTTOM = P_IMGS

        self.passed = False
        self.set_height()

    def set_height(self):
        self.height = random.randrange(50,450)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.GAP
    
    def move(self):
        self.x -= self.VEL

    def draw(self,win):
        win.blit(self.PIPE_TOP,(self.x,self.top))
        win.blit(self.PIPE_BOTTOM,(self.x,self.bottom))

    def collision(self,bird):
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)

        top_iffset = (self.x-bird.x, self.top - round(bird.y) )
        bottom_offset = (self.x-bird.x, self.bottom - round(bird.y))

        bottom_pt = bird_mask.overlap(bottom_mask,bottom_offset)
        top_pt = bird_mask.overlap(top_mask,top_iffset)

        if top_pt or bottom_pt: # to check collision
            return True
        return False


class Base:
    VEL = 5
    WIDTH = BASE_IMGS.get_width()
    IMG = BASE_IMGS

    def __init__(self,y):
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH

    def move(self):
        self.x1 -= self.VEL
        self.x2 -= self.VEL

        if self.x1 + self.WIDTH <0:
            self.x1 = self.x2+self.WIDTH

        if self.x2 + self.WIDTH <0:
            self.x2 = self.x1+self.WIDTH

    def draw(self,win):
        win.blit(self.IMG,(self.x1,self.y))
        win.blit(self.IMG,(self.x2,self.y))
    

def draw_window(win,birds,pipes,base,score,gen):
    win.blit(BG_IMGS,(0,0))
    for pipe in pipes:
        pipe.draw(win)
    text = STAT_FONT.render("Score: "+str(score),1,(255,255,255))
    win.blit(text,(WIN_WIDTH-10-text.get_width(),10))

    text = STAT_FONT.render("Gen: "+str(gen),1,(255,255,255))
    win.blit(text,(10,10))
    base.draw(win)
    for bird in birds:
        bird.draw(win)
    pygame.display.update()
    
def main(genomes,config):
    global GEN
    GEN+=1
    nets = []
    gee = []
    birds = []
    for _,ge in genomes:
        net = neat.nn.FeedForwardNetwork.create(ge,config)
        nets.append(net)
        birds.append(Bird(230,350))
        ge.fitness = 0   
        gee.append(ge)


    # bird = Bird(230,350)
    base = Base(750)
    pipes = [Pipe(550)]
    win = pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT))
    clock = pygame.time.Clock()
    score = 0

    run = True
    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()


        pipe_idx = 0
        if len(birds)>0:
            if(len(pipes)>1 and birds[0].x>pipes[0].x+pipes[0].PIPE_TOP.get_width()):
                pipe_idx = 1
        else:
            run =False
            break

        # bird.move()

        for x,bird in enumerate(birds):
            bird.move()
            gee[x].fitness +=0.1

            output = nets[x].activate((bird.y,abs(bird.y-pipes[pipe_idx].height),abs(bird.y-pipes[pipe_idx].bottom)))

            if output[0]>0.5:
                bird.jump()
        p = []
        pipe_passed =False
        add_pipe = False
        for pipe in pipes:
            for x,bird in enumerate(birds):
                if pipe.collision(bird):
                    gee[x].fitness -= 1
                    birds.pop(x)
                    gee.pop(x)
                    nets.pop(x)
                    
                if not pipe.passed and pipe.x < bird.x:
                    pipe.passed = True
                    add_pipe = True

            if pipe.x + pipe.PIPE_TOP.get_width()<0:
                p.append(pipe)

            pipe.move()
        
        if add_pipe:
            score+=1
            for ge in gee:
                ge.fitness +=2
            pipes.append(Pipe(550))

        for r in p:
            pipes.remove(r)
        for x, bird in enumerate(birds):
            if bird.y + bird.img.get_height() >=750 or bird.y<0 :
                birds.pop(x)
                gee.pop(x)
                nets.pop(x)

        if(score>1000):
            pickle.dump(nets[0],open("best.pickle", "wb"))
            
        base.move()
        draw_window(win,birds,pipes,base,score,GEN)





def run(config_path):
    config = neat.config.Config(neat.DefaultGenome,neat.DefaultReproduction,neat.DefaultSpeciesSet,neat.DefaultStagnation,config_path)

    p = neat.Population(config)
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(main,30)

if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir,"config.txt")
    run(config_path)
