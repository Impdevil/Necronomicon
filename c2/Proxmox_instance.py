import logging
from ssl import VerifyFlags
import proxmoxer
from proxmoxmanager import ProxmoxManager
import asyncio
import json


class Proxmox_instance:
    api=None
    WHITELIST = None
    
    def __init__(self, ip, port,username,tokenID,token,nodeID):
        try:
            self.api = proxmoxer.ProxmoxAPI(ip,port=port,user=username, verify_ssl=False, token_name=tokenID, token_value=token)
            self.ProxManager = ProxmoxManager(host=ip+":"+port, user=username,token_name=tokenID,token_value=token)

            logging.info("connection to server: "  + ip + ":" + port + " as user: " + username +" has been made")

            self.nodeID = nodeID
        except:
            raise Exception("connection Failed")
            logging.critical("Connection to server failed.")



    def get_vm_status(self):
        statuslist= []
        for node in self.api.nodes.get():
            for vm in self.api.nodes(node["node"]).qemu.get():
                #print(vm)
                statuslist.append('{}:{} status: {} for {}'.format(vm['vmid'], vm['name'],vm["status"], vm['uptime']))
                print('{}:{} status: {} for {}'.format(vm['vmid'], vm['name'],vm["status"], vm['uptime']))
        return statuslist



    async def start_vm(self,  vmid):
        if self.api:
            node = self.api.nodes.get()
            qemu = self.api.nodes(self.nodeID).qemu(vmid).status.current.get()
            status = list(findKeys(qemu,"qmpstatus"))
            print("status:"+ str(status))
            self.ProxManager.vms[vmid].start()
            await asyncio.sleep(10)
            qemu = self.api.nodes(self.nodeID).qemu(vmid).status.current.get()
            status = list(findKeys(qemu,"qmpstatus"))
            print("status:"+ str(status))



    async def get_status_name(self, vmid):

            qemu = self.api.nodes(self.nodeID).qemu(vmid).status.current.get()
            status = list(findKeys(qemu,"qmpstatus"))[0]
            name = list(findKeys(qemu,"name"))[0]
            print(str(name )+ str(status))
            return [name, status]


    async def stop_vm(self,  vmid):
        if self.api:
            node = self.api.nodes.get()
            qemu = self.api.nodes(self.nodeID).qemu(vmid).status.current.get()
            status = list(findKeys(qemu,"qmpstatus"))
            print("status:"+ str(status))
            self.ProxManager.vms[vmid].stop()
            await asyncio.sleep(10)
            qemu = self.api.nodes(self.nodeID).qemu(vmid).status.current.get()
            status = list(findKeys(qemu,"qmpstatus"))
            print("status:"+ str(status))
 

    async def shutdown_vm(self,  vmid):
        if self.api:
            node = self.api.nodes.get()
            qemu = self.api.nodes(self.nodeID).qemu(vmid).status.current.get()
            status = list(findKeys(qemu,"qmpstatus"))
            print("status:"+ str(status))
            self.ProxManager.vms[vmid].shutdown()
            await asyncio.sleep(10)
            qemu = self.api.nodes(self.nodeID).qemu(vmid).status.current.get()
            status = list(findKeys(qemu,"qmpstatus"))
            print("status:"+ str(status))

    async def wait_till_running(self, vmid):
        vmData = await self.get_status_name(vmid)
        while(vmData[1] != "running"):
            print(vmData[1])
            vmData = await self.get_status_name(vmid)


    async def wait_till_Stopped(self, vmid):
        vmData = await self.get_status_name(vmid)
        while(vmData[1] != "stopped"):
            print(vmData[1])
            vmData = await self.get_status_name(vmid)

def findKeys(node,kv):
        if isinstance(node,list):
            for i in node:
                for x in self.findKeys(i,kv):
                    yield x
        elif isinstance(node, dict):
            if kv in node:
                yield node[kv]
            for j in node.values():
                for x in findKeys(j,kv):
                    yield x