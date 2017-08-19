# Classifying math blocks with Keras/TensorFlow for use in CoreML

Thanks to fine tuning, you don't require a super computer or a massive amounts of images to train an image classifier with a pretty incredible accuracy.

This repo shows how to train your own classifier with the intent to transform it into a CoreML model.

As at the time of this writing CoreML doesn't support TensorFlow models. This is unfortunate as TensorFlow can do transfer learning from your categories in one line of code which is hard to beat ([see this article] (https://www.tensorflow.org/tutorials/image_retraining))

Neural networks can be converted to [CoreML](https://developer.apple.com/documentation/coreml/converting_trained_models_to_core_ml) format from Caffe and Keras.

## Fast.ai and Keras over Tensorflow to the rescue
[Fast.ai] (http://www.fast.ai/) is a fantastic resource for practical deep learning. Within lesson one, i was able to create my trained model with over 97% accuracy and after some messing up convert it to CoreML.

Fast.ai de uses Theano as backend, which is not supported by coreml conversion tools, however it is very easy to switch to TensorFlow and the docker image below is configured this way already.

Beware that not all layers from Keras as supported by the CoreML conversion tools, in particular lambda layers. In the model derived in the fast.ai class, the lambda preprocess the images to normalize to the original weights for which the VGG model was trained. Fortunately, CoreML provides parameters to replace that functionality at the conversion layer.

A possible approach:
 1 - Fine tune the VGG model from fast.ai lesson 1 with your categories, save the weights
 2 - Create a new model removing the lambda preprocessing layer, load your trained weights
 3 - Use this model with the rgb - gbr, plus rgb offset as input of the CoreML convert function.


### Get your environment ready
I created a docker image with the supported versions of Keras for CoreML.
https://hub.docker.com/r/jfplante/keras_tensorflow/

This is derived from https://hub.docker.com/r/gw000/keras-full/ with additional packages needed including coremltools.

Usage:
docker run -d -p=6006:6006 -p=8888:8888 -v=local_path_to_notebooks:/srv jfplante/keras_tensorflow

local_path_to_notebooks refers to the fast.ai notebooks, and notebooks from this repo for model training and coreml conversion.

### Capturing your images
I used my iPhone in Burst mode to take photos of my 2 categories which are [Math-U-See blocks](http://4.bp.blogspot.com/-Et6_8IvPOW0/VEPMsOiyVAI/AAAAAAAAPHo/Psw6lMVvAWo/s1600/Math%2BU%2BSee%2B(Review)06.jpg) for 1 and 10. With such different characteristics, distinct colors, I was thinking this would be a good way to start.

With the burst mode, I took around 400 images for each categories in different backgrounds.

Here is an example of block 1:
![Image of Block  1](https://github.com/jeanfredericplante/blocks_classifier/blob/master/resources/one.jpg)

And block 10:

![Image of Block  1](https://github.com/jeanfredericplante/blocks_classifier/blob/master/resources/ten.jpg)
