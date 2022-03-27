from typing import NamedTuple


class NetOpts(NamedTuple):
    listen_port: int
    publish_port: int
    publish_addr: str


