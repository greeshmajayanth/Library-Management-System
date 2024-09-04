class CloudStorage:
    def __init__(self):
        self.files = {}  # Dictionary to store file names and their sizes
        self.users = {}  # Dictionary to store users and their capacities
        self.user_files = {}  # Dictionary to store users and their files

    def add_user(self, user_id: str, capacity: int) -> bool:
        if user_id in self.users:
            return False  # User with the same ID already exists
        self.users[user_id] = capacity
        self.user_files[user_id] = {}
        return True
    
    def add_file(self, name: str, size: int) -> bool:
        if name in self.files:
            return False
        self.files[name] = size
        return True
    
    def add_file_by(self, user_id: str, name: str, size: int) -> int | None:
        if user_id not in self.users:
            return None  # User does not exist
        if name in self.files:
            return None  # File with the same name already exists

        user_files = self.user_files[user_id]
        current_usage = sum(user_files.values())

        if current_usage + size > self.users[user_id]:
            return None  # Exceeds user's capacity limit

        self.files[name] = size
        user_files[name] = size
        return self.users[user_id] - (current_usage + size)
    
    def copy_file(self, name_from: str, name_to: str) -> bool:
        if name_from not in self.files or name_to in self.files:
            return False  # File to copy from does not exist or target file already exists

        # Find the owner of the source file
        owner_id = None
        for user_id, files in self.user_files.items():
            if name_from in files:
                owner_id = user_id
                break
        
        if owner_id is None:
            return False  # Source file does not have a valid owner

        # Check if copying the file would exceed the user's capacity
        if owner_id != "admin":
            current_usage = sum(self.user_files[owner_id].values())
            if current_usage + self.files[name_from] > self.users[owner_id]:
                return False  # Exceeds user's capacity limit

        # Copy the file
        self.files[name_to] = self.files[name_from]
        self.user_files[owner_id][name_to] = self.files[name_from]
        return True
    
    def get_file_size(self, name: str) -> int | None:
        return self.files.get(name)  # Returns None if the file does not exist

    def find_file(self, prefix: str, suffix: str) -> list[str]:
        matching_files = [
            (name, size) for name, size in self.files.items()
            if name.startswith(prefix) and name.endswith(suffix)
        ]
        # Sort first by size in descending order, then by name lexicographically
        matching_files.sort(key=lambda x: (-x[1], x[0]))
        return [f"{name} ({size})" for name, size in matching_files]
    
    def update_capacity(self, user_id: str, capacity: int) -> int | None:
        if user_id not in self.users:
            return None  # User does not exist
        self.users[user_id] = capacity

        user_files = self.user_files[user_id]
        current_usage = sum(user_files.values())
        if current_usage <= capacity:
            return 0  # No files need to be removed

        # Remove files until usage is within capacity
        files_to_remove = sorted(user_files.items(), key=lambda x: (-x[1], x[0]))
        removed_files_count = 0

        while current_usage > capacity and files_to_remove:
            file_to_remove = files_to_remove.pop(0)
            del self.files[file_to_remove[0]]
            del user_files[file_to_remove[0]]
            current_usage -= file_to_remove[1]
            removed_files_count += 1

        return removed_files_count

# Example usage:
storage = CloudStorage()
print(storage.add_user("admin", float('inf')))  # Output: True (admin has unlimited capacity)
print(storage.add_user("user1", 500))  # Output: True
print(storage.add_user("user2", 1000))  # Output: True

# Add files by users
print(storage.add_file_by("user1", "file1.txt", 100))  # Output: 400 (remaining capacity)
print(storage.add_file_by("user1", "file2.txt", 300))  # Output: 100 (remaining capacity)
print(storage.add_file_by("user1", "file3.txt", 200))  # Output: None (exceeds capacity)
print(storage.add_file_by("user2", "file4.txt", 500))  # Output: 500 (remaining capacity)

# Update user capacity
print(storage.update_capacity("user1", 300))  # Output: 1 (number of files removed)
print(storage.update_capacity("user3", 300))  # Output: None (user does not exist)



import unittest

class TestCloudStorage(unittest.TestCase):
    def setUp(self):
        self.storage = CloudStorage()
        self.storage.add_user("admin", float('inf'))  # Ensure admin user is set up for other tests
    
    def test_level_1_case_03_add_copy_and_get_files(self):
        self.assertTrue(self.storage.add_file('/dir/file1.mov', 20))
        self.assertTrue(self.storage.copy_file('/dir/file1.mov', '/file2.mp4'))
        self.assertEqual(self.storage.get_file_size('/dir/file1.mov'), 20)
        self.assertEqual(self.storage.get_file_size('/file2.mp4'), 20)
                         
    def test_level3_case_03_should_copy_files_of_specific_user_only(self):
        self.assertTrue(self.storage.add_user('new_user', 100))
        self.assertTrue(self.storage.add_user('super_user', 100))
        self.assertEqual(self.storage.add_file_by('new_user', '/tmp/file.txt', 60), 40)
        self.assertEqual(self.storage.add_file_by('super_user', '/tmp/super/file.txt', 40), 60)
        self.assertEqual(self.storage.add_file_by('admin', '/tmp/root/file.txt', 150))
        self.assertFalse(self.storage.copy_file('/tmp/file.txt', '/file.txt'))
        self.assertTrue(self.storage.copy_file('/tmp/super/file.txt', '/super/file.txt'))
        self.assertTrue(self.storage.copy_file('/tmp/root/file.txt', '/root/file.txt'))

if __name__ == '__main__':
    unittest.main()