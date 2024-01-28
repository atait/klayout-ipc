# Inter-process communication for KLayout (lyipc)
[![Build Status](https://travis-ci.com/atait/klayout-ipc.svg?branch=master)](https://travis-ci.com/atait/klayout-ipc)
[![Downloads](https://static.pepy.tech/personalized-badge/lyipc?period=total&units=international_system&left_color=grey&right_color=brightgreen&left_text=Downloads)](https://pepy.tech/project/lyipc)
[![DOI](https://zenodo.org/badge/138979016.svg)](https://zenodo.org/badge/latestdoi/138979016)

Approaches for integrated circuit layout fall into two main categories: GUI-driven, interactive design; and script-driven, non-interactive programming. The latter is more repeatable, modifiable, and reusable once the script has been written; however, the layout object state and its evolution through time is realtively opaque to the programmer.

__lyipc__ is used as a graphical debugging workflow that uses the KLayout viewer but is not necessarily dependent on the klayout scripting language or IDE. The idea is to create a communication link between two processes:
1. A server that is launched from within the klayout.app GUI
2. A client that can control various aspects of that klayout.app GUI

By separating the processes, the KLayout server GUI can be fully featured, initializing a large virtual program memory, while the client can be lightweight and in any sort of python environment or layout language (e.g. phidl, gdspy, nazca, etc.).

![](icons/lyipc.png?raw=true)


### Detail: a debug process flow looks like this
1. [process #1] From klayout.app
    - From menu item, start a simple server (Cmd-I)
2. [process #2: programmer] From the geometry creation program
    - Import `lyipc` client package
    - Stop this program in a debugger like PDB or Spyder (examine/change program variables)
    - Write to a file "x.gds", and call `ipc.load("x.gds")`, or
    - Call on a layout object such as `ipc.kqp(my_Device)`
3. [process #2: lyipc] The lyipc.client module will
    - Initiate a socket connection on port 11078
    - Send a command that means load
4. [process #1] Upon receiving a connection request
    - Received command is parsed
    - An action is taken. In this case, load that file into the current view
5. [process #2: lyipc] closes the socket and continues execution

### Other uses
- Remote debugging
- XOR error visualization with [lytest](https://github.com/atait/lytest)
- Animation: timed sequence of layouts
- Tracing: refresh display at every step of the program


## Installation
#### From PyPI

```sh
pip install lyipc
```

You then have to install it into klayout with this command

```bash
lygadgets_link lyipc
```

#### Suppress reload prompt
When an open file changes on disk, by default, KLayout asks whether to reload it. This blocks lyipc until a human clicks the prompt. Disable checks by going to klayout.app's preferences > Application > General, and uncheck the box for "Check for file updates."

#### From klayout salt package manager
As of 0.1.12, this is no longer supported.


## Usage
#### Server side
-- press Ctrl+`I` --

or go to "Tools>Inter-process communication server"

__Warning: clients have the ability to close and reload layout views that are unsaved, including ones in other tabs.__ It is often useful to start a second instance of klayout.app: one for persistent viewing/editing, and one to host the lyipc server.

#### Client side
To load a layout file called "mylayout.gds" in the remote window, put these lines
```python
import lyipc.client as ipc
ipc.load('mylayout.gds')
```

You can also send layout objects in memory directly. This is the more commonly used approach
```python
from lyipc import kqp
kqp(my_Device)
```
where `my_Device` is a layout object, such as a `Cell` in pya or a `Device` in phidl. `kqp` has an optional argument "fresh" (defaults to False). When False, the current layout is reloaded, keeping viewbox, layers, etc. When True, the new object is loaded as a fresh layout.

Usage examples for klayout and non-klayout clients are included in this repo in the "examples" folder.

#### Command line interface
As of v0.2.14, there is a CLI entry point `lyipc_reload` for convenience.
With no arguments, it reloads the current view. When a filename is provided, `lyipc_reload` will detect that it needs a fresh load. With `--fresh` (or `-f`), the file is always loaded as a new file. `lyipc_reload -f x.gds` is similar to `open x.gds` on some systems.

```bash
lyipc_reload output.gds  # Opens fresh if needed
python script_that_affect_outputgds
lyipc_reload output.gds  # Reloads without closing
lyipc_reload  # Same thing, unless the user has closed the view
```

## Remote debug and jobs
Using ssh, rsync, sshfs, and lyipc, you can work on a remote, high performance computer the same way you work on your laptop - without being able to notice the difference. These features are still somewhat experimental. You must first configure two-way RSA authentication. Here is the process:

1. [laptop] initiates klayout IPC configured for incoming connections
1. [remote HPC] point the "LYIPCTARGET" environment variable to your laptop
1. [remote HPC via sshfs] expose remote filesystem for editing on your laptop
1. [remote HPC via ssh] command to run script
1. [remote HPC] kqp is called, which writes a temporary gds file
1. [laptop via rsync] receives the temporary file
1. [laptop via lyipc server] receives command to load that file into the klayout window

#### Network IPC (Done)
Run a server on one computer. Configure something in lyipc in the second computer. Send lyipc commands. At first, do load with the gds already on the first computer. Next, combine with rsync and gds on local computer with client.load

#### remote build (Done)
1. [laptop user] lyipc-job script.py
1. [laptop] rsync script.py
1. [HPC] python script.py
1. [HPC] rsync output.gds


#### file transfer and IPC and lytest (done)
Set some configuration of lytest, which sets some configuration of lyipc. Run `lytest diff file1.gds file2.gds`. These files are shipped to remote. XOR is run there. Error is detected and sent back to the klayout GUI of the first computer. This will involve actual file transfer.

Edit: this did not set anything in lytest. It was a matter of lyipc:`set_target_hostname` and the HPC using `ship_file` to get things back down.

Notes: to send a file for testing, to call commands and get printouts, to rsync (either direction) -- you need a one-way RSA authorization. If you want to run remote tests that pop up in the local GUI, that currently *requires a two-way RSA authorization*. When the HPC is running, its lytest has the ball (kind of). It decides when to send a pair of files to lyipc. Then lyipc notices that it has to ship those files remotely, requiring rsync. Huh, what if the QTcpSocket in lyipc could send a notice back down that said: rsync this thing from me; it is ready.


#### Author: Alex Tait, June 2018
#### National Institute of Standards and Technology, Boulder, CO, USA
