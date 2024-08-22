from cryptography.fernet import Fernet
import os
def encrypt_vote(vote, key):
    f = Fernet(key)
    encrypted_vote = f.encrypt(vote.encode())
    return encrypted_vote
def cast_vote(voter_id, candidates, voter_ids, votes, key):
    if voter_id in voter_ids:
        print("You have already voted.")
        return False
    else:
        print("Candidates:")
        for index, candidate in enumerate(candidates, 1):
            print(f"{index}. {candidate}")
        choice = input("Enter the number of your choice: ").strip()
        os.system('cls' if os.name == 'nt' else 'clear')  # This clears the terminal
        if choice.isdigit() and 1 <= int(choice) <= len(candidates):
            selected_candidate = candidates[int(choice) - 1]
            encrypted_vote = encrypt_vote(selected_candidate, key)
            votes.append(encrypted_vote)
            voter_ids.add(voter_id)
            print("Vote cast successfully and encrypted.")
            return True
        else:
            print("Invalid choice. Please select a valid candidate number.")
            return False
def count_votes(votes, candidates, key):
    f = Fernet(key)
    vote_count = {candidate: 0 for candidate in candidates}
    for vote in votes:
        decrypted_vote = f.decrypt(vote).decode()
        if decrypted_vote in candidates:
            vote_count[decrypted_vote] += 1
    return vote_count
def main():
    key = Fernet.generate_key()
    candidates = ["Candidate 1", "Candidate 2", "Candidate 3"]
    voter_ids = set()
    votes = []
    print("Welcome to the Secure Voting System")
    while True:
        voter_id = input("Enter your voter ID: ").strip()
        if cast_vote(voter_id, candidates, voter_ids, votes, key):
            continue_voting = input("Is there another voter? (yes/no): ").strip().lower()
            if continue_voting == "no":
                break
    results = count_votes(votes, candidates, key)
    print("Final Results:")
    for candidate, count in results.items():
        print(f"{candidate}: {count} votes")
if __name__ == "__main__":
    main()
