import os
from diagrams import Diagram, Cluster
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS
from diagrams.aws.network import ELB

# Ensure the output asset directory exists
os.makedirs("docs/assets", exist_ok=True)

with Diagram(
    name="Company Core Architecture", 
    show=False, 
    filename="docs/assets/system_architecture",
    outformat="png"
):
    lb = ELB("Ingress Load Balancer")
    
    with Cluster("Application Tier"):
        web_servers = [EC2("Worker Nodes 1"),
                       EC2("Worker Nodes 2")]

    db = RDS("Primary Database Instance")

    lb >> web_servers >> db
