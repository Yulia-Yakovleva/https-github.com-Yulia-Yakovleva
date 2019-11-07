from Bio.Blast.Applications import NcbiblastpCommandline
import glob

faa_files = glob.glob("/Bmo/jyakovleva/metavirome/marine_and_seawater_metagenome/domtblout_to_prot/*.fasta")
for pth in faa_files:
    ind = faa_files.index(pth)
    my_cmd = NcbiblastpCommandline(query=pth, db="/Bmo/ncbi_nr_database/nr",
                                   num_alignments=5, outfmt=5,
                                   out='out_blast_' + str(ind) + '.xml', num_threads=16)
    print(my_cmd)
    stdout, stderr = my_cmd()