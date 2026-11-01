"""PayNTax CI/CD: from pull request to production."""
from diagrams import Cluster, Diagram, Edge
from diagrams.aws.compute import ECR, ECS
from diagrams.onprem.ci import GithubActions
from diagrams.onprem.client import User
from diagrams.onprem.iac import Terraform
from diagrams.onprem.vcs import Github

with Diagram(
    "PayNTax - CI/CD Pipeline",
    show=False,
    filename="docs/assets/cicd_pipeline",
    outformat="png",
    direction="LR",
    graph_attr={"fontsize": "20", "pad": "0.5", "splines": "spline"},
):
    dev = User("Developer")
    repo = Github("payntax-app\nPR to main")

    with Cluster("GitHub Actions: CI"):
        ci = GithubActions("CI\nlint, tests,\naccuracy, CodeQL")
        build = GithubActions("Build images")

    registry = ECR("ECR")
    iac = Terraform("Terraform")

    with Cluster("GitHub Actions: CD"):
        deploy = GithubActions("Deploy")

    with Cluster("AWS accounts"):
        env_dev = ECS("dev\n(every merge)")
        env_stg = ECS("staging\n(tag vX.Y.Z)")
        env_prod = ECS("prod\n(manual approval)")

    dev >> repo >> ci >> build >> registry >> deploy
    iac >> Edge(style="dashed", label="infra changes") >> deploy
    deploy >> env_dev
    deploy >> env_stg
    deploy >> Edge(color="firebrick", label="approval gate") >> env_prod
