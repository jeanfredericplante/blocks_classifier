# Classifying math blocks with Keras/TensorFlow for use in CoreML

Thanks to fine tuning, you don't require a super computer or a massive amounts of images to train an image classifier with a pretty incredible accuracy.

This repo shows how to train your own classifier with the intent to transform it into a CoreML model.
![](https://github.com/jeanfredericplante/block_count/blob/master/resources/v1.gif)

As at the time of this writing CoreML doesn't support TensorFlow models. This is unfortunate as TensorFlow can do transfer learning from your categories in one line of code which is hard to beat ([see this article] (https://www.tensorflow.org/tutorials/image_retraining))

Neural networks can be converted to [CoreML](https://developer.apple.com/documentation/coreml/converting_trained_models_to_core_ml) format from Caffe and Keras.

## Fast.ai and Keras over Tensorflow to the rescue
[Fast.ai] (http://www.fast.ai/) is a fantastic resource for practical deep learning. Within lesson one, i was able to create my trained model with over 97% accuracy and after some messing up convert it to CoreML.

Fast.ai de uses Theano as backend, which is not supported by coreml conversion tools, however it is very easy to switch to TensorFlow and the docker image below is configured this way already.

Beware that not all layers from Keras as supported by the CoreML conversion tools, in particular lambda layers. In the model derived in the fast.ai class, the lambda preprocess the images to normalize to the original weights for which the VGG model was trained. Fortunately, CoreML provides parameters to replace that functionality at the conversion layer.

A possible approach:
 1. Fine tune the VGG model from fast.ai lesson 1 with your categories, save the weights
 2. Create a new model removing the lambda preprocessing layer, load your trained weights
 3. Use this model with the rgb - bgr, plus rgb offsets as input of the CoreML convert function.


### Get your environment ready
I created a docker image with  supported versions of Keras and TensorFlow for CoreML. It has Keras 1.2.2 and TensorFlow 1.0.1.
https://hub.docker.com/r/jfplante/keras_tensorflow/

This is derived from https://hub.docker.com/r/gw000/keras-full/ with additional packages needed including coremltools.

Usage:
docker run -d -p=6006:6006 -p=8888:8888 -v=local_path_to_notebooks:/srv jfplante/keras_tensorflow

local_path_to_notebooks refers to the fast.ai notebooks, and notebooks from this repo for model training and coreml conversion.

Notebooks should be available by loading your Jupyter notebooks from http://localhost:8888/tree/notebooks/nbs (password: keras)

Navigate to inceptionv3_retraining notebook for training and CoreML conversion.

### Capturing your images
I used my iPhone in Burst mode to take photos of my 2 categories which are [Math-U-See blocks](http://4.bp.blogspot.com/-Et6_8IvPOW0/VEPMsOiyVAI/AAAAAAAAPHo/Psw6lMVvAWo/s1600/Math%2BU%2BSee%2B(Review)06.jpg) for 1 and 10. With such different characteristics, distinct colors, it hopefully should be an easy job for the classifier.

With the burst mode, I took around 400 images for each categories in different backgrounds.
Here is an example of block 1:

![Image of Block  1](https://github.com/jeanfredericplante/blocks_classifier/blob/master/resources/one.jpg)

And block 10:

![Image of Block  1](https://github.com/jeanfredericplante/blocks_classifier/blob/master/resources/ten.jpg)

After downloading your photos on you client, locate the bursts by looking at the location of of photo of the burst, and you'll find the other ones. Organize them in different folders for each category.

### Preparing your training, validation and test sets
#### Resizing and removing metadata from your images
First you'll need to resize your images (and optionally remove your metadata). The ```resize_images.sh``` script uses utilities available on mac (including sips), creates a "processed" directory and resizes the images to a max of 640 px. The VGG model used as a base for fine-tuning uses images for 224x224 as input so you can further optimize there.

#### Training, validation and test set
```create-test-train-set.py``` takes originals from your categories folder and creates a "training", "test" and "valid" folders with randomized. You can select the % allocated to each set.

### Fine tuning VGG
Notes: For my data set, retraining only the last layer laid to overfitting.
- Open inceptionv3_retraining notebook (planning to compare with Inception retraining)
- Adjust parameters to your dataset categories

### Export to CoreML
- Docker environment should have at least 12GB dedicated
- CoreML expects TensorFlow image ordering which is why you have to get the backend of keras as Tensorflow (i.e., shape of the image should be (img_rows, img_cols, 3))
- CoreML doesn't support lambdas, so the normalization of the input should be done elsewhere. Thankfully, those are parameters that can be set as part of the convert function in CoreML as well as color channel ordering. VGG's training input bias is reflected below:
```is_bgr=True, red_bias=-123.68, green_bias=-116.78, blue_bias=-103.94```


## Adding bounding boxes
### Fully Convolutional Model and heatmap
- block_classifier_with_bounding_boxes notebook details a new fully fully convolutional model, where i plan to use the last layer to detect the bounding boxes.
- By sizing my last convolutional layer with the number of classes (currently 2), if my model learns the right features I get a heatmap of my ones and tens. The idea is to automatically generate bounding boxes and recycle them as input for a new model with bounding boxes output. A nice side effect of the heatmap is to visualize overfitting and generalization capacity and Dropout definitely made a great difference in getting the model to latch on the right features.

Block 1 with throughout Dropout 0.2 with heatmap overlay of last conv layer output

![Image of Block  1](https://github.com/jeanfredericplante/blocks_classifier/blob/master/resources/one_dropout02.png)

Block 1 with throughout Dropout 0.6 with heatmap overlay of last conv layer output

![Image of Block  1](https://github.com/jeanfredericplante/blocks_classifier/blob/master/resources/one_dropout06.png)


## Importing in an iPhone app
###
- Code in [block_count repo] (https://github.com/jeanfredericplante/block_count)
