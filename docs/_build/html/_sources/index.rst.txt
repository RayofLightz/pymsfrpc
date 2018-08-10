.. pymsfrpc documentation master file, created by
   sphinx-quickstart on Wed Dec 13 17:47:08 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to pymsfrpc's documentation!
====================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


geting started
==============

install from pip.

.. code-block:: bash

  sudo pip3 install pymsfrpc

open msfconsole and setup the server.

.. code-block:: bash

  msfconsole
  msf> load msgrpc

This will output the username and password of the server.
In a pyhon script type out this. To properly index a returned dict use
the b tack before the index str.

.. highlight:: python
.. code-block:: python

  from pymsfrpc import msfrpc 
  ip = "your server ip"
  port = "your server port"
  user = "your username"
  passwd = "your passwd"
  c = msfrpc.client(ip,port,user,password)
  output = c.get_version
  print(output[b"version"])
  print(output[b"ruby"])

|

Docs and refferance
====================

**Errors**
  AuthError(Exception)
    AuthError is thrown when a problem occurs during
    authentication

  ConnectionError(Exception)
    ConnectionError occurs when the server can't be connected to
**Class**
 Client(*str* adress, *str* username, *str* password)
   This object contains all the meathods dealing with interacting with the server.
   It takes arguments for the ip of the server, the username and the password.
   
   Client.get_version()
     Returns a binary formated dict with the ruby and metasploit versions

   Client.list_consoles()
     Returns a binary formated dict with the consoles and each ones id, prompt and if they are busy

   Client.create_console()
     Creates a console returns a binary formated dict with the id and prompt.

   Client.destroy_console(*str* id)
     Destroys a console based on the id of the console.
    
   Client.read_console(*str* id)
     Reads the text from a console given the id

   Client.write_console(*str* id, *str* cmd, *bool* process=True)
     Writes to the console given the id the text inside cmd. If process dosn't equal true the command
     will not execute.

   Client.list_sessions()
     Lists all the sessions

   Client.stop_sessions(*str* id)
     stops the session with the given id

   Client.write_shell(*str* ses_id, *str* data, *bool* process=true)
     writes data to a shell using a session id.
     If process is not true it does not execute

   Client.read_shell(*str* ses_id)
     reads data from a shell using a session id

   Client.read_meterpreter(*str* ses_id)
     reads data from a meterpreter session

   Client.write_meterpreter(*str* ses_id *str* data)
     sends a command to a meterpreter session

   Client.run_module(*str* _type, *str* name, *str* HOST, *str* PORT, *bool* payload=false)
     runs a given module where _type is the type of module, name is the name, and host and port are the ip and port.
     **PAYLOAD MUST BE TRUE IF USING THE PAYLOAD TYPE**
Port other meathods
===================
  The metasploit project has more meathods in the pro version. I can't
  properly test any of the modules becuase I don't own a copy of the pro
  version. So instead I can show you how one would port the meathod.
.. highlight:: python
.. code-block:: python

    from pymsfrpc import msfrpc
    ip = "your ip"
    port = "your port"
    user = "your user"
    passwd = "your passwd"
    c = msfrpc.Client(ip,port,user,passwd)
    c.send_command(["your call",self.token])
|

 If there are any args they are add after the token.
