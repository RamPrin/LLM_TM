# TMLLM

## Description

This is an example of server, which can communicate with OpenAI and Anthropic APIs to use LLMs for threat modeling

## Prerequisites

- Python 3.11.x

- Install prerequisites from requirements.txt

    ```bash
    pip install -i requirements.txt
    ```

- OpenAI and Anthropic API keys should be stored as enviroment variables (`OPENAI_API_KEY` and `ANTHROPIC_API_KEY`)

## Usage

Run the server by this command:

```bash
fastapi dev server.py
```

After this, SwaggerAPI should be accessible by (http://localhost:8000/docs) URL

## System info sources

|System|Source link|
| ---- | --------- |
|Oauth2.0|[Link](https://datatracker.ietf.org/doc/html/rfc6819)|
|SSL|[Link](https://www.ssllabs.com/projects/index.html)|
|DNS|[Link](https://www.netmeister.org/blog/doh-dot-dnssec.html)|
|S3|[Link](https://controlcatalog.trustoncloud.com/dashboard/aws/s3#Data%20Flow%20Diagram)|
|Google Cloud Service|[Link](https://www.nccgroup.com/us/research-blog/threat-modelling-cloud-platform-services-by-example-google-cloud-storage/)|
|IoT Authentication|[Link](https://safecode.org/wp-content/uploads/2017/05/SAFECode_TM_Whitepaper.pdf)|
|PCI DSS|[Link](https://shostack.org/files/papers/A_PCI_Threat_Model_2020.pdf)|
|Certificate Transparency|[Link](https://datatracker.ietf.org/doc/html/draft-ietf-trans-threat-analysis-16)|
|K8S|[Link 1](https://github.com/cncf/financial-user-group/tree/main/projects/k8s-threat-model)  [Link 2](https://cloudsecdocs.com/containers/theory/threats/k8s_threat_model/) [Link 3](https://www.trendmicro.com/vinfo/us/security/news/security-technology/a-deep-dive-into-kubernetes-threat-modeling)|
|CI/CD|[Link](https://github.com/rung/threat-matrix-cicd)|
|AWS ECS Fargate|[Link](https://sysdig.com/blog/ecs-fargate-threat-modeling/)|
|Password Store Manager|[Link](https://crypto.stanford.edu/~dabo/pubs/papers/pwdmgrBrowser.pdf)|
|IoT Supply Chain|[Link](https://www.enisa.europa.eu/publications/guidelines-for-securing-the-internet-of-things)|
|Trinity|[Link]()|
|Conn_Cars|[Link](https://documents.trendmicro.com/assets/white_papers/wp-driving-security-into-connected-cars.pdf)|
|Email encryption gateway|[Link](https://www.slideshare.net/NCC_Group/real-world-application-threat-modelling-by-example)|
|Bitcoin|[Link](https://github.com/JWWeatherman/bitcoin_security_threat_model)|
|Containers|[Link 1](https://github.com/krol3/container-security-checklist#container-threat-model)  [Link 2](https://cloudsecdocs.com/containers/theory/threats/docker_threat_model/)|
|Medical Devices|[Link](https://www.mitre.org/sites/default/files/2021-11/Playbook-for-Threat-Modeling-Medical-Devices.pdf)|
|Contact Tracing Applications|[Link](https://www.linkedin.com/pulse/threat-modeling-contact-tracing-applications-jakub-kaluzny/)|
|Vehicle charging|[Link](https://www.pnnl.gov/main/publications/external/technical_reports/PNNL-34280.pdf)|
|Agentic AI|[Link](https://genai.owasp.org/resource/agentic-ai-threats-and-mitigations/)|
|Trusted firmware M|[Link](https://tf-m-user-guide.trustedfirmware.org/docs/security/threat_models/generic_threat_model.html)|
|ROS 2 Robotic System|[Link](https://design.ros2.org/articles/ros2_threat_model.html)|
