# Classifying math blocks with Keras/TensorFlow for use in CoreML

Thanks to fine tuning, you don't require a super computer or a massive amounts of images to train an image classifier with a pretty incredible accuracy.

This repo shows how to train your own classifier with the intent to transform it into a CoreML model.

As at the time of this writing CoreML doesn't support TensorFlow models. This is unfortunate as TensorFlow can do transfer learning from your categories in one line of code which is hard to beat ([see this article] (https://www.tensorflow.org/tutorials/image_retraining))

Neural networks can be converted to [CoreML](https://developer.apple.com/documentation/coreml/converting_trained_models_to_core_ml) format from Caffe and Keras.

## Fast.ai and Keras over Tensorflow to the rescue
Fast.ai is a fantastic resource for practical deep learning. Within lesson one, i was able to create my trained model with over 97% accuracy and after some messing up convert it to CoreML. Here are the steps

### Get your environment ready
I created a docker image with the supported versions of Keras for CoreML

## Getting a  docker image for Fast.ai setup
https://hub.docker.com/r/deeprig/fastai-course-1/
