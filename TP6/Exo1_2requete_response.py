import json
import socket

    
def httpclient(type:str,path:str,version:str,body:str="",headers:dict={}):
    if type not in ["GET", "PUT", "POST", "DELETE", "HEAD"]:
        raise TypeError("erreur : Mauvaise methode http")
    if version=='1':
        vers="HTTP/1.1"
    elif version=='2':
        vers="HTTP/2.0"
    else:
        vers="HTTP/3.0"
    return json.dumps({"type":type,"url":path, "version":vers,"body":body,"headers":headers})
    
def httpresponse(version:str,status,body:str,headers:dict={},info:str=""):
    if not info:
        if status==404:
            info="NOT FOUND"
    if version=='1':
        vers="HTTP/1.1"
    elif version=='2':
        vers="HTTP/2.0"
    else:
        vers="HTTP/3.0"
    return json.dumps({"version":vers,"status":status,"info":info,"body":body,"headers":headers})
    
        
        
        
        