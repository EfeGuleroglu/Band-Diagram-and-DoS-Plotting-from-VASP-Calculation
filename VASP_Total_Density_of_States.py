# Last update: 31.03.2024
#
# This code takes TDOS.dat and OUTCAR as input files.
# You need of specify the directories of those files in the very first lines of this code.
# Fermi energy is printed and written in the title of the plot. 
# You can choose to set the Fermi Energy to zero on the y-axis.
# You can choose how much around Fermi Energy will be plotted.
# Plot will be created and saved as .pdf

import numpy as np
import matplotlib.pyplot as plt

# Read the data from the files
TDOS = "TDOS.dat"
OUTCAR = "OUTCAR"
TITLE_OF_PLOT = ""
set_fermi_energy_to_zero = True

# Open the file and search for the Fermi energy line
with open(OUTCAR, 'r') as file:
    for line in file:
        if "Fermi energy:" in line:
            # Extract the energy value from the line
            fermi_energy = float(line.split(":")[-1].strip())
            break  # Exit the loop once the Fermi energy is found

# Check if Fermi energy is found
if fermi_energy is not None:
    print("Fermi energy:", fermi_energy)
else:
    print("Fermi energy not found in the file.")

# Get data from TDOS.dat (Energy(eV),TDOS-UP,TDOS-DOWN)
tdos = np.loadtxt(TDOS)

title = TITLE_OF_PLOT+" (Fermi Energy = "+str(round(fermi_energy,2))+" eV)"

fe = ''
if set_fermi_energy_to_zero:
    fermi_energy = 0
    fe = ' - Fermi Energy '

# By default, Fermi Energy is set to zero, shift it
energy = tdos[:,0]
spin_up = tdos[:,1] + fermi_energy
spin_down = tdos[:,2] + fermi_energy

plt.plot(spin_up,energy,color='blue',label="spin up")
plt.plot(spin_down,energy,color='green',label="spin down")

plt.axhline(y=fermi_energy,linestyle="dashed",color="grey",linewidth=0.5,alpha=0.5)
plt.xlabel("TDOS(states/eV)")
plt.ylabel("Energy"+fe+"(eV)")
plt.title(title)
plt.legend(loc="upper right")
figpdf = 'fig.pdf'
plt.savefig(figpdf,format='pdf')

plt.show()