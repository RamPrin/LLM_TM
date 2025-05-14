# Model:

```python
from pytm.pytm import TM, Server, Datastore, Dataflow, Boundary, Process, Actor

tm = TM("Virtual Container Threat Model")

# Boundaries
Internet = Boundary("Internet")
Host_OS = Boundary("Host OS")
Container = Boundary("Container")

# Components
User = Actor("User", inBoundary=Internet)
OrchestrationTool = Process("Container Orchestration Tool", inBoundary=Host_OS)
Kernel = Server("Shared OS Kernel", inBoundary=Host_OS)
ContainerRuntime = Process("Container Runtime", inBoundary=Host_OS)
ContainerApp = Process("Containerized Application", inBoundary=Container)
ContainerRegistry = Datastore("Container Registry", inBoundary=Internet)

# Dataflows
User_to_OrchestrationTool = Dataflow(User, OrchestrationTool, "Interacts with Orchestration Tool", inBoundary=Internet)
OrchestrationTool_to_Runtime = Dataflow(OrchestrationTool, ContainerRuntime, "Commands to manage containers", inBoundary=Host_OS)
Runtime_to_Kernel = Dataflow(ContainerRuntime, Kernel, "System calls for containers", inBoundary=Host_OS)
Kernel_to_ContainerApp = Dataflow(Kernel, ContainerApp, "Allocation of resources", inBoundary=Host_OS)
ContainerApp_to_Registry = Dataflow(ContainerApp, ContainerRegistry, "Pull/Push images", inBoundary=Internet)

tm.process()
```

# Threats

Spoofing:
- Fake User Access: Malicious user may attempt to spoof legitimate user access to the orchestration tool.
- Container Registry Spoofing: An attacker might spoof the container registry to supply malicious images.

Tampering:
- Container Image Tampering: Images in the container registry could be tampered with to include malicious code.
- Dataflow Alteration: Dataflows between containers or to the kernel can be intercepted and altered.

Repudiation:
- Action Non-repudiation: Users can deny actions in interacting with the container orchestration without proper logging.
- Deployment Activity Repudiation: Deployment actions within the orchestration tool might not be adequately logged, allowing repudiation.

Information Disclosure:
- Container Data Leak: Sensitive information within a container could be exposed to unauthorized parties.
- Image Information Leakage: Unauthorized users might access sensitive metadata or environment details of container images.

Denial of Service:
- Resource Exhaustion Attack: A container may consume excessive resources, leading to denial of service for other containers.
- Container Flooding: Excessive container instantiation can overwhelm the container orchestration and host resources.

Elevation of Privilege:
- Privilege Escalation in Host OS: Exploiting container vulnerabilities to gain elevated privileges in the host operating system.
- Kernel Exploitation: Leveraging a kernel exploit to gain greater control over the host OS or other containers.

