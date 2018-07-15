import argparse
import pickle

def test_layout(filepath):
    layout = pickle.load(open(filepath, 'r'))
    letters = map(lambda x: x['letter'], layout['letters'])
    l_type, l_count, d_count = layout['layout_type'], len(letters), len(set(letters))
    print("Filepath: {0}".format(filepath))
    print("Layout type: {0}, letters count: {1}, distinct letters count: {2}\n".format(l_type, l_count, d_count))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('layouts_path', metavar='P', type=str)
    parser.add_argument('layouts_count', metavar='C', type=int)
    args = parser.parse_args()
    for i in range(1, args.layouts_count + 1):
        test_layout("{0}/keyboard{1}.layout".format(args.layouts_path, i))
    
main()


