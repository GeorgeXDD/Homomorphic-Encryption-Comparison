import random
import time
import psutil
import tenseal as ts

# Brakerski/Fan-Vercauteren(BFV)
# using the same initial steps as in the paillier.py and CKKS.py file
def get_memory_usage():
    process = psutil.Process()
    return process.memory_info().rss / (1024 ** 2)


overall_start_time = time.time()
overall_start_memory = get_memory_usage()


poly_modulus_degree = 8192 
plain_modulus = 786433  # prime number congruent to 1 mod 2*8192 => 786433 mod 16384=1
context = ts.context(ts.SCHEME_TYPE.BFV, poly_modulus_degree, plain_modulus)
context.generate_galois_keys()  # required for homomorphic operations
print("BFV context created.")

num_voters = 1000
num_candidates = 5

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

# encrypt votes using BFV with batching
encrypted_votes = [ts.bfv_vector(context, vote) for vote in votes]
print("Encrypted votes generated.")

# make the homomorphic addition
encrypted_tally = encrypted_votes[0]
for row in range(1, num_voters):
    encrypted_tally += encrypted_votes[row]
print("Encrypted tally calculated.")

# decrypt the final tally
decrypted_tally = encrypted_tally.decrypt()
print("Decrypted tally:", decrypted_tally[:num_candidates])

# verify data correctness by comparing plaintext tally with decrypted tally
# (here we don't need to round since we work with integers)
plaintext_tally = [sum(row[col] for row in votes) for col in range(num_candidates)]
print("Plaintext tally:", plaintext_tally)

assert decrypted_tally[:num_candidates] == plaintext_tally, "Decryption mismatch!"
print("Decryption verified: Decrypted tally matches plaintext tally.")

# end tracking for time and memory
overall_end_time = time.time()
overall_end_memory = get_memory_usage()

# display the time and memory usage
print(f"Overall execution time: {overall_end_time - overall_start_time:.4f} seconds.")
print(f"Overall memory used: {overall_end_memory - overall_start_memory:.2f} MB.")
