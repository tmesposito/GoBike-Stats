#!/usr/bin/env python3

#import glob
import time
import requests
from datetime import datetime
import numpy as np
import geocoder
import sqlite3
# I'm using table-handling functions from astropy, an astronomy-related module, because I'm
# familiar with it, but there are other options out there (like pandas).
from astropy import table
from astropy.io import ascii


class GoBike:
	
	def __init__(self, epochs):
		"""
		Initialization of the GoBike object.
		
		Inputs:
			epochs: list or array of str with data epoch names matching the
				"<epoch>-fordgobike-tripdata.csv" files to be used.
		"""
		
		self.epochs = epochs
		self.N_epochs = len(epochs) # total number of epochs
		
		self.readdata()
	
	
	###############
	### Methods ###
	###############
	def readdata(self,):
		"""
		Method to read GoBike raw data from publicly available .csv files.
		
		Inputs:
			None
		
		Returns:
			Technically none. It saves data tables to the .tables attribute.
		"""
		
		# Table filenames changed format when program name changed in 05/2019.
		filenames = ['%s-fordgobike-tripdata.csv' % epoch
					 for epoch in self.epochs[self.epochs.astype(int) < 201905]]
		filenames += ['%s-baywheels-tripdata.csv' % epoch
					 for epoch in self.epochs[self.epochs.astype(int) >= 201905]]
		
		# Read the files into handy tables using astropy.io.ascii.
		# Convert the 'NULL' empty entries to -1 for easier handling later.
		# This will take ~10 seconds.
		tables = [ascii.read(fn, Reader=ascii.Basic,
							  delimiter=',', header_start=0, data_start=1,
							  fill_values=[('NULL', -1)]) for fn in filenames]
		
		self.tables = tables
		
		print("Epochs loaded:", self.epochs)
		
		return


def build_db():
	"""
	Build an SQL database from the supplied tables.
	"""
	import csv
	
	data = csv.reader('%s-fordgobike-tripdata.csv' % '201801')
	
	conn = sqlite3.connect("gobike_sql.db")
	
	cursor = conn.cursor()
	
	cursor.execute("""
					CREATE TABLE ep0 (
					duration_sec,
					start_time,
					end_time,
					start_station_id,
					start_station_name,
					start_station_latitude,
					start_station_longitude,
					end_station_id,
					end_station_name,
					end_station_latitude,
					end_station_longitude,
					bike_id,
					user_type,
					member_birth_year,
					member_gender,
					bike_share_for_all_trip
					""")
	
	
	
	return
