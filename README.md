[![Release](https://img.shields.io/github/release/Roboy/ravestate.svg)](https://github.com/ro-boy/ravestate)
[![Build Status](https://travis-ci.org/Roboy/ravestate.svg?branch=master)](https://travis-ci.org/Roboy/ravestate)
[![codecov](https://codecov.io/gh/Roboy/ravestate/branch/master/graph/badge.svg)](https://codecov.io/gh/Roboy/ravestate)

## About

```
(C) Roboy 2019                               _ __    _ __   
   _____        _ ___ ____  __  ______  ______/ /_____/ /___ 
  /_   _\    _ _ /  \/ __ \/ / / / __ \/ ___\, / __ \, /__  \
   0>  0>   _ _ / /\/ /_/ /\ \/ / /_/ /\__, / / /_/ / / /_/ /
  \__⊽__/     _ \/ _\__/\/ _\__/ ,___/\____/\/\__/\/\/ ,___/ 
     ⋂                      _ _\____/             _ _\____/  
```

Ravestate is a reactive library for real-time natural language dialog systems. It combines elements from event-based and reactive programming into an API, where application states are defined as functions that are run when a certain boolean set of criteria (signals) in the current application context is satisfied. It is the first reactive API to allow for boolean combinations of events.

### Reactive Hello World

```python
from ravestate.context import startup, Context
from ravestate.state import state
from ravestate.module import Module

# We want to write some text output, so we
# need the raw:out context property from ravestate_rawio.
from ravestate_rawio import output as raw_out

# Make sure that we use some i/o implementation,
# so we can actually see stuff that is written to rawio:out.
import ravestate_conio

# Ravestate applications should always be wrapped in a Module.
# This allows easier scoping, and enables separation of concerns
# beyond states.
with Module(name="hi!"):

    # Create an application state which reacts to the `:startup` signal,
    # and writes a string to raw:out. Note: State functions are
    # always run asynchronously!
    @state(cond=startup(min_age=3.), write=raw_out.id())
    def hello_world(context):
        context[raw_out.id()] = "Waddup waddup waddup!"

# Run context with console input/output and our 'hi!' module.
Context("conio", "hi!").run()
```

## Installation

### Via PIP

The easiest way to install ravestate is through pip:

``
pip install ravestate
``

__Note:__ Ravestate requires Python 3.6 or higher. It is tested
on Ubuntu 16.04 and 18.04, as well as macOS > High Sierra.
It is currently not tested on Windows.

For reliability, we recommend using an environment virtualization tool,
like [virtualenv](https://virtualenv.pypa.io/en/latest/)
or [conda](https://conda.io/en/latest/).

### For developers

First, install dependencies:

```bash
pip install -r requirements.txt

# To run tests, install pytest, mocking, fixtures...
pip install -r requirements-dev.txt
```

Then, you may open the repository in any IDE, and mark the
`modules` folder as a sources root. Alternatively for development
purposes, call `export PYTHONPATH=$PYTHONPATH:$(pwd)/modules` from
your ravestate clone, to tell python that there are modules
to be loaded in the `modules` directory (the IDE does this for you).

## Running Hello World

Ravestate applications are defined by a configuration,
which specifies the ravestate modules that should be loaded.

To run the basic hello world application, run ravestate
with a config file or command line arguments:

### Running with command line spec

You can easily run a combination of ravestate modules in a shared context,
by listing them as arguments to the `rasta` command, which is installed
with ravestate:

```bash
python3 -m ravestate \
    ravestate_wildtalk \
    ravestate_conio \
    ravestate_hibye \
    ravestate_akinator \
    ravestate_fillers
```
Run `python3 -m ravestate -h` to see more options!

### Running with config file(s) 

You may specify a series of config files to configure ravestate context,
when specifying everything through the command line becomes too laborious:

```yaml
# In file hello_world.yml
module: core
config:
  import:
    - ravestate_conio
    - ravestate_hello_world
```
Then, run `ravestate` with this config file:

```bash
python3 -m ravestate -f hello_world.yml
```

## Module overview

Ravestate offers a landscape of fine-grained modules
for different aspects of dialog application tasks, which
may be seen in the following dependency diagram. Broadly,
the modules are categorized into Core (Blue), I/O (Yellow),
External (Red) and Skills (Green):

<img src="resources/docs/modules_sm.png" width="480" align="middle" style="text-align: center">

## Running tests

If you have installed the dependencies from ``requirements-dev.txt`` you
may run the ravestate test suite as follows:

``
./run_tests.sh
``

## Building/maintaining the docs

If you have installed the dependencies from ``requirements-dev.txt``,
generate the docs by running this command at project root:

```bash
export PYTHONPATH=$PYTHONPATH:$(pwd)/modules
git rm -rf docs
rm -rf _build docs
pydocmd build
git add docs/*
```

The structure and content of the docs are defined in the file ``pydocmd.yml``.
