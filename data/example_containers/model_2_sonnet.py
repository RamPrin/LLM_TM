
from pytm import TM, Server, Dataflow, Boundary, Actor, Data, DataStore, Process, Threat, Element

# Initialize the threat model
tm = TM("Virtual Container Security")
tm.description = "Threat model for containerized applications focusing on isolation, shared kernel, and resource management"

# Define boundaries
host_os = Boundary("Host Operating System")
container_runtime = Boundary("Container Runtime", parent=host_os)

# Define actors and elements
admin = Actor("Administrator")
developer = Actor("Developer")
user = Actor("End User")

host_server = Server("Host Server")
host_server.inBoundary = host_os

kernel = Process("Host Kernel")
kernel.inBoundary = host_os
kernel.isPrivileged = True

container_engine = Process("Container Engine")
container_engine.inBoundary = container_runtime
container_engine.OS = "Host OS"
container_engine.implementsAuthenticationScheme = True
container_engine.handlesResources = True
container_engine.hasAccessControl = True

image_registry = DataStore("Container Registry")
image_registry.inScope = True
image_registry.storesLogData = False
image_registry.storesSensitiveData = True
image_registry.isEncrypted = True

container1 = Process("Container 1")
container1.inBoundary = container_runtime
container1.implementsAuthenticationScheme = False
container1.isIsolated = True

container2 = Process("Container 2")
container2.inBoundary = container_runtime
container2.implementsAuthenticationScheme = False
container2.isIsolated = True

app_data = Data("Application Data", classification="Sensitive")
config_data = Data("Configuration", classification="Restricted")
container_image = Data("Container Image", classification="Public")

# Define dataflows
df_admin_host = Dataflow(admin, host_server, "Administrates Host")
df_admin_host.protocol = "SSH"
df_admin_host.dstPort = 22
df_admin_host.authenticatesDestination = True
df_admin_host.authenticatesSource = True

df_dev_engine = Dataflow(developer, container_engine, "Manages Containers")
df_dev_engine.protocol = "HTTPS"
df_dev_engine.dstPort = 443
df_dev_engine.authenticatesDestination = True
df_dev_engine.authenticatesSource = True

df_engine_registry = Dataflow(container_engine, image_registry, "Pull Container Images")
df_engine_registry.protocol = "HTTPS"
df_engine_registry.dstPort = 443
df_engine_registry.data = container_image
df_engine_registry.authenticatesDestination = True

df_engine_container1 = Dataflow(container_engine, container1, "Deploys Container")
df_engine_container1.protocol = "Local Socket"
df_engine_container1.data = container_image

df_engine_container2 = Dataflow(container_engine, container2, "Deploys Container")
df_engine_container2.protocol = "Local Socket"
df_engine_container2.data = container_image

df_container_kernel = Dataflow(container1, kernel, "System Calls")
df_container_kernel.protocol = "Syscall"
df_container_kernel.isEncrypted = False

df_container_container = Dataflow(container1, container2, "Container Communication")
df_container_container.protocol = "TCP/IP"
df_container_container.isEncrypted = False

df_user_container = Dataflow(user, container1, "Access Application")
df_user_container.protocol = "HTTPS"
df_user_container.dstPort = 443
df_user_container.data = app_data

# Define specific threats for containers
container_escape = Threat("Container Escape")
container_escape.description = "Attacker escapes container isolation to access host system"
container_escape.target = [container1, container2]
container_escape.prerequisites = "Vulnerability in container runtime or kernel"
container_escape.mitigations = "Implement seccomp filters, AppArmor profiles, and keep runtime updated"

kernel_exploit = Threat("Shared Kernel Exploitation")
kernel_exploit.description = "Attacker exploits vulnerability in shared kernel affecting all containers"
kernel_exploit.target = kernel
kernel_exploit.mitigations = "Regular kernel patching, reduced capabilities, secure kernel configuration"

resource_exhaustion = Threat("Resource Exhaustion")
resource_exhaustion.description = "Denial of service by exhausting host resources from container"
resource_exhaustion.target = [container1, container2, host_server]
resource_exhaustion.mitigations = "Implement cgroups limits and resource quotas"

malicious_image = Threat("Malicious Container Image")
malicious_image.description = "Introduction of malicious code via compromised container image"
malicious_image.target = [image_registry, container_image]
malicious_image.mitigations = "Image scanning, signed images, trusted base images"

network_compromise = Threat("Container Network Compromise")
network_compromise.description = "Attacker intercepts or manipulates container-to-container communication"
network_compromise.target = df_container_container
network_compromise.mitigations = "Network segmentation, encryption, network policies"

insufficient_isolation = Threat("Insufficient Isolation")
insufficient_isolation.description = "Weak isolation between containers allows for information leakage"
insufficient_isolation.target = [container1, container2]
insufficient_isolation.mitigations = "Proper namespace configuration, avoid privileged containers"

tm.process()