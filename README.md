# Inter-process communication for klayout (lyipc)

## There are two main pieces of code
1. A server that is launched from within a klayout.app GUI
2. A client API that lets an external program control that klayout.app GUI


## Initial goal: a debug process flow like this
1. [process #1] Launch klayout.app
    - From menu item, start a simple server on port <XXY>
2. [process #2] Run a python program in _either_ klayout or python
    - Import `lyipc` client package
    - Stop this program in a debugger like PDB or Spyder
    - Write to a file "x.gds"
    - Call `ipc.load("x.gds")`
3. [process #2] The ipc.client module will
    - Initiate a socket connection on port <XXY>
    - Send a command that means load
4. [process #1] Upon receiving a connection request
    - Received command is parsed
    - An action is taken. In this case, load that file into the current view
5. [process #2] closes the socket and continues execution


### Other use cases
This could potentially be modified to allow the server to execute arbitrary commands. Essentially, a klayout app could be fully controlled by another klayout app or external process on a local or remote machine. For example, klayout on my laptop could send a big chip to klayout on a cluster to draw the thing, run a tough DRC, and rsync the results back.

Any other ideas?

## Installation
1. From source
    - git clone ...
    - ln -s ~/.../klayout-ipc/klayout_dot_config ~/.klayout/salt/klayout_ipc
    or
    - export KLAYOUT_PATH="~/.../klayout-ipc/klayout_dot_config"
2. From package manager 
    - (TODO)

## Usage
Server side: press Ctrl+I

Client side: 
```python
import lyipc.client as ipc
ipc.load('mylayout.gds')
```

## Released version incompatibility
In my application, I have fully disabled `&m_file_changed_timer` to prevent the "do you want to reload?" prompt. In a later version of klayout, this could be controlled in a preference pane. The prompt does not limit functionality; just tolerate it, or, if you can compile from source, comment these lines in `layMainWindow.cpp`
```c++
683 // connect (&m_file_changed_timer, SIGNAL (timeout ()), this, SLOT (file_changed_timer()));
684 // m_file_changed_timer.setSingleShot (true);
```

## Author: Alex Tait, June 2018