from kfp import dsl
from kfp.dsl import component, Output, Artifact
from kfp import compiler

# declare macros - can also add as arguments at runtime
# Define GCS URIs at the top of your file
bucket_uri = 'gs://baby-cry-bucket'

# component for data download
@component(
    base_image='us-east1-docker.pkg.dev/ac215-project-400018/ac215-crycrybaby-ar/download_from_dac:latest',
)
def download_from_dac(
        download_dac_output_bucket: str,
):
    # In this case, the body can be left empty, as the behavior
    # of the component is defined by the entrypoint of `my-image`.
    pass

@component(
    base_image='us-east1-docker.pkg.dev/ac215-project-400018/ac215-crycrybaby-ar/preprocessing:latest',
)
def preprocessing(
        preprocessing_input_bucket: str,
        preprocessing_output_bucket: str
):
    pass

@component(
    base_image='us-east1-docker.pkg.dev/ac215-project-400018/ac215-crycrybaby-ar/model1:latest',
)
def model1(
        model1_input_bucket: str,
        model1_output_bucket: str
):
    pass
@component(
    base_image='us-east1-docker.pkg.dev/ac215-project-400018/ac215-crycrybaby-ar/model2:latest',
)
def model2(
        model2_input_bucket: str,
        model2_output_bucket: str
):
    pass


# declare the pipeline as a Python function
@dsl.pipeline(
    name='AC215_CryCryBaby',
    description='A pipeline to train and deploy a model to classify baby cries.'
)
def my_pipeline(
    download_dac_output_bucket: str = bucket_uri,
    preprocessing_input_bucket: str = bucket_uri,
    preprocessing_output_bucket: str = bucket_uri,
    model1_input_bucket: str = bucket_uri,
    model1_output_bucket: str = bucket_uri,
    model2_input_bucket: str = bucket_uri,
    model2_output_bucket: str = bucket_uri

):
    # Create a task for the first component
    my_component1_task = download_from_dac(download_dac_output_bucket=download_dac_output_bucket)

    # Create a task for the second component
    my_component2_task = preprocessing(preprocessing_input_bucket=preprocessing_input_bucket, preprocessing_output_bucket=preprocessing_output_bucket)

    # Specify that my_component2_task should run after my_component1_task
    my_component2_task.after(my_component1_task)

    # Create a task for the third component
    my_component3_task = model1(model1_input_bucket=model1_input_bucket, model1_output_bucket=model1_output_bucket)
    my_component3_task.after(my_component2_task)

    # Create a task for the fourth component
    my_component4_task = model2(model2_input_bucket=model2_input_bucket, model2_output_bucket=model2_output_bucket)
    my_component4_task.after(my_component3_task)

if __name__ == '__main__':
    compiler.Compiler().compile(
        pipeline_func=my_pipeline,
        package_path='kubeflow/my-pipeline.json'
    )

# upload to Vertex AI if we want to automate
# pipeline = aiplatform.PipelineJob(
#     display_name='my-pipeline',
#     template_path='ml-pipeline.zip',
#     enable_caching=False,
# )
# # run the pipeline on Vertex AI
# pipeline.run(
#     parameter_values={
#         'download_dac_output_bucket': 'gs://baby-cry-bucket',
#         'preprocessing_input_bucket': 'gs://baby-cry-bucket',
#         'preprocessing_output_bucket': 'gs://baby-cry-bucket',
#     },
#     replica_count=1,
# )