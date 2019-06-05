# coding: utf-8
# Barthelemy Caron, Clinical BioInformatics Lab, IMAGINE

# This script take the direct ouput of AnnoVar gene annotation as input.
# It will use both the *.variant_function and *.invalid_input files generated by AnnoVar to retrieve the variants and the header.
# It outputs the variants with cleaned gene-associations and associated non-coding regions, as well as the corresponding gene-based
# features and one-hot encoded non-coding regions.

#START_my_chages

# def update_intergenic(closest_gene, chrom, pos) :
#     genes = closest_gene.replace("(dist=", " ")
#     genes = genes.replace("),", " ")
#     genes = genes.replace(")", "")
#     genes = genes.split(" ")
#     if check_in_geneDB(genes[0]) == False:
#         genes[0] = 'NONE'
#     if check_in_geneDB(genes[2]) == False:
#         genes[2] = 'NONE'
#     if (genes[0] == 'NONE') and (genes[2] == 'NONE'):
#         gene_symbol = 'NOT_FOUND'
#     elif genes[0] == 'NONE':
#         gene_symbol = genes[2]
#     elif genes[2] == 'NONE':
#         gene_symbol = genes[0]
#     elif int(genes[1]) <= int(genes[3]):
#         gene_symbol = genes[0]
#     elif int(genes[3]) <= int(genes[1]):
#         gene_symbol = genes[2]
#     elif int(genes[3]) == int(genes[1]):
#         gene_symbol = genes[0]
#     return gene_symbol


def def PCHIC_update_intergenic(chrom, pos) :

    -

    return gene_symbol

#END_my_chages

def update_intronic(closest_gene, chrom, pos) :
    genes = closest_gene.split(",")
    if len(genes) >=2:
        gene_list = []
        for gene in genes:
            is_gene_present = check_in_geneDB(gene)
            if is_gene_present is True:
                gene_list.append(gene)
            if len(gene_list) >=2:
                gene_symbol = gene_list[0]
            elif len(gene_list) == 1:
                gene_symbol = gene_list[0]
            elif len(gene_list) == 0:
                gene_symbol = 'NOT_FOUND'
            elif len(genes) == 1:
                gene_symbol = genes[0]
    else:
        if check_in_geneDB(genes[0]) == True:
            gene_symbol = genes[0]
        else:
            gene_symbol = 'NOT_FOUND'
    return gene_symbol

def update_UTRs(annovar_annotation, closest_gene, chrom, pos) :
    # 1- check if annovar_annotation  is composed of both UTR5 and UTR3
    if annovar_annotation == "UTR5;UTR3":
        # if both UTR are different, one gene has to be sampled, and the corresponding annovar_annotation selected
        genes = re.split(r'\);',closest_gene)
        local_gene_list = []
        for local_gene_index, local_gene in enumerate(genes):
            local_cleaned_gene = local_gene.split("(")[0]
            if check_in_geneDB(local_cleaned_gene) is True:
                local_gene_list.append(local_cleaned_gene)
        if len(local_gene_list) >= 2:
            for local_index_2, local_gene_2 in enumerate(genes):
                local_func_pos = re.split(";", annovar_annotation)[local_index_2]
                if local_func_pos == "UTR5":
                    # compute the distance for the UTR5 variant
                    distance_1 = int(local_gene_2.split("(")[1].split(">")[0].split("-")[1][:-1])
                elif local_func_pos == "UTR3":
                    # compute the distance for the UTR3 variant
                    distance_2 = int(local_gene_2.split("(")[1].split(">")[0].split("*")[1][:-1])
            if distance_1 < distance_2:
                # if gene 1 is closer than gene 2, select gene 1
                selected_gene = local_gene_list[0]
                selected_annovar_annotation = re.split(";", annovar_annotation)[0]
            elif distance_2 < distance_1:
                # if gene 2 is closer than gene 1, select gene 2
                selected_gene = local_gene_list[1]
                selected_annovar_annotation = re.split(";", annovar_annotation)[1]
            elif distance_1 == distance_2:
                # if both distances are equal, select gene 1
                selected_gene = local_gene_list[0]
                selected_annovar_annotation = re.split(";", annovar_annotation)[0]
        elif len(local_gene_list) == 1:
            # if only one gene is protein coding, return it
            selected_gene = local_gene_list[0]
        elif len(local_gene_list) == 0:
            # if both genes were not present in the database, return 'NOT_FOUND' as gene name
            selected_gene = 'NOT_FOUND'
    # 2- If both UTR are the same, one gene has to be sampled
    elif len(re.split(r'\),',closest_gene)) > 1:
        genes = re.split(r'\),',closest_gene)
        local_gene_list = []
        for local_gene_index, local_gene in enumerate(genes):
            local_cleaned_gene = local_gene.split("(")[0]
            if check_in_geneDB(local_cleaned_gene) is True:
                local_gene_list.append(local_cleaned_gene)
        if len(local_gene_list) >= 2:
            local_position_list = []
            for local_index_2, local_gene_2 in enumerate(genes):
                if annovar_annotation == "UTR5":
                    # compute the distance for the UTR5 variant
                    distance_1 = int(local_gene_2.split("(")[1].split(">")[0].split("-")[1][:-1])
                    local_position_list.append(distance_1)
                elif annovar_annotation == "UTR3":
                    # compute the distance for the UTR3 variant
                    distance_2 = int(local_gene_2.split("(")[1].split(">")[0].split("*")[1][:-1])
                    local_position_list.append(distance_2)
            if local_position_list[0] <  local_position_list[1]:
                # if gene 1 is closer than gene 2, select gene 1
                selected_gene = local_gene_list[0]
                selected_annovar_annotation = annovar_annotation
            elif local_position_list[1] <  local_position_list[0]:
                # if gene 2 is closer than gene 1, select gene 2
                selected_gene = local_gene_list[1]
                selected_annovar_annotation = annovar_annotation
            elif local_position_list[0] == local_position_list[1]:
                # if both distances are equal, select gene 1
                selected_gene = local_gene_list[0]
                selected_annovar_annotation = annovar_annotation
        elif len(local_gene_list) == 1:
            #if only one gene is protein coding, return it
            selected_gene = local_gene_list[0]
            selected_annovar_annotation = annovar_annotation
        elif len(local_gene_list) == 0:
            #if both genes were not present in the database, return 'NOT_FOUND' as gene name
            selected_gene = 'NOT_FOUND'
            selected_annovar_annotation = annovar_annotation
    # 3- If only one gene is present, clean the name and check that it is present in geneDB
    elif len(re.split(r'\),',closest_gene)) == 1:
        if check_in_geneDB(re.split(r'\(',closest_gene)[0]) == True:
            selected_gene = re.split(r'\(',closest_gene)[0]
            selected_annovar_annotation = annovar_annotation
        else:
            selected_gene = 'NOT_FOUND'
            selected_annovar_annotation = annovar_annotation
    return selected_gene, selected_annovar_annotation

def check_in_geneDB(gene_name):
    if gene_name in geneDB_gene_names:
        return True
    else:
        return False

def get_gene_tss(gene_name_to_query):
    tss = geneDB.loc[geneDB["gene_name"] == gene_name_to_query, "tss"].values[0]
    return tss

def get_gene_tse(gene_name_to_query):
    tse = geneDB.loc[geneDB["gene_name"] == gene_name_to_query, "tse"].values[0]
    return tse

def update_updowns(annovar_annotation, closest_gene, chrom, pos):
    if len(re.split(r';', annovar_annotation)) == 1:
        # check if annotation is not upstream;dowstream, but only 'upstream' or 'downstream'
        if len(re.split(r',', closest_gene)) == 1:
            # check if only one gene is associated to the variant, if True, return the gene name
            if check_in_geneDB(closest_gene) == False:
                selected_gene = 'NOT_FOUND'
            else:
                selected_gene = closest_gene
            selected_annovar_annotation = annovar_annotation
        elif len(re.split(r',', closest_gene)) > 1:
            # check if more than two genes are associated to the variant
            genes = re.split(r',', closest_gene)
            local_gene_list = []
            for gene in genes:
                # check if the genes are present in the database
                if check_in_geneDB(gene) == True:
                    local_gene_list.append(gene)
            if len(local_gene_list) > 1:
                # if several genes are present, compute absolute SNV-tss / SNV-tse distances for all genes
                local_gene_position = []
                if annovar_annotation == "upstream":
                    # for upstream variants, get gene tss
                    for gene in local_gene_list:
                        local_gene_position.append(get_gene_tss(gene))
                elif annovar_annotation == "downstream":
                    # for downstream variants, get gene tse
                    for gene in local_gene_list:
                        local_gene_position.append(get_gene_tse(gene))
                # compute absolute distance
                distances = [abs(x - pos) for x in local_gene_position]
                try:
                    # get the closest_gene. If several are reported, np.nanargmin only returns the first
                    index_closest_gene = np.nanargmin(distances)
                    selected_gene = genes[index_closest_gene]
                    selected_annovar_annotation = annovar_annotation
                except ValueError:
                    # In case none of the genes had a tss/tse reported in the database, the first gene is returned
                    selected_gene = genes[0]
                    selected_annovar_annotation = annovar_annotation
                    pass
            elif len(local_gene_list) == 1:
                selected_gene = local_gene_list[0]
                selected_annovar_annotation = annovar_annotation
            elif len(local_gene_list) == 0:
                selected_gene = 'NOT_FOUND'
                selected_annovar_annotation = annovar_annotation
    elif len(re.split(r';', annovar_annotation)) > 1:
        anno_annotation_list = ['upstream','downstream']
        gene_list_up = re.split(r';', closest_gene)[0].split(',')
        gene_list_down = re.split(r';', closest_gene)[1].split(',')
        # for Upstream variants
        local_up_gene_list = []
        for up_gene in gene_list_up:
            # check if upstream associated gene(s) are present in the database
            if check_in_geneDB(up_gene) is True:
                local_up_gene_list.append(up_gene)
        if len(local_up_gene_list) == 1:
            # if only one gene is present in the database, it is returned as upstream selected gene
            selected_gene_up = local_up_gene_list[0]
            distance_gene_up = abs(get_gene_tss(selected_gene_up) - pos)
        elif len(local_up_gene_list) == 0:
            # if no genes are present in the database, 'NOT_FOUND' is returned
            selected_gene_up = 'NOT_FOUND'
            distance_gene_up = np.nan
        elif len(local_up_gene_list) > 1:
            # if several upstream genes are present in the database, tss-SNV distances are computed
            local_up_gene_position = []
            for gene in local_up_gene_list:
                local_up_gene_position.append(get_gene_tss(gene))
            distances = [abs(x - pos) for x in local_up_gene_position]
            try:
                # get the closest_gene. If several are reported, np.nanargmin only returns the first
                index_closest_gene = np.nanargmin(distances)
                selected_gene_up = local_up_gene_list[index_closest_gene]
                distance_gene_up = np.nanmin(distances)
            except ValueError:
                # In case none of the genes had a tss/tse reported in the database, the first gene is returned
                selected_gene_up = local_up_gene_list[0]
                distance_gene_up = np.nan
                pass
        # for Downstream variants
        local_down_gene_list = []
        for down_gene in gene_list_down:
            if check_in_geneDB(down_gene) is True:
                local_down_gene_list.append(down_gene)
        if len(local_down_gene_list) == 1:
            selected_gene_down = local_down_gene_list[0]
            distance_gene_down = abs(get_gene_tse(selected_gene_down) - pos)
        elif len(local_down_gene_list) == 0:
            selected_gene_down = 'NOT_FOUND'
            distance_gene_down = np.nan
        elif len(local_down_gene_list) > 1:
            local_down_gene_position = []
            for gene in local_down_gene_list:
                local_down_gene_position.append(get_gene_tse(gene))
            distances = [abs(x - pos) for x in local_down_gene_position]
            try:
                # get the closest_gene. If several are reported, np.nanargmin only returns the first
                index_closest_gene = np.nanargmin(distances)
                selected_gene_down = local_down_gene_list[index_closest_gene]
                distance_gene_down = np.nanmin(distances)
            except ValueError:
                # In case none of the genes had a tss/tse reported in the database, the first gene is returned
                selected_gene_down = local_down_gene_list[0]
                distance_gene_down = np.nan
                pass
        # aggregate upstream and downstream selected genes and distances are gathered
        selected_updown = [selected_gene_up, selected_gene_down]
        selected_updown_distance = [distance_gene_up, distance_gene_down]
        # if both genes are reported as 'NOT_FOUND', 'NOT_FOUND' is returned
        if selected_updown[0] == 'NOT_FOUND' and selected_updown[1] == 'NOT_FOUND':
            selected_gene = 'NOT_FOUND'
            selected_annovar_annotation = 'NOT_FOUND'
        # if one of the reported gene is 'NOT_FOUND', the other is selected.
        elif selected_updown[0] == 'NOT_FOUND':
            selected_gene = selected_updown[1]
            selected_annovar_annotation = 'downstream'
        elif selected_updown[1] == 'NOT_FOUND':
            selected_gene = selected_updown[0]
            selected_annovar_annotation = 'upstream'
        # if two genes are available, the closest will be determined through the distance.
        # if both distances could not be computed, the first gene is selected
        # (and the corresponding genomic region)
        else:
            try:
                selected_gene = selected_updown[np.nanargmin(selected_updown_distance)]
                selected_annovar_annotation = anno_annotation_list[np.nanargmin(selected_updown_distance)]
            except ValueError:
                selected_gene = selected_updown[0]
                selected_annovar_annotation = anno_annotation_list[0]
    if check_in_geneDB(selected_gene) == False:
        selected_gene = 'NOT_FOUND'
    return selected_gene, selected_annovar_annotation

def one_hot_encoding(annovar_annotation_to_encode):
    d = {'UTR3': [0], 'UTR5': [0], 'upstream': [0], 'downstream': [0], 'intronic': [0], 'intergenic': [0]}
    df = pd.DataFrame(data=d)
    if annovar_annotation_to_encode in ['UTR3', 'UTR5','downstream','intergenic','intronic', 'upstream']:
        df['{}'.format(annovar_annotation_to_encode)] = 1
    else:
        print("provided annovar_annotation is not standard", annovar_annotation_to_encode)
    return df.values[0]

import numpy as np
import pandas as pd
import re, sys

argvL = sys.argv
inF = argvL[1]
inF_header = argvL[2]
outF = argvL[3]

# Load the gene database containing the gene-based features, and create a 'NOT_FOUND' gene entry, to allow the annotation of all variants.
geneDB = pd.read_csv("NCBoost_data/NCBoost_geneDB.tsv", sep='\t', delimiter=None,  dtype={"chr":"unicode"}, header=0)
not_found_gene = pd.DataFrame([['NOT_FOUND']+ ['NA'] * (len(geneDB.columns.values)-1)], columns=geneDB.columns.values)
geneDB = geneDB.append(not_found_gene)
geneDB.chr = geneDB.chr.str.replace("chr","")
geneDB_gene_names = geneDB.gene_name.unique()
gene_annotations = [ 'gene_type', 'pLI', 'familyMemberCount', 'ncRVIS', 'ncGERP', 'RVIS_percentile', 'slr_dnds', 'GDI', 'gene_age']
context_features = ['UTR3', 'UTR5','downstream','intergenic','intronic', 'upstream']

#START_my_chages
# Load the PCHIC table to retrive the genes releted to intergenic position





#END_my_chages


header = pd.read_csv("{}".format(inF_header), sep='\t', delimiter=None, header=None)
common_header = header.loc[0,0:4].values
extra_header = header.loc[0,5:len(header.loc[0,].values)].values
non_SNV_count = 0

with open(inF, 'r') as f, open(outF, 'w') as fo:
    # write header
    fo.write("chr\tpos\tref\talt\tannovar_annotation\tclosest_gene_name\t%s\n" % ('\t'.join((gene_annotations + context_features + extra_header.tolist()))))
    exonic_count = 0
    retained_count = 0
    for index, l in enumerate(f):
        t = l.rstrip().split('\t')
        annovar_annotation = t[0]
        closest_gene_name = t[1]
        chrom = t[2].replace('chr', '')
        pos = int(float(t[3]))
        ref = t[5]
        alt = t[6]
        rest = t[7:]
        if ((len(ref) > 1) or (len(alt) > 1)):
            non_SNV_count += 1
            pass
        else:
            retained_count += 1
            if any(re.findall(r'exonic|splicing|ncRNA', annovar_annotation, re.IGNORECASE)):
              exonic_count += 1
              pass
            elif annovar_annotation == 'intergenic':
                #START_my_chages
                #updated_gene = update_intergenic(closest_gene_name, chrom, pos)
                updated_gene = PCHIC_update_intergenic(chrom, pos)
                #END_my_chages
                local_gene_annotations = geneDB.loc[geneDB["gene_name"] == updated_gene].iloc[0,4:].values
                encoded_regions = one_hot_encoding(annovar_annotation)
                fo.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % (chrom, pos, ref, alt, annovar_annotation, updated_gene,'\t'.join(str(x) for x in (list(local_gene_annotations) + list(encoded_regions) + rest))))
            elif any(re.findall(r'downstream|upstream', annovar_annotation, re.IGNORECASE)):
                updated_gene, updated_annovar_annotation = update_updowns(annovar_annotation, closest_gene_name, chrom, pos)
                local_gene_annotations = geneDB.loc[geneDB["gene_name"] == updated_gene].iloc[0,4:].values
                encoded_regions = one_hot_encoding(updated_annovar_annotation)
                fo.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % (chrom, pos, ref, alt, updated_annovar_annotation, updated_gene,'\t'.join(str(x) for x in (list(local_gene_annotations) + list(encoded_regions) + rest))))
            elif annovar_annotation == 'intronic':
                updated_gene = update_intronic(closest_gene_name, chrom, pos)
                local_gene_annotations = geneDB.loc[geneDB["gene_name"] == updated_gene].iloc[0,4:].values
                encoded_regions = one_hot_encoding(annovar_annotation)
                fo.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % (chrom, pos, ref, alt, annovar_annotation, updated_gene,'\t'.join(str(x) for x in (list(local_gene_annotations) + list(encoded_regions) + rest))))
            elif any(re.findall(r'UTR5|UTR3', annovar_annotation, re.IGNORECASE)):
                updated_gene, updated_annovar_annotation = update_UTRs(annovar_annotation, closest_gene_name, chrom, pos)
                local_gene_annotations = geneDB.loc[geneDB["gene_name"] == updated_gene].iloc[0,4:].values
                encoded_regions = one_hot_encoding(updated_annovar_annotation)
                fo.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % (chrom, pos, ref, alt, updated_annovar_annotation, updated_gene,'\t'.join(str(x) for x in (list(local_gene_annotations) + list(encoded_regions) + rest))))
    print('{} exonic/splicing/ncRNA associated positions have been removed'.format(exonic_count))
    print('{} positions have been retained, among {} total lines'.format(retained_count-exonic_count, index+1))
    print('{} non-SNV have been removed.'.format(non_SNV_count))
    print('saving in {}'.format(outF))
