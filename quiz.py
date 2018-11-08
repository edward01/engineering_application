from cryptography.fernet import Fernet

key = 'TluxwB3fV_GWuLkR1_BzGs1Zk90TYAuhNMZP_0q4WyM='

# Oh no! The code is going over the edge! What are you going to do?
message = b'gAAAAABb4O8MZdwUHEzlrDVJbPX8UTFCiKMEwsjEo1iCCN6CdFv1wY-fcPh1tY35RBua95rD5i9_sN1ONZRu_Q13hy-2pDxGkzuTzorwX8WOMvOJTOiP7AVuPZk6zchPALxRx8EgwNgGK29cfIPk0FhQWEwqDjrdFCYRa8Ppb8noHIOpNm6M3xV0-xabkbVY2p-tBgJ1Dhz-'

def main():
    f = Fernet(key)
    print(f.decrypt(message))


if __name__ == "__main__":
    main()