import os, utils, glob


def combine_text(input_dir, output_dir, image_order):
    '''
    Combines the text of multiple scans into one file in the image order specified by the user, and writes output to text file
    '''
    print("input_dir", input_dir)
    print("output_dir", output_dir)
    for root, subdirs, files in os.walk(input_dir):
        output_file = output_dir + root[len(input_dir):] + ".txt"
        print("root", root)
        print("output_file", output_file)
        print("root[len..]", root[len(input_dir):])
        structure = os.path.dirname(output_file)
        utils.construct_output_dir(structure)
        if os.path.exists(output_file):
            continue
        pages = []
        for file in files:
            if file.split(".")[1] == "txt":
                pages.append(file)
        if pages:
            if image_order == "underscore_numerical": #eg book_1.jpg book_2.jpg book_3.jpg
                pages.sort(key = lambda pages: int(pages.split(".")[0].split("_")[-1]))
            elif image_order == "dash_numerical": # eg book-1.jpg, book-2.jpg, book-3.jpg
                pages.sort(key = lambda pages: int(pages.split(".")[0].split("-")[-1]))
            elif image_order == "numerical": #eg. 1.jpg, 2.jpg, 3.jpg
                pages.sort(key = lambda pages: int(pages.split(".")[0]))
            else: # alphabetical, eg a.jpg, b.jpg, c.jpg, d.jpg
                pages.sort()

            with open(output_file, 'w') as output:
                for file in pages: # add a sort by for file naming
                    abspath = os.path.join(root, file)
                    with open(abspath) as f:
                        for line in f:
                            output.write(line)
            print(str(len(pages)) + " images combined and written to " + output_file)
    return

