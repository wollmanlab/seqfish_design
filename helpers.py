import sys
from os import path
fname = sys.argv[1]
fname_out = sys.argv[2]

def remove_ensembl_version(fname):
  with open(fname, 'r') as f:
      with open(fname_out, 'w') as w:
          for line in f.readlines():
              if line[0]=='>':
                  line = line.split('|')
                  t_id = line[0]
                  gene_name = line[-4]
                  w.write(t_id+' gene='+gene_name+'\n')
                  print(gene_name)
              else:
                  w.write(line)


