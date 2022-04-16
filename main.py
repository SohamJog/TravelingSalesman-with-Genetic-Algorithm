
#Travelling Salesman Problem with Genetic Algorithm


import pygame
import random
import math



pygame.init()


#window variables
WIDTH, HEIGHT = 1000,750
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
BLACK = (0,0,0)
WHITE=(255, 255, 255)
YELLOW = (255,255,0)
FPS = 60
WORD_FONT = pygame.font.SysFont('comicsans', 20)


#general variables
N = 10


def distance(p1,p2):
    return math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

#node variables
RADIUS = 10
centers = []
mindist = 30
#create nodes
while len(centers)<N:
    x = random.randint((WIDTH//10), WIDTH-(WIDTH//10))
    y = random.randint((HEIGHT//5), HEIGHT-(HEIGHT//10))
    ok = True
    for Z in centers:
        lol = (x,y)
        if distance(Z, lol)<mindist:
            ok = False
            break
    if ok: centers.append((x,y))



#Gene Variables
maxPopulation = 500
mutationRate = 0.01
population = {}
previous_population = {}
fitness = []
BestOfAll = []



def find_fitness(arr):
    score = 1

    for i in range(len(arr)-1):
        score+=distance(centers[arr[i]], centers[arr[i+1]])
    score+=math.dist(centers[arr[0]], centers[arr[N-1]])

    return score


#initialize first generation
for i in range(maxPopulation):
    temp = []
    for j in range(N):temp.append(j)
    previous_population[i] = []
    population[i] = []
    random.shuffle(temp)
    population[i]=temp
    previous_population[i]=temp 
    
    fitness.append(find_fitness(temp))





#draw the BestOfAll set of edges
def mainedge():
    curr = BestOfAll[0]
    nxt = BestOfAll[1]
    for i in range(N):
        pygame.draw.line(WIN, YELLOW, (centers[curr]), (centers[nxt]), 3)
        curr = nxt
        nxt = BestOfAll[(i+1)%N]
    pygame.draw.line(WIN, YELLOW, (centers[BestOfAll[N-1]]), (centers[BestOfAll[0]]), 3)

#draw edges from the population
#currently not in use
def auxedge(arr):
    curr = arr[0]
    nxt = arr[1]
    for i in range(N):
        pygame.draw.line(WIN, WHITE, (centers[curr]), (centers[nxt]), 1)
        curr = nxt
        nxt = arr[(i+1)%N]
    pygame.draw.line(WIN, WHITE, (centers[arr[N-1]]), (centers[arr[0]]), 1)


gen = 0
F =10000000000   





#functions for reproduction
#call during every replication phase    
#based on towardsdatascience
def mutate(individual):
    for swapped in range(len(individual)):
        if(random.random() <= mutationRate):

            swapWith = int(random.random() * len(individual))
            
            p1 = individual[swapped]
            p2 = individual[swapWith]
            
            individual[swapped] = p2
            individual[swapWith] = p1
    return individual

    

#binary search
def chooseParent(prob, sum):

    target = random.randrange(0,100)
    lo = 0
    hi = maxPopulation-1
    while(lo<hi):
        mid = ((lo+hi+1)//2)
        if(prob[mid]>target):
            hi = mid-1
        else: lo = mid
    
    #print(lo)
    return previous_population[lo]
    

#return array
#based on towardsdatascience
def crossover(p1, p2):


    geneA = int(random.random() * len(p1))
    geneB = int(random.random() * len(p2))

    child = []
    childP1 = []
    childP2 = []
    
    startGene = min(geneA, geneB)
    endGene = max(geneA, geneB)

    for i in range(startGene, endGene):
        childP1.append(p1[i])
    
    childP2 = [item for item in p2 if item not in childP1]

    child = childP1 + childP2
    return child




def draw():


    global previous_population
    global population
    global F, BestOfAll

    #print(gen)
  
  


    #if(gen==2):print(BestOfAll)
    for node in centers:
        x,y = node
        pygame.draw.circle(WIN, WHITE, (x,y), RADIUS, 10)
    


    for i in range(maxPopulation):


        if(fitness[i]<F):
            #print('*')

            BestOfAll = population[i]
            F=fitness[i]
            
    
    mainedge()
    output = WORD_FONT.render(f"Distance: {F}", 1, YELLOW)
    WIN.blit(output, (100,10))
    output = WORD_FONT.render(f"Generation: {gen}", 1, YELLOW)
    WIN.blit(output, (100,60))

    pygame.display.update()

    
    previous_population = population

    prob = []
    for i in range(maxPopulation):prob.append(0)
    sum = 0
    for p in fitness:
        sum+=1/p
    
    for i in range(maxPopulation):
        prob[i]= 100*(1/fitness[i])/sum

    
    #make it cumulative
    for i in range(maxPopulation):
        if i==0: continue
        prob[i]+=prob[i-1]

    for i in range(maxPopulation):

        #change the chooseParent algo

        A = chooseParent(prob, sum)
        B = chooseParent(prob, sum)
        #dont mutate yet


        child = mutate((crossover(A,B)))

        population[i] = child
        fitness[i] = find_fitness(child)

    



    





#print(population)




run = True


while run:
    for event in pygame.event.get():
        if (event.type==pygame.QUIT): 
            run = False
    draw()
    gen+=1
    WIN.fill(BLACK)


pygame.quit()
