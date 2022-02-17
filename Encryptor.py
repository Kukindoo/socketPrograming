from cryptography.fernet import Fernet

original_message = "Hello"

key = Fernet.generate_key()

fernet = Fernet("ahoj".encode("UTF-8"))

encrypted_message = fernet.encrypt(original_message.encode("UTF-8"))

print(original_message)
print(encrypted_message)


decrypted_message = fernet.decrypt(encrypted_message).decode("UTF-8")
print(decrypted_message)

print(key)