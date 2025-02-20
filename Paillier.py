import random
import time
import psutil
from lightphe import LightPHE

# in order to install the lightphe library I had to clone it and install it manually since pip install lightphe did not work
# git repo: https://github.com/serengil/LightPHE


# measure memory usage
def get_memory_usage():
    process = psutil.Process()
    return process.memory_info().rss / (1024 ** 2)  # here i convert the memory to MB

# start tracking overall time and memory
overall_start_time = time.time()
overall_start_memory = get_memory_usage()

# since lightphe has multiple algorithms, first we must specify which algorithm we want to use
cs = LightPHE(algorithm_name="Paillier")

num_voters = 1000
num_candidates = 5

# simulate random voting with a fiex seed to 42 such that all the other programs have the same votes
def generate_votes(seed=42, num_voters=1000, num_candidates=5):
    random.seed(seed)
    votes = []
    for _ in range(num_voters):
        vote = [0] * num_candidates
        selected_candidate = random.randint(0, num_candidates - 1)
        vote[selected_candidate] = 1
        votes.append(vote)
    return votes



votes = generate_votes()
print("Votes generated")

# encrypt votes using the library function encrypt
encrypted_votes = [list(map(cs.encrypt, vote)) for vote in votes]
print("Encryption completed")

# here we make the homomorphic addition with the encrypted votes column by column
encrypted_tally = []
for col in range(num_candidates):
    column_sum = encrypted_votes[0][col] 
    for row in range(1, len(encrypted_votes)):
        column_sum += encrypted_votes[row][col]
    encrypted_tally.append(column_sum)
print("Encrypted tally calculated")

# decrypt the final tally
decrypted_tally = [cs.decrypt(ct) for ct in encrypted_tally]
print("Decryption tally: ", decrypted_tally)

# verify data correctness by comparing plaintext tally with decrypted tally
plaintext_tally = [sum(row[col] for row in votes) for col in range(num_candidates)]
print("Plaintext tally: ", plaintext_tally)

assert decrypted_tally == plaintext_tally, "Decryption mismatch"
print("Decryption verified: Decrypted tally matches plaintext tally")

# end tracking for time and memory
overall_end_time = time.time()
overall_end_memory = get_memory_usage()

# display the time and memory usage
print(f"Overall execution time: {overall_end_time - overall_start_time:.4f} seconds.")
print(f"Overall memory used: {overall_end_memory - overall_start_memory:.2f} MB.")
