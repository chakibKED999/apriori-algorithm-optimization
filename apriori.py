import pandas as pd
import numpy as np
from itertools import combinations
import time
import matplotlib.pyplot as plt


INPUT_CSV = "cancer_poumon.csv"  
MINCONF = 0.60
MINLIFT = 1.10
MINSUP_CLASSIC = 0.20


df = pd.read_csv(INPUT_CSV)

transactions = []
for _, row in df.iterrows():
    transaction = []
    for col, val in row.items():
        transaction.append(f"{col}={val}")
    transactions.append(transaction)

n = len(transactions)
all_items = sorted(set(item for t in transactions for item in t))

print("=" * 60)
print("APRlORI CLASSIQUE VS APRIORI AMELIORE")
print("=" * 60)
print(f"Transactions : {n}")
print(f"Items uniques : {len(all_items)}")



def get_support(itemset):
    itemset = set(itemset)
    count = sum(1 for t in transactions if itemset.issubset(set(t)))
    return count / n



def compute_dynamic_minsup():
    lengths = [len(t) for t in transactions]
    avg_len = np.mean(lengths)
    unique_items = len(all_items)

    
    minsup = avg_len / unique_items

    minsup = min(max(minsup, 0.05), 0.30)
    return minsup



def apriori(minsup):
    frequent_itemsets = []
    tested_candidates = 0

    L = []
    for item in all_items:
        tested_candidates += 1
        s = get_support([item])
        if s >= minsup:
            L.append((tuple([item]), s))
    frequent_itemsets.extend(L)

    k = 2
    while L:
        prev_itemsets = [tuple(sorted(itemset)) for itemset, _ in L]
        prev_itemsets_set = set(prev_itemsets)

        candidates = set()
        for i in range(len(prev_itemsets)):
            for j in range(i + 1, len(prev_itemsets)):
                union = tuple(sorted(set(prev_itemsets[i]) | set(prev_itemsets[j])))
                if len(union) == k:
                    all_subsets_frequent = True
                    for subset in combinations(union, k - 1):
                        if tuple(sorted(subset)) not in prev_itemsets_set:
                            all_subsets_frequent = False
                            break
                    if all_subsets_frequent:
                        candidates.add(union)

        L = []
        for c in sorted(candidates):
            tested_candidates += 1
            s = get_support(c)
            if s >= minsup:
                L.append((c, s))

        frequent_itemsets.extend(L)
        k += 1

    return frequent_itemsets, tested_candidates



def generate_rules(freq_itemsets, minconf):
    rules = []

    for itemset, sup_ab in freq_itemsets:
        if len(itemset) < 2:
            continue

        for i in range(1, len(itemset)):
            for A in combinations(itemset, i):
                B = tuple(sorted(set(itemset) - set(A)))

                sup_a = get_support(A)
                sup_b = get_support(B)

                if sup_a == 0 or sup_b == 0:
                    continue

                conf = sup_ab / sup_a
                lift = conf / sup_b

                if conf >= minconf and lift >= MINLIFT:
                    rules.append((A, B, sup_ab, conf, lift))

    return sorted(rules, key=lambda x: x[4], reverse=True)



minsup_dynamic = compute_dynamic_minsup()

print("\nPARAMETRES")
print("-" * 60)
print(f"Apriori classique  : minsup = {MINSUP_CLASSIC:.3f}, minconf = {MINCONF:.2f}")
print(f"Apriori ameliore   : minsup = {minsup_dynamic:.3f}, minconf = {MINCONF:.2f}")
print("Amelioration visible : le support minimum devient automatique.\n")

start = time.time()
freq_classic, cand_classic = apriori(MINSUP_CLASSIC)
rules_classic = generate_rules(freq_classic, MINCONF)
time_classic = time.time() - start

start = time.time()
freq_improved, cand_improved = apriori(minsup_dynamic)
rules_improved = generate_rules(freq_improved, MINCONF)
time_improved = time.time() - start

print("RESULTATS")
print("-" * 60)
print(f"{'Métrique':<25} {'Classique':<15} {'Amélioré':<15}")
print("-" * 60)
print(f"{'Candidates testés':<25} {cand_classic:<15} {cand_improved:<15}")
print(f"{'Patterns fréquents':<25} {len(freq_classic):<15} {len(freq_improved):<15}")
print(f"{'Règles finales':<25} {len(rules_classic):<15} {len(rules_improved):<15}")
print(f"{'Temps (s)':<25} {time_classic:<15.4f} {time_improved:<15.4f}")

if time_classic > 0:
    gain = ((time_classic - time_improved) / time_classic) * 100
    print(f"{'Gain de temps':<25} {'-':<15} {gain:.2f}%")

print("\nTOP 10 REGLES AMELIOREES")
print("-" * 60)
for A, B, sup, conf, lift in rules_improved[:10]:
    print(f"{A} ==> {B}")
    print(f"support={sup:.3f} | confiance={conf:.3f} | lift={lift:.3f}")
    print("-" * 60)



labels = ["Candidates", "Patterns", "Règles"]
classic_values = [cand_classic, len(freq_classic), len(rules_classic)]
improved_values = [cand_improved, len(freq_improved), len(rules_improved)]

x = np.arange(len(labels))
width = 0.35

plt.figure(figsize=(8, 5))
plt.bar(x - width/2, classic_values, width, label="Classique")
plt.bar(x + width/2, improved_values, width, label="Amélioré")
plt.xticks(x, labels)
plt.title("Comparaison Apriori classique vs amélioré")
plt.legend()
plt.tight_layout()
plt.show()
