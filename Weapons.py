import pandas as pd
import random


simple_weapons = pd.read_excel("Weapons/Light Weapons.xlsx", sheet_name= "Planilha1",index_col= 0)
martial_weapons = pd.read_excel("Weapons/Light Weapons.xlsx",sheet_name="Planilha2",index_col=0)
exotic_weapons = pd.read_excel("Weapons/Light Weapons.xlsx", sheet_name= "Planilha3",index_col= 0)

weapons_all= pd.concat([simple_weapons,martial_weapons,exotic_weapons])
a = weapons_all.loc['Gauntlet']
print(a["Reach"])