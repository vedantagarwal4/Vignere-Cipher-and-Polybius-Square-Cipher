# importing the required libraries  
import cv2  
import os
import numpy as np  
import types   
from string import ascii_uppercase as alphabet

path = os.getcwd()
# converting types to binary  
def msg_to_bin(msg):  
    if type(msg) == str:  
        return ''.join([format(ord(i), "08b") for i in msg])  
    elif type(msg) == bytes or type(msg) == np.ndarray:  
        return [format(i, "08b") for i in msg]  
    elif type(msg) == int or type(msg) == np.uint8:  
        return format(msg, "08b")  
    else:  
        raise TypeError("Input type not supported")  

  
# defining function to hide the secret message into the image  
def hide_data(img, secret_msg):  
    # calculating the maximum bytes for encoding  
    nBytes = img.shape[0] * img.shape[1] * 3 // 8  
    #print("Maximum Bytes for encoding:", nBytes)  
    # checking whether the number of bytes for encoding is less  
    # than the maximum bytes in the image  
    if len(secret_msg) > nBytes:  
        raise ValueError("Error encountered insufficient bytes, need bigger image or less data!!")  
    secret_msg += '#####'       # we can utilize any string as the delimiter  
    dataIndex = 0  
    # converting the input data to binary format using the msg_to_bin() function  
    bin_secret_msg = msg_to_bin(secret_msg)  
    #print("bin_secret_msg ********** : ", bin_secret_msg)
    # finding the length of data that requires to be hidden  
    dataLen = len(bin_secret_msg)  
    #print("length of bin_secret_msg : ", bin_secret_msg)
    for values in img:  
        for pixels in values:  
            # converting RGB values to binary format  
            r, g, b = msg_to_bin(pixels)  
            # modifying the LSB only if there is data remaining to store  
            if dataIndex < dataLen:  
                # hiding the data into LSB of Red pixel  
                pixels[0] = int(r[:-1] + bin_secret_msg[dataIndex], 2)  
                dataIndex += 1  
            if dataIndex < dataLen:  
                # hiding the data into LSB of Green pixel  
                pixels[1] = int(g[:-1] + bin_secret_msg[dataIndex], 2)  
                dataIndex += 1  
            if dataIndex < dataLen:  
                # hiding the data into LSB of Blue pixel  
                pixels[2] = int(b[:-1] + bin_secret_msg[dataIndex], 2)  
                dataIndex += 1  
            # if data is encoded, break out the loop  
            if dataIndex >= dataLen:  
                break  
      
    return img

def show_data(img):  
    bin_data = ""  
    for values in img:  
        for pixels in values:  
            # converting the Red, Green, Blue values into binary format  
            r, g, b = msg_to_bin(pixels)  
            # data extraction from the LSB of Red pixel  
            bin_data += r[-1]  
            # data extraction from the LSB of Green pixel  
            bin_data += g[-1]  
            # data extraction from the LSB of Blue pixel  
            bin_data += b[-1]  
    # split by 8-Bits  
    allBytes = [bin_data[i: i + 8] for i in range(0, len(bin_data), 8)]  
    # converting from bits to characters  
    decodedData = ""  
    for bytes in allBytes:  
        decodedData += chr(int(bytes, 2))  
        # checking if we have reached the delimiter which is "#####"  
        if decodedData[-5:] == "#####":  
            break  
    # print(decodedData)  
    # removing the delimiter to display the actual hidden message  
    return decodedData[:-5]  

# defining function to encode data into Image  
def encodeText(data):  
    img_name = input("Enter name of the image (with extension): ")
    img_name = os.path.join(path,img_name)  
    # reading the input image using OpenCV-Python  
    img = cv2.imread(img_name)  
    # printing the details of the image    
    data = data
    if (len(data) == 0):  
        raise ValueError('Data is Empty')  
      
    file_name = input("Enter name of the new encoded image (with extension): ") 
    file_name = os.path.join(path,file_name)
    # calling the hide_data() function to hide the secret message into the selected image  
    encodedImage = hide_data(img, data)  
    cv2.imwrite(file_name, encodedImage) 
    print("The shape of the image is: ", img.shape) # checking the image shape to calculate the number of bytes in it  
    #print("The original image is as shown below: ")  
    # resizing the image as per the need  
    resizedImg = cv2.resize(img, (500, 500))  
    # displaying the image  
    cv2.imshow('',resizedImg)
    cv2.waitKey(0) 
  
# defining the function to decode the data in the image  
def decodeText():  
    # reading the image containing the hidden image  
    img_name = input("Enter the name of the Steganographic image that has to be decoded (with extension): ")  
    img = cv2.imread(img_name)  # reading the image using the imread() function  
  
    key = str(input("[+] Enter your key - "))
    print("The Steganographic image is as follow: ")  
    resizedImg = cv2.resize(img, (500, 500))    # resizing the actual image as per the needs  
    cv2.imshow('',resizedImg)  # displaying the Steganographic image  
    cv2.waitKey(0) 
    text = show_data(img)  
    return text




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
    if mode == 0:
        text = str(input("[+] Enter your plain text - "))
        text_upper = text.upper()
        keyword = str(input("[+] Enter your key - "))
        keyword = keyword.upper()
        string = text_upper
        key = generateKey(string, keyword) # The newly generated autokey is stored in the key variable. 
        print("String : " , string)
        print("Key : ", key) 
        cipher_text = cipherText(string,key) 
        finished_text = encoding(cipher_text)
        print("After Vignere Cipher : ", cipher_text)

        print("\n »» Encoded Text via Hybrid Application of Vignere and Polybius Square Cipher : ««")
        print(finished_text)
        print()
        encodeText(string)
        print("The given image has been Encoded.") 

    else:
        print("Decoded message is : " + decodeText())



def main():
    print("[x]Hybrid of Vigenere & Polybius Square Cryptography Algorithm. [x]")
    print(" • 0. Encoding mode.\n • 1. Decoding mode.")

    mode = int(input("[?] Select program mode - "))
    assembly(mode)


if __name__ == '__main__':
    main()


