Fishnet v1.0.0 
Bounding box label attribute descriptions

img_id - UUID for each image. Value corresponds to image names
seq_id - unique id for images that are grouped into a sequence
frame_id - unique id for each frame in a sequence
bbox_id - unique id for bounding box
x_min - minimum x coordinate value in image pixel units 
x_max - maxium x coordinate value in image pixel units
y_min - minimum y coordinate value in image pixel units
y_max - maximum y coordinate value in image pixel units
label_l1 - fine scale fish species classes
label_l2 - course scale fish species group classes
fao_mfa - United Nations Food and Agriculture Organization Major Fishing Areas identifiers. Boundaries can be viewed at https://www.fao.org/en/area/search
train - images for model training, True = include, False = exclude
val - images for model validation, True = include, False = exclude
test - images for model testing, True = include, False = exclude



Logic for populating train, val, and test

Goal:
Test set : 15% of images. Half is from 'unseen' cameras (not in the Train set), half is from 'seen' cameras (in the Train set)
Val set : 15% of images. Half is from 'unseen' cameras (not in the Train set), half is from 'seen' cameras (in the Train set)

Steps:
1. Add 'unseen' cameras to Test/Val: Sort cameras by number of images, ascending (so, start with the camera with the fewest images). Alternately add cameras to Test, Val, and Train until the combined size of Test+Val is 15% of the data (so Test and Val each contain around ~7.5% of the images). Add the rest to Train.
2. Chekc class balance: Make sure the Train set contains at least 30% of each Label_l2 class. Manually move any cameras from Test/Val to Train in order to make this true. (In the last version, just 1 camera had to be moved at this step)
3. Add 'seen' cameras to Test/Val: For each camera in Train, chop off the final 7.5% of images and add them to Test. Then chop off another 7.5% and add them to Val. The assumption is that catch events are grouped together - to do this best, you would also want to make sure the split points here are at the beginning/end of a sequence. You want to make sure each sequence of images from each catch event stays together (it's kind of cheating if half a catch event is partially in Train, and partially in Test. The model can memorize the fish.)
4. Class balance sanity check: Check for any Label_l1 classes that ended up entirely in Test or Val. Move these image sequences (or the whole camera, if you don't feel like inspecting sequences) to Train. We want to make sure every class is in the training set.