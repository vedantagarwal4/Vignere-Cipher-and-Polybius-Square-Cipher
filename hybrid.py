from string import ascii_uppercase as alphabet


# This function generates the 
# autokey in which the key will not be 
# repeated in a cyclic manner.  
def generateKey(string, key):  
    if len(string) == len(key): 
        return(key) 
    else:
        length = len(string)
        newkey = key+string
        newkey = newkey[0:len(newkey) - len(key)]
    return newkey 
    
# This function returns the 
# encrypted text generated 
# with the help of the key 
def cipherText(string, key): 
    cipher_text = [] 
    for i in range(len(string)): 
        x = (ord(string[i]) +
            ord(key[i])) % 26
        x += ord('A') 
        cipher_text.append(chr(x)) 
    return("" . join(cipher_text)) 
    
# This function decrypts the 
# encrypted text and returns 
# the original text 
def originalText(cipher_text, key): 
    orig_text = [] 
    for i in range(len(cipher_text)): 
        x = (ord(cipher_text[i]) -
            ord(key[i]) + 26) % 26
        x += ord('A') 
        orig_text.append(chr(x)) 
    return("" . join(orig_text)) 
    
 
 



#This dictionary helps to map all the alphabets to their
# respective values as per the Polybius Square  
def codes_table(char):
    table = {
        "A": 11, "B": 12, "C": 13, "D": 14, "E": 15,
        "F": 21, "G": 22, "H": 23, "I": 24, "K": 25,
        "L": 31, "M": 32, "N": 33, "O": 34, "P": 35,
        "Q": 41, "R": 42, "S": 43, "T": 44, "U": 45,
        "V": 51, "W": 52, "X": 53, "Y": 54, "Z": 55, "J": 0,

        11: "A", 12: "B", 13: "C", 14: "D", 15: "E",
        21: "F", 22: "G", 23: "H", 24: "I", 25: "K",
        31: "L", 32: "M", 33: "N", 34: "O", 35: "P",
        41: "Q", 42: "R", 43: "S", 44: "T", 45: "U",
        51: "V", 52: "W", 53: "X", 54: "Y", 55: "Z", 0: "J"
    }

    return table[char]


#This function helps to encode the output of the
#Vignere cipher to random numbers , thereby producing the
#output for the Polybius Square Cipher
def encoding(text):
    text, finished_text = text.upper(), ""
    for symbol in text:
        if symbol in alphabet:
            finished_text += str(codes_table(symbol)) + " "

    return finished_text


#This function helps to decode the random numbers which 
# were generated as a result of the hybrid application of the two 
#algorithms.
def decoding(text, key):
    text, finished_text = text.upper(), ""
    for symbol in list(map(int, text.split())):
        finished_text += codes_table(symbol)

    decrypted_text = originalText(finished_text, key)
    return decrypted_text


def assembly(mode):
    text = str(input("[+] Enter your plain text - "))
    if mode == 0:
        keyword = str(input("[+] Enter your key - "))
        string = text
        key = generateKey(string, keyword) # The newly generated autokey is stored in the key variable. 
        print("String : " , string)
        print("Key : ", key) 
        cipher_text = cipherText(string,key) 
        finished_text = encoding(cipher_text)
        print("After Vignere Cipher : ", cipher_text)

        print("\n »» Encoded Text via Hybrid Application of Vignere and Polybius Square Cipher : ««")
        print(finished_text)

    else:
        key = str(input("[+] Enter your key - "))
        finished_text = decoding(text, key)
        print("\n »» Decoded Text via Hybrid Application of Vignere and Polybius Square Cipher : ««")
        print(finished_text)

    


def main():
    print("[x]Hybrid of Vigenere & Polybius Square Cryptography Algorithm. [x]")
    print(" • 0. Encoding mode.\n • 1. Decoding mode.")

    mode = int(input("[?] Select program mode - "))
    assembly(mode)


if __name__ == '__main__':
    main()


