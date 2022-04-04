# Example 2

This example demonstrates how to use the SystemManager to implement game logic.

The `SystemManager` manages the different parts of the logic for your game. It requires that you
describe each system as a `pyecs.typing.ISystem`. `ISystem` is a simple interface that provides
a consistant way for your system to be called.

## Creating A SystemManager

The system manager manages systems. We have not built any systems yet but that's ok. We will do that
in a moment.  Lets first create a new SystemManager object.

```
system_manager = SystemManager()
```

That's not to complicated but we need to do more if we are going to get anything out of it. Next, we
need to add systems.

## Creating A System

In order to use the `SystemManager`, you first needs systems. A system is a class that implements
the `ISystem` interface.

Here is an example of a simple system.

```
from pyecs.typing import ISystem

class ExampleSystem(ISystem):
    def update(self):
        print("Frame Update")
```

This is great but not to useful. The above example cannot interact with game objects which is pretty
important for writting game logic.  Lets fix that.

```
from pyecs.typing import ISystem, ISystemManager

class ExampleSystem(ISystem):
    def update(self):
        for entity in self.em.get_entities(SOME_QUERY):
            print(f"Look, a game object: {entity}")

    def __init__(self, em: IEntityManager):
        self.em = em
```

Notice how the entity manager is passed into the system through the constructor. Ofcourse, you can
pass in other dependencies as well if you want to add additional functionality to a system. This
approach is called dependency injection and can be a bit cumbersome to manage. `pyecs` does provide
a manager for dependency injection called the `GameBuilder`. That is described in Example 4.

## Registering Systems

Now that we have a `SystemManager` and some `ISystem`s. lets regiser them so we can use them.

```
example_system = ExampleSystem(em)
system_manager.install(example_system)
```

First we instanciate our systems. Note, I assume you already have an `EntityManager` object named
`em`. Then, we install it.

## Using the SystemManager

Lastly, we need to use the `SystemManager` in the main game loop. Here we will use a simple `for`
loop that will never exit. but you can see more in the demo.

```
while True:
    system_manager.update()
```

And that's it.  In the next example, we will demonstrate a better approach to the game loop.
