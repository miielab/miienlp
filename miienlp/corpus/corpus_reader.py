from nltk.tokenize import line_tokenize

class CorpusReader():
    def read_corpus(_dir, subcats, _type, ignore_lines_startswith="\n"):
        '''
        Create list of strings containing either genders or domains
        '''
        subcats = [cat + '.txt' for cat in subcats] if subcats else []
        d = {}
        for root, subdir, files in os.walk(_dir):
            for _file in files:
                if not _file.endswith('.txt'): continue
                if subcats and _file in subcats:
                    d = construct_vocab_dict(d, root, _file, _type)
                elif not subcats:
                    d = construct_vocab_dict(d, root, _file, _type)

        return d

    def construct_vocab_dict(d, root, _file, _type):
        '''
        Creates dictionary of specific word construct and related words
        '''
        vocab_set = set()
        path = os.path.join(root, _file)
        try:
            with open(path, 'r') as f:
                vocab = f.read().splitlines()
                for word in vocab:
                    if _file.split(".")[0] == "male_pronouns_lower" or _file.split(".")[0]  == "female_pronouns_lower":
                        vocab_set.add(word.lower())
                    elif _file.split(".")[0] == "male_pronouns_upper" or _file.split(".")[0]  == "female_pronouns_upper":
                        vocab_set.add(word.capitalize())
                    elif _type == "L":
                        vocab_set.add(word.lower())
                    elif _type == "U":
                        vocab_set.add(word.capitalize())
                    else:
                        vocab_set.update([word.lower(), word.capitalize()])

            d[_file.split(".")[0]] = vocab_set
            return d
        except FileNotFoundError:
            print("Warning: the filepath", path, "was not able to be opened.")