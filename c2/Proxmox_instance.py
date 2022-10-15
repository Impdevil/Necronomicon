
from ssl import VerifyFlags
import proxmoxer

class Proxmox_instance:
    api=None
    
    
    def __init__(self, ip, port,username,password,tokenID,token):
        print(ip)
        self.api = proxmoxer.ProxmoxAPI(ip,port=port,user=username, verify_ssl=False, password=token)
        #self.api._backend.
        
        
    