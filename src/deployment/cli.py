"""
Module that contains the command line app.
 
Typical usage example from command line:
        python cli.py
"""

import os
import argparse
import random
import string
from kfp import dsl
from kfp import compiler
import google.cloud.aiplatform as aip
from model import model_training, model_deploy


GCP_PROJECT = os.environ["GCP_PROJECT"]
GCS_BUCKET_NAME = os.environ["GCS_BUCKET_NAME"]
BUCKET_URI = f"gs://{GCS_BUCKET_NAME}"
PIPELINE_ROOT = f"{BUCKET_URI}/pipeline_root/root"
GCS_SERVICE_ACCOUNT = os.environ["GCS_SERVICE_ACCOUNT"]
GCS_PACKAGE_URI = os.environ["GCS_PACKAGE_URI"]
GCP_REGION = os.environ["GCP_REGION"]

# Read the docker tag file
with open(".docker-tag") as f:
    tag = f.read()

tag = tag.strip()

print("Tag>>", tag, "<<")

DATA_COLLECTOR_IMAGE = f"gcr.io/{GCP_PROJECT}/ccb-download_from_dac:{tag}"
DATA_PROCESSOR_IMAGE = f"gcr.io/{GCP_PROJECT}/ccb-preprocessing:{tag}"


def generate_uuid(length: int = 8) -> str:
    return "".join(random.choices(string.ascii_lowercase + string.digits, k=length))


def main(args=None):
    print("CLI Arguments:", args)

    if args.data_collector:
        # Define a Container Component
        @dsl.container_component
        def data_collector():
            container_spec = dsl.ContainerSpec(
                image=DATA_COLLECTOR_IMAGE,
                command=[],
                args=[
                    "cli.py",
                    "--search",
                    "--nums 5",
                    "--query oyster+mushrooms crimini+mushrooms amanita+mushrooms",
                    f"--bucket {GCS_BUCKET_NAME}",
                ],
            )
            return container_spec

        # Define a Pipeline
        @dsl.pipeline
        def data_collector_pipeline():
            data_collector()

        # Build yaml file for pipeline
        compiler.Compiler().compile(
            data_collector_pipeline, package_path="data_collector.yaml"
        )

        # Submit job to Vertex AI
        aip.init(project=GCP_PROJECT, staging_bucket=BUCKET_URI)

        job_id = generate_uuid()
        DISPLAY_NAME = "mushroom-app-data-collector-" + job_id
        job = aip.PipelineJob(
            display_name=DISPLAY_NAME,
            template_path="data_collector.yaml",
            pipeline_root=PIPELINE_ROOT,
            enable_caching=False,
        )

        job.run(service_account=GCS_SERVICE_ACCOUNT)

    if args.data_processor:
        print("Data Processor")

        # Define a Container Component for data processor
        @dsl.container_component
        def data_processor():
            container_spec = dsl.ContainerSpec(
                image=DATA_PROCESSOR_IMAGE,
                command=[],
                args=[
                    "cli.py",
                    "--clean",
                    "--prepare",
                    f"--bucket {GCS_BUCKET_NAME}",
                ],
            )
            return container_spec

        # Define a Pipeline
        @dsl.pipeline
        def data_processor_pipeline():
            data_processor()

        # Build yaml file for pipeline
        compiler.Compiler().compile(
            data_processor_pipeline, package_path="data_processor.yaml"
        )

        # Submit job to Vertex AI
        aip.init(project=GCP_PROJECT, staging_bucket=BUCKET_URI)

        job_id = generate_uuid()
        DISPLAY_NAME = "mushroom-app-data-processor-" + job_id
        job = aip.PipelineJob(
            display_name=DISPLAY_NAME,
            template_path="data_processor.yaml",
            pipeline_root=PIPELINE_ROOT,
            enable_caching=False,
        )

        job.run(service_account=GCS_SERVICE_ACCOUNT)

    if args.model_training:
        print("Model Training")

        # Define a Pipeline
        @dsl.pipeline
        def model_training_pipeline():
            model_training(
                project=GCP_PROJECT,
                location=GCP_REGION,
                staging_bucket=GCS_PACKAGE_URI,
                bucket_name=GCS_BUCKET_NAME,
            )

        # Build yaml file for pipeline
        compiler.Compiler().compile(
            model_training_pipeline, package_path="model_training.yaml"
        )

        # Submit job to Vertex AI
        aip.init(project=GCP_PROJECT, staging_bucket=BUCKET_URI)

        job_id = generate_uuid()
        DISPLAY_NAME = "mushroom-app-model-training-" + job_id
        job = aip.PipelineJob(
            display_name=DISPLAY_NAME,
            template_path="model_training.yaml",
            pipeline_root=PIPELINE_ROOT,
            enable_caching=False,
        )

        job.run(service_account=GCS_SERVICE_ACCOUNT)

    if args.model_deploy:
        print("Model Deploy")

        # Define a Pipeline
        @dsl.pipeline
        def model_deploy_pipeline():
            model_deploy(
                bucket_name=GCS_BUCKET_NAME,
            )

        # Build yaml file for pipeline
        compiler.Compiler().compile(
            model_deploy_pipeline, package_path="model_deploy.yaml"
        )

        # Submit job to Vertex AI
        aip.init(project=GCP_PROJECT, staging_bucket=BUCKET_URI)

        job_id = generate_uuid()
        DISPLAY_NAME = "mushroom-app-model-deploy-" + job_id
        job = aip.PipelineJob(
            display_name=DISPLAY_NAME,
            template_path="model_deploy.yaml",
            pipeline_root=PIPELINE_ROOT,
            enable_caching=False,
        )

        job.run(service_account=GCS_SERVICE_ACCOUNT)

    if args.pipeline:
        # Define a Container Component for data collector
        @dsl.container_component
        def data_collector():
            container_spec = dsl.ContainerSpec(
                image=DATA_COLLECTOR_IMAGE,
                command=[],
                args=[
                    "cli.py",
                    "--search",
                    "--nums 50",
                    "--query oyster+mushrooms crimini+mushrooms amanita+mushrooms",
                    f"--bucket {GCS_BUCKET_NAME}",
                ],
            )
            return container_spec

        # Define a Container Component for data processor
        @dsl.container_component
        def data_processor():
            container_spec = dsl.ContainerSpec(
                image=DATA_PROCESSOR_IMAGE,
                command=[],
                args=[
                    "cli.py",
                    "--clean",
                    "--prepare",
                    f"--bucket {GCS_BUCKET_NAME}",
                ],
            )
            return container_spec

        # Define a Pipeline
        @dsl.pipeline
        def ml_pipeline():
            # Data Collector
            data_collector_task = (
                data_collector()
                .set_display_name("Data Collector")
                .set_cpu_limit("500m")
                .set_memory_limit("2G")
            )
            # Data Processor
            data_processor_task = (
                data_processor()
                .set_display_name("Data Processor")
                .after(data_collector_task)
            )
            # Model Training
            model_training_task = (
                model_training(
                    project=GCP_PROJECT,
                    location=GCP_REGION,
                    staging_bucket=GCS_PACKAGE_URI,
                    bucket_name=GCS_BUCKET_NAME,
                    epochs=1,
                    batch_size=16,
                    model_name="mobilenetv2",
                    train_base=False,
                )
                .set_display_name("Model Training")
                .after(data_processor_task)
            )
            # Model Deployment
            model_deploy_task = (
                model_deploy(
                    bucket_name=GCS_BUCKET_NAME,
                )
                .set_display_name("Model Deploy")
                .after(model_training_task)
            )

        # Build yaml file for pipeline
        compiler.Compiler().compile(ml_pipeline, package_path="pipeline.yaml")

        # Submit job to Vertex AI
        aip.init(project=GCP_PROJECT, staging_bucket=BUCKET_URI)

        job_id = generate_uuid()
        DISPLAY_NAME = "mushroom-app-pipeline-" + job_id
        job = aip.PipelineJob(
            display_name=DISPLAY_NAME,
            template_path="pipeline.yaml",
            pipeline_root=PIPELINE_ROOT,
            enable_caching=False,
        )

        job.run(service_account=GCS_SERVICE_ACCOUNT)


if __name__ == "__main__":
    # Generate the inputs arguments parser
    # if you type into the terminal 'python cli.py --help', it will provide the description
    parser = argparse.ArgumentParser(description="Workflow CLI")

    parser.add_argument(
        "-c",
        "--download_from_dac",
        action="store_true",
        help="Run just the Data Collector - download_from_dac",
    )
    parser.add_argument(
        "-p",
        "--data_processor",
        action="store_true",
        help="Run just the Data Processor",
    )
    parser.add_argument(
        "-t",
        "--model_training",
        action="store_true",
        help="Run just Model Training",
    )
    parser.add_argument(
        "-d",
        "--model_deploy",
        action="store_true",
        help="Run just Model Deployment",
    )
    parser.add_argument(
        "-w",
        "--pipeline",
        action="store_true",
        help="Mushroom App Pipeline",
    )

    args = parser.parse_args()

    main(args)