import pygame
from pyioc3 import ScopeEnum
from pyecs import GameBuilder, Game
from pyecs.typing import IGame
from argparse import ArgumentParser

from .systems import RenderSystem, MovementSystem, InputSystem, PlaySystem, AiSystem, TemporialSystem, NetworkSystem
from .components import flags, models, queries
from .providers import NetworkInput, NetworkOutput, NetOpts
from .worlds import PLAY, SPLASH, play, play_net_client, play_net_host, splash


class Pong(Game):
    """
    Override the Game object so we can tear down the network.
    This is only used if playing a network game.
    """

    def teardown(self):
        self.factory.get_provider(NetworkInput).shutdown()

def main(host=None, client=None):
    """Construct the game and start playing"""

    # The game builder will simplify dependecy management.
    game = GameBuilder()
    game.using_screen_mode((800, 600))
    game.using_clock(60)

    # Install the core systems
    game.using_system(InputSystem)
    game.using_system(AiSystem)
    game.using_system(MovementSystem)
    game.using_system(PlaySystem)
    game.using_system(RenderSystem)
    game.using_system(TemporialSystem)

    # Inform the EntityManager of the queries made by the systems
    game.using_component_groups({
        queries.BALL,
        queries.PADDLE,
        queries.PLAYER_PADDLE,
        queries.RECT,
        queries.CIRCLE,
        queries.RECT_COLLIDERS,
        queries.TEXT,
        queries.HUD,
        queries.NPC_PADDLE,
        queries.TEMPORIAL,
        queries.NETSYNC_IN,
        queries.NETSYNC_OUT,
        queries.SCENE_CHANGE_TRIGGER,
    })

    # Add the splash world as a template and activate
    # it so it's the first scene we run.
    game.using_world_template(SPLASH, splash.ENTITIES)
    game.using_active_world(SPLASH)

    # Setup game for specific play mode.
    if host:
        # Inject specific bits if the player is Hosting a network game
        game.using_system(NetworkSystem)
        game.using_constant(NetOpts, host)
        game.using_provider(Pong, IGame, scope=ScopeEnum.SINGLETON)
        game.using_provider(NetworkInput, scope=ScopeEnum.SINGLETON)
        game.using_provider(NetworkOutput, scope=ScopeEnum.SINGLETON)
        game.using_world_template(PLAY, play_net_host.ENTITIES)
    elif client:
        # Inject specific bits if the player is joining a network game
        game.using_system(NetworkSystem)
        game.using_constant(NetOpts, client)
        game.using_provider(Pong, IGame, scope=ScopeEnum.SINGLETON)
        game.using_provider(NetworkInput, scope=ScopeEnum.SINGLETON)
        game.using_provider(NetworkOutput, scope=ScopeEnum.SINGLETON)
        game.using_world_template(PLAY, play_net_client.ENTITIES)
    else:
        # Inject the specific bits for a local-only game
        game.using_world_template(PLAY, play.ENTITIES)

    # pyecs does NOT initialize pygame.
    pygame.init()
    game.play()


if __name__ == "__main__":

    # Accept arguments to allow player to select a playmode.
    ap = ArgumentParser()
    ap.add_argument("--host", action="store_true")
    ap.add_argument("--client", action="store_true")
    ap.add_argument(
        "--remote-endpoint",
        help="The ip address and port of the remote endpoint",
        default=None,
        nargs=2)
    ap.add_argument(
        "--listen-port",
        help="The ip address and port of the remote endpoint",
        default=None)
    opts = ap.parse_args()

    # Build parameters from client input
    kwargs = {}
    if opts.host:
        ep_a, ep_p = opts.remote_endpoint
        kwargs["host"] = NetOpts(
            listen_port=int(opts.listen_port),
            publish_port=int(ep_p),
            publish_addr=ep_a,
        )
    elif opts.client:
        ep_a, ep_p = opts.remote_endpoint
        kwargs["client"] = NetOpts(
            listen_port=int(opts.listen_port),
            publish_port=int(ep_p),
            publish_addr=ep_a,
        )

    # Play the game
    main(**kwargs)
