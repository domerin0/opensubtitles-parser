'''
The point of this script is to parse all subtitle xml data for source target pairs
It will assume each line is the target of the previous line.
This will store the text data in a tokenized format, meant to be parsed by a deep learning
framework and put into a pre-processed data file.
'''
import xml.etree.ElementTree as ET
import argparse
import os
import re
import errno

raw_file = "raw.txt"
inc = 0


def main():
    parser = argparse.ArgumentParser(description='Set parameters for xml parser.')
    parser.add_argument('--rootXmlDir', default="OpenSubtitles/en/",
                        help='Path to root directory of xml files')
    parser.add_argument('--dataDir', default="data/",
                        help='Path to directory process data will be saved.')
    args = parser.parse_args()
    processed_data_dir = args.dataDir
    raw_data_dir = args.rootXmlDir

    files = findXmlFiles(raw_data_dir)
    print("Have {} to parse!".format(len(files)))
    # Setup folder structure and data file
    mkdir_p(processed_data_dir)
    for f in files:
        try:
            extractTokenizedPhrases(f, processed_data_dir)
        except KeyboardInterrupt:
            print("Process stopped by user...")
            return 0
        except Exception as e:
            print(e)
            print("Error in " + f)
            pass


'''
Loops through folders recursively to find all xml files
'''


def findXmlFiles(directory):
    xmlFiles = []
    for f in os.listdir(directory):
        if os.path.isdir(directory + f):
            xmlFiles = xmlFiles + findXmlFiles(directory + f + "/")
        else:
            xmlFiles.append(directory + f)
    return xmlFiles


'''
The assumption is made (for now) that each <s> node in the xml docs represents
a token, meaning everything has already been tokenized. At first observation
this appears to be an ok assumption.

This function has been modified to print to a single file for each movie
This is for memory consideration when processing later down the pipeline
'''


def extractTokenizedPhrases(xmlFilePath, dataDirFilePath):
    global inc
    inc += 1
    mkfile(dataDirFilePath + str(inc) + raw_file)
    tree = ET.parse(xmlFilePath)
    root = tree.getroot()
    print("Processing {}...".format(xmlFilePath))
    for child in root.findall('s'):
        A = []
        for node in child.getiterator():
            if node.tag == 'w':
                A.append(node.text.encode('ascii', 'ignore').replace('-', ''))
        text = " ".join(A)
        text = cleanText(text)
        try:
            if text[0] != '[' and text[-1] != ':':
                with open(dataDirFilePath + str(inc) + raw_file, 'a') as f:
                    f.write(text + "\n")
        except IndexError:
            pass

'''
This function removes funky things in text
There is probably a much better way to do it, but unless the token list is
much bigger this shouldn't really matter how inefficient it is
'''


def cleanText(text):
    t = text.strip('-')
    t = t.lower()
    t = t.strip('\"')
    regex = re.compile('\(.+?\)')
    t = regex.sub('', t)
    t.replace('  ', ' ')
    regex = re.compile('\{.+?\}')
    t = regex.sub('', t)
    t = t.replace('  ', ' ')
    t = t.replace("~", "")
    t = t.strip(' ')
    return t


'''
Taken from http://stackoverflow.com/questions/600268/mkdir-p-functionality-in-python
'''


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def mkfile(path):
    try:
        with open(path, 'w+'):
            return 1
    except IOError:
        print("Data file open, ensure it is closed, and re-run!")
        return 0


if __name__ == "__main__":
    main()
