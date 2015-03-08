from ea_impl.suprising_sequences import SurprisingEA
import yaml
import ea.config


cfg = yaml.load(open('surprising.yaml', 'r'))
for key, val in cfg.items():
    setattr(ea.config, key, val)

ea = SurprisingEA()
ea.run()
