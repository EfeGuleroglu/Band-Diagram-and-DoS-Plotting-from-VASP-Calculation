# Last update: 29.03.2024
#
# This code takes BAND.dat, KLABELS, OUTCAR as input files.
# You need of specify the directories of those files in the very first lines of this code.
# Fermi energy is printed and written in the title of the plot(s). 
# You can choose to set the Fermi Energy to zero on the y-axis.
# You can choose how much around Fermi Energy will be plotted.
# If there are discontinuities at the high-symmetry points, several plots will be created and saved as .pdf
# Energy values are limited as [fermi_energy-1,fermi_energy+1]

import numpy as np
import matplotlib.pyplot as plt

# Read the data from the files
KLABELS = "KLABELS"
BAND = "BAND.dat"
OUTCAR = "OUTCAR"
TITLE_OF_PLOT = ""
set_fermi_energy_to_zero = True

# Set how much eV around Fermi Energy will be shown
afe = 3

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

# Initialize empty lists to store labels and values
labels = []
values = []

# Open the file and parse the data
with open(KLABELS, 'r') as file:
    for line in file:
        if line.strip():  # Check if the line is not empty
            parts = line.split()  # Split the line into parts
            if len(parts) == 2:  # Check if it has two parts
                labels.append(parts[0])  # First part is label
                values.append(float(parts[1]))  # Second part is value, converted to float

# Convert lists to numpy array
klabels = np.array([labels, values]).T

# Get data from BAND.dat (kpoints,spin-up(eV),spin-down(eV))
bands = np.loadtxt(BAND)

# Initialize an empty list to store values corresponding to labels containing "|"
values_with_pipe = []

# Find values corresponding to labels containing "|"
for label, value in zip(labels, values):
    if "|" in label:
        values_with_pipe.append(value)

# Discontinuous points
dcp = values_with_pipe

title = TITLE_OF_PLOT+" (Fermi Energy = "+str(round(fermi_energy,2))+" eV)"

fe = ''
if set_fermi_energy_to_zero:
    fermi_energy = 0
    fe = ' - Fermi Energy '

# By default, Fermi Energy is set to zero, shift it
k_points = bands[:,0]
spin_up = bands[:,1] + fermi_energy
spin_down = bands[:,2] + fermi_energy

if len(dcp) == 0:

    plt.plot(k_points,spin_up,color='blue',label="spin up")
    plt.plot(k_points,spin_down,color='green',label="spin down")
    for xv in values:
        plt.axvline(x=xv,linestyle="dashed",color="grey",linewidth=0.5,alpha=0.5)

    plt.axhline(y=fermi_energy,linestyle="dashed",color="grey",linewidth=0.5,alpha=0.5)
    
    # Extract labels and values from the result_array
    labels = klabels[:, 0]
    values = klabels[:, 1]
    
    # Convert the values to floats
    values = values.astype(float)
    
    # Set the x-axis ticks to the labels
    plt.xticks(values)
    
    # Replace "GAMMA" with the Unicode representation of the Greek letter gamma (γ)
    labels = [label.replace("GAMMA", "Γ") for label in labels]
    
    # Label the x-axis ticks with the corresponding labels
    plt.gca().set_xticklabels(labels)
    plt.ylim([fermi_energy-afe,fermi_energy+afe])
    plt.xlabel("Wave number")
    plt.ylabel("Energy"+fe+"(eV)")
    plt.title(title)
    plt.legend(loc="upper right")
    figpdf = 'fig_'+str(i)+'.pdf'
    plt.savefig(figpdf,format='pdf')

else:
    for i in range(len(dcp)+1):
        plt.figure()
        plt.plot(k_points,spin_up,color='blue',label="spin up")
        plt.plot(k_points,spin_down,color='green',label="spin down")
        for xv in values:
            plt.axvline(x=xv,linestyle="dashed",color="grey",linewidth=0.5,alpha=0.5)

        plt.axhline(y=fermi_energy,linestyle="dashed",color="grey",linewidth=0.5,alpha=0.5)
        
        # Extract labels and values from the result_array
        labels = klabels[:, 0]
        values = klabels[:, 1]
        
        # Convert the values to floats
        values = values.astype(float)
        
        # Set the x-axis ticks to the labels
        plt.xticks(values)
        
        # Replace "GAMMA" with the Unicode representation of the Greek letter gamma (γ)
        labels = [label.replace("GAMMA", "Γ") for label in labels]
        
        # Label the x-axis ticks with the corresponding labels
        plt.gca().set_xticklabels(labels)
        if i == 0:
            plt.xlim([values[0],dcp[0]])
        elif i<len(dcp):
            plt.xlim([dcp[i-1],dcp[i]])
        else:
            plt.xlim([dcp[-1],values[-1]])
        plt.ylim([fermi_energy-afe,fermi_energy+afe])
        plt.xlabel("Wave number")
        plt.ylabel("Energy"+fe+"(eV)")
        plt.title(title)
        plt.legend(loc="upper right")
        figpdf = 'fig_'+str(i)+'.pdf'
        plt.savefig(figpdf,format='pdf')

plt.show()