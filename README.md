# SOS: SKA Observation Simulator

It simulates SKA1_Mid visibility (radio observation) for a given radio sky. Simulator uses python and CASA-toolkit
for simulation. It needs to be run within CASA and at the moment is compatible with CASA version 4.7.2 or earlier.
CASA compatible SKA1_Mid configuration file is provided here which contains coordinates of the telescope that we knew were
part of SKA1_Mid until mid 2017.  

SOS contains
--------------

1. make_img.py : It makes a toy-model radio sky based on the inputs provided.
	
2. SOS.py : It simulates SKA visibility when a radio sky and SKA configuration file is provided.

3. ska_mid.cfg : configuration file containing antenna details of SKA1_Mid. List of 197 antennas (including MeerKAT).

4. ska_mid133.cfg : configuration file containing antenna details of SKA1_Mid. List of 133 antennas (excluding MeerKAT).

5. ska_uv.png : sample uv coverage of SKA (15-min observation) for the inputs used in SOS.py file.

*SOS works in CASA 4.7.2 or earlier.*
--------------------------------------

Using instructions:
-------------------
1) Run the script within CASA via -- execfile('script_name')
2) Make sure SKA configuration file is in the same folder where your SOS script is.

Authors of SOS:
----------------

Deepak Deo and Dr. Ruta Kale

