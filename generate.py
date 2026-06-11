import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import lognorm

# Data from the table for "Livsvarig pension (ekskl. ATP)"
mean_m = 897944
med_m = 459547

mean_w = 940019
med_w = 580881

# Calculations
mu_m = np.log(med_m)
sigma_m = np.sqrt(2 * np.log(mean_m / med_m))

mu_w = np.log(med_w)
sigma_w = np.sqrt(2 * np.log(mean_w / med_w))

print(f"Men - mu: {mu_m:.4f}, sigma: {sigma_m:.4f}")
print(f"Women - mu: {mu_w:.4f}, sigma: {sigma_w:.4f}")

# Plotting
x = np.linspace(1, 4000000, 1000) # Start from 1 to avoid division by zero in log
pdf_m = lognorm.pdf(x, s=sigma_m, scale=np.exp(mu_m))
pdf_w = lognorm.pdf(x, s=sigma_w, scale=np.exp(mu_w))

plt.figure(figsize=(12, 7))
plt.plot(x, pdf_m, label=f'Men ($\mu$={mu_m:.2f}, $\sigma$={sigma_m:.2f})', color='#1f77b4', linewidth=2)
plt.fill_between(x, pdf_m, alpha=0.2, color='#1f77b4')

plt.plot(x, pdf_w, label=f'Women ($\mu$={mu_w:.2f}, $\sigma$={sigma_w:.2f})', color='#ff7f0e', linewidth=2)
plt.fill_between(x, pdf_w, alpha=0.2, color='#ff7f0e')

# Medians and Means
plt.axvline(med_m, color='#1f77b4', linestyle='--', alpha=0.8, label=f'Median Men: {med_m:,} kr.')
plt.axvline(mean_m, color='#1f77b4', linestyle=':', alpha=0.8, label=f'Mean Men: {mean_m:,} kr.')

plt.axvline(med_w, color='#ff7f0e', linestyle='--', alpha=0.8, label=f'Median Women: {med_w:,} kr.')
plt.axvline(mean_w, color='#ff7f0e', linestyle=':', alpha=0.8, label=f'Mean Women: {mean_w:,} kr.')

# Formatting
plt.title('Lognormal Distribution of Pension Wealth\n(Livsvarig pension, 65-69 år)', fontsize=14)
plt.xlabel('Pension Wealth (kr.)', fontsize=12)
plt.ylabel('Probability Density', fontsize=12)
plt.legend()
plt.grid(True, alpha=0.3)
plt.ticklabel_format(style='plain', axis='x') # Prevent scientific notation on x-axis
plt.tight_layout()

# Save the figure to your current working directory
plt.savefig("pension_distribution.png")

# DISPLAY THE FIGURE
plt.show()