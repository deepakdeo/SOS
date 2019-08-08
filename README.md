# SOS: SKA Observation Simulator

SOS contains

1. make_img.py : It makes a toy-model radio sky based on the inputs provided.
	
2. make_vis_ska.py : It simulates noise-free SKA visibility, depends on the SKA configuration file you provide.

3. ska_mid.cfg : configuration file containing antenna details of SKA1_Mid. List of 133 antennas (including MeerKAT).

4. ska_mid133.cfg : configuration file containing antenna details of SKA1_Mid. List of 133 antennas (excluding MeerKAT).

5. ska_uv.png : sample uv coverage of SKA (15-min observation) for the inputs used in make_vis_ska.py file.

*SOS works in CASA 4.7.2 or earlier.*
--------------------------------------

Authors of SOS:
----------------

Deepak Deo and Dr. Ruta Kale

