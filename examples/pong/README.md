# Pong Example

This is a pyecs demo that exorsizes many features of the pyecs framework.

These features include:

1. Using the builder to provide automatic dependency injection.
2. Using custom providers to give systems access to external resources.
3. Loading "worlds" from templates to allow for simple scene transitions.

## Example Overview

Before we dig into the details, I would like to callout a few points.

First, the folder structure is not perscriptive. I attempted to structure this game in a way that
can grow without turning into chaos. I don't know if I actually achieved that and the world
management is probably not optimal.  So take the application structure as a my best guess. 

Next, the implementation of networking is probably terrable. I have never built a networked
game before so I am probably breaking some fundimental rules. If nothing else, the client
and host don't know who eachother are so cheating would be exceedingly simple. Also, pyecs
is lacking real network support.  The EntityManager needs a way to communicate with the client
so we can spawn additional entities.  If anyone would like to add this functionality, PullRequests
are welcome!

Lastly, The AI is terrible.  I know it's terrible and i am not going to fix it.  It's just a demo.


### Entry Point: Building the game

In the `__main__.py` file, you will find the game entry point. This will create the game using
the `pyecs.GameBuilder` class. Every system, and provider are given to the builder so it can
manage automatic dependecy injection.

In addition to providers and systems, the builder is also made aware of every possible query that
can be issued to the EntityManager. During development, I continualy forgot to update this list. so,
don't forget to update that code if you add more queries.

### Components: Keep it orginized

Inside the `components` module are the data structures, flags, and queries used to define
entityies.

*Flags* are component identifiers used to extract the datastructures from an entity

*Queries* are groups of component flags used to find entities with matching flags.

*Models* are the datastructures of the components.

When you query the EntityManager Manager you will get an iterator of entities that have
at least all of the components included in the query. You can then get to the model by
indexing into the resulting entity.

```
Query using queries
for entity in self.em.get_entities(queries.BALL):
    # Get datastructures using flags
    transform: Transform = entity[flags.TRANSFORM]
    # use the datastructure
    print(transform.position)
```

### Systems: The actual game logic

In the `systems` module, you will find the game logic broke into functional groups. For
example, in `input.py` exists the `InputSystem` which is responsible for collecting user
input and mutating the appropriate entity data.

Here is the intended scope of each system.

The *AiSystem* implements logic to control the second-player paddle as an NPC.

The *InputSystem* Collects user input and applies it to the player's paddle or other
components that can take input.

The *MovementSystem* applies the physics of motion (as simple as they are) to the movable
entities in the game.

The *NetworkSystem* uses external providers to exchange data over the network with another player.

The *PlaySystem* manages win-conditions and tracks the game score.

The *RenderSystem* draws sprites to the screen and updates the hardware surface.

The *TemporialSystem* desrtoys entities that have expired due to a timestamp.

### Providers: Poorly written networking

The `providers` module contains code that is not part of the ECS pattern and provide external
logic to the system.

The *NetworkInput* object collects data from a remote players. The `NetworkSystem` uses that
data to update the local entities.

The *NetworkOutput* object sends data to remote players. The `NetworkSystem` uses this class
to send local data to the remote player.

# Play the game

This game implements 2 play modes.

1. Play an AI that almost to good.
2. Play a friend over a local network.

## Play the AI

Run the following command in a terminal from the pyecs project root.

```
python -m examples.pong
```

## Play over the Network

First, collect the IP address for each computer that is playing.

Than, run the following commanad from the player's terminal running as the host. Note: replace
`CLIENT_IP` with the IP address of the other computer.

```
python -m examples.pong --host --remote-endpoint CLIENT_IP 2040 --listen-port 2041
```

Next, run the following command from the player's terminal running as the client. Note: replace
`HOST_IP` with the ip address of the other computer.

```
python -m examples.pong --client --remote-endpoint HOST_IP 2041 --listen-port 2040
```

Once both hosts are running, Have the client player press enter.  Once the client can see the game
field, the host player can press enter. This will start the game.

