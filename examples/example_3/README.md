# Example 3

This example demonstrates how use the built-in `Game` class to simplify the game loop.

The `Game` class provides 4 things.

1. Keeps track of the frame delay.
2. Executes the `SystemManager`'s update(...) method.
3. Monitors `pygame.event`s for an exit signal.
4. Holds references to other game classes like the `EntityManager`.

## Creating A Game

First, you will need to have functional `EntityManager` and `SystemManager`. Additionally, you can
provide a `IFactory` object if you would like. However, this is not required in this example. We
will learn more about `IFactory` in the 4th example.

If we have those things ready, we can create a game like this:

```
from pyecs import Game
my_game = Game(entity_manager, system_manager, factory=None)
my_game.play()
```

Alternativly, you can subclass the `Game` class to add startup and teardown code.

```
class MyGame(Game):

    p1: int

    def setup(self):
        """Add some setup code here. Like, loading player data."""
        entity = load_player_data()
        self.p1 = self.entity_manager.spawn(entity)

    def teardown(self):
        """Add some teardown code. Like saving player data."""
        entity = self.entity_manager.get_entity(self.p1)
        save_player_data(entity)
```

And now we can create the game object in the same way we did before, but using our new class.

```
my_game = MyGame(entity_manager, system_manager, factory=None)
my_game.play()
```

And that is pretty much all there is to it.
