# Project Κινητός και Διάχυτος Υπολογισμός

Title: ["Broadcasting on-demand data with time constraints using multiple channels in wireless broadcast environments."](https://www.sciencedirect.com/science/article/pii/S0020025513003307?via%3Dihub)
Authors: Chuan-Ming Liu, Ta-Chih Su

In this paper, Liu C. and Su T., suggest two algorithms, "Most Popular Firts Heutistic" (MPFH) and "Most Popular Last Heuristic" (MPLH).
We implemented the first one, MPFH.


## Requirements

Python version 3.x is the default python version to run the program.
It is also possible to execute the code if you have a Python version 2.x but then you have to uncomment the lines 47, 48, 49.

## Testing the code

Input for the programm is the file with name "requests.txt" that is included into the same folder with the "mpfh.py".
All requests are written in file "requests.txt"
Requests should have the following format: ID,deadline,timeArrived,(dataItem1/dataItem2/.../dataItemn),()

The programm prints at each time slot the existing requests and the item or items that selected for broadcasting.
At the end prints the time slot that terminated.

It is necessary not change the name of "requests.txt" file.

It is necessary to follow the specific format as described above if you want to test other requests.

## Example

	Time slot =  1
	Requests:
	Q1 ['d1', 'd2', 'd3']
	Q2 ['d2', 'd3', 'd4', 'd5']
	Q3 ['d4', 'd3']
	bcast_list:  ['d3']
	Time slot =  2
	Requests:
	Q1 ['d1', 'd2']
	Q2 ['d2', 'd4', 'd5']
	Q3 ['d4']
	Q4 ['d3', 'd6']
	bcast_list:  ['d4', 'd2']
	Time slot =  3
	Requests:
	Q1 ['d1']
	Q2 ['d4', 'd5']
	Q4 ['d3', 'd6']
	bcast_list:  ['d3', 'd1']
	Time slot =  4
	Requests:
	Q2 ['d4', 'd5']
	Q4 ['d6']
	bcast_list:  ['d4', 'd6']
	Time slot =  5
	Requests:
	Q2 ['d5']
	bcast_list:  ['d5']
	Program has ended in time slot:  6

