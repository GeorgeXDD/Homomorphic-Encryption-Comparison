import random
import time
import psutil
import tenseal as ts

# Cheon-Kim-Kim-Song(CKKS)
# using the same initial steps as in the paillier.py file
def get_memory_usage():
    process = psutil.Process()
    return process.memory_info().rss / (1024 ** 2)

def generate_votes(seed=42, num_voters=1000, num_candidates=5):
    random.seed(seed)
    votes = []
    for _ in range(num_voters):
        vote = [0] * num_candidates
        selected_candidate = random.randint(0, num_candidates - 1)
        vote[selected_candidate] = 1
        votes.append(vote)
    return votes

overall_start_time = time.time()
overall_start_memory = get_memory_usage()

num_voters = 1000
num_candidates = 5
votes = generate_votes()
print("Votes generated")

# here i created the tenseal context for the CKKS scheme, we set the polynomial modulus degree to 8192 and 
# the coefficient modulus bit sizes to [60, 40, 40, 60], while using a global scale of 2^40 to avoid scaling issues.
context = ts.context(ts.SCHEME_TYPE.CKKS, poly_modulus_degree=8192, coeff_mod_bit_sizes=[60, 40, 40, 60])
context.global_scale = 2**40
context.generate_galois_keys()
print("TenSEAL context created")

# encrypt votes
encrypted_votes = [ts.ckks_vector(context, vote) for vote in votes]
print("Encrypted votes generated")

# make the homomorphic addition
encrypted_tally = encrypted_votes[0]
for row in encrypted_votes[1:]:
    encrypted_tally += row 
print("Encrypted tally calculated")

# decrypt the final tally
decrypted_tally = encrypted_tally.decrypt()

# since CKKS works with real/complex numbers we also need to round the values to avoid floating-point errors
rounded_tally = [round(x) for x in decrypted_tally]
print("Decrypted tally: ", rounded_tally)

# verify data correctness by comparing plaintext tally with decrypted tally
plaintext_tally = [sum(row[col] for row in votes) for col in range(num_candidates)]
print("Plaintext tally: ", plaintext_tally)

assert rounded_tally == plaintext_tally, "Decryption mismatch"
print("Decryption verified: Decrypted tally matches plaintext tally")

# end tracking for time and memory
overall_end_time = time.time()
overall_end_memory = get_memory_usage()

# display the time and memory usage
print(f"Overall execution time: {overall_end_time - overall_start_time:.4f} seconds.")
print(f"Overall memory used: {overall_end_memory - overall_start_memory:.2f} MB.")
