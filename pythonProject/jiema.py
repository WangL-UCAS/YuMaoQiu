import base64

value = "hgHXqwQHD8+BfGWe/3LHr34kQ5ekCaDCmcK07yu8B6+oYoXqb0j3k6MVbxt/urWGd4NGEawnkNNlgIs+lez4Y8gjw0kp3pBsyouVZMiSGzU="
decoded = base64.b64decode(value)
print(decoded)