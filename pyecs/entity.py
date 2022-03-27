class Entity(dict):

    indentity: int = 0

    def __repr__(self):
        return f"<Entity-{self.indentity}:{super().__repr__()}>"
