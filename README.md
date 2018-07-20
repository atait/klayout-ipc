# Inter-process communication for KLayout (lyipc)

[KLayout](https://www.klayout.de/index.php) is a layout editor and viewer. It is arguably the highest-performing and most advanced layout viewer in the 10<sup>0</sup>€/$ –
 10<sup>4</sup>€/$ range. KLayout is free software. Among its editing functions is a generic scripting interface (GSI) that supports Python and Ruby, and there are other python scripting projects that specialize in various other ways (e.g. phidl, gdspy, nazca, MatlabGDSPhotonics, KiCad, etc.).

Approaches for integrated circuit layout fall into two main categories: GUI-driven, interactive design aided by software macros; and script-driven, non-interactive programming. The latter is more repeatable, modifiable, and reusable once the script (and its library modules) has been written. The problem lies in developing the code – the layout object state and its evolution through time is realtively opaque to the programmer.

__The main application of lyipc__ is a graphical debugging workflow that uses the excellent KLayout viewer but is not necessarily dependent on the klayout scripting language or IDE. The idea is to create a communication link between two processes:
1. A server that is launched from within the klayout.app GUI
2. A client that can control various aspects of that klayout.app GUI

By separating the processes, the server GUI can be fully featured, initializing a large virtual program memory, while the client can be pretty lightweight.

### Detail: a debug process flow looks like this
1. [process #1] Launch klayout.app
    - From menu item, start a simple server on port <XXY>
2. [process #2: programmer] Run a python program in _either_ klayout or python
    - Import `lyipc` client package
    - Stop this program in a debugger like PDB or Spyder (examine/change program variables)
    - Write to a file "x.gds"
    - Call `ipc.load("x.gds")`
3. [process #2: lyipc] The lyipc.client module will
    - Initiate a socket connection on port <XXY>
    - Send a command that means load
4. [process #1] Upon receiving a connection request
    - Received command is parsed
    - An action is taken. In this case, load that file into the current view
5. [process #2: lyipc] closes the socket and continues execution

### Other uses
- Animation: timed sequence of layouts
- Tracing: refresh display at every step of the program
- (future) Behavioral unit tests: Test whether code changes break previous layout behavior by keeping a reference.gds and creating a test.gds, then send them to klayout's visual diff tool.

## Installation
#### From salt package manager
In klayout.app, go to "Tools>Manage Packages". Go to "Install New Packages" and find "klayout_ipc". Double-click it, and press "Apply".

_At the time of writing, the grain is NOT live._

#### From source
1. In a directory of choice, `git clone git@github.com:atait/klayout-ipc.git`
2. "Install" in .klayout system files
    - (OSX, Linux) `ln -s ~/your/path/to/klayout-ipc/klayout_dot_config ~/.klayout/salt/klayout_ipc`
    - (Windows) right click the folder and create an alias to C:\\Username\KLayout\salt [path right?]

or

2. Show klayout where it is
    - `export KLAYOUT_PATH="~/your/path/to/klayout-ipc/klayout_dot_config"`

## Setup
When an open file changes on disk, by default, KLayout asks whether to reload it. These prompts persist when reload is triggered by a communicating process instead of a human. Disable checks by going to klayout.app's preferences > Application > General, and uncheck the box for "Check for file updates."

The lyipc package is visible within klayout's interpreter namespace, but it is not on the system PYTHONPATH. In order for any python-based client to use it, lyipc must be installed with
```sh
pip install ~/.klayout/salt/klayout_ipc/python
```
For development mode, use pip's `-e` flag.

## Usage
#### Server side
-- press Ctrl+`I` --

or go to "Tools>Inter-process communication server"

__Warning: clients have the ability to close and reload layout views that are unsaved, including ones in other tabs.__ It is highly recommended that you start a second instance of klayout.app dedicated to serving. This has to be done from command line. Tip for UNIX folks, put a shortcut to the klayout executable on your PATH
```sh
ln -s /Applications/klayout.app/Contents/MacOS/klayout /usr/local/bin/klayout
```

Note: as of now, the port is hard-coded (11078), so there can only be one server at a time. Communication is initiated by the client as a command or query. That means using multiple clients concurrently is possible, but they would clash unless synchronized somehow.

#### Client side
To load a layout file in the remote window, put these lines
```python
import lyipc.client as ipc
ipc.load('mylayout.gds')
```
in a file called `test-lyipc.py`.

Run it with either a standard python interpreter
```sh
python test-lyipc.py
```
or the klayout general scripting interface (GSI) in non-GUI mode
```sh
klayout -b -r test-lyipc.py
```
The former is faster because a new klayout instance is not created, but of course, the latter must be used for `pya` to work.

Usage examples for klayout and non-klayout layout clients are included in this repo.

#### Author: Alex Tait, June 2018