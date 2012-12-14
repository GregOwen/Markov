"""
 "  Written By: Gregory Owen
 "  Date: 04-12-2012 
 "  Last Modified: Fri Dec 14 00:35:52 2012
 "  
 "  Execution: python markov.py fileName outputChars linkLength
 "  
 "  Description: Opens the file fileName and then models it as a Markov chain with
 "   links of linkLength characters. Randomly samples this Markov chain to output
 "   outputChars characters, beginning with the first linkLength characters of the
 "   input file.
"""

from sys import argv
from sys import stdout
from collections import defaultdict
import random

def getNextLink(currLink, chainDict, chainNumDict):
    """ Randomly selects one of the possible transitions from currLink using the
         transition frequencies provided in chainDict and the number of total
         transitions provided in chainNumDict.
        Returns the selected state. """

    offset = random.randint(0, chainNumDict[currLink] - 1)

    for link, occurrences in chainDict[currLink].iteritems():
        if offset < occurrences:
            return link
        offset -= occurrences

def processFile(fileName, linkLength):
    """ Splits the file fileName into strings of length linkLength, encoding the
         transition probabilities between different strings in a dictionary.
        Returns a list containing that dictionary, a defaultdict containing the 
         total number of transitions out of each state, and the first link in the 
         chain. """

    # Dictionary of dictionaries: chainDict[link] is a set of key-value pairs in
    #  which the key is a possible transition from link and the value is the number 
    #  of times that that transition has been seen
    chainDict = {}

    # Dictionary of number of transitions: chainNumDict[link] is the number of total
    #  transitions (not necessarily distinct) out of link. Used to calculate the
    #  probability of any given transition.
    chainNumDict = defaultdict(int)

    textFile = open(fileName)
    text = textFile.read()
    length = len(text)

    if length <= linkLength:
        print "Error: input length must be greater than chain length"
        textFile.close()
        return [None, None, None]

    firstLink = text[0:linkLength]
    link = firstLink

    for i in range(1, length - linkLength):
        prevLink = link
        link = text[i:i+linkLength]

        if prevLink not in chainDict:
            chainDict[prevLink] = defaultdict(int)

        chainDict[prevLink][link] += 1
        chainNumDict[prevLink] += 1

    # Add a transition from the last link to the first so that chain doesn't break
    if link not in chainDict:
        chainDict[link] = defaultdict(int)

    chainDict[link][firstLink] += 1
    chainNumDict[link] += 1

    textFile.close()
    return [chainDict, chainNumDict, firstLink]

def main():

    code, fileName, outputCharsIn, linkLengthIn = argv

    outputChars = int(outputCharsIn)
    linkLength = int(linkLengthIn)

    if outputChars < linkLength:
        print "Error: output length must be >= linkLength"
        return

    chains, chainNums, firstLink = processFile(fileName, linkLength)

    if chains == None:
        return

    stdout.write(firstLink);
    link = str(firstLink);

    for i in range(outputChars - linkLength):
        link = str(getNextLink(link, chains, chainNums))
        stdout.write(link[-1])
    
    stdout.write("\n")

main()
