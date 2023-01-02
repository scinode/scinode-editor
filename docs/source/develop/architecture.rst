

Architecture
======================

There are different kind of jobs need to be executed.

- DFT calculations, take long time (hours or days)
- Batoms generations, could be very fast (ms) (Should be executed always)
- Parameters generations, super fast. (Should be executed always)



Node
-------------------
Base node should has the following features:
- Blender node with properties, input sockets and output sockets.
- execute function
- interface to database
- read state of parent nodes.
- Advanced Node Settings for options don't use often.


sockets
--------------

``math.pow``

socket should has the following features:

- dynamic socket based on custom choose (use ``udpate``)
- For input socket, "positional" or "keyword" argument.
- For output socket, has index





Daemon
-------------------
Use a python daemon for manging nodetreesin the background.

data retrieval, upd        ates, refresh

Triggers
-------------------
