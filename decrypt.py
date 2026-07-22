#!/usr/bin/env python3
import os
import sys
import struct
import glob
from arc4 import ARC4

MASTER_KEY = b'Jfkdskfku2ir32y7432uroduw8y7318i9018urewfdsZ2Oaifwuieh~~cudsffdsd'

def decrypt_file(key_file: str):
    target_file = key_file.replace('.C_I_0P', '')
    if not os.path.exists(target_file):
        print(f"[-] Файл не найден: {target_file}")
        return

    try:
        with open(key_file, 'rb') as f:
            meta = f.read()

        cipher_master = ARC4(MASTER_KEY)
        file_key = cipher_master.decrypt(meta[:117])

        enc_size = struct.unpack('<Q', meta[221:229])[0]

        with open(target_file, 'rb') as f:
            enc_data = f.read()

        cipher_file = ARC4(file_key)
        dec_data = cipher_file.decrypt(enc_data[:enc_size]) + enc_data[enc_size:]

        dec_file = target_file + '.decrypted'
        with open(dec_file, 'wb') as f:
            f.write(dec_data)

        print(f"[+] Успешно расшифрован: {dec_file}")
    except Exception as e:
        print(f"[-] Ошибка при расшифровке {key_file}: {e}")

def main():
    if len(sys.argv) < 2:
        print(f"Использование: {sys.argv[0]} <путь_к_папке_или_файлу_.C_I_0P>")
        sys.exit(1)

    path = sys.argv[1]
    if os.path.isfile(path) and path.endswith('.C_I_0P'):
        decrypt_file(path)
    elif os.path.isdir(path):
        search_pattern = os.path.join(path, '**/*.C_I_0P')
        key_files = glob.glob(search_pattern, recursive=True, include_hidden=True)
        
        if not key_files:
            print("[-] Файлы ключей *.C_I_0P не найдены.")
            return
        print(f"[*] Найдено файлов для расшифровки: {len(key_files)}")
        for kf in key_files:
            decrypt_file(kf)
    else:
        print("[-] Указан неверный путь или файл не имеет расширения .C_I_0P")

if __name__ == '__main__':
    main()