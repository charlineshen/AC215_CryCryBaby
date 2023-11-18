import tensorflow as tf

# Load the existing .h5 model
model = tf.keras.models.load_model('./output_model-model1_v1.h5')

# Save the model in TensorFlow SavedModel format
model.save('./output_model-model1_v1_tf', save_format='tf')