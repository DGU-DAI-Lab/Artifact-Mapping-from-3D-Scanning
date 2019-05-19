import cv2
import numpy as np

from Artifact import *
from Oldway import *
from Newway import *

CONTOUR_THICKNESS = 1
ARTIFACT_LIST = [
    { 'name' : "고배",        'altname' : "a" },
    { 'name' : "굽다리접시1", 'altname' : "b" },
    { 'name' : "토기6",       'altname' : "c" }
]

def __main__():
    global CONTOUR_THICKNESS
    # Depth-Based Segmentation
    # Body/Window Seperation
    samples = load_samples()
    for artifact in samples:
        print("Artifact processing - [%s]" % (artifact.name))
        oldway = Oldway(artifact)
        oldway.CONTOUR_THICKNESS = CONTOUR_THICKNESS

        newway = Newway(artifact)
        newway.CONTOUR_THICKNESS = CONTOUR_THICKNESS
        
        opacity = 1
        final = np.zeros(artifact.shape,dtype=np.uint8)
        for section in ["front", "back", "slice"]:
            result = newway.combination[section]
            final = cv2.addWeighted(final, 1, result, opacity, 0)
            opacity *= .3

            cv2.imwrite("../%s_%s_%s.jpg" % (artifact.name, section, "all-contours"), result)
        cv2.imwrite("../%s_%s.jpg" % (artifact.name, "all-contours"), final)
    # Fin.
    cv2.waitKey(0)


def load_samples():
    samples = []
    for info in ARTIFACT_LIST:
        artifact = Artifact()
        artifact.name = info['altname']
        artifact.load("../test_data/%s.png" % info['name']) # TO CHANGE
        samples.append(artifact)
    return samples
        
__main__()
exit()