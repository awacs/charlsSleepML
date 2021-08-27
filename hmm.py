from accelerometer import accUtils
from io import BytesIO
import numpy as np
import os
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import sklearn.ensemble._forest as forest
import sklearn.metrics as metrics
from sklearn.metrics import confusion_matrix
import joblib
import tarfile
import warnings
from summariseEpoch import *
def getFileFromTar(tarArchive, targetFile):
    """Read file from tar
    This is currently more tricky than it should be see
    https://github.com/numpy/numpy/issues/7989
    :param str tarArchive: Input tarfile object
    :param str targetFile: Target individual file within .tar
    :return: file object byte stream
    :rtype: object
    """
    t = tarfile.open(tarArchive, 'r')
    array_file = BytesIO()
    array_file.write(t.extractfile(targetFile).read())
    array_file.seek(0)
    return array_file
def viterbi(observations, states, priors, transitions, emissions,
            probabilistic=False):
    """Perform HMM smoothing over observations via Viteri algorithm
    :param list(str) observations: List/sequence of activity states
    :param numpy.array states: List of unique activity state labels
    :param numpy.array priors: Prior probabilities for each activity state
    :param numpy.array transitions: Probability matrix of transitioning from one
        activity state to another
    :param numpy.array emissions: Probability matrix of RF prediction being true
    :param bool probabilistic: Write probabilistic output for each state, rather
        than writing most likely state for any given prediction.
    :return: Smoothed list/sequence of activity states
    :rtype: list(str)
    """

    def norm(x):
        return x / x.sum()

    tinyNum = 0.000001
    nObservations = len(observations)
    nStates = len(states)
    v = np.zeros((nObservations,nStates)) # initialise viterbi table
    # Set prior state values for first observation...
    for state in range(0, len(states)):
        v[0,state] = np.log(priors[state] * emissions[state,states.index(observations[0])]+tinyNum)
    # Fill in remaning matrix observations
    # Use log space as multiplying successively smaller p values)
    for k in range(1,nObservations):
        for state in range(0, len(states)):
            v[k,state] = np.log(emissions[state,states.index(observations[k])]+tinyNum) + \
                        np.max(v[k-1,:] + np.log(transitions[:,state]+tinyNum), axis=0)

    # Now construct viterbiPath (propagating backwards)
    viterbiPath = observations
    # Pick most probable state for final observation
    viterbiPath[nObservations-1] = states[np.argmax(v[nObservations-1,:],axis=0)]

    # Probabilistic method will give probability of each label
    if probabilistic:
        viterbiProba = np.zeros((nObservations,nStates)) # initialize table
        viterbiProba[nObservations-1,:] = norm(v[nObservations-1,:])

    # And then work backwards to pick most probable state for all other observations
    for k in list(reversed(range(0,nObservations-1))):
        viterbiPath[k] = states[np.argmax(v[k,:] + np.log(transitions[:,states.index(viterbiPath[k+1])]+tinyNum),axis=0)]
        if probabilistic:
            viterbiProba[k,:] = norm(v[k,:] + np.log(transitions[:,states.index(viterbiPath[k+1])]+tinyNum))

    # Output as list...
    return viterbiProba if probabilistic else viterbiPath
### continuous HMM
def getFileFromTar(tarArchive, targetFile):
    """Read file from tar
    This is currently more tricky than it should be see
    https://github.com/numpy/numpy/issues/7989
    :param str tarArchive: Input tarfile object
    :param str targetFile: Target individual file within .tar
    :return: file object byte stream
    :rtype: object
    """
    t = tarfile.open(tarArchive, 'r')
    array_file = BytesIO()
    array_file.write(t.extractfile(targetFile).read())
    array_file.seek(0)
    return array_file
def viterbi(observations, states, priors, transitions, emissions,
            probabilistic=False):
    """Perform HMM smoothing over observations via Viteri algorithm
    :param list(str) observations: List/sequence of activity states
    :param numpy.array states: List of unique activity state labels
    :param numpy.array priors: Prior probabilities for each activity state
    :param numpy.array transitions: Probability matrix of transitioning from one
        activity state to another
    :param numpy.array emissions: Probability matrix of RF prediction being true
    :param bool probabilistic: Write probabilistic output for each state, rather
        than writing most likely state for any given prediction.
    :return: Smoothed list/sequence of activity states
    :rtype: list(str)
    """

    def norm(x):
        return x / x.sum()

    tinyNum = 0.000001
    nObservations = len(observations)
    nStates = len(states)
    v = np.zeros((nObservations,nStates)) # initialise viterbi table
    # Set prior state values for first observation...
    for state in range(0, len(states)):
        v[0,state] = np.log(priors[state] * emissions[state,states.index(observations[0])]+tinyNum)
    # Fill in remaning matrix observations
    # Use log space as multiplying successively smaller p values)
    for k in range(1,nObservations):
        for state in range(0, len(states)):
            v[k,state] = np.log(emissions[state,states.index(observations[k])]+tinyNum) + \
                        np.max(v[k-1,:] + np.log(transitions[:,state]+tinyNum), axis=0)

    # Now construct viterbiPath (propagating backwards)
    viterbiPath = observations
    # Pick most probable state for final observation
    viterbiPath[nObservations-1] = states[np.argmax(v[nObservations-1,:],axis=0)]

    # Probabilistic method will give probability of each label
    if probabilistic:
        viterbiProba = np.zeros((nObservations,nStates)) # initialize table
        viterbiProba[nObservations-1,:] = norm(v[nObservations-1,:])

    # And then work backwards to pick most probable state for all other observations
    for k in list(reversed(range(0,nObservations-1))):
        viterbiPath[k] = states[np.argmax(v[k,:] + np.log(transitions[:,states.index(viterbiPath[k+1])]+tinyNum),axis=0)]
        if probabilistic:
            viterbiProba[k,:] = norm(v[k,:] + np.log(transitions[:,states.index(viterbiPath[k+1])]+tinyNum))

    # Output as list...
    return viterbiProba if probabilistic else viterbiPath
# activityModel="/u/project/sriram/haroldzw/WQE/biobankAccelerometerAnalysis/activityModels/walmsley-jan21.tar"
# priors = np.load(getFileFromTar(activityModel, 'hmmPriors.npy'))
# transitions = np.load(getFileFromTar(activityModel, 'hmmTransitions.npy')) #rowwise sum is one
# emissions = np.load(getFileFromTar(activityModel, 'hmmEmissions.npy')) #rowwise sum is one
# emis=np.array([[1-sum(emissions[0:3,3]),sum(emissions[0:3,3])],[1-emissions[3,3],emissions[3,3]]])
# trans=np.array([[1-sum(transitions[0:3,3]),sum(transitions[0:3,3])],[1-transitions[3,3],transitions[3,3]]])
# prior=np.array([sum(priors[0:3]),priors[3]])
import pickle
with open("hmmbeta.obj", "rb") as input_file:
   para = pickle.load(input_file)
trans,prior,asleep,bsleep,awake,bwake,emis=para

if __name__ == "__main__":
   V=np.array(list('xyxyyxyxyyyyxxxxxxxyyyyyyyy'))
   print(viterbi(V,['x',"y"], prior,trans,emis))
# a=np.array([[0.641,0.359],[0.729,0.271],])
# print(a)
# Emission Probabilities
# b = np.array(((1, 3, 5), (2, 4, 6)))
# b = b / np.sum(b, axis=1).reshape((-1, 1))
# b=np.array([[0.117,0.691,0.192],[0.097,0.42,0.483]])
# print(b)
# data = pd.read_csv('data_python.csv')
 
# V = data['Visible'].values
# V=np.array(list('xyxyyxyxyyyyxxxxxxxyyyyyyyy'))

# Equal Probabilities for the initial distribution
# initial_distribution = np.array((0.5, 0.5))
# print(viterbi(V,['x',"y"], prior,trans,emis))