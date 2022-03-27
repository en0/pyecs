class Entity(dict):

    identity: int = 0

    def __repr__(self):
        return f"<Entity-{self.identity}:{super().__repr__()}>"
