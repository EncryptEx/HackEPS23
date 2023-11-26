# HackEPS23
Built a pathfinder to search the fastest way to get some articles in the minimum amount of time possible.


## Inspiration
We've been prompted with an innovative TSP but in a supermarket enviroment, where we are have some extra parameters to take into account inside the equation: 
There are two levels, which we foucsed mainly on the first one (since we wanted to build the skateboard and if possible, then improve it till it's a lanmborgini)

The first level is based on the following statement and rules (4th section):
Take a look at the [documentation PDF (ES)](docs/statement.pdf)

## What it does
We have implemented how to solve the [TSP (Travell Sales Problem)](https://en.wikipedia.org/wiki/Travelling_salesman_problem) with a dynamic algorithm aproach called: Held-Karp TSP

<!-- TODO: COMPLETE THIS -->

## How we built it
We split the project into two main parts, as they suggestes us to do so:
- The frontend

This part was the easiest one, since we met the specified requierments in order to acomplish the following goals:
    - T1: Highlight the cell whenever its being accessed by a user. 
    (We have opted to simplify this by highlighting the user's cell position, due to the fact that there's no other cell to access an article from another cell apart from the one next to it)

- The algorith/backend
The Held-Karp TSP algorithm we've implemented needs some data, so we first started parsing it. After some iterations, we managed to get complete controll over the input datasets, located inside the `input` folder. We have based the data controll by using Python dictionaries, which are very useful because of key-value paired data, this helps us to relate specific customer_id data in a single place.


The algorithm breaks into smaller pieces the huge problem to be able to solve it:
It first gets all the coordinates from the required checkpoints to stop on. Then, we compute the necessary steps to reach from a checkpoint to another (including the entrance and exit of the building)
<!-- TODO: algorithm explanation -->




## Challenges we ran into
The hardest task was to join the frontend, backend and its parts. The main problem was that we had to work both paralelly and assume each other would provide the correct data and formats. Spoiler: That didn't happen XD. So first, we had to fix our code, finish the implementation and try to bring it to life, which ended up with us pair-programming the most of the time to avoid human errors (a great thing to be a 2p team).




## Accomplishments that we're proud of
We accomplish to finish successfully the **graphic part**, as well as all 3 challenges in it (T1, T2, T3)


## What we learned
Regarding the algortihm, it was a great experience learning how can we break into pieces a problem to solve it by parts into a smaller and easier problem to approached

## What's next for 
We'd like to spend more time with this problem, thanks to its great documentation and high time-consuming preparation (yes, its extremely hard to preparate such challenge)


## Aknowledgements
Thanks to LleidaHack for hosting HackEPS 2023 and BonArea IT to bring us this challenge.