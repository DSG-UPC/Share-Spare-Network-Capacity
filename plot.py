import os
import fnmatch
import pandas as pd
import ipdb
import matplotlib as mpl
from matplotlib import pyplot as plt
import numpy as np
import seaborn as sns

sns.set_style("whitegrid")
sns.set_context("paper")

ticks_size = 16
mpl.rcParams['xtick.labelsize'] = ticks_size 
mpl.rcParams['ytick.labelsize'] = ticks_size
mpl.rcParams['legend.fontsize'] = ticks_size

label_size=18
mpl.rcParams['axes.labelsize'] = label_size
mpl.rcParams['axes.titlesize'] = label_size
plt.rc('legend',**{'fontsize':15})



dirs = ['ipip','baseline','codel', 'sfq', 'tcplp']
#dirs = ['baseline', 'tcplp']
mixed = 'mix'
def getECDF(df):
        df = df.sort_values().value_counts()
        ecdf = df.sort_index().cumsum()*1./df.sum()
        return ecdf

def parseLatencies(target='primary'):
	latencies = {}
	for dir in dirs:
		latencies[dir] = []
		latencies[dir+mixed] = []
		print(os.listdir(dir))
		files = [os.path.join(os.getcwd(),dir,f) for f in os.listdir(dir) if fnmatch.fnmatch(f,'latency*'+target+'.csv')]
		#ipdb.set_trace()
		#print files
		for fil in files:
			#print(fil)
			with open(fil,'r') as f:
				if mixed in str(fil):
					print str(fil)
					latencies[dir+mixed].extend(f.read().split())
				else:
					latencies[dir].extend(f.read().split())	
		# conver to int milliseconds
	for dir in dirs:
		latencies[dir] = [int(lat.split('.')[0])/1000 for lat in latencies[dir]]
		latencies[dir+mixed] = [int(lat.split('.')[0])/1000 for lat in latencies[dir+mixed]]

	return latencies

def parseThroughput(target):
	through = {}
	mix_through = {}
	for dir in dirs:
                mix_through[dir] = {}
                through[dir] = {}
                print(os.listdir(dir))
		files = [os.path.join(os.getcwd(),dir,f) for f in os.listdir(dir) if fnmatch.fnmatch(f,'summary*'+target+'.csv')]
		for fil in files:
			df = pd.read_csv(fil,delimiter=',',names=['duration','requests','bytes'])		
			df['throughput'] = 1.*8*df['bytes']/df['duration']
			if mixed in str(fil):
				mix_through[dir][target] = df.throughput.mean()
			else:
				through[dir]['alone']=df.throughput.mean()
	
	if target == 'primary':
		return pd.DataFrame.from_dict(through), pd.DataFrame.from_dict(mix_through)
	else:
		return pd.DataFrame.from_dict(mix_through)


def plotLatencies(latencies, target):
	df=pd.DataFrame.from_dict(latencies,orient='index').T
	ecdfs = []
	for dir in dirs:
		if target == 'primary':
		#ipdb.set_trace()
			ecdf = getECDF(df[dir].dropna())
			ecdf.name = dir
			ecdfs.append(ecdf)
		ecdf_mixed = getECDF(df[dir+mixed].dropna())
	        ecdf_mixed.name = dir+mixed
		ecdfs.append(ecdf_mixed)
	ecdfs_df = pd.concat(ecdfs,axis=1)
	#for n,i in enumerate(ecdfs_df.columns):
	#	if 'mix' in i:
	#		ecdfs_df.rename(columns={i:i.rsplit('mix',1)},inplace=True)
	ecdfs_df.rename(columns={'baseline':'Single Client'},inplace=True)
	#ipdb.set_trace()
	#ecdfs_df.columns = cols
	#ecdfs_df.columns = [for c in ecdfs_df.columns if c == 'baseline']
	#ecdfs_df.columns = [for c in ecdfs_df.columns if 'mix' in c]
	ecdfs_df1 = ecdfs_df.copy()
	if target == 'secondary':
		for n,i in enumerate(ecdfs_df1.columns):
	               if 'mix' in i:
	                       ecdfs_df1.rename(columns={i:i.rsplit('mix',1)[0]},inplace=True)

		ecdfs_df1.plot(legend=True,logx=True, style='o')
		label = "Latency per Request of %s traffic (ms)" % target
		plt.xlabel(label)
		plt.ylabel('ECDF')
		if target == 'primary':
			plt.xlim(10**2,10**5)
		else: 
			plt.xlim(10**3,10**5)
		plt.show()
	#raw_input('End')
	return ecdfs_df	
	#exit()

prim_latencies = parseLatencies('primary')
prim_ecdfs_df  = plotLatencies(prim_latencies,'primary')
second_latencies = parseLatencies('secondary')
second_ecdfs_df = plotLatencies(second_latencies,'secondary')


prim_ecdfs_df1 = prim_ecdfs_df[['Single Client','baselinemix','codelmix','sfqmix','tcplpmix']].copy()
for n,i in enumerate(prim_ecdfs_df1.columns):
               if 'mix' in i:
                       prim_ecdfs_df1.rename(columns={i:i.rsplit('mix',1)[0]},inplace=True)

prim_ecdfs_df1[['Single Client','baseline','codel','sfq','tcplp']].plot(legend=True, style='o')
plt.xlabel('Latency per Request of primary traffic (ms)')
plt.ylabel('ECDF')
#plt.xlim(10**2,10**5)
plt.xscale('log')
plt.show()
#raw_input('End')
		
# Print single client Configs
#prim_ecdfs_df[['Single Client','ipip','codel','sfq','tcplp']].plot(legend=True, style='o')
#plt.xlabel('Latency per Request (ms)')
#plt.ylabel('ECDF')
#plt.xlim(10**2,10**5)
#plt.xscale('log')
#plt.show()
#raw_input('End')	


alone_through,prim_through = parseThroughput('primary')
second_through = parseThroughput('secondary')
through_df = pd.concat([prim_through,second_through,alone_through])
through_df.loc['alone','ipip'] = np.nan
through_df.loc['alone','tcplp'] = np.nan
#ipdb.set_trace()
#ipdb.set_trace()
through_df.loc[['primary','secondary'],:].plot.bar(rot=0)
plt.axhline(y=through_df.loc['alone':].mean(axis=1).values[0],color='r',label='Single Client Throughput',ls='--')
plt.ylabel('Throughput (Mbps)')
plt.show()
raw_input('End')
