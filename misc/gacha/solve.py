import threading
import subprocess

# Define the path to the gacha executable
gacha_executable = "./gacha"

# Define the number of threads to use for concurrent pulling
num_threads = 10

# Initialize a list to store the obtained keys and ciphertexts
results = []

def pull_string():
    try:
        # Run the gacha executable and capture its output and exit code
        output, exit_code = subprocess.Popen([gacha_executable], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        output = output.decode("utf-8")

        # Check if the executable encountered an error
        if exit_code != 0:
            raise Exception(f"Error: Executable returned non-zero exit code {exit_code}. Output: {output}")

        # Check if the output indicates an SSR result
        if "SSR" in output:
            # Extract the key and ciphertext from the output
            key = output.split(":")[1].strip()
            cipher_text = output.split(":")[2].strip()

            # Append the obtained key and ciphertext to the results list
            results.append((key, cipher_text))
    except Exception as e:
        print(f"Error: {e}")

# Create and start threads to perform concurrent pulling
threads = []
for _ in range(num_threads):
    thread = threading.Thread(target=pull_string)
    thread.start()
    threads.append(thread)

# Wait for all threads to finish
for thread in threads:
    thread.join()

# Print the obtained keys and ciphertexts
for idx, (key, cipher_text) in enumerate(results, start=1):
    print(f"Thread {idx}: Key: {key}, Cipher Text: {cipher_text}")
