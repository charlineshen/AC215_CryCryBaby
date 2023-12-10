import tensorflow as tf

def load_and_inspect_model(model_path):
    try:
        # Load the model
        model = tf.keras.models.load_model(model_path)
        
        # Print a summary of the model
        model.summary()

        return "Model loaded and appears to be formatted correctly."
    except Exception as e:
        return f"An error occurred: {e}"

# Replace 'path_to_your_model.h5' with the actual path to your .h5 model file
model_path = './output_model-model1_v1.h5'
result = load_and_inspect_model(model_path)
print(result)