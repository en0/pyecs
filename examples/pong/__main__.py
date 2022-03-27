import pygame
from pyioc3 import ScopeEnum
from pyecs import GameBuilder, Game
from pyecs.typing import IGame
from argparse import ArgumentParser

from .systems import RenderSystem, MovementSystem, InputSystem, PlaySystem, AiSystem, TemporialSystem, NetworkSystem
from .components import flags, models, queries
from .providers import NetworkInput, NetworkOutput, NetOpts
from .worlds import play, play_net_client, play_net_host


class Pong(Game):
    def teardown(self):
        self.factory.get_provider(NetworkInput).shutdown()

def main(host=None, client=None):
    game = GameBuilder()
    game.using_screen_mode((800, 600))
    game.using_system(InputSystem)
    game.using_system(AiSystem)
    game.using_system(MovementSystem)
    game.using_system(PlaySystem)
    game.using_system(RenderSystem)
    game.using_system(TemporialSystem)
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
    })

    # Override the game object with a custom one
    # so the network listener can be stopped
    if host:
        game.using_system(NetworkSystem)
        game.using_provider(Pong, IGame, scope=ScopeEnum.SINGLETON)
        game.using_provider(NetworkInput, scope=ScopeEnum.SINGLETON)
        game.using_provider(NetworkOutput, scope=ScopeEnum.SINGLETON)
        game.using_constant(NetOpts, host)
        game.using_active_world(play_net_host.NAME)
    elif client:
        game.using_system(NetworkSystem)
        game.using_provider(Pong, IGame, scope=ScopeEnum.SINGLETON)
        game.using_provider(NetworkInput, scope=ScopeEnum.SINGLETON)
        game.using_provider(NetworkOutput, scope=ScopeEnum.SINGLETON)
        game.using_constant(NetOpts, client)
        game.using_active_world(play_net_client.NAME)
    else:
        game.using_active_world(play.NAME)

    game.using_world_template(play.NAME, play.ENTITIES)
    game.using_world_template(play_net_host.NAME, play_net_host.ENTITIES)
    game.using_world_template(play_net_client.NAME, play_net_client.ENTITIES)


    pygame.init()
    game.play()

if __name__ == "__main__":
    opts_host = NetOpts(
        listen_port=2040,
        publish_port=2041,
        publish_addr="localhost",
    )

    opts_client = NetOpts(
        listen_port=2041,
        publish_port=2040,
        publish_addr="localhost",
    )

    ap = ArgumentParser()
    ap.add_argument("--host", action="store_true")
    ap.add_argument("--client", action="store_true")
    opts = ap.parse_args()
    if opts.host:
        main(host=opts_host)
    elif opts.client:
        main(client=opts_client)
    else:
        main()
