class BeerTrackerGenotypeCoder():
    """ Holds the configuration of the genotype parameters and provides a way to encode/decode genotype"""
    def __init__(self, bits_per_weight):
        self.min_ranges = []
        self.max_ranges = []
        self.init_funcs = []
        self.bits_per_weight = bits_per_weight

    def add_parameter(self, min_range, max_range, init_func):
        """
        Add new genotype parameter
        :param min_range: minimum range (eg. -1)
        :param max_range: maximum range (eg. +1)
        """

        self.min_ranges.append(min_range)
        self.max_ranges.append(max_range)
        self.init_funcs.append(init_func)

    def generate_init_genotype(self):
        genotype = []
        for i in range(len(self.init_funcs)):
            encoded_value = self.encode_decimal_value(self.init_funcs[i](), self.min_ranges[i], self.max_ranges[i])
            genotype.extend(self.to_binary(encoded_value, self.bits_per_weight))

        return genotype

    def decode_genotype(self, genotype):
        assert len(genotype) == len(self.min_ranges), "wrong input length"

        output = []
        for i in range(len(genotype)):
            output.append(self.decode_decimal_value(genotype[i], self.min_ranges[i], self.max_ranges[i]))

        return output

    def decode_decimal_value(self, value, min_range, max_range):
        """ Decodes the value from decimal genotype
        :param value: decimal value to be decoded (eg. 120)
        :param min_range: minimum range (eg. -1)
        :param max_range: maximum range (eg. +1)
        :return: decimal output value (eg. -0.01)
        """

        return (max_range - min_range) * value/(2**self.bits_per_weight-1) + min_range

    def encode_decimal_value(self, value, min_range, max_range):
        """ Encodes decimal value to decimal genotype representation, output is the closest possible value from the interval
        :param value: decimal input value (eg. -0.01)
        :param min_range: minimum range (eg. -1)
        :param max_range: maximum range (eg. +1)
        :return: decoded output to interval [0, 2^self.bits_number_per_weight] in decimal (eg. 120)
        """

        return min(range(2**self.bits_per_weight),
                   key=lambda x: abs(self.decode_decimal_value(x, min_range, max_range)-value))

    @staticmethod
    def to_binary(num, length):
        binary = bin(num)[2:].zfill(length)
        return [int(digit) for digit in binary]