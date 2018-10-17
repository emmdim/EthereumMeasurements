import os
import ipdb

import pandas as pd
import matplotlib as mpl
from matplotlib import pyplot as plt
import numpy as np
import seaborn as sns

##PARAMETERS
EXP_NAME = 'test'
MAX_ROUNDS = 699
MAX_YVAL = 14
# DEFINE OUTPUT DIR
RESULTS_DIR = os.path.join( os.getcwd(),'results')
GRAPHS_DIR = os.path.join( os.getcwd(), 'graphs')

##SET SEABORN STYLE
sns.set_style("whitegrid")
sns.set_context("paper")

##SET MATPLOTLIB STYLE
TICKS_FONTSIZE = 16
LABEL_FONTSIZE=18
LEGEND_FONTSIZE=15

mpl.rcParams['xtick.labelsize'] = TICKS_FONTSIZE
mpl.rcParams['ytick.labelsize'] = TICKS_FONTSIZE
mpl.rcParams['legend.fontsize'] = TICKS_FONTSIZE
mpl.rcParams['axes.labelsize'] = LABEL_FONTSIZE
mpl.rcParams['axes.titlesize'] = LABEL_FONTSIZE
mpl.rcParams['font.size'] = LABEL_FONTSIZE
plt.rc('legend',**{'fontsize':LEGEND_FONTSIZE})


######################### BASIC FUNCTIONS  ###########################
#######################################################################


def read_results():
	"""Reads the results for all the nodes and returns
	a list of pandas Dataframes, one for each node"""
	#Get list of nodes(files) with results
	files = [f for f in os.listdir(RESULTS_DIR) if os.path.isfile(os.path.join(RESULTS_DIR, f))]
	#for x in ['1','10','']
	#files = filter_parallel(files,1,'1000');
	#print(files)
	#Load results from each node
	nodes_results = {}
	for node in files:
		f = os.path.join(RESULTS_DIR,node)
		try:
			#Read csv
			df = pd.read_csv(f,usecols=['start','mindTime','completionTime'])
			df = df.replace('None',np.nan)
			#Create column with seconds
			seconds = node.split('_')[2].split('.')[0]
			values = np.empty(shape=len(df),dtype=int)
			values.fill(int(seconds))
			seconds_df = pd.DataFrame({'second':values})
			df = df.join(seconds_df)
			#Create column with parallel transactions
			parallel = node.split('_')[1]
			values = np.empty(shape=len(df),dtype=int)
			values.fill(int(parallel))
			parallel_df = pd.DataFrame({'parallelTrans':values})
			df = df.join(parallel_df)
			#Write df
			nodes_results[node] = df
			#ipdb.set_trace()
		except Exception, e:
			print e
			ipdb.set_trace()
	final = pd.concat(nodes_results.values(),ignore_index=True)
	ipdb.set_trace()
	return final

def plot_averages(df):
	result = df.groupby(by='parallelTrans').aggregate(np.median)
	result = result[['mindTime','completionTime']]/1000
	result1 = df.groupby(by='parallelTrans').aggregate(np.std)
	result1 = result1[['mindTime','completionTime']]/1000
	ipdb.set_trace()

	#fig = plt.figure()
	#result = result[['mindTime','completionTime']].set_index('')
	#Print the plot
	#result.plot(marker='o', xticks=result.index, logx=True,  yerr=result1)
	result.plot.bar(yerr=result1)
	#Modify parameters
	plt.xlabel('# Parallel Transactions')
	plt.ylabel('Seconds')
	plt.show()
	#plt.xlim(0,MAX_ROUNDS)
	#plt.ylim(0,MAX_YVAL)
	#Dummy line to avoid bug of matplotlib that closes image right after plot
	#It's a readline function, just press enter
	raw_input('Done')
	#You can also automatically save figures
	#fig.savefig(os.path.join(GRAPHS_DIR,var.replace(' ','_')+'_per_round.png'), format='png', dpi=fig.dpi)


############################### HELPERS  ##############################
#######################################################################

def getMedianDF(nodes_results,var):
	""""Helper function that extracts median time series of the var
	accross the various nodes"""
	series = []
	for name,r in nodes_results.iteritems():
		#Normalize duplicate rounds
		r['round'] = r['round'].apply(np.trunc)
		s = r.groupby('round',axis=0).mean()[var]
		s.name = name
		series.append(s)
	try:
		df = pd.concat(series,axis=1)
	except:
		ipdb.set_trace()
	median = df.median(axis=1)
	median.name = var
	return median



def getECDF(df):
	"""Helper function that caclulates the ECDF of a
	dataframe"""
	df = df.sort_values().value_counts()
	ecdf = df.sort_index().cumsum()*1./df.sum()
	return ecdf

def filter_parallel(files,index,value):
	"""Filter which files will be loaded"""
	return filter(lambda x: x.split('_')[index] == value,files)


##########################  MAIN  #######################################
#######################################################################


if __name__ == '__main__':
	df = read_results()
	plot_averages(df)
	#plot_var_ecdf_per_round(nodes_results,'HTTP Error')
	#plot_comparative(nodes_results,['HTTP Error', 'UDP Error'])
