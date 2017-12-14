# metasploit_com.py 
# contaions metasploit rpc api
# Author Tristan Messner
import msgpack
import http.client as request
import sys
class AuthError(Exception):
    # Error for authentication problems
    pass
class ConnectionError(Exception):
    # Error for inital connection error
    pass
class Client(object):
    # This is the client for Metasploit rpc
    def __init__(self,ip,user,passwd):
        # this will set all global vars and then create the intial auth to get the token
        self.user = user
        self.passwd = passwd
        self.server = ip
        self.headers = {"Content-Type": "binary/message-pack"}
        self.client = request.HTTPConnection(self.server,55552)
        self.auth()
    #various properties and setters
    @property
    def headers(self):
        return self._headers
    @headers.setter
    def headers(self,value):
        self._headers = value
    @property
    def options(self):
        return self._options

    @options.setter
    def options(self,value):
        #packs the data while setting options
        self._options = msgpack.packb(value)
    @property
    def token(self):
        return self._token

    @token.setter
    def token(self,value):
        self._token = value

    def auth(self):
        # auth.login
        # returns a random token
        # this is the function for the handshake
        print("Attempting to access token")
        self.options = ["auth.login",self.user,self.passwd]
        self.client.request("POST","/api",body=self.options,headers=self.headers)
        c = self.client.getresponse()
        if c.status != 200:
           raise ConnectionError()
           print("Connection Error")
        else:
            res = msgpack.unpackb(c.read())
            print(res)
            if res[b'result'] == b'success':
                self.token = res[b'token']
                print("Token recived:> %s",self.token)
            else:
                raise AuthError()
                print("Authentication failed")
                sys.exit()
    def send_command(self,options):
        self.options = options
        self.client.request("POST","/api/1.0",body=self.options,headers=self.headers)
        c = self.client.getresponse()
        if c.status != 200:
            raise ConnectionError()
        else:
            res = msgpack.unpackb(c.read())
            return res
    def get_version(self):
        # core.version
        # returns the ruby version and msf version
        res = self.send_command(["core.version",self.token])
        return res

    def create_console(self):
        # console.destroy
        # creates a console and returns a success
        res = self.send_command(["console.create",self.token])
        return res

    def destroy_console(self,console_id):
        # console.destroy
        # destroys a console based on id
        # [cmd,token,id]

        # forces console id to str
        str(console_id)
        res = self.send_command(["console.destroy",self.token,console_id])
        return res

    def list_consoles(self):
        # console.list
        # reutrns a dictionary of consoles and
        # their ids, prompt, and if they are busy
        res = self.send_command(["console.list",self.token])
        return res
    def write_console(self,console_id,data,process=True):
        # console.write
        # if true the command automatically runs
        # data is the command to run
        # console id is the console to run it under
        if process == True:
            data +="\n"
        #santy checks console_id
        str(console_id)
        res = self.send_command(["console.write",self.token,console_id,data])
        return res
    def read_console(self,console_id):
        # console.read
        # reads data from a console
        # specficaly output

        #sanaty check on console
        str(console_id)
        res = self.send_command(["console.read",self.token,console_id])
        return res

    def list_sessions(self):
        # session.list
        # list all sessions and information about them
        res = self.send_command(["session.list",self.token])
        return res

    def stop_session(self,ses_id):
        # session.stop
        # stops the session with the
        # given session id
        str(ses_id)
        res = self.send_command(["session.stop",self.token,ses_id])
        return res

    def read_shell(self,ses_id,read_ptr=0):
        # session.shell_read
        # reads data from shell
        str(ses_id)
        res = self.send_command(["session.shell_read",self.token,ses_id,read_ptr])
        return res

    def write_shell(self,ses_id,data,process=True):
        # session.shell_write
        # writes a cmd to the session
        if process == True:
            data += "\n"
        str(ses_id)
        res = self.send_command(["session.shell_write",self.token,ses_id,data])
        return res

    def write_meterpreter(self,ses_id,data):
        # session.meterperter_write
        # writes to a meterpreter session
        # <cmd> sessionid
        str(ses_id)
        res = self.send_command(["session.meterperter_write",self.token,session,data])
        return res

    def read_meterpreter(self,ses_id):
        # session.meterperter_read
        # returns back what is read
        str(ses_id)
        res = self.send_command(["session.meterperter_read",self.token,ses_id])
        return res
    def run_module(self,_type,name,HOST,PORT,payload=False):
        #module.execute
        # moduletype moduleName
        if payload != False:
            d = ["module.execute",self.token,_type,name,{"LHOST":HOST,"LPOST":PORT}]
        else:
            d = ["module.execute",self.token,_type,name,{"RHOST":HOST,"RHOST":PORT}]
        res = self.send_command(d)
        return res

# this if statement is for testing funtions inside of auth
# only put tests here
if __name__ == "__main__":
    auth = Client("127.0.0.1","msf","yFdkc6fB")
    print(auth.get_version())
    print(auth.list_consoles())
    print(auth.create_console())
    print(auth.read_console(1))
    print(auth.write_console(1,"ls"))
    print(auth.destroy_console(1))
    print(auth.list_sessions())
    print(auth.run_module("exploit","ms17_010_eternalblue","1.1.1.1","1"))
