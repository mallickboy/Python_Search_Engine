import random
class knapsack:
    def __init__(self) -> None:
        pass
    def gcd(self,a,b):
        while b:
            a, b = b, a % b
        return a
    def extended_gcd(self,a, b):
        if a == 0:
            return b, 0, 1
        else:
            g, y, x = self.extended_gcd(b % a, a)
            return g, x - (b // a) * y, y
    def mod_inverse(self,a, m): # (a*x)%m=1        
        g, x, y = self.extended_gcd(a, m)
        if g != 1:
            return None
        else:
            # print(x % m)
            return x % m
    def generate_superincreasing_sequence(self,length):
        sequence = [random.randint(2,100)]
        for _ in range(length - 1):
            next_element = random.randint(sum(sequence) + 1, sum(sequence) * 2)
            sequence.append(next_element)
        return sequence
    def private_public_key(self,array_len,digits_no):
        array=self.generate_superincreasing_sequence(array_len)
        # print(f"Generated series :{array}\t length : {array_len}")
        # check if superincreasing sequence
        self.arr_len=len(array)
        for i,el in enumerate(array):
            if el<=sum(array[:i]):
                print("The array elements must be in superincreasing sequence")
                return "Key generation error"
        min_m=sum(array)+1
        # m=random.randint(max(1000000000000000,min_m),10000000000000000*min_m) # 110
        m=random.randint(max(10**(digits_no-1),max(array)), max((10**(digits_no) - 1),max(array))) # 
        # get private key 
        while True:
            n = random.randint(2, m - 1)  # Choose a random number between 2 and m-1 # 31
            if self.gcd(m, n) == 1:
                break
        private_key=n
        # print(m,n)
        public_key=[]
        for element in array:
            key=(element *n) % m
            # print("pub gen :",element,n,m,key)
            public_key.append(key)
        # get n inverse for decryption
        # print (public_key,private_key)
        # decription_key=self.mod_inverse(n,m)
            self.private_key,self.mod_value,self.array,self.public_key=private_key,m,array,public_key
        return private_key,m,public_key
    def string_to_bin(self,string):
        string_bin=''
        for ch in string:
            ascii=ord(ch)
            ch_bin=bin(ascii)[2:].zfill(8)
            string_bin+=ch_bin
        # print(string_bin)
        return string_bin
    def break_into_sum_of(self,target,arr):
        def backtrack(start, path, target):
            if target == 0:
                result.append(path)
                return
            if target < 0 or start >= len(arr):
                return
            for i in range(start, len(arr)):
                if i > start and arr[i] == arr[i - 1]:
                    continue  # Skip duplicate elements
                backtrack(i + 1, path + [arr[i]], target - arr[i])

        result = []
        arr.sort()  # Sort the array to handle duplicate elements
        backtrack(0, [], target)
        return result[0]
    def encryption(self,str_bin,public_key):
        # public_key=self.public_key
        str_bin=self.string_to_bin(str_bin)
        if len(str_bin)%self.arr_len>0:
            print("GCD(string length,array length) must be 0 so that\n1.No element left in encryption\n2.No elements overproduced in decryption\n")
            return "Encryption Error"
        bin=''
        for ch in str_bin:
            if ch=='0'or ch=='1':bin+=ch
        str_bin=bin
        pub_len=len(public_key)
        i,portion_val=0,0
        cy=''
        for val_bin in str_bin:
            val_bin=int(val_bin)
            if val_bin:
                portion_val+=val_bin*public_key[i]
                # print("encryp gen: ",val_bin,"*",public_key[i],portion_val) # ok
            i=(i+1) %pub_len
            if not i:
                cy+=str(portion_val)+' '
                portion_val=0
        if i: # adding remaining potrion for bin_len % array_len !=0
            cy+=str(portion_val)+' '
            portion_val=0
        # print(cy)
        return cy
    def decryption(self,cypher_text):
        private_key,mod_val,array=self.private_key,self.mod_value,self.array
        decription_key=self.mod_inverse(private_key,mod_val)
        cypher=cypher_text.split()
        text=''
        for cy in cypher:
            val=(int(cy)*decription_key)%mod_val
            comb=self.break_into_sum_of(val,array)
            if not len(comb) and val:
                print("ERR: decryption -> no combination found")
            decode=''
            for element in array:
                if element in comb:decode+='1'
                else:decode+='0'
            text+=decode
            # print("decrep gen: ",cy,private_key,mod_val,val,comb,decode) # ok
        return self.bin_to_text(text)
    def bin_to_text(self,bin):
        if len(bin)%8 !=0:
            print("Not convertable")
            return
        string=''
        start=0
        while start<len(bin):
            string+=chr(int(bin[start:start+8],2))
            start+=8
        return string
    

my_knapsack = knapsack()
    
private_key, modulus, public_key = my_knapsack.private_public_key(8, 8)
plaintext = "Hello, world!"
encrypted_text = my_knapsack.encryption(plaintext, public_key)
decrypted_text = my_knapsack.decryption(encrypted_text)

