# BooleanRetrieval

Inverted index is one of the most fundamental and powerful tools of information retrieval. We will be creating a simple inverted index against a document collection and then run queries against it. You would need to download Cranfield collection which is a well-known IR test collection containing about 1,400 aerodynamics documents.

The indexerA.py can be run as python indexerA.py <document collection path>

The program will create an inverted index which will be stored on disk in a Json format. This index file is then used in the second program that uses the index to run simple Boolean queries against the index.

The queriesA can be run as python queriesA.py <sample queries text>
