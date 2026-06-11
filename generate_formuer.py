import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# --- 1. Opsætning af parametre ---
total_personer = 50000
andel_kvinder = 0.52
andel_mænd = 0.48
loft_formue = 50000000  # 50 mio. kr.

# Beregn det præcise antal
antal_kvinder = int(total_personer * andel_kvinder)  # 26.000
antal_mænd = int(total_personer * andel_mænd)        # 24.000

# Vores tidligere beregnede parametre (Aldersgruppe 65-69 år)
mu_mænd, sigma_mænd = 13.0380, 1.1575
mu_kvinder, sigma_kvinder = 13.2723, 0.9812

# --- 2. Funktion til trunkeret lognormalfordeling ---
def generer_trunkeret_lognormal(antal, mu, sigma, max_værdi):
    """
    Genererer lognormalfordelte værdier og kasserer alt over max_værdi,
    indtil vi har det præcise 'antal' vi beder om.
    """
    godkendte_værdier = []
    
    # Kør indtil vi har nok godkendte værdier
    while len(godkendte_værdier) < antal:
        # Træk en portion (vi trækker lidt ekstra for at dække dem der kasseres)
        batch = np.random.lognormal(mean=mu, sigma=sigma, size=antal)
        
        # Filtrer dem der er under eller lig med vores loft
        gyldige = batch[batch <= max_værdi]
        
        # Tilføj til vores liste
        godkendte_værdier.extend(gyldige)
        
    # Returner præcis det antal vi bad om
    return np.array(godkendte_værdier[:antal])

# --- 3. Generer portføljen ---
# Mænd
formuer_mænd = generer_trunkeret_lognormal(antal_mænd, mu_mænd, sigma_mænd, loft_formue)
df_mænd = pd.DataFrame({
    'Køn': 'Mand',
    'Formue': formuer_mænd
})

# Kvinder
formuer_kvinder = generer_trunkeret_lognormal(antal_kvinder, mu_kvinder, sigma_kvinder, loft_formue)
df_kvinder = pd.DataFrame({
    'Køn': 'Kvinde',
    'Formue': formuer_kvinder
})

# Saml til én samlet portfølje
df_portfølje = pd.concat([df_mænd, df_kvinder], ignore_index=True)

# Bland rækkerne tilfældigt (valgfrit, men gør det mere realistisk)
df_portfølje = df_portfølje.sample(frac=1).reset_index(drop=True)

# Afrund formuerne til hele kroner
df_portfølje['Formue'] = df_portfølje['Formue'].round(0).astype(int)

# --- 4. Tjek resultatet ---
print("--- Simulering fuldført ---")
print(f"Total antal i portfølje: {len(df_portfølje):,}".replace(',', '.'))
print(f"Højeste formue i portføljen: {df_portfølje['Formue'].max():,} kr.".replace(',', '.'))
print("\nOversigt over fordelingen:")
print(df_portfølje.groupby('Køn')['Formue'].describe().map(lambda x: f"{x:,.0f}".replace(',', '.')))

df_portfølje.to_csv('pensionsportfoelje.csv', index=False, sep=';')
