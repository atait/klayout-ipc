# Interprocess communication for klayout

## There are two main pieces of code
1. A server that is launched from within the klayout.app GUI
2. A client API for "remotewrite" that is imported from pya by an external program
    - The external program does not explicitly worry about sockets

## Goal: a process flow like this
1. [process #1] Launch klayout.app
    - Open a shared file ("x.gds")
    - From menu item, start a simple server on port <XXY>
2. [process #2] Run a interpreted python program with, e.g. `klayout -b -r myscript.py`
    - Stop this program in a debugger like PDB or Spyder
    - Call `pya.remotewrite("x.gds")`
3. [process #2] Inside remotewrite, pya will
    - Write to file using builtin `Layout.write("x.gds")`
    - Initiate a socket connection on port <XXY>
4. [process #1] Upon receiving a connection request
    - The main view is refreshed
5. [process #2] closes the socket


## Released version incompatibility
In my application built from source, I have fully disabled `&m_file_changed_timer` to prevent the "do you want to reload?" prompt. In a later version, this could be controlled by a preference item.


## Installation
1. From source
    - git clone ...
    - ln -s ~/.../klayout-ipc/klayout_dot_config ~/.klayout/salt/klayout_ipc
2. From package manager (TODO)


## Questions
Can the server be non-blocking? I would like to be able to zoom around. Will it allow us to put that server in a thread from QApplication?

What about sending a real payload? Useful?

The server can communicate back to the client. Is there any use for this?

Can the client be phidl?

## Author: Alex Tait, June 2018