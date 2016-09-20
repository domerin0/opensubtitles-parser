# opensubtitles-parser
This automates the process of downloading, extracting, and tokenizing all the text from the opensubtitles dataset into one large corpus text file. Each phrase is on it's own line, and each phrase is delimited by a space separating each token in the phrase.

## Attribution

This script uses the data set found at:http://opus.lingfil.uu.se/OpenSubtitles.php

It was made possible by: Jörg Tiedemann, 2009, News from OPUS - A Collection of Multilingual Parallel Corpora with Tools and Interfaces. In N. Nicolov and K. Bontcheva and G. Angelova and R. Mitkov (eds.) Recent Advances in Natural Language Processing (vol V), pages 237-248, John Benjamins, Amsterdam/Philadelphia

## Usage

When using the script for the first time, run ``./setup.sh ``. This will download the dataset and then parse it.

If you have already downloaded the dataset, run ``python opensubtitleparser.py ``.


##Notes

Some words are appearing in the corpus file without a space between tokens (ex/ and the -> andthe) I don't know if this is from the original dataset, or a problem with my script. I need to look more into it.
