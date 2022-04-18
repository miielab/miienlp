import utils, json, sys, os
from wordtest import Multiple_WordTests
from fetchvec import FetchVec
from cleaning import Clean_WEAT

def main():
    params = utils.get_params()

    if params["run_analysis"] == 't':
        if params["reuse_fetchvec"] != 't':
            print('Preprocessing.............................')
            fv = FetchVec(params["model_directory"],
                          params["output_directory"],
                          params["test_directory"],
                          params["vocabulary_suffix"],
                          params["embeddings_suffix"])
            fv.fetch_vectors()

        wt = Multiple_WordTests(params["test_directory"],
                                params["output_directory"],
                                params["output_file"])

        print('Computing Scores..........................')
        wt.batch_test()

    if params["run_cleaning"] == 't':
        cw = Clean_WEAT(params["clean_csv"],
                           params["clean_out"])
        cw.clean()
        

if __name__ == '__main__':
    main()
        
