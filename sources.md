# Current research in multirobot systems
* p2: implicit vs explicit communication

# Modeling and Control of Formations of Nonholonomic Mobile Robots
* p1: locomotion can be broken down into 3 subproblems: trajectory planning, locomotion control, and formation control
* p1: "decentralized control laws that allows each robot to maintain a desired position within a formation and to enable changes in the shape of a team"
* p2: "Within the formation, the follower robots depend on other robots for their motion. Thus there are many leaders that 'lead' other follower robots, but there is a unique lead robot"
* p2: very interesting maths breakdown of hierarchy and formations

# What Is Artificial Life Today, and Where Should It Go?
__Alan Dorin, Susan Stepney; What Is Artificial Life Today, and Where Should It Go?. Artif Life 2024; 30 (1): 1–15. doi: https://doi.org/10.1162/artl_e_00435__

__(Alan Dorin, Susan Stepney,)__

# Biologically Inspired Multi-Robot Foraging
* bee inspired non-pheromone algorithms
* couldn't have worded it better myself: "multiple robots with limited sensing and computing power randomly explore an unknown environment until a food location is found and start foraging. By using local communication, the robots can ask other robots they encounter for the vector to the closest food location."
* "no map of the environment is built and the only known reference point is the hive location marker"
* "To simulate local communication, the robots can only communicate with another robot when it is in view and in close proximity, i.e. less than one meter away"

# A Study on Foraging Behavior of Simple Multi-robot System
* "Foraging is an act to go around searching for food or other supplies, and it can be considered the combination problem of parallel searching and cooperative transportation"
* Defines multiple behaviors for robots: wandering, broadcasting, attracted, homing, staying. and avoiding.
* Compares fixed vs unfixed point collecting

# Ant colony optimization
* "Biologists have shown that many colony-level behaviors observed in social insects can be explained via rather simple models in which only stigmergic [indirect] communication is present"
* "By sensing pheromone trails foragers can follow the path to food discovered by other ants. This collective trail-laying and trail-following behavior whereby an ant is influenced by a chemical trail left by other ants is the inspiring source of ACO"
* "In the Ant Colony Optimization, ants use heuristic information, which is available in many problems, and pheromone that they deposit along paths which guides them towards the most promising solutions. The most important feature of the ACO metaheuristic is that the ants search experience can be used by the colony as the collective experience in the form of pheromone trails on the paths, and a better solution will emerge as a result of cooperation."

# Stigmergy as a universal coordination mechanism
* "The principle is that work performed by an agent leaves a trace in the environment that stimulates the performance of subsequent work—by the same or other agents. This mediation via the environment ensures that tasks are executed in the right order, without any need for planning, control, or direct interaction between the agent"

# Reynolds CW. Flocks, herds and schools: a distributed behavioral model [the OG boids paper!!]
* "To build a simulated flock, we start with a boid model that supports geometric flight. We add behaviors that correspond to the opposing forces of collision avoidance and the urge to join the flock. Stated briefly as rules... the behaviors that lead to simulated flocking are:"
  1. collision avoidance
  2. velocity matching
  3. flock centering
* "Because each boid has a localized perception of the world, 'center of the flock' actually means the center of the nearby flockmates"
* If a boid is deep inside a flock, the population density in its neighborhood is roughly homogeneous; the boid density is approximately the same in all directions... so the flock centering urge is small
* As long as an individual boid can stay close to its nearby neighbors, it does not care if the rest of the flock turns away [ie the flock splits] More simplistic models proposed for flock organization (such as a central force model or a follow the designated leader model) do not allow splits."
* "The bold model does not directly simulate the senses used by real animals during flocking... the perception model tries to make available to the behavior model approximately the same information that is available to a real animal as the end result of its perceptual and cognitive processes"
* "The primary tool for scripting [directing] the flock's path is the migratory urge built into the boid model... specified in terms of a global target, either as a global direction (as in "going Z for the winter") or as a global position--a target point toward which all birds fly... Of course, it is not necessary to alter all boids at the same time,"

# Autonomous Boids
* Renamed 3 behaviors of boids to slightly snappier sounding names:
  1. separation (collision avoidance)
  2. alignment (velocity matching)
  3. cohesion (flock centering)
* Boids have limited vision that is defined by a variable that corresponds approximately to the five times the boid’s size. Every boid has associated a visibility sphere and everything that is inside is visible by the boid." Note this is just for boid like behaviour, not necessarily whatever perception we want!!

# An introduction to genetic algorithms
__Melanie Mitchell. (1998). An Introduction to Genetic Algorithms. Cambridge, Massachusetts: The MIT Press.__

__(Melanie Mitchell, 1998, p. x)__
* p5: "Most applications of genetic algorithms employ haploid individuals, particularly, single−chromosome individuals"
* p7: "most methods called "GAs" have at least the following elements in common: populations of chromosomes, selection according to fitness, crossover to produce new offspring, and random mutation of new offspring"
* p7: "The GA most often requires a fitness function that assigns a score (fitness) to each chromosome [ie each individual] in the current population."

# Other crap
__The British Beekeepers Association. (n.d.). What's in the hive?. [Online]. bbka.org.uk. Available at: https://www.bbka.org.uk/whats-in-the-hive [Accessed 16 April 2025].__

__(The British Beekeepers Association, n.d.)__
* A beehive can have between 5 and 60 thousand bees depending on colony size and season - [british beekeepers association](https://www.bbka.org.uk/whats-in-the-hive)

__San Diego Zoo. (n.d.). Meerkat. [Online]. animals.sandiegozoo.org. Available at: https://animals.sandiegozoo.org/animals/meerkat [Accessed 16 April 2025].__

__San Diego Zoo, n.d.__

__Kalahari Meerkat Project. (n.d.). Meerkat Population. [Online]. kalahariresearchcentre.org. Available at: https://kalahariresearchcentre.org/krc/fauna-and-flora/meerkat-population/ [Accessed 16 April 2025].__
 
__Kalahari Meerkat Project, n.d.__
* a group of meerkats, ranging from 5 to 30 members per group
* meerkats live in burrows

__Hannes Rollin. (2023). A Brief Introduction to Ultrastability. [Online]. Medium. Last Updated: 21 November 2023. Available at: https://medium.com/@hannes.rollin/a-brief-introduction-to-ultrastability-f8f413b1608a [Accessed 16 April 2025].__

__(Hannes Rollin, 2023)__
* Good article on, and overview of, ultrastability from [Medium](https://medium.com/@hannes.rollin/a-brief-introduction-to-ultrastability-f8f413b1608a)