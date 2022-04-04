# Example 4

This example demonstrates how use `GameBuilder`.

The `GameBuilder` is a better way to handle dependency injection. It is not required but sure makes
life easy.

## Creating a GameBuilder

Nothing special here. Instanciate the object and start using it.

```
from pyecs import GameBuilder

builder = GameBuilder()
```

## Specify Build Options

We can start to manipulate the game's enviroment by calling the `using_*` methods.

Lets set the screen size and add some systems

```
builder.using_screen_mode((800, 600))
builder.using_system(MySystem)
```

Next, lets add some entity queries that will be passed to the `EntityManager`.

```
builder.using_component_groups({
    PLAYER_CONTROLLABLE,
    MOVEABLE_BALL,
    RENDERABLE,
})
```

Now lets add a world template and activate it.

```
builder.using_world_template("HelloScene", [
    {
        TRANSFORM: {"position": (100, 100)},
        TEXT_SPRITE: {"value": "Hello, World"},
    },
])

builder.using_active_world("HelloScene")
```

And lastly, play the game!

```
builder.play()
```

Alternativly you can get get the game object and start it yourself.

```
game = builder.build()
game.play()
```

## Custom Providers

In order to provide dependency injection to external classes, the `GameBuilder` offers a method to
bind additional providers to the dependency graph. This is done with the `using_provider` method.

Lets bind a provider.

```
class Provider1:
    ...

builder.using_provider(Provider1)
```

Provider1 can now be accessed in 2 ways.

1. By specifying it as a constructor parameter in a service or other provider.
2. Obtaining it directly from the `IFactory` object.

Here is an example of a constructor parameter used inside a ISystem.

```
class MySystem(ISystem):

    def update(self):
        ...

    def __init__(self, provider_1: Provider1)
        self.provider_1 = provider_1
```

Here is an example of accessing `Provider1` inside the `Game.setup` method.

```
MyGame(Game):
    def setup(self):
        provider_1 = self.factory.get_provider(Provider1)
        ...
```

There are additional parameters that can be passed to the `using_provider` method to control
things like the scope of the object and the annotation under which the provider is accessed.
Here is an example of a provider.

```
class SomeInterface(ABC):
    @abstractmethod
    def some_method(self):
        raise NotImplementedError()

class Provider2(SomeInterface):
    message = None
    def some_method(self):
        print(message)

def activate_provider_2(provider_2) -> SomeInterface:
    provider_2.message = "Hello, World"
    return provider_2

builder.using_provider(
    provider=Provider2,
    annotation=SomeInterface,
    scope=ScopeEnum.TRANSIENT,
    on_activate=activate_provider_2
)
```

To access Provider2 we will need to use the annotation `SomeInterface` and a new instance will be
created each time we ask for it.  This means each object that depends on `SomeInterface` will get
it's own instance.  Additionally, whenever a new instance is retrieved, the resulting instance will
be passed through the `activate_provider_2` function before returning it to the caller.

