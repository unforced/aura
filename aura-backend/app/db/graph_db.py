from neo4j import GraphDatabase, Driver
from app.core.config import settings

class GraphDB:
    def __init__(self, uri, user, password):
        self._driver: Driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        if self._driver is not None:
            self._driver.close()

    def get_session(self):
        return self._driver.session() 