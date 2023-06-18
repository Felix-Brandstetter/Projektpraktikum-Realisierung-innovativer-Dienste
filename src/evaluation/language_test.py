import sys

sys.path.append("/RIDSS2023/src")
import pandas as pd

englisch = pd.read_csv("/RIDSS2023/englisch.tsv", sep='\t')
deutsch = pd.read_csv("/RIDSS2023/deutsch.tsv", sep='\t')
chi_sim = pd.read_csv("/RIDSS2023/chi_sim.tsv", sep='\t')
all = pd.read_csv("/RIDSS2023/all.tsv", sep='\t')
none = pd.read_csv("/RIDSS2023/none.tsv", sep='\t')


average_eng = englisch['conf'].mean()
average_deu = deutsch['conf'].mean()
average_chi_sim = chi_sim['conf'].mean()
average_all = all['conf'].mean()
average_none = none['conf'].mean()


sum_eng = englisch['conf'].sum()
sum_deu = deutsch['conf'].sum()
sum_chi_sim = chi_sim['conf'].sum()
sum_all = all['conf'].sum()
sum_none = none['conf'].sum()

print(average_eng)
print(average_deu)
print(average_chi_sim)
print(average_all)
print(average_none)
print("")

print(sum_eng)
print(sum_deu)
print(sum_chi_sim)
print(sum_all)
print(sum_none)