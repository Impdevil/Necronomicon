import discord
import yaml
import app.Proxmox_instance as pi

#load yml
##check if yml already loaded, create instances of proxmox
config =None
prox_instances = []

def LoadConfig():
    
    print("potato")
    #try: 
    with open("envVars.yml", "r") as yamlFile:
            config = yaml.safe_load(yamlFile)
    print(config)
        
    for server in config["Servers"]:
            print(server)
            prox_instances.append( pi.Proxmox_instance(server["ip"], server["port"],server["username"],server["password"],server["tokenID"],server["token"]))
    #except:
    print("Config failed to load.")
    