import hashlib  # For generating secure hashes
import time     # For timestamps when creating blocks

# Defining the Block class
class Block:
    """
    This class defines what a single block in the blockchain looks like.
    """
    def __init__(self, index, previous_hash, timestamp, data, proof):
        self.index = index  # The position of the block in the chain
        self.previous_hash = previous_hash  # The hash of the block before this one
        self.timestamp = timestamp  # Time when this block was created
        self.data = data  # Whatever data we want to store in the block
        self.proof = proof  # The nonce/proof of work value
        self.hash = self.calculate_hash()  # Generate the hash as soon as block is created
    def calculate_hash(self):
        """
        This method calculates the SHA-256 hash based on the block's content.
        """
        block_content = (
            str(self.index) +
            self.previous_hash +
            str(self.timestamp) +
            str(self.data) +
            str(self.proof)
        )
        return hashlib.sha256(block_content.encode()).hexdigest()
    # The Blockchain class to manage the whole chain
class Blockchain:
    """
    This class represents the entire blockchain itself.
    """
    def __init__(self):
        self.chain = [self.create_genesis_block()]  # Start the chain with the genesis block
        self.difficulty = 2  # This is the mining difficulty level, i.e. number of starting zeroes needed
    def create_genesis_block(self):
        """
        This creates the very first block, called the Genesis Block.
        """
        return Block(0, "0", time.time(), "Genesis Block", 0)
    def get_latest_block(self):
        """
        This returns the most recent block in the chain.
        """
        return self.chain[-1]
    def proof_of_work(self, block):
        """
        Simple proof-of-work: we keep changing the proof until
        the hash starts with the required number of zeros.
        """
        block.proof = 0
        while True:
            block.hash = block.calculate_hash()
            if block.hash.startswith('0' * self.difficulty):
                break  # Found a valid proof!
            block.proof += 1
            if block.proof % 1000 == 0:
                print(f"Still mining... tried proof: {block.proof}")
    def add_data(self, data):
        """
        Adds a new block with the given data to the chain, after mining.
        """
        previous_hash = self.get_latest_block().hash
        new_block = Block(
            index=len(self.chain),
            previous_hash=previous_hash,
            timestamp=time.time(),
            data=data,
            proof=0
        )
        self.proof_of_work(new_block)  # Mining the block before adding
        self.chain.append(new_block)
        print(f"Block {new_block.index} mined with proof {new_block.proof}!")
    def is_chain_valid(self):
        """
        Validates the blockchain: ensures no data was tampered with.
        """
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]

            # Check if the current block's hash is still valid
            if current.hash != current.calculate_hash():
                print(f"Block {current.index} hash mismatch!")
                return False

            # Check if the chain linkage is correct
            if current.previous_hash != previous.hash:
                print(f"Block {current.index} previous hash doesn't match!")
                return False

        return True

if __name__ == "__main__":
    blockchain = Blockchain()

    while True:
        print("\nOptions Menu:")
        print("1. Add a new block")
        print("2. Display the blockchain")
        print("3. Validate blockchain integrity")
        print("4. Exit the program")

        choice = input("What do you want to do? Enter your choice: ").strip()

        if choice == "1":
            data = input("Type the data you want to store in the block: ")
            print("Hold on, mining in progress...")
            blockchain.add_data(data)
            print("New block successfully added!")

        elif choice == "2":
            for block in blockchain.chain:
                print(f"\nBlock Number: {block.index}")
                print(f"  Timestamp: {block.timestamp}")
                print(f"  Data: {block.data}")
                print(f"  Proof: {block.proof}")
                print(f"  Previous Hash: {block.previous_hash}")
                print(f"  Hash: {block.hash}")

        elif choice == "3":
            if blockchain.is_chain_valid():
                print("Everything looks good! The blockchain is valid.")
            else:
                print("Warning! Blockchain integrity is compromised!")

        elif choice == "4":
            print("Exiting the blockchain program. See ya!")
            break

        else:
            print("Invalid choice, please select 1, 2, 3, or 4.")