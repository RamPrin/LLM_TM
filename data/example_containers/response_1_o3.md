# Model:
```python
from pytm import TM, Boundary, Server, Process, Datastore, Dataflow, ExternalEntity

# Create the threat model
tm = TM("Containerization Threat Model")

# Boundaries
host = Boundary("Host OS Boundary")
network = Boundary("Network Boundary")

# Components
developer = ExternalEntity("Developer", description="Builds and pushes container images")
container_registry = Datastore("Container Registry", description="Stores container images", boundary=network)
image_builder = Process("Image Builder", description="Builds images from Dockerfiles", boundary=host)
orchestrator = Process("Orchestrator API", description="Schedules and manages containers", boundary=host)
container_runtime = Process("Container Runtime", description="Creates and runs containers (runc/containerd)", boundary=host)
container_fs = Datastore("UnionFS Layer", description="Read-only base image + writable layers", boundary=host)
container = Process("Container", description="Isolated application runtime", boundary=host)

# Dataflows
Dataflow(developer, container_registry, "push(image)", protocols="HTTPS", auth="TLS client cert")
Dataflow(container_runtime, container_registry, "pull(image)", protocols="HTTPS", auth="TLS server cert")
Dataflow(developer, orchestrator, "deploy(cmd)", protocols="HTTPS", auth="Token")
Dataflow(orchestrator, container_runtime, "schedule(container)", protocols="gRPC", auth="mTLS")
Dataflow(container_runtime, container_fs, "read/write(layers)", protocols="Local FS")
Dataflow(container, container, "inter-container comm", protocols="Virtual Network")
Dataflow(container, network, "egress/ingress", protocols="TCP/IP", auth="None")
Dataflow(orchestrator, network, "cluster state sync", protocols="HTTPS", auth="mTLS")
Dataflow(container_runtime, host, "manage namespaces & cgroups", protocols="Kernel API", auth="root")

tm.process()
```

# Threats

Spoofing:
- Registry Impersonation: Attacker poses as the container registry to serve malicious images.   
- Orchestrator Spoofing: Malicious actor spoofs the orchestration API to schedule unauthorized containers.
- DNS Spoofing: Redirect image pull or deploy requests to attacker-controlled endpoints.
- Container Identity Spoofing: One container impersonates another to access its network - services or data.  

Tampering:
- Image Tampering: Unauthorized modification of image layers in the registry to inject malware. 
- Runtime Configuration Tampering: Alteration of container runtime settings (cgroups, seccomp profiles) to weaken isolation.
- Host FS Tampering: Container breakout allowing write access to host file system (e.g., `/var/lib/docker`).  
- Network Packet Tampering: MITM attacker modifies in-flight container-to-container or external traffic. 

Repudiation:
- Insufficient Audit Logging: Container lifecycle events (start/stop) are not logged or are easily deleted.
- Missing Image Provenance Logs: Inability to track who built or pushed a specific image version. 
- Unlogged Orchestrator Actions: Deploy, scale or delete commands not recorded centrally.
- Namespace Operation Gaps: Changes to namespaces (PID, network) are not audited.

Information Disclosure:
- Secrets in Environment Variables: Sensitive keys or credentials exposed inside container images or logs.  
- Volume Mount Data Exposure: Containers reading host directories (e.g., `/etc/credentials`) leak secrets.  
- Network Eavesdropping: Unencrypted traffic between containers or to external services can be intercepted.  
- Registry Metadata Leakage: Attackers enumerate image tags and repository structure to map infrastructure.
- Side‐channel Memory Disclosure: Co‑located containers infer host or other container data via shared caches.

Denial of Service:
- Host Resource Exhaustion: Malicious containers spawn unlimited processes to consume CPU/memory.  
- Cgroup Limit Bypass: Misconfigured cgroups allow a container to exhaust system resources.
- Registry Overload: Flooding the registry with pull/push requests to degrade service.
- Network Flooding: Containers generate excessive traffic, saturating host network interface.
- Orchestrator API Flood: High‐volume deploy/delete requests overwhelm the orchestration control plane.

Elevation of Privilege:
- Namespace Escape: Exploiting kernel vulnerabilities to break out of PID or mount namespaces.
- Kernel Exploit: Leveraging unpatched vulnerabilities (e.g., dirty COW) for host root access.
- Privileged Container Abuse: A container started with `--privileged` flag gains full host privileges.  
- Docker Socket Mount: Mounting `/var/run/docker.sock` to control the Docker daemon and spawn root containers. 
- Malicious Runtime Plugin: Installing or loading a rogue plugin into containerd or runc to execute host code.