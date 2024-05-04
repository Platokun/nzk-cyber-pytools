# i took many hours trying to figure out how to use __dunder__ methods  and @decorators because this morning i watched a video on them when i woke up so instead of doing it the easy way im im finguring it out.
#ive also never f ully understood classes nor why you'd use them so i just tried to use em here to practice for making things easier in the future
class Converter:
    def __init__(self, input_format: str = "", output_format: str = "", value: str = "") -> None:
        self.input_format = input_format
        self.output_format = output_format
        self.value = value

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Converter) and (self.input_format, self.output_format, self.value) == (other.input_format, other.output_format, other.value)

    def __repr__(self) -> str:
        return f"Converter(input_format={self.input_format}, output_format={self.output_format}, value={self.value})"
    
    def __or__(self, other: object) -> 'Converter':
        if isinstance(other, Converter):
            return Converter(self.input_format, other.output_format, self.value + other.value)
        raise ValueError("Operand must be a Converter")
    
    def __getitem__(self, index: int) -> str:
        return self.value[index]
    
    def __format__(self, format_spec: str) -> str:
        # Assuming hex value formatting is required directly from value
        formatted_value = self.convert()
        if format_spec == 'x':
            return formatted_value  # Already hex
        elif format_spec == 'b':
            return format(int(formatted_value, 16), 'b')
        elif format_spec == 'o':
            return format(int(formatted_value, 16), 'o')
        elif format_spec == 'd':
            return str(int(formatted_value, 16))
        return formatted_value
    
    @property
    def value_details(self) -> str:
        return f"Value: {self.value} | Input: {self.input_format} | Output: {self.output_format}"
    


    def get_user_input(self) -> None:
        programmed_formats = ["hex", "bin", "oct", "dec", "text", "ascii", "unicode"]
        self.programmed_formats = programmed_formats
        override = True
        if override:
            self.input_format = "all"
            self.output_format = "text"
            #self.value = "143 157 155 160 165 164 145 162" # "computer" in octal, i thought it was in decimal or ascii table format, idk why but it allways converts to the cent symbol instead of multiple characters.
            #self.value = "0x636f6d7075746572" # "computer" in hex but causes problems coz its too big normally
            #self.value = "01110000 01101001 01100101" # "pie" in binary
            self.value = input("Enter value: ")
            return  
        else:
            print("auto mode disabled")
            #self.output_format = input("Enter output format: ").lower()
            #self.value = input("Enter value: ")

        input_locks = [False, False, False]
        while not all(input_locks):
            for i, locked in enumerate(input_locks):
                if not locked:
                    try:
                        if i == 0:
                            self.input_format = input("Enter input format: ").lower()
                            if self.input_format in programmed_formats:
                                input_locks[0] = True
                            else:
                                print("Invalid input format.")
                        elif i == 1:
                            self.output_format = input("Enter output format: ").lower()
                            if self.output_format in programmed_formats:
                                input_locks[1] = True
                            else:
                                print("Invalid output format.")
                        elif i == 2:
                            self.value = input("Enter value: ")
                            try:
                                # Attempt conversion to validate input
                                self.convert()
                                input_locks[2] = True
                            except ValueError:
                                print("Invalid value or conversion error.")
                    except ValueError as ve:
                        print(f"Invalid {['input format', 'output format', 'value'][i]}: {ve}")
        print("All inputs accepted.")
 
    def convert(self) -> str:
        #bro this was so hard to make smaller. i tried some mega long case system but this is so much shorter.
        #originally it was going to be just if input and choice of output but the flag was burried behind multiple conversions
        #and it was timed and figuring out which one was hard
        #so trying with all possible inputs to word was the easiest way to get the flag.
        #still tf is lambda. i dont get it but i guess it works. (but this format is shorter than case or if else)
        self.conversion_table = {
            ("bin", "oct"): lambda x: format(int(x, 2), 'o'),
            ("bin", "dec"): lambda x: str(int(x, 2)),
            ("bin", "hex"): lambda x: format(int(x, 2), 'x'),
            ("bin", "text"): lambda x: ''.join(chr(int(b, 2)) for b in x.split()),
            ("oct", "bin"): lambda x: format(int(x, 8), 'b'),
            ("oct", "dec"): lambda x: str(int(x, 8)),
            ("oct", "hex"): lambda x: format(int(x, 8), 'x'),
            ("oct", "text"): lambda x: ''.join(chr(int(o, 8)) for o in x.split()),
            ("dec", "bin"): lambda x: format(int(x), 'b'),
            ("dec", "oct"): lambda x: format(int(x), 'o'),
            ("dec", "hex"): lambda x: format(int(x), 'x'),
            ("dec", "text"): lambda x: ''.join(chr(int(d)) for d in x.split()),
            ("hex", "bin"): lambda x: format(int(x, 16), 'b'),
            ("hex", "oct"): lambda x: format(int(x, 16), 'o'),
            ("hex", "dec"): lambda x: ''.join(str(int(x[i:i+2], 16)) for i in range(2 if x.startswith('0x') else 0, len(x), 2)),
            ("hex", "text"): lambda x: ''.join(chr(int(x[i:i+2], 16)) for i in range(2 if x.startswith('0x') else 0, len(x), 2)),
            ("text", "bin"): lambda x: ' '.join(format(ord(c), 'b') for c in x),
            ("text", "oct"): lambda x: ' '.join(format(ord(c), 'o') for c in x),
            ("text", "dec"): lambda x: ' '.join(str(ord(c)) for c in x),
            ("text", "hex"): lambda x: ' '.join(format(ord(c), 'x') for c in x),
        }
        if self.input_format == "all":
            try:
                #which is why i put this here
                #and i put 
                #self.input_format = "all"
                #self.output_format = "text"
                #self.value = input("Enter value: ")
                #at the start so it was easy to test
                self.convert_with_input_all()

            except ValueError as e:
                print(str(e))
            
        if self.input_format == self.output_format:
            return self.value
        try:
            return self.conversion_table[(self.input_format, self.output_format)](self.value)
        except KeyError:
            raise ValueError(f"Unsupported conversion from {self.input_format} to {self.output_format}")
             
    def convert_with_input_all(self) -> str:
        #im not sure how to use the previous convert table here so i just made a new one

        # Split the string into a list of strings
        values = self.value.split()

        for possible_input_format in self.programmed_formats:
            try:
                values_str = ' '.join(values)
                possible_output = self.conversion_table[(possible_input_format, self.output_format)](values_str)
                print(possible_output)
            except (KeyError, ValueError) as e:
                print(f"error: {e}")
                continue

def main() -> None:
    aaaa = True
    while aaaa == True:
        try:
            conv = Converter()
            conv.get_user_input()
            result = conv.convert()
            #result = is a leftover from the original super long attempt, but its still runs  sooo print(result)?
            #and doing print(result) doesnt print anything for some reason? idk challenge is over now so someone else can figure it out or 
            #maybe i will later whenever i add this to github or re re re rewrite this code.
            print("-" * 20)
            print(f"Value accessed by index 0: {conv[0]}")
            print(repr(conv))
            print("--" * 20)
            match conv.input_format:
                case "hex":
                    print(f"Converted result in {conv.output_format}: {format(conv, 'x')}")
                case "bin":
                    print(f"Converted result in {conv.output_format}: {format(conv, 'b')}")
                case "oct":
                    print(f"Converted result in {conv.output_format}: {format(conv, 'o')}")
                case "dec":
                    print(f"Converted result in {conv.output_format}: {format(conv, 'd')}")
                case "text":
                    print(f"Converted result in {conv.output_format}: {conv}")
                case "ascii":
                    print(f"Converted result in {conv.output_format}: {conv}")
                case "unicode":
                    print(f"Converted result in {conv.output_format}: {conv}")
                case _:
                    print(f"Converted result in {conv.output_format}: {conv}")
        except ValueError as e:
            print(str(e))
        if input("More conversion? (y/n): ").lower() == "n":
            aaaa = False
            
if __name__ == "__main__":
    main()
