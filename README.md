# 🚀 Adaptive Apriori Algorithm

An optimized implementation of the **Apriori Algorithm** that automatically adapts the **Minimum Support (MinSup)** according to the dataset characteristics, reducing computational cost while preserving high-quality association rules.

Instead of relying on a manually selected support threshold, this project computes a dynamic MinSup based on the average transaction density, making the algorithm more efficient and easier to apply on different datasets.

---

## 📌 Overview

Association Rule Mining is widely used to discover relationships between items in transactional datasets. The classical Apriori algorithm requires manually choosing a minimum support threshold, which often leads to either:

* Too many irrelevant patterns (low MinSup)
* Missing important associations (high MinSup)

This project introduces an adaptive approach where **MinSup is automatically calculated** from the dataset before the mining process begins.

The implementation was evaluated using a **lung cancer dataset** containing patient symptoms and diagnoses.

---

## ✨ Features

* ✅ Classical Apriori implementation
* ✅ Adaptive Minimum Support calculation
* ✅ Automatic candidate pruning
* ✅ Association Rule generation
* ✅ Rule evaluation using Support, Confidence and Lift
* ✅ Performance comparison between both approaches
* ✅ Result visualization with Matplotlib

---

# 📊 Dataset

* **Dataset:** Lung Cancer Dataset
* **Transactions:** 276
* **Attributes:** 16
* **Unique Items:** 34

---

# ⚙️ Adaptive MinSup

Instead of using a fixed support threshold, the algorithm computes:

MinSup = Average Transaction Length / Number of Unique Items

The computed value is then bounded between **0.05** and **0.30** to avoid extreme thresholds.

For this dataset:

* Average transaction length: **16**
* Unique items: **34**
* Computed MinSup: **0.471**
* Final adaptive MinSup: **0.30**

---

# 📈 Performance Comparison

| Metric             | Classical Apriori | Adaptive Apriori |      Improvement |
| ------------------ | ----------------: | ---------------: | ---------------: |
| Tested Candidates  |              3048 |              807 |       **-73.5%** |
| Frequent Patterns  |              1172 |              225 |       **-80.8%** |
| Association Rules  |              2856 |              261 |       **-90.9%** |
| Average Support    |             0.240 |            0.349 |       **+45.4%** |
| Average Confidence |             0.746 |            0.735 |            -1.4% |
| Average Lift       |             1.389 |            1.274 |            -8.3% |
| Execution Time     |           1.837 s |          0.196 s | **89.3% faster** |

---

# 🏆 Results

The adaptive approach successfully:

* Reduced candidate generation by **73.5%**
* Reduced frequent patterns by **80.8%**
* Reduced generated rules by **90.9%**
* Increased the average support of discovered rules
* Achieved an **89.3% reduction in execution time**

These improvements demonstrate that automatically adapting the support threshold can significantly reduce computational complexity while preserving meaningful association rules.

---

# 📋 Example Rule

One of the strongest discovered rules is:

**Anxiety = Yes** AND **Lung Cancer = Yes**
➡️ **Difficulty Swallowing = Yes** AND **Yellow Fingers = Yes**

* **Support:** 0.304
* **Confidence:** 0.672
* **Lift:** 1.912

---

# 🛠 Technologies Used

* Python
* Pandas
* NumPy
* Matplotlib
* Itertools


---

# 🚀 Future Improvements

* Adaptive Minimum Confidence
* FP-Growth comparison
* Parallel candidate generation
* Interactive dashboard
* Benchmark on larger datasets
