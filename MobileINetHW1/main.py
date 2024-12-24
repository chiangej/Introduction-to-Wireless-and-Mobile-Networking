import numpy as np
import matplotlib.pyplot as plt

k = 1.38e-23

T = 273 + 27
BandWidth = 10e6
Pt_dbm = 33
G_trans = 14
G_rec = 14
h_base = 1.5 + 50
h_device = 1.5
sigma = 6

Pt = 10**((Pt_dbm - 30)/10)
Gt = 10**(G_trans/10)
Gr = 10**(G_rec/10)

N = k*T*BandWidth
I = 0


distance = np.linspace(10, 5000, 500)

def received_power_two_ray( d ):
    return Pt*Gr*Gt*(h_device*h_base) **2/ (d ** 4)

Pr = received_power_two_ray( distance )
Pr_db = 10 * np.log10(Pr)

SINR_cal = Pr / ( I + N )
SINR = SINR_cal
SINR_db = 10 * np.log10(SINR)


def apply_shadowing(Pr, sigma, size):

    shadowing = np.random.normal(0, sigma, size)
    Pr_shadowed = Pr * 10**(shadowing / 10)
    return Pr_shadowed

# Apply log-normal shadowing
Pr_shadowed = apply_shadowing(Pr, sigma, len(distance))

# Convert received power to dB
Pr_shadowed_db = 10 * np.log10(Pr_shadowed)

SINR2 = Pr_shadowed/ (I + N)
SINR2_db = 10 * np.log10(SINR2)


# Plotting
plt.figure(figsize=(8,6))
plt.plot(distance, Pr_db)
plt.title("Received Power vs Distance (Two-Ray Ground Model)")
plt.xlabel("Distance between BS and Mobile Device (meters)")
plt.ylabel("Received Power (dB)")
plt.grid(True)
plt.show()

# Plotting SINR
plt.figure(figsize=(8,6))
plt.plot(distance, SINR_db)
plt.title("SINR vs Distance (Two-Ray Ground Model)")
plt.xlabel("Distance between BS and Mobile Device (meters)")
plt.ylabel("SINR (dB)")
plt.grid(True)
plt.show()

# Plotting
plt.figure(figsize=(8,6))
plt.plot(distance, Pr_shadowed_db, label='With Shadowing')
plt.title("Received Power vs Distance (With Log-normal Shadowing)")
plt.xlabel("Distance between BS and Mobile Device (meters)")
plt.ylabel("Received Power (dB)")
plt.grid(True)
plt.legend()
plt.show()

# Plotting
plt.figure(figsize=(8,6))
plt.plot(distance, SINR2_db, label='With Shadowing')
plt.title("SINR vs Distance (With Log-normal Shadowing)")
plt.xlabel("Distance between BS and Mobile Device (meters)")
plt.ylabel("SINR_shadowing (dB)")
plt.grid(True)
plt.legend()
plt.show()