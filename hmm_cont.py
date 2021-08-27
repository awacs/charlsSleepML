import tensorflow as tf
from rftest import gettraining
import numpy as np
import tensorflow_probability as tfp
tfd = tfp.distributions
import pickle
with open("hmmbeta.obj", "rb") as input_file:
   para = pickle.load(input_file)
with open("hourtrans.obj", "rb") as input_file:
   hour_trans = pickle.load(input_file)
def viterbi_cont(observations, params=para):
  # print(para)
  if type(observations) != list:
    observations=observations.tolist()
  n=len(observations)
  observations = [(i* (n-1)+0.5)/n for i in observations]
  # observations = observations.astype('double')
  trans,prior,asleep,bsleep,awake,bwake,emis=para
  asleep=float(asleep)
  awake=float(awake)
  bsleep=float(bsleep)
  bwake=float(bwake)
  initial_distribution = tfd.Categorical(probs=prior.tolist())
  transition_distribution = tfd.Categorical(probs=trans.tolist())
  observation_distribution = tfp.distributions.Beta(concentration1=[awake,asleep], concentration0=[bwake,bsleep])
  model = tfd.HiddenMarkovModel(
    initial_distribution=initial_distribution,
    transition_distribution=transition_distribution,
    observation_distribution=observation_distribution,
    num_steps=len(observations))
  out=model.posterior_mode(observations).numpy()
  return out

def viterbi_time(observations, hour_trans=hour_trans,para=para):
  def get_trans(lst,trans_lst):
    hr=lst.index.hour[:-1]
    time_trans=[trans_lst[x] for x in hr]
    return time_trans
  transh=get_trans(observations,hour_trans)
  stringinput=False
  if type(observations[0])==str:
    observations=(observations=="sleep").astype(int)
    stringinput=True
  if type(observations) != list:
    observations=observations.tolist()
  n=len(observations)
# observations = [(i* (n-1)+0.5)/n for i in observations]
  trans,prior,asleep,bsleep,awake,bwake,emis=para
  initial_distribution = tfd.Categorical(probs=prior.tolist())
  # here be dragons
  # transition_distribution = tfd.Categorical(probs=trans.tolist())
  transition_distribution = tfd.Categorical(probs=transh)
  ###
  observation_distribution = tfd.Categorical(probs=emis.tolist())
  model = tfd.HiddenMarkovModel(
    initial_distribution=initial_distribution,
    transition_distribution=transition_distribution,
    observation_distribution=observation_distribution,
    num_steps=n,time_varying_transition_distribution=True)
  out=model.posterior_mode(observations).numpy()
  if stringinput:
    out=[['nosleep','sleep'][x] for x in out]
  return out
  
  
# if __name__ == "__main__":
  # import pandas as pd
  # id="MATA00-1000796-20210610-170838" # exp "MATA00-1000796-20210610-170838"
  # Xfile="convert_"+id+"-X.csv.gz" 
  # yfile="convert_"+id+"-Y.txt"
  # xtrain,ytrain=gettraining(Xfile,yfile,kick='')
  # Suppose we observe gradually rising temperatures over a week:
  # c=viterbi_time(ytrain)
  # print(c)
