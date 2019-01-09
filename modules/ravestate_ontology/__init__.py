from ravestate import registry
from ravestate.state import state
from ravestate.constraint import s

from scientio.ontology.ontology import Ontology
from scientio.session import Session

from os.path import realpath, dirname, join

from reggol import get_logger
logger = get_logger(__name__)

onto = None
sess = None
NEO4J_ADDRESS_KEY: str = "neo4j_address"
NEO4J_USERNAME_KEY: str = "neo4j_username"
NEO4J_PASSWORD_KEY: str = "neo4j_pw"


@state(triggers=s(":startup"))
def hello_world_ontology(ctx):
    """
    Creates a scientio session with neo4j backend.
    (neo4j is a knowledge graph)
    an ontology is loaded from a yaml file - it can be accessed with a getter
    (the ontology description is a collection of named entity types,
    their properties and relationships)
    then the session is created - it can be accessed with a getter
    """
    global onto, sess
    onto = Ontology(path_to_yaml=join(dirname(realpath(__file__)), "ravestate_ontology.yml"))
    # Create a session (with default Neo4j backend)
    sess = Session(
        ontology=onto,
        neo4j_address=ctx.conf(key=NEO4J_ADDRESS_KEY),
        neo4j_username=ctx.conf(key=NEO4J_USERNAME_KEY),
        neo4j_password=ctx.conf(key=NEO4J_PASSWORD_KEY))


registry.register(
    name="ontology",
    states=(hello_world_ontology,),
    config={
        NEO4J_ADDRESS_KEY: "bolt://localhost:7687",
        NEO4J_USERNAME_KEY: "neo4j",
        NEO4J_PASSWORD_KEY: "neo4j"
    }
)


def get_session():
    return sess


def get_ontology():
    return onto
