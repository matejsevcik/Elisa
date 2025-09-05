# Word Count Program

This program counts the number of occurrences of individual words in text files and print the 5 most common ones. The intended use is:

1. Place the provided text files (dracula.txt, frankenstein.txt) inside the project's root folder

2. Open two terminals in the project’s root directory. In each terminal, run a server with a specific text file and port:

```
python server.py <filename1.txt> 5001
python server.py <filename2.txt> 5002
```
Press ctrl+c (Windows) to terminate them.

3. Open a third terminal in the project’s root directory and run the client:
```
python client.py
```

**Expected output**

Top 5 most common words:\
the: 12483\
and: 9018\
i: 7647\
to: 6919\
of: 6517
