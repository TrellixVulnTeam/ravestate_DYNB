from ravestate.property import Property
from ravestate.module import Module
from ravestate.wrappers import ContextWrapper
from ravestate.receptor import receptor

import ravestate_rawio
import ravestate_interloc
from ravestate_verbaliser.verbaliser import get_phrase_list
import ravestate_phrases_basic_en
import ravestate_ontology

from scientio.ontology.node import Node
from scientio.session import Session
from scientio.ontology.ontology import Ontology

from reggol import get_logger
logger = get_logger(__name__)


with Module(name="interloc"):

    # TODO: Make interloc:all a special property type, that only accepts ScientioNodeProperty as children
    all = Property(name="all", allow_read=True, allow_write=False, allow_push=True, allow_pop=True)


def handle_single_interlocutor_input(ctx: ContextWrapper, input_value: str, id="anonymous_interlocutor") -> None:
    """
    Forwards input to `rawio:in` and manages creation/deletion of a singleton
     interlocutor. A new interlocutor node is pushed, when the input is a greeting,
     and there is no interlocutor present. The interlocutor is popped,
     if the input is a farewell, and there is an interlocutor present.

    * `ctx`: Context Wrapper of the calling state. Must have read permissions
     for `interloc:all`.

    * `input_value`: The string input value that should be written to `rawio:in`.

    * `id`: Name of the interlocutor context property, and initial name for
     the interlocutor's Neo4j node (until a proper name is set by persqa).
    """

    @receptor(ctx_wrap=ctx, write="rawio:in")
    def write_input(ctx_input, value: str):
        ctx_input["rawio:in"] = value

    @receptor(ctx_wrap=ctx, write="interloc:all")
    def push_interloc(ctx: ContextWrapper, interlocutor_node: Node):
        if ctx.push(parent_property_or_path="interloc:all",
                    child=Property(name=id, default_value=interlocutor_node)):
            logger.debug(f"Pushed {interlocutor_node} to interloc:all")

    @receptor(ctx_wrap=ctx, write="interloc:all")
    def pop_interloc(ctx: ContextWrapper):
        if ctx.pop(f"interloc:all:{id}"):
            logger.debug(f"Popped interloc:all:{id}")

    write_input(input_value)

    interloc_exists = f"interloc:all:{id}" in ctx.enum("interloc:all")

    # push Node if you got a greeting
    if input_value.strip() in get_phrase_list("greeting") and not interloc_exists:
        # set up scientio
        ravestate_ontology.initialized.wait()
        sess: Session = ravestate_ontology.get_session()
        onto: Ontology = ravestate_ontology.get_ontology()

        # create scientio Node of type Person
        new_interloc = Node(metatype=onto.get_type("Person"))
        new_interloc.set_name(id)
        push_interloc(new_interloc)

    # pop Node if you got a farewell
    elif input_value.strip() in get_phrase_list("farewells") and interloc_exists:
        pop_interloc()
