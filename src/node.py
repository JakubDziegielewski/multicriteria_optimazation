class Node:
    def __init__(self, name: str) -> None:
        self.name = name
    def __repr__(self):
        return f"Name: {self.name}"


class PhysicalNode(Node):
    def __init__(self, name: str, longitude: float, latitude: float) -> None:
        super().__init__(name)
        self.longitude = longitude
        self.latitude = latitude
    def __repr__(self):
        return f"{super().__repr__()}, Longitude: {self.longitude}, Latitude: {self.latitude}"
