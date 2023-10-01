# Alexia Ntantouri - 3871
# Implementation of Cyclic Redundancy Check (CRC)


import random


# Returns a string representing a random binary sequence of n bits
def random_message(n):

        data = ''

        for i in range(n):
                bit = str(random.randint(0, 1))
                data += bit
                
        return data


# Returns the result of the XOR operation of the two arguments
# a and b that represent two binary sequences of same length
def xor(a, b):

        result = ''

        for i in range(len(b)):
                if a[i] == b[i]:
                        result += '0'
                else:
                        result += '1'
                        
        return result


# Returns the result of the modulo-2 division of the two arguments
# divident and divisor that represent two binary sequences
def mod2div(divident, divisor):

        pick = len(divisor)

        # get a the first bits of the divident
        # that are same size as the divisor
        tmp = divident[0 : pick]

        while pick < len(divident):
                if tmp[0] == '1':

                        # XOR the tmp with the divisor ignoring the first bit
                        # of the result and append the next bit from the divisor
                        tmp = xor(divisor, tmp)[1:] + divident[pick]

                else:

                        # if the leftmost bit of the tmp is 0, remove it
                        # and append the next bit from the divisor
                        tmp = tmp[1:] + divident[pick]
                
                # increment pick to point to the next bit of the divident
                pick += 1

        # when all bits of the divident have been pulled down
        if tmp[0] == '1':
                # XOR the tmp with the divisor ignoring the first bit of the result 
                tmp = xor(divisor, tmp)[1:]
        else:
                # if the leftmost bit of the tmp is 0, remove it
                tmp = tmp[1:]
        
        return tmp


# Returns a string the represents the binary sequence
# that will be sent, based on the data (D) and the number p (P)
def encodeData(data, p, printDetails):

        # append n-k zeroes at end of data
        appended_data = data + '0'*(len(p)-1)
        remainder = mod2div(appended_data, p)

        if(printDetails):
                print("FCS (F):", remainder)

        # append remainder to the original data
        return data + remainder


# Returns a string that represents the binary sequence
# that will be received by the recipient
# by corrupting the original data based on the bit error rate
def receiveData(sentData, ber):

        changedData = ''
        
        for i in range(0, len(sentData)):
            
                # generate random number between 0 and 1
                randNum = random.uniform(0, 1)
                
                # if the random number is less than the BER
                # change the bit from '1' to '0', or from '0' to '1'
                if randNum < ber:
                        if sentData[i] == '1':
                                changedData += '0'
                        else:
                                changedData += '1'
                else:
                        changedData += sentData[i]
        
        return changedData


# Returns True if there was an error found
# in the received data by the CRC, else returns False
def decodeData(receivedData, p, printDetails):

        remainder = mod2div(receivedData, p)

        if(printDetails):
                print("Remainder: ", remainder)

        # if remainder is not zero then error
        if '1' in remainder:
            return True
        else:
            return False
            
        return foundError


# main
numOfMessages = int(input("Enter number of random messages you want to send: "))
k = int(input("Enter number of bits (k): "))
p = input("Enter binary number (P): ")
ber = float(input("Enter bit error rate (BER): "))

if(numOfMessages == 1):
        data = random_message(k)
        print("Desired length random binary string is (D): ", data)

        sentData = encodeData(data, p, True)
        print("Sent data (T):      ", sentData)
            
        receivedData = receiveData(sentData, ber)
        print("Received data (Tr): ", receivedData, "\n")

        errorFound = decodeData(receivedData, p, True)
        if(not errorFound):
                print("No error found in received data")
        else:
                print("Error found in received data")
                
else: #if number of messages is not 1
        receivedIncorrect = 0
        detected = 0
        undetected = 0
        for i in range(numOfMessages):
            data = random_message(k)
            
            sentData = encodeData(data, p, False)
            
            receivedData = receiveData(sentData, ber)
            
            errorFound = decodeData(receivedData, p, False)

            if sentData != receivedData:
                receivedIncorrect += 1

            if errorFound:
                detected += 1

            if (sentData != receivedData) and (not errorFound):
                undetected += 1

        print("Received incorrectly: ", receivedIncorrect)
        print("Detected: ", detected)
        print("Undetected: ", undetected)

        ans1 = (receivedIncorrect/numOfMessages)*100
        ans2 = (detected/numOfMessages)*100
        ans3 = (undetected/numOfMessages)*100

        print("Ποσοστό των μηνυμάτων που φθάνουν με σφάλμα στον αποδέκτη: ", round(ans1,10), "%")
        print("ποσοστό των μηνυμάτων που ανιχνεύονται ως εσφαλμένα από το CRC: ", round(ans2,10), "%")
        print("Tο ποσοστό των μηνυμάτων που φθάνουν με σφάλμα στο αποδέκτη και δεν ανιχνεύονται από το CRC: ", round(ans3,10), "%")
