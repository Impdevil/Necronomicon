
from ssl import VerifyFlags
import proxmoxer

class Proxmox_instance:
    api=None
    
    
    def __init__(self, ip, port,username,tokenID,token):
        #print(ip)
        self.api = proxmoxer.ProxmoxAPI(ip,port=port,user=username, verify_ssl=False, token_name=tokenID, token_value=token)
       

    def get_vm_status(self):
        for node in self.api.nodes.get():
            #print(node)
            for vm in self.api.nodes(node["node"]).qemu.get():
                #print(vm)
                print('{}:{} status: {} for {}'.format(vm['vmid'], vm['name'],vm["status"], vm['uptime']))

    def start_vm(self):
        if self.api:
