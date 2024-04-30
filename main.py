import masterServer
import keyGeneratorServer
from IBE import IBE
 
if __name__ == "__main__":
    ibe=IBE(3,3)
    
    ibe.generateSecretKeyShares("student")
    print("master server:")
    for i in range(3):
        print(f"master share {i}: {ibe.getMasterKeyShare(i)}")
        
    print()
    
    for i in range(3):
        print(f"KGC {i}:",end="\t")
        print(f"secret key {i}: {ibe.getSecretKeyShare(i)}")
    
    print()
    
    shares=[]
    
    print("=========USER1=========")
    for i in range(3):
        shares.append(ibe.getSecretKeyShare(i))
        print(f"secret key {i}: {ibe.getSecretKeyShare(i)}")
    
    secretKey=ibe.secretKeyReconstruct(shares)
    print(f"secret key : {secretKey}")
    cypher,iv=ibe.encrypt("Hello world",secretKey)
    print("cypher:")
    print(cypher)
    
    print()
    print("=========USER2=========")
    for i in range(3):
        print(f"secret key {i}: {ibe.getSecretKeyShare(i)}")
    
    print(f"secret key : {secretKey}")
    plaintext = ibe.decrypt(cypher, iv,secretKey)
    print("plaintext:")
    print(plaintext)
