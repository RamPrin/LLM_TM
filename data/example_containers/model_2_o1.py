
from pytm import TM, Actor, Asset, Boundary, Dataflow, Process, Server

# Define the threat model
tm = TM("Virtual Containers Threat Model")

# Define actors
developer = Actor("Developer")
attacker = Actor("Attacker")

# Define assets and processes
hostOS = Asset("Host Operating System")
container = Asset("Virtual Container")
kernel = Server("Shared Kernel")
network = Boundary("Network")

# Define processes
containerRun = Process("Container Runtime")
orchestration = Process("Orchestration Tool")

# Define boundaries
apiBoundary = Boundary("API")

# Define data flows
codeToContainer = Dataflow(developer, container, "Code Deployment")
runtimeToKernel = Dataflow(containerRun, kernel, "Kernel Interaction")
networkToContainer = Dataflow(network, container, "Network Traffic")
orchestrationToContainer = Dataflow(orchestration, container, "Orchestration Commands")

# Define threats
codeToContainer.threats.append("Unauthorized Code Injection")
runtimeToKernel.threats.append("Kernel Exploit via Container Runtime")
networkToContainer.threats.append("Network Sniffing or Spoofing")
orchestrationToContainer.threats.append("Unauthorized Access to Orchestration Tool")

# Set up the threat model
tm.process()

# Display the threat model
tm.report()