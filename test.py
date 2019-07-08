
import pexpect
import re
import numpy as np

class router:
    
    def connect_new (self, router_name):                     #COnnect to the device and return the child process created
        child = pexpect.spawn ("telnet 10.64.97.249 2029")
        print("telnetting")
        
        
        child.expect ('Trying 10.64.97.249...')
        child.expect('Connected to 10.64.97.249.')
        child.expect('Escape character is \'^]\'.')
        print("connecting",child.before)
        child.sendline('\n')
        
        child.expect('Router>')
        print("Telnet done")
    
        return child 

    def parse_and_get_data():
        f=open("parse.txt","r")
        ch=f.read()
        f.close()
        ch= ch.replace('\\r\\n','\n')
        rem=['\\t','|\\r\\n|','>','<','..','|','==','__','**','##','--']
        for i in rem:
            ch=ch.replace(i,'')
        f=open("parsed.txt",'w')
        f.write(ch)       
        print(ch)
        f.close()
        f=open("parsed.txt",'r')
        ch=f.read()

        '''
        cpu=re.findall(r'CPU-util\(5 min\):([^\s]+)',ch)
        cpu=int(cpu[0])
        
        iosd=re.findall(r'IOSd-util\(5 min\):([^\s]+)',ch)
        iosd=int(iosd[0])
        

        mem=re.findall(r'Percent Used:([^\s]+)',ch)
        mem=int(mem[0])
        

        ipv4=re.findall(r'Total V4 prefixes:[0-9]*/[0-9]*-([^%]+)',ch)
        ipv4=ipv4[0]
        
        ipv6=re.findall(r'Total V6 prefixes:[0-9]*/[0-9]*-([^%]+)',ch)
        ipv6=ipv6[0]
        
        mac=re.findall(r'Total MACs Learnt:[0-9]*/[0-9]*-([^%]+)',ch)
        mac=mac[0]
        
        fan=re.findall(r'Fan-speed:([^%]+)',ch)
        fan=fan[0]
        
        power=re.findall(r'Power consumed:([^\s]+)',ch)
        power=int(power[0])                      #in watts
      

        mpls=re.findall(r'Total MPLS Labels:([^\s]+)',ch)
        if (not mpls):
            mpls=0 
        
        tcam=re.findall(r'[a-z0-9A-Z\s]*:[0-9]*/[0-9]*:([^%]+)',ch)
        tcam=sum(map(float,tcam))
        
        res=re.findall(r'ID Allocation Mgr in ASICH(.*?)(?=FRU_CC)',ch,re.DOTALL)[0]
        res=re.findall(r'[a-z0-9A-Z\s]*:([^%]+)',res)
        res=sum(map(float,res))
        
        err=int(re.findall(r'Pending Objects:([^\s]+)',ch)[0])+int(re.findall(r'Error objects:([^\s]+)',ch)[0])
        
        faults=re.findall(r'Faults on the IM cardsH(.*?)(?=\")',ch,re.DOTALL)[0]
        faults=np.array(re.findall(r'[0-9]*/[0-9]*',faults))
        faults=len(np.unique(faults))
        '''
        print(faults)
        f.close()


myrouter=router()
#ch=myrouter.connect_new("router name")
#router.parse_data()
router.get_data()
