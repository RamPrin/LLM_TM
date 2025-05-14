
from pytm import TM, Boundary, Process, Server, Datastore, Actor, Dataflow

tm = TM("Virtual Containers Threat Model")

# Boundaries
internet = Boundary("Internet")
hostOS   = Boundary("Host OS")

# Actors
attacker = Actor("Attacker", boundary=internet)

# Components
ci_cd        = Process("CI/CD Pipeline", boundary=internet)
imageRegistry= Server("Container Image Registry", boundary=internet)
orchestrator = Server("Container Orchestrator", boundary=hostOS)
runtime      = Process("Container Runtime", boundary=hostOS)
kernel       = Process("Host Kernel", boundary=hostOS)
unionFS      = Datastore("Union File System", boundary=hostOS)
container    = Process("Application Container", boundary=hostOS)

# Dataflows
Dataflow(ci_cd,        imageRegistry, "Push Image",              protocols=["HTTPS"])
Dataflow(runtime,      imageRegistry, "Pull Image",              protocols=["HTTPS"])
Dataflow(orchestrator, runtime,       "Schedule/Start Container", protocols=["API"])
Dataflow(runtime,      kernel,        "Manage Namespaces & cgroups")
Dataflow(container,    unionFS,       "Read/Write FS")
Dataflow(attacker,     runtime,       "Exploit Runtime Vulnerability", protocols=["TCP"])

tm.process()