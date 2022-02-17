import time

print(time.ctime())
message = "ahoj"
print(message)
msg_length = len(message)
print(msg_length)
send_length = str(msg_length).encode()
print(msg_length)
send_length += b" " * (64 - len(send_length))
print(msg_length)