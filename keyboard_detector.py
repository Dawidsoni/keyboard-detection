from argparse import ArgumentParser
import cv2
import numpy as np
from letter_extraction import EdgeDetector
from metrics import KeyboardLayout

def get_image_path():
    parser = ArgumentParser()
    parser.add_argument('filepath', metavar='P', help='Path to image file')
    return parser.parse_args().filepath

def get_image(filepath):
    image = cv2.imread(filepath, 1)
    if image is None:
        raise Exception("Invalid filepath")
    return image

def get_contours_extractor():
    pass

def get_recognition_model():
    model = load_base_dense_net('letter_recognition/state_dicts/eval/in_place_m20_base_dense.pt', 20)
    model.eval()
    return model

def get_middle_point(coord):
    ps, pe = coord['start_pos'], coord['end_pos']
    return ((ps[0] + pe[0]) / 2, (ps[1] + pe[1]) / 2)

def get_pred_list(image, contours_extractor, recognition_model):
    fragment_list = contours_extractor.get_fragment_list(image)
    image_list = map(lambda x: x[1], fragment_list)
    image_data = np.array(image_list, dtype=np.float64).reshape(-1, 1, 32, 32)
    output_data = get_output_data(model, image_data)
    pred_list = map(lambda i: {
        'image': image_list[i], 
        'output': output_data[i], 
        'coord': fragment_list[i][0],
        'middle': get_middle_point(fragment_list[i][0])
    }, range(len(fragment_list)))
    letter_preds_map = get_all_above_threshold(pred_list, 0.99)
    return [pred for sublist in letter_preds_map.values() for pred in sublist]

def main():
    filepath = get_image_path()
    image = cv2.imread(filepath, 1)
    contours_extractor = get_contours_extractor()
    recognition_model = get_recognition_model()
    pred_list = get_pred_list(image, contours_extractor, recognition_model)



main()
