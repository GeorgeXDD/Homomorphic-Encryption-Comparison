# Homomorphic Encryption Algorithm Comparison

## Project Overview
This repository contains a comparative analysis of three homomorphic encryption algorithms—Paillier, CKKS, and BFV—through a secure voting scenario. The project evaluates the performance of these algorithms based on execution time, memory usage, scalability, and data correctness.

### Homomorphic Encryption
Homomorphic encryption is a cryptographic technique that allows computations on encrypted data without requiring decryption. This ensures data privacy and security, particularly in applications like secure cloud computations, healthcare, and finance.

## Algorithms Compared
1. **Paillier** (Partially Homomorphic Encryption - PHE)
   - Supports only additive operations.
   - Suitable for applications with limited computational needs.
   - Minimal memory usage but high execution times.

2. **CKKS** (Fully Homomorphic Encryption - FHE)
   - Supports approximate arithmetic on real/complex numbers.
   - Best execution time with moderate memory usage.
   - Ideal for high-performance applications needing approximate results.

3. **BFV** (Fully Homomorphic Encryption - FHE)
   - Supports exact arithmetic on integers.
   - Low execution time but higher memory usage.
   - Provides precise results without approximation errors.

## Methodology
The algorithms were evaluated through a secure voting scenario where encrypted votes were aggregated securely for multiple candidates. The system simulated voting for 200 citizens and extended scalability tests to 1000 citizens.

### Performance Metrics
- **Execution Time:** Time taken for encryption, computation, and decryption.
- **Memory Usage:** Monitored using the `psutil` library.
- **Scalability:** Evaluated by increasing the number of voters.
- **Data Correctness:** Ensured through decryption validation.

## Results Summary
| Algorithm | Execution Time (200 Votes) | Memory Usage (200 Votes) | Execution Time (1000 Votes) | Memory Usage (1000 Votes) |
|-----------|-----------------------------|---------------------------|-----------------------------|---------------------------|
| Paillier  | 11.89s                      | 0.88 MB                   | 68.72s                      | 4.35 MB                   |
| CKKS      | 1.37s                       | 160.82 MB                 | 6.05s                       | 461.69 MB                 |
| BFV       | 1.53s                       | 239.46 MB                 | 6.24s                       | 640.03 MB                 |

## Conclusion
- **Paillier:** Best for low-memory environments but struggles with large datasets.
- **CKKS:** Offers the fastest execution times and is suitable for high-performance scenarios with approximate results.
- **BFV:** Balances execution speed and exactness but demands more memory.

## Getting Started
### Prerequisites
- Python 3.x
- Required libraries:
```bash
pip install LightPHE
pip install TenSEAL
pip install psutil
```

### Running the Tests
1. Clone the repository:
```bash
git clone https://github.com/GeorgeXDD/Homomorphic-Encryption-Comparison.git
```

2. Run the performance tests:
```bash
python BFV.py
python CKKS.py
python Paillier.py
```

### Viewing Results
The results will be displayed in the console for each script, the default value for the votes is 1000 and 5 candidates.

## Acknowledgements
- [LightPHE](https://github.com/serengil/LightPHE)
- [TenSEAL](https://github.com/microsoft/TenSEAL)

