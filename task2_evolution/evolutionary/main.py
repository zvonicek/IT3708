import sys
from ea_impl.suprising_sequences import SurprisingEA
import yaml
import ea.config


config_file = 'one_max.yaml'

if __name__ == '__main__':
    if len(sys.argv) >= 2:
        config_file = sys.argv[1]


cfg = yaml.load(open(config_file, 'r'))
for key, val in cfg.items():
    setattr(ea.config, key, val)

ea = ea.config.ea
ea.__init__()
ea.run()