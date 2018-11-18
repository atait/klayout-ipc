# Inter-process communication for KLayout (lyipc)

[KLayout](https://www.klayout.de/index.php) is a layout editor and viewer. It is arguably the highest-performing and most advanced layout viewer in the 10<sup>0</sup>€/$ –
 10<sup>4</sup>€/$ range. KLayout is free software. Among its editing functions is a generic scripting interface (GSI) that supports Python and Ruby, and there are other python scripting projects that specialize in various other ways (e.g. phidl, gdspy, nazca, MatlabGDSPhotonics, KiCad, etc.).

Approaches for integrated circuit layout fall into two main categories: GUI-driven, interactive design aided by software macros; and script-driven, non-interactive programming. The latter is more repeatable, modifiable, and reusable once the script (and its library modules) has been written. The problem lies in developing the code – the layout object state and its evolution through time is realtively opaque to the programmer.

__The main application of lyipc__ is a graphical debugging workflow that uses the excellent KLayout viewer but is not necessarily dependent on the klayout scripting language or IDE. The idea is to create a communication link between two processes:
1. A server that is launched from within the klayout.app GUI
2. A client that can control various aspects of that klayout.app GUI

By separating the processes, the server GUI can be fully featured, initializing a large virtual program memory, while the client can be pretty lightweight.

![](icons/lyipc.png?raw=true)


### Detail: a debug process flow looks like this
1. [process #1] Launch klayout.app
    - From menu item, start a simple server on port 11078
2. [process #2: programmer] Run a python program in _either_ klayout or python
    - Import `lyipc` client package
    - Stop this program in a debugger like PDB or Spyder (examine/change program variables)
    - Write to a file "x.gds"
    - Call `ipc.load("x.gds")`
3. [process #2: lyipc] The lyipc.client module will
    - Initiate a socket connection on port 11078
    - Send a command that means load
4. [process #1] Upon receiving a connection request
    - Received command is parsed
    - An action is taken. In this case, load that file into the current view
5. [process #2: lyipc] closes the socket and continues execution

### Other uses
- XOR testing with [lytest](https://github.com/atait/lytest): automatically presents rich information upon geometric behavior changes
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

#### From github
Clone the project in a directory of your choice

```sh
git clone git@github.com:atait/klayout-ipc.git
pip install klayout-ipc/
```

For development mode, use pip's `-e` flag. You then have to install it into klayout with this command

```bash
lygadgets_link lyipc
```

#### From klayout salt package manager
As of 0.1.12, this is no longer supported. The reason is that it is difficult for klayout to detect what version of python will be used outside of the klayout interpreter.

#### Application setup
When an open file changes on disk, by default, KLayout asks whether to reload it. These prompts persist when reload is triggered by a communicating process instead of a human. Disable checks by going to klayout.app's preferences > Application > General, and uncheck the box for "Check for file updates."


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

Usage examples for klayout and non-klayout layout clients are included in this repo in the "examples" folder.


## Long shot wishlist item: remote jobs
Tests run a lot. Integration tests of entire wafers can take a really long time. Yet they can be parallelized – on the good side of Amdahl's law. This also has relevance to dataprep

Here is the process

1. [laptop] initiates klayout IPC configured for incoming connections (firewalled)
1. [laptop (or CI)] command for test
1. [laptop] sends IPC port info to remote HPC
1. [laptop] rsyncs ref_layouts and the new code, changes only, to the remote computer
    - you might also have to synchronize lygadgets, or just do it manually
    - can we override rsync's archive detection with geometry instead of binary
    - no it is based on file modification time, so we are good
1. [laptop] sends command to remote computer to initiate test
1. [remote HPC] runs tests on all cores using pytest-xdist and klayout tiling
1. [remote HPC] sends progress reports
    - pipe pytest output by redirecting stdout?
1. [remote HPC] if there are errors, sends the layout pairs to the IPC server on the laptop
1. [remote HPC] sends some kind of completion signal
1. [laptop] rsyncs run_layouts for further examination
    - only the failures?

Following are the steps to enabling this

#### Network IPC (Done)
Run a server on one computer. Configure something in lyipc in the second computer. Send lyipc commands. At first, do load with the gds already on the first computer. Next, combine with rsync and gds on local computer with client.load

#### stdout piping
Test script will look something like
```python
with redirect_stdout():
    print('heyo')
```
This script should be initiated by the laptop but run on the HPC.

I got this working, but its not live.

#### remote build
1. [laptop user] lyipc-job script.py
1. [laptop] rsync script.py
1. [HPC] python script.py
1. [HPC] rsync output.gds

Should this use container functions?

#### file transfer and IPC and lytest
Set some configuration of lytest, which sets some configuration of lyipc. Run `lytest diff file1.gds file2.gds`. These files are shipped to remote. XOR is run there. Error is detected and sent back to the klayout GUI of the first computer. This will involve actual file transfer.

#### script building
lytest not only sends a ref_layout but also a script. This scripted layout is built remotely. The XOR is done remotely.

#### tiling
To take full advantage, we eventually want to distribute tiles over cores. At first, we will get good results from xdist alone... when it comes to testing, but not dataprep.



#### Author: Alex Tait, June 2018
#### National Institute of Standards and Technology, Boulder, CO, USA
