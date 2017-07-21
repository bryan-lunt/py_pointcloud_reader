from . import read_vpc

import numpy as _np

from itertools import groupby as _groupby,izip as _izip, count as _count
from collections import OrderedDict as _OD


class PointCloud_Cohort(object):
	def __init__(self,name,time,colnames,data,embryospergene=None):
		self.name = name
		self.time = time
		self.column_names = colnames
		self.column_index = _OD(_izip(colnames,_count()))
		self.pos = None
		self.Npos = None
		self.pos_other = dict()
		if "x" in self.column_index and "y" in self.column_index and "z" in self.column_index:
			self.pos = _np.vstack([data[:,self.column_index[j]] for j in ["x","y","z"]]).T
		if "Nx" in self.column_index and "Ny" in self.column_index and "Nz" in self.column_index:
			self.Npos = _np.vstack([data[:,self.column_index[j]] for j in ["Nx","Ny","Nz"]]).T
		self.data = data
		self.embryospergene = embryospergene
	

class PointCloud(object):
	def __init__(self):
		self.cohorts = list()
		self.all_headers = None
		self.all_data = None

	def load_vpc(self,source):
		#TODO: handle file-like, filename, and an alraedy read dataset.
		cohort_colnames = [[j.rsplit("__",1)[0] for j in i[1]] for i in _groupby(source[0]["column"][1:],lambda x:int(x.split("__")[-1]))]
		n_cols_per_cohort = [len(i) for i in cohort_colnames]
		split_columns = _np.split(source[1],_np.cumsum(n_cols_per_cohort[:-1]),axis=1)
		for i in range(len(source[0]["cohort_names"])):
			self.cohorts.append(PointCloud_Cohort(
				source[0]["cohort_names"][i],
				source[0]["cohort_times"][i],
				cohort_colnames[i],
				split_columns[i],
				source[0]["embryospergene"][i]))

		self.all_headers = source[0]
		self.all_data = source[1]
