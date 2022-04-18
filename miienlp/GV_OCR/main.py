import utils
from ocr import OCR
import argparse

ap = argparse.ArgumentParser()
ap.add_argument('-i', "--input", required=False, help="Path to input yaml file")
args = vars(ap.parse_args())


def main():
    '''
    Runs OCR pipeline
    '''
    try:
        params = utils.get_params(args['input'])
    except:
        params = utils.get_params()
    ocr = OCR(params["raw_data_directory"], params["output_combined"], params['output_uncombined'], params["ocr_method"], 
        params["confidence_threshold"], params["image_ordering"], params["language"], 
        params["project_id"], params["model_id"], params["remove_cover_ends"], 
        params["preprocess_images"])
    ocr.run_ocr_pipeline()
    return

if __name__ == "__main__":
    main()

