import sys
from os import path
import numpy

fname = sys.argv[1]
fname_out = sys.argv[2]

def select_best_isoform(isodf, columns = {'length': 'l',
                                          'isofract': 'isofract', 
                                          'expression': 'FPKM'}, 
                       accepted_length=3000):
    isodf = isodf.sort_values([columns['isofract'], columns['length']], ascending=False)
    length_sort = np.argsort(isodf[columns['length']].values)[::-1]
    length_ranks = np.empty_like(length_sort)
    length_ranks[length_sort] = np.arange(len(length_sort))
    #length_rank = np.argsort(isodf[columns['length']])[::-1]
    isodf['lrank'] = length_ranks
    #pdb.set_trace()
    if isodf.iloc[0]['lrank']==0:
        return isodf.iloc[0]
    elif isodf.iloc[0][columns['length']] >= accepted_length:
        
        return isodf.iloc[0]
    else:
        return isodf.iloc[:3].sort_values('lrank').iloc[0]
        

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

def read_codebook(cbook_fname, shuffle=True):
    """Read CSV of n-bit codewords."""
    cwords = []
    with open(cbook_fname, 'r') as f:
        column_name = f.readline().strip()
        for l in f.readlines():
            cwords.append(l.strip())
    return numpy.random.shuffle(cwords)
  
# readout_names = ['RS0095', 'RS0109', 'RS0175', 'RS0237', 'RS0307', 'RS0332', 'RS0384', 'RS0406', 
#                 'RS0451', 'RS0468', 'RS0548', 'RS64.0', 'RS156.0', 'RS278.0', 'RS313.0', 'RS643.0', 
#                 'RS740.0', 'RS810.0']
def write_codebook(row_tuples, fname, codewords, readout_names, codebook_style = '148MHD4'):
    with open(fname, 'w') as f:
        f.write('version'+','+str(1)+'\n')
        f.write('codebook_name'+','+codebook_style+'\n')
        f.write('bit_names,'+','.join(readout_names)+'\n')
        f.write('name, id, barcode\n')
        for row in row_tuples:
            f.write(','.join([row[0], row[1], row[2]+'\n']))



