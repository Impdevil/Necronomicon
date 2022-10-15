import discord
import yaml
import c2.Proxmox_instance as pi

#load yml
##check if yml already loaded, create instances of proxmox
config =None
#prox_instances = []

async  def LoadConfig():

    #try: 
        with open("envVars.yml", "r") as yamlFile:
            config = yaml.safe_load(yamlFile)
        #print(config)
        
        for server in config["Servers"]:
            #print(server)
            prox_instances = pi.Proxmox_instance(server["ip"], server["port"],server["username1"],server["password1"],server["tokenID1"],server["token1"])
    #except:
        print("Config failed to load.")
        prox_instances.get_vm_status();
        return  "potato"
