# Example 1

This example demonstrates how to use the `EntityManager` to add and remove objects from a
game. 

The `EntityManager` manages game objects called Entities. Each entity is composed of separate
components that describe the entity. Note that in a strict ECS system, these components contain
only data and no behavior. The behavior is implemented in the System. You can see this in more
detail in Example 2. That said, there is nothing stopping you from adding behavior to these
components.


## Creating EntityManager

The entity manager is created with a list of all the queries that the systems will
use to access groups of entities during execution.

```
manager = EntityManager(EntityManagerOpts({
    PLAYER_CONTROLLABLE,
    MOVEABLE_BALL,
    RENDERABLE
}))
```

`PLAYER_CONTROLLABLE`, `MOVEABLE_BALL`, and `RENDERABLE` are all groups of flags defined
at the top of the code page.

## Spawning

New entities can be added to the `EntityManager`'s instance using the `spawn` method.

```
manager.spawn({
    TRANSFORM: {
        "position": (400, 300)
    },
    CIRCLE_SPRITE: {
        "radius": 10,
        "color": (255,255,255)
    },
})
```

This will add a new entity with a `TRANSFORM` and `CIRCLE_SPRITE` component to the world. This
entity will be picked up by the `render_circle` function and drawn on the screen.

## Queries

Each time around the game-loop, the _systems_, which are just functions in this case, are
called and given the `EntityManager`.  The _system_ can then query the entities and do something.

```
def render_circle(manager: EntityManager, ...):
    # Get all the entities
    for entity in manager.get_entities(RENDERABLE):
        sprite = entity[CIRCLE_SPRITE]
        # Do something with the components
        ...
```

Notice that the call to `get_entities` passes a constant called `RENDERABLE`. The `RENDERABLE`
constant is set at the top of `__main__` to the bitwise `or` of `TRANSFORM` and `CIRCLE_SPRITE`.

So, this query is obtaining every entity in the system that contains both a `TRANSFORM` and
`CIRCLE_SPRITE` component. The entity might contain more components but it is guarenteed to have at
least those two components.

You can use any query you would like as long as the EntityManager knows about it. See how to
build the entity manager above for details on how to speicify queries.

## Changing Scenes (Worlds)

The `EntityManager` implements an idea of _worlds_ where each world is a indpenent list of entities.
This is useful for moving between pause screens, settings, gameplay, and so on. 

To create a new, empty world, just call `activate_world` with an appropriate name and spawn
in new entities.

```
em.activate_world("PauseScene")
em.spawn(...)
```

You can then return to the privous world by calling `reactivate_world`.

```
em.reactivate_world("PlayScene")
```

note the `PauseScene` world still exists. It's just not active. You can return to the `PauseScene`
using reactivate or you can recreate the `PauseScene` by calling `activate_world` and `spawn`.

Lastly, you can destory a world.

```
em.destroy_world("PlayScene")
```

## Creating World from Templates

A better way to populate a world with in initial set of entities would be to use world templates.
This will store a entities in memory and copy them into a scene when activated.

First, create a scene template.

```
em.set_world_template("PauseScene", [
    {
        TEXT_SPRITE: {"value": "Hello, world"}
        TRANSFORM: {"position": (100, 100)}
    }
])
```

Now when we call `activate_world`, A new empty entity set will be created and the template will be
copied into it.

```
em.activate_world("PauseScene")
```

Note, a call to `reactivate_world` will NOT load the template unless the world doesn't exist. If the
world doesn't exist, it will call `activate_world` internally and thus, load the template.

## Other Features

Here are some other features not used in this demo but are avaiable in the `EntityManager`.

1. Killing an entity. `kill(entity)`
2. Adding a component to an entity. `add_component(entity, TRANFORM, {"position": (0, 0)})`
3. Removing a component from an entity. `remove_component(entity, TRANSFORM)`

Note in all three cases, you can pass the `entity` or `entity.identity`. Also note that it is
important to use the add and remove methods when changing the component list for an entity. If you
do not, the query groups will not reflect the correct component list.

## The Main Loop

In this example, we have a very simple gameloop that just calls the systems.  See examples 2 and 3
for ways to do this using features in the pyecs framework.

