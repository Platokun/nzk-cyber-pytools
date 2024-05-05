class endieness:
    def convert_endian(self, hex_str: str) -> str:
        if len(hex_str) % 2 != 0:
            hex_str = '0' + hex_str
        return ''.join(reversed([hex_str[i:i+2] for i in range(0, len(hex_str), 2)]))

    def main(self):
        while True:
            endianness = input("wuts your input? for endieness: ")
            if endianness == "exit":
                break
            print(self.convert_endian(endianness))
            flipendienness = endianness[::-1]
            print(self.convert_endian(flipendienness))
            word_to_hex = bytes(endianness, 'utf-8').hex()
            converted = self.convert_endian(word_to_hex)
            print(f"flipped Little to Big: {endianness} -> {converted}")
            word_to_hex = bytes(flipendienness, 'utf-8').hex()
            converted = self.convert_endian(word_to_hex)
            print(f"flipped Big to little: {flipendienness} -> {converted}")
            
if __name__ == "__main__":
    endieness.main(self=endieness())
