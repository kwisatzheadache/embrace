Binary Activity Classification

Objective: 
	Write a program that classifies time series signals as walking, standing, or sitting 
	using a binary classification scheme. That is, for each of the activities walking, 
	standing, and sitting, develop a classifier that labels a time series input as poitive 
	(activity match) or negative (activity mismatch) 

Input:
	stand_sit.csv contains data from standing and siting activities. The data file starts in 
		a sitting position and then repeats between standing and sitting states. The 
		datafiles are [Nx10] csv files in order accel_x, accel_y, accel_z, gy_x, gy_y, gy_z, 
		mag_x, mag_y, magnetometerag_z. Units: acceleration = m/s^2, gyroscope = deg/s, 
		magnetometer = gauss

	walking*.csv contains data from a walking sequence. Same input format as stand_sit.csv

	random_seq.csv contains a data sequence containing standing, sitting, and walking
		activities. 


Output:
	The location of windows of size n (where you determine the window size) in the input 
	signal that are identified as a specific acticity. Only windows that are positively 
	identified by their classifier and negatively identified by the remaining two classifiers 
	should be counted as a successful classification.

Hints: do not stress over algorithmic performace - this is meant as an exercise to make you 
familar with our data and for us to get a chance to evaluate your code. Signal magnitude and 
variance are two common features used in these classification problems, but we have also seen 
some interesting results using frequency data obtained from the fouier transform. You are 
encouraged to create a number of feature profiles to use with your classifier. Good luck :D