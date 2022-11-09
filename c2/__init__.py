import discord
import yaml
import c2.Proxmox_instance as pi
import c2.intents as intents

#load yml
##check if yml already loaded, create instances of proxmox
config =None
prox_instances = None

async  def LoadConfig():
    global prox_instances
    try: 
        with open("envVars.yml", "r") as yamlFile:
            config = yaml.safe_load(yamlFile)
        #print(config)
        
        for server in config["Servers"]:
            #print(server)
            prox_instances = pi.Proxmox_instance(server["ip"], server["port"],server["username"],server["tokenID"],server["token"],server["id"])
    except:
        print("Config failed to load.")


    prox_instances.get_vm_status();
    

async def Start_bot():
    await LoadConfig()
    await intents.start_bot();