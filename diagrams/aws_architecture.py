"""PayNTax proposed AWS architecture for the December 2026 pilot."""
from diagrams import Cluster, Diagram, Edge
from diagrams.aws.compute import ECS
from diagrams.aws.database import ElasticacheForRedis, RDSPostgresqlInstance
from diagrams.aws.general import General, Users
from diagrams.aws.management import Cloudtrail, Cloudwatch
from diagrams.aws.ml import Textract
from diagrams.aws.network import ALB, CloudFront, Route53
from diagrams.aws.security import KMS, WAF, Cognito, SecretsManager
from diagrams.aws.storage import S3
from diagrams.onprem.monitoring import Sentry

graph_attr = {"fontsize": "20", "pad": "0.5", "splines": "spline", "nodesep": "0.6", "ranksep": "1.0"}

with Diagram(
    "PayNTax - AWS Architecture (proposed)",
    show=False,
    filename="docs/assets/aws_architecture",
    outformat="png",
    direction="LR",
    graph_attr=graph_attr,
):
    cpa = Users("CPA firms")

    with Cluster("AWS us-east-2 (US-only data)"):
        dns = Route53("DNS")
        waf = WAF("WAF")
        cdn = CloudFront("CloudFront")
        auth = Cognito("Auth + MFA\n(ADR pending)")

        with Cluster("VPC"):
            alb = ALB("ALB")

            with Cluster("ECS Fargate - private subnets"):
                web = ECS("Web\nNext.js")
                api = ECS("API\nDjango + DRF")
                worker = ECS("Workers\nCelery")

            with Cluster("Data - private subnets"):
                db = RDSPostgresqlInstance("PostgreSQL\n(encrypted)")
                redis = ElasticacheForRedis("Redis\njob queue")

        docs = S3("Documents\n(SSE-KMS)")

        with Cluster("Document AI"):
            ocr = Textract("Textract\n(OCR, ADR pending)")
            llm = General("LLM vision\npay stubs")

        with Cluster("Security"):
            kms = KMS("KMS keys\nfield encryption")
            secrets = SecretsManager("Secrets")

        with Cluster("Observability and audit"):
            logs = Cloudwatch("CloudWatch")
            trail = Cloudtrail("CloudTrail")

    stripe = General("Stripe Billing\n+ Stripe Tax")
    sentry = Sentry("Sentry")

    cpa >> dns >> waf >> cdn >> alb
    cpa >> Edge(label="login + MFA", style="dashed") >> auth
    alb >> web >> api
    api >> db
    api >> redis >> worker
    api >> Edge(label="pre-signed URL") >> docs
    worker >> docs
    worker >> ocr
    worker >> llm
    worker >> db
    api >> Edge(style="dotted") >> [kms, secrets]
    api >> Edge(label="hosted checkout\n+ webhooks", style="dashed") >> stripe
    api >> Edge(style="dotted") >> logs
    web >> Edge(style="dotted") >> sentry
