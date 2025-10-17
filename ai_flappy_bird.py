import neat.population
import pygame
import neat
import os
import random

GEN=0
WIN_WIDTH=500
WIN_HEIGHT=800

BIRD_IMAGES = [
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird1.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird2.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird3.png")))
]
PIPE_IMAGE=pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","pipe.png")))
BASE_IMAGE=pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","base.png")))
BG_IMAGE=pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bg.png")))

pygame.font.init()
STAT_FONT=pygame.font.SysFont("comicsans",50)


class Bird:

    IMGS=BIRD_IMAGES
    MAX_ROTATION=25 #how much bird can tilt when moving up/down.
    ROT_VELOCITY=20 #how fast bird rotates.
    ANIMATION_TIME=5 #how long it takes to change bird animation.

    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.tilt=0
        self.tick_count=0 
        self.vel=0
        self.height=self.y
        self.img_count=0 #tells you what image is currently being shown.
        self.img=self.IMGS[0]

    def jump(self):
        self.vel= -10.5 #negative velocity to go upwards.
        self.tick_count=0 #keeps track of when we last jumped.
        self.height=self.y #keeps track of where the bird jumped from.
        
    def move(self): #controls bird's vertical movement and rotation. Simulates gravity.
        self.tick_count+=1
        d=self.vel*self.tick_count+1.5*self.tick_count**2 #displacement

        if d>=16: # limits downward speed.
            d=16
        if d<0:
            d-=2
        self.y=self.y+d

        if d<0 or self.y<self.height+50: # If bird is moving upwards, this tilts it upwards.
            if self.tilt<self.MAX_ROTATION:
                self.tilt=self.MAX_ROTATION

        else: #If bird is falling, it gradually tilts till -90 degrees (straight down).
            if self.tilt>-90:
                self.tilt-=self.ROT_VELOCITY
    
    def draw(self,win): #Animates bird movement by switching between images.
        self.img_count+=1
        if self.img_count<self.ANIMATION_TIME:
            self.img=self.IMGS[0]
        elif self.img_count<self.ANIMATION_TIME*2:
            self.img=self.IMGS[1]
        elif self.img_count<self.ANIMATION_TIME*3:
            self.img=self.IMGS[2]
        elif self.img_count<self.ANIMATION_TIME*4:
            self.img=self.IMGS[1]
        elif self.img_count<self.ANIMATION_TIME*4+1:
            self.img_count=0
        
        if self.tilt<=-80: #If bird is nose diving use image 1.
            self.img=self.IMGS[1]
            self.img_count=self.ANIMATION_TIME*2
        
        rotated_image=pygame.transform.rotate(self.img,self.tilt)
        #new_rect so we can rotate the image around the centre.
        new_rect=rotated_image.get_rect(center=self.img.get_rect(topleft=(self.x,self.y)).center)

        win.blit(rotated_image, new_rect.topleft)
    
    def get_mask(self):
        return pygame.mask.from_surface(self.img) #Returns 2D list of coordinates where the bird actually is. Helps with collison determination.

class Pipe:
    GAP=200 #gap b/w pipes.
    VEL=5

    def __init__(self,x):
        self.x=x
        self.height=0
        self.top=0 #where top of pipe is drawn
        self.bottom=0#where bottom of pipe is drawn
        self.PIPE_TOP=pygame.transform.flip(PIPE_IMAGE,False,True)
        self.PIPE_BOTTOM=PIPE_IMAGE

        self.passed=False
        self.set_height()

    #Defines where top,bottom,and how tall pipe is.
    def set_height(self):
        self.height=random.randrange(50,450)
        self.top=self.height-self.PIPE_TOP.get_height()

        self.bottom=self.height+self.GAP
    def move(self):
        self.x-=self.VEL

    def draw(self,win):
        win.blit(self.PIPE_TOP, (self.x,self.top))
        win.blit(self.PIPE_BOTTOM, (self.x,self.bottom))

    def collide(self,bird):
        bird_mask=bird.get_mask()
        top_mask=pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask=pygame.mask.from_surface(self.PIPE_BOTTOM)

        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

        b_point = bird_mask.overlap(bottom_mask, bottom_offset) #checks for collision. None if not
        t_point = bird_mask.overlap(top_mask,top_offset)

        if b_point or t_point:
            return True

        return False

class Base:

    VEL=5
    WIDTH=BASE_IMAGE.get_width()
    IMG=BASE_IMAGE

    def __init__(self,y):
        self.y=y
        self.x1=0
        self.x2=self.WIDTH

    def move(self): #moves floor.
        self.x1-=self.VEL
        self.x2-=self.VEL

        if self.x1 + self.WIDTH < 0: #If image is off the screen, move it behinhd the second image.
            self.x1 = self.x2 + self.WIDTH

        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH

    def draw(self, win):
        win.blit(self.IMG, (self.x1, self.y))
        win.blit(self.IMG, (self.x2, self.y))







def draw_window(win,birds,pipes,base,score, gen):
    win.blit(BG_IMAGE,(0,0))
    for pipe in pipes:
        pipe.draw(win)
    base.draw(win)
    for bird in birds:
        bird.draw(win)
    text=STAT_FONT.render("Score: " + str(score),1,(255,255,255))
    win.blit(text, (WIN_WIDTH-10-text.get_width(),10))

    text=STAT_FONT.render("Gen: " + str(gen),1,(255,255,255))
    win.blit(text,(10,10))
    pygame.display.update()


def main(genomes,config): #Runs game and acts as fitness function for NEAT.
    global GEN
    GEN+=1
    nets=[]
    ge=[]
    birds=[]



    for _,g in genomes:
        net=neat.nn.FeedForwardNetwork.create(g,config)
        nets.append(net)
        birds.append(Bird(230,350))
        g.fitness=0
        ge.append(g)
    
    base=Base(650)
    win=pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT))
    pipes=[Pipe(650)]
    run=True
    clock=pygame.time.Clock()
    score=0
    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False
                pygame.quit()
                quit()
        
        pipe_ind=0
        if len(birds)>0: #updates what pipe is being looked at once the bird passes previous pipe.
            if len(pipes)>1 and birds[0].x> pipes[0].x+pipes[0].PIPE_TOP.get_width():
                pipe_ind=1
        else:
            run=False
            break
       

        for x,bird in enumerate(birds):
            bird.move()
            ge[x].fitness+=0.1

            output=nets[x].activate((bird.y,abs(bird.y-pipes[pipe_ind].height), abs(bird.y-pipes[pipe_ind].bottom)))
            
            if output[0]>0.5:
                bird.jump()
    

        
        base.move()
        rem=[]
        add_pipe=False
        for pipe in pipes:
            for x,bird in enumerate(birds):
                if pipe.collide(bird):
                    ge[x].fitness-=1
                    birds.pop(x)
                    nets.pop(x)
                    ge.pop(x)

                if not pipe.passed and pipe.x<bird.x: #Checks if bird is infront of/passed the pipe.
                    pipe.passed=True
                    add_pipe=True
            if pipe.x+pipe.PIPE_TOP.get_width()<0:
                rem.append(pipe) 

            pipe.move()
        if add_pipe:
            score+=1
            for g in ge:
                g.fitness+=5
            pipes.append(Pipe(650))
        
        for r in rem:
            pipes.remove(r)
        
        for x,bird in enumerate(birds):
            if bird.y+bird.img.get_height()>=650 or bird.y<0: #removes bird if it goes higher/lower than top/bottom of screen.
                birds.pop(x)
                nets.pop(x)
                ge.pop(x)
                
        if score>50:
            break

      
        draw_window(win,birds,pipes,base,score,GEN)
        
        
    




def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)

    
    p=neat.Population(config)

    #Give stats on our populations.
    p.add_reporter(neat.StdOutReporter(True))
    stats=neat.StatisticsReporter()
    p.add_reporter(stats)

    winner=p.run(main,50)


if __name__ == "__main__":
    local_dir=os.path.dirname(__file__) #path to current directory.
    config_path=os.path.join(local_dir, "config_NEAT.txt")
    run(config_path)

            


