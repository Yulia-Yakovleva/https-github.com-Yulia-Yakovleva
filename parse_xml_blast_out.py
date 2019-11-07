from Bio.Blast import NCBIXML
import csv

with open('/home/yulia/metavirome/marin_and_seawater/blast_out/parse_out.csv', 'w') as f:
    for i in range(0, 208):
        f.write("Query_Name," "Hit_id," + "Query_cover," + "Identity" + "\n")
        wr = csv.writer(f, dialect='excel')
        blast_record = NCBIXML.parse(open('/home/yulia/metavirome/marin_and_seawater/blast_out/out_blast_' +
                                          str(i) + '.xml', 'r'))
        sample_list = []
        for query in blast_record:
            query_id = query.query.split(';')[0]
            for alignment in query.alignments:
                acc = alignment.accession
                for hsp in alignment.hsps:
                    cov = hsp.align_length / query.query_length
                    ident = hsp.identities / hsp.align_length
                    sample_list.append([query_id, acc, cov, ident])
                    for item in sample_list:
                        wr.writerow(item)
