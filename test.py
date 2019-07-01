
import pexpect

class router:
    
    def connect_new (self, router_name):                     #COnnect to the device and return the child process created
        child = pexpect.spawn ("telnet 10.64.97.249 2013")
        print("telnetting")
        
        
        child.expect ('Trying 10.64.97.249...')
        child.expect('Connected to 10.64.97.249.')
        child.expect('Escape character is \'^]\'.')
        print("connecting",child.before)
        child.sendline('\n')
        
        child.expect('Router>')
        print("Telnet done")
    
        return child 
myrouter=router()
ch=myrouter.connect_new("router name")
