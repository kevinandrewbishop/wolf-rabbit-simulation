# wolf-rabbit-simulation
Pygame simulation of wolf and rabbit population dynamics. 


##Overview
This simulation was inspired by <a href="https://en.wikipedia.org/wiki/Lotka%E2%80%93Volterra_equation">wolf/rabbit
population dynamics</a>. In some areas, wolves and rabbits undergo counter-cyclical population levels in which  
* Rabbits reproduce to great levels
* The wolf population rises due to the abundance of food
* The rabbit population is reduced due to hunting
* The wolf population is reduced due to lack of food
* Rabbits now have fewer natural predators... repeat step 1
  
The simulation wasn't designed with this dynamic hard-wired into it. Instead I wanted the cycle to be
a property that emerged naturally from a simulation of wolves, rabbits (and lettuce) all reproducing and dying
based on contact with mates and prey.  

Each animal is a python class representing a <a href="https://en.wikipedia.org/wiki/Finite-state_machine">state transition machine<a/> having three states: hungry, horny, and roaming with corresponding actions of hunting, mating
and walking around randomly.  

Each animal has different characteristics such as speed, distance of vision, starvation thresholds etc. These
characteristics are determined by the genetics of the animal, which are determined by the genetics of the animal's
parents. Each animal has a genotype and phenotype for each of its characteristics, complete with dominant and
recessive traits. When two animals mate, their genetics are randomly mixed to create the genotype of the offspring.
Over time, natural selection alters the genetic landscape of the animal populations. Sometimes starvation or overhunting
cause <a href="https://en.wikipedia.org/wiki/Population_bottleneck">population bottlenecks</a> in one of the animal
populations that also change the genetic landscape.  

All of this data is recorded every 500 frames of the main game loop and is written to a file called "Wolf Rabbit
Data.txt" when the game screen is closed. This data can be used to plot population changes over time. The simluation
typically needs to be run for several thousand frames before interesting results become clear. Additionally, because
the simulation has a stochastic component and because it is relatively small scale (i.e. population size are in the 10s
to 100s) sometimes a population dies out quickly before any cycles or interesting genetic results become apparent.