
from ssl import VerifyFlags
import proxmoxer

class Proxmox_instance:
    api=None
    
    
    def __init__(self, ip, port,username,password,tokenID,token):
        #print(ip)
        self.api = proxmoxer.ProxmoxAPI(ip,port=port,user=tokenID, verify_ssl=False, password=token)
       

    def get_vm_status(self):
        for node in self.api.nodes.get():
            for vm in self.api.nodes(node["node"].openvz.get()):
                print(f"{0}. {1} => {2}".format(vm["vmid"], vm["name"], vm["status"]))
        
        
    