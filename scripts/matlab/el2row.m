function row = el2row(el)
%converts the electrode number on 32-ch NeuroNexus array (HC32 connector; el = 1 at the tip, el = 32 at the base)
%to numering of rows in Matlab after data are read in using
%read_Intan_RHS2000
%
%assumes that the 1710 amplifier is connected to the connector on the right
%(when electrodes are facing in the upper direction), and that 1710 is the
%B channel

%       tip (el 1)                                                                           base (el 32)
rows = [20 5 19 6 18 7 32 9 31 10 30 11 21 4 22 3 23 2 25 16 26 15 27 14 28 13 24 1 29 12 17 8];

row = rows(el);