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

GCP_PROJECT = os.environ["GCP_PROJECT"]
GCS_BUCKET_NAME = os.environ["GCS_BUCKET_NAME"]
BUCKET_URI = f"gs://{GCS_BUCKET_NAME}"
PIPELINE_ROOT = f"{BUCKET_URI}/pipeline_root/root"
GCS_SERVICE_ACCOUNT = os.environ["GCS_SERVICE_ACCOUNT"]
GCP_REGION = os.environ["GCP_REGION"]

# Read the docker tag file
with open(".docker-tag") as f:
    tag = f.read()

tag = tag.strip()

print("Tag>>", tag, "<<")

DOWNLOAD_FROM_DAC = f"gcr.io/{GCP_PROJECT}/ccb-download_from_dac:{tag}"
PREPROCESSING = f"gcr.io/{GCP_PROJECT}/ccb-preprocessing:{tag}"
MODEL1 = f"gcr.io/{GCP_PROJECT}/ccb-model1:{tag}"
MODEL2 = f"gcr.io/{GCP_PROJECT}/ccb-model2:{tag}"


def generate_uuid(length: int = 8) -> str:
    return "".join(random.choices(string.ascii_lowercase + string.digits, k=length))


def main(args=None):
    print("CLI Arguments:", args)

    if args.pipeline:
        # Define a Container Component for data collector
        @dsl.container_component
        def download_from_dac():
            container_spec = dsl.ContainerSpec(
                image=DOWNLOAD_FROM_DAC,
                command=[],
                args=[
                    "cli.py",
                ],
            )
            return container_spec

        @dsl.container_component
        def preprocessing():
            container_spec = dsl.ContainerSpec(
                image=PREPROCESSING,
                command=[],
                args=[
                    "cli.py",
                ],
            )
            return container_spec

        @dsl.container_component
        def model1():
            container_spec = dsl.ContainerSpec(
                image=MODEL1,
                command=[],
                args=[
                    "cli.py",
                ],
            )
            return container_spec

        @dsl.container_component
        def model2():
            container_spec = dsl.ContainerSpec(
                image=MODEL2,
                command=[],
                args=[
                    "cli.py",
                ],
            )
            return container_spec
        
        # Define a Pipeline
        @dsl.pipeline
        def ml_pipeline():
            
            download_from_dac_task = (
                download_from_dac()
                .set_display_name("download_from_dac")
                .set_cpu_limit("500m")
                .set_memory_limit("2G")
            )

            preprocessing_task  = (
                preprocessing()
                .set_display_name("preprocessing")
                .set_cpu_limit("500m")
                .set_memory_limit("2G")
                .after(download_from_dac_task)
            )

            model1_task = (
                model1()
                .set_display_name("model1")
                .set_cpu_limit("500m")
                .set_memory_limit("2G")
                .after(preprocessing_task)
            )

            model2_task = (
                model2()
                .set_display_name("model2")
                .set_cpu_limit("500m")
                .set_memory_limit("2G")
                .after(model1_task)
            )


            
        # Build yaml file for pipeline
        compiler.Compiler().compile(ml_pipeline, package_path="pipeline.yaml")

        # Submit job to Vertex AI
        print("Submitting job to Vertex AI...")
        aip.init(project=GCP_PROJECT, staging_bucket=BUCKET_URI)

        job_id = generate_uuid()
        DISPLAY_NAME = "ccb-app-pipeline" + job_id
    
        print("Creating PipelineJob")
        job = aip.PipelineJob(
            display_name=DISPLAY_NAME,
            template_path="pipeline.yaml",
            pipeline_root=PIPELINE_ROOT,
            enable_caching=False,
        )
        
        # Print information about the PipelineJob
        print("Job ID:", job_id)

        print("Running job:", job)
        job.run(service_account=GCS_SERVICE_ACCOUNT)


if __name__ == "__main__":
    # Generate the inputs arguments parser
    # if you type into the terminal 'python cli.py --help', it will provide the description
    parser = argparse.ArgumentParser(description="Workflow CLI")

    parser.add_argument(
        "-w",
        "--pipeline",
        action="store_true",
        help="Mushroom App Pipeline",
    )

    args = parser.parse_args()

    main(args)