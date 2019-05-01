class Seq:
    def __init__(self, strbases):
        """A class for representing sequences"""
        #print("New sequence created!")


        # Initialize the sequence with the value
        # passed as argument when creating the object
        self.strbases = strbases

    def get_strbases(self):
        """Function that gets the string sequence"""
        return self.strbases

    def len(self):
        """Function that returns the length of the sequence."""
        tl = len(self.strbases)
        return tl

    def count(self, base):
        """Function that returns the number of the base "base" appears in the sequence"""
        return self.strbases.count(base)

    def perc(self, base):
        """Function that returns the percentage that the base "base" appears in the sequence"""
        if len(self.strbases) < 0:
            return "Sorry that is not a valid sequence"

        elif len(self.strbases) > 0:
            perc= round(100.0 * self.strbases.count(base) / len(self.strbases), 1)
            return perc


    def complement(self):
        """Function that returns the complement sequence to the original one"""
        output = []
        for i in self.strbases:
            if i == "A":
                output.append("T")
            elif i == "T":
                output.append("A")
            elif i == "C":
                output.append("G")
            elif i == "G":
                output.append("C")

        str = "".join(output) #Conversion from list to str

        return str

    def reverse(self):
        "This function returns the reverse of your sequence"
        return (self.strbases[::-1])


#Testing our new class to see if it works:
#s1 = Seq("ACTG")

#print(s1.perc("A"))
#print(s1.count("A"))
#print(s1.reverse())
#print(s1.complement())

