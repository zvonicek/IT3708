class Network():
    def __init__(self, layers):
        self.layers = layers

    def compute(self, vals):
        for i in range(self.layers):
            vals = self.layers[i].compute(vals)

        return vals

    def set_weights(self, phenotype):
        pass