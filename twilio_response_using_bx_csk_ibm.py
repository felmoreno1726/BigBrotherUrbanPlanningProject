import  subprocess
import ast
import json

command=["bx", "wsk", "activation", "list"]

p=subprocess.check_output(command)
p=p.decode()
p=p.split("\n")
actlog=p[1].split(" ")[0]
print(actlog)

command2=["bx", "wsk", "activation", "result", actlog]
p2=subprocess.check_output(command2).decode()
print("p2=",p2)

output = json.loads(p2)
print (output["greeting"])

"""
print(type(p2))
p2=p2.split(" ")
p2=p2[-1].split("\n")
print(type(p2))
print(p2)
p3 = print (str(p2[0]))
"""
