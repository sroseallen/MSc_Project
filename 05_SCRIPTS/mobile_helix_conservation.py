from Bio import AlignIO
import pandas as pd
from matplotlib import pyplot as plt

def plot_insertion(start, end, save_path, alignment_path = "./01_DATA/Amidase_3/04_Multiple_Alignment/alignment_3_thresh1.0.fa"):
    alignment = AlignIO.read(alignment_path, "fasta")
    insertion_region = list(range(start, end))

    # write sequence annotations into dataframe
    df = pd.DataFrame({
        "taxid": [],
        "family": [],
        "genus_species":[],
        "amr_phylum":[],
        "full_name":[],
        "gram_status":[],
        "occupancy": []
    })

    for seq in alignment:
        seq_occupancy = 0
        seq_split = seq.description.split(":")
        # quantify the number of occuped (non-gap) columns in the region
        for pos in insertion_region:
            if seq[pos-1] != '-':
                seq_occupancy += 1
        # add this as a new annotation to the species name
        seq_split.append(int(seq_occupancy))
        # read annotation into the initialised dataframe above
        seq_split = pd.DataFrame([seq_split], columns=df.columns)
        df = pd.concat([df, seq_split], ignore_index=True)

    # reformat for plotting: gram staining status 
    df_grouped = df.groupby(["occupancy","gram_status"]).size().reset_index(name="count")
    df_grouped["occupancy"] = df_grouped["occupancy"].astype("int64")
    for num in range((end-start)+2):
        df_grouped = pd.concat([df_grouped, pd.DataFrame([{"occupancy":num, "gram_status":"NA", "count":0}])])
    df_plotting = df_grouped.pivot_table(index="occupancy", columns="gram_status", values='count', fill_value=0).reset_index()

    # stacked bar chart for raw counts
    df_plotting.plot(x='occupancy', kind='bar', stacked=True)
    plt.title('Conservation across region, Raw Counts')
    plt.xlabel('Number of non-gap columns')
    plt.ylabel('Number of species')
    plt.xticks(rotation=0, ha='center')
    plt.tight_layout()
    plt.savefig(save_path)

print ("Now plotting region 1...")
plot_insertion(10, 45, save_path="./01_DATA/Amidase_3/05_1_Region_Conservation/I1_region.png") #I-1
print ("Now plotting region 2...")
plot_insertion(68, 75, save_path="./01_DATA/Amidase_3/05_1_Region_Conservation/I2_region.png") #I-2
print ("Now plotting region 3...")
plot_insertion(90, 106, save_path="./01_DATA/Amidase_3/05_1_Region_Conservation/I3_region.png") #I-3
print ("Now plotting region 4...")
plot_insertion(130, 140, save_path="./01_DATA/Amidase_3/05_1_Region_Conservation/I4_region.png") #I-4
print ("Now plotting region 5...")
plot_insertion(145, 145, save_path="./01_DATA/Amidase_3/05_1_Region_Conservation/I5_region.png") #I-5
print ("Now plotting region 6...")
plot_insertion(149, 220, save_path="./01_DATA/Amidase_3/05_1_Region_Conservation/I6_region.png") #I-6
print ("Now plotting region 7...")
plot_insertion(234, 267, save_path="./01_DATA/Amidase_3/05_1_Region_Conservation/I7_region.png") #I-7
print ("Now plotting region 8...")
plot_insertion(314, 351, save_path="./01_DATA/Amidase_3/05_1_Region_Conservation/I8_region.png") #I-8
print ("Plots saved!")


from Bio import AlignIO
import pandas as pd
from matplotlib import pyplot as plt

# initialise dictionary for fingerprints
fingerprints = {}
id=0
for seq in AlignIO.read("./01_DATA/Amidase_3/04_Multiple_Alignment/alignment_3_thresh1.0.fa", "fasta"):
    unique_key = str(id) + ":" + seq.description
    fingerprints[unique_key] = []
    id +=1

# create region fingerprint for each sequence
def region_fingerprint(start, end, region_length, alignment_path = "./01_DATA/Amidase_3/04_Multiple_Alignment/alignment_3_thresh1.0.fa"):
    alignment = AlignIO.read(alignment_path, "fasta")
    insertion_region = list(range(start, end))
    id=0

    for seq in alignment:
        seq_occupancy = 0
        unique_key = str(id) + ":" + seq.description
        # quantify the number of occuped (non-gap) columns in the region
        for pos in insertion_region:
            if seq[pos-1] != '-':
                seq_occupancy += 1
        # if occupancy more than 50%, consider species to have the insertion, add to fingerprint
        if seq_occupancy/region_length >= 0.5:
            #sufficient occupancy in alignment: insertion region present
            fingerprints[unique_key].append(1)
        elif seq_occupancy/region_length < 0.5:
            #not enough occupancy: no insertion region
            fingerprints[unique_key].append(0)
        id+=1

print ("Creating fingerprinting dictionary...")
region_fingerprint(10, 45, 36, alignment_path = "./01_DATA/Amidase_3/04_Multiple_Alignment/alignment_3_thresh1.0.fa") #I-1
region_fingerprint(68, 75, 8, alignment_path = "./01_DATA/Amidase_3/04_Multiple_Alignment/alignment_3_thresh1.0.fa") #I-2
region_fingerprint(90, 106, 17, alignment_path = "./01_DATA/Amidase_3/04_Multiple_Alignment/alignment_3_thresh1.0.fa") #I-3
region_fingerprint(130, 140, 11, alignment_path = "./01_DATA/Amidase_3/04_Multiple_Alignment/alignment_3_thresh1.0.fa") #I-4
region_fingerprint(145, 145, 1, alignment_path = "./01_DATA/Amidase_3/04_Multiple_Alignment/alignment_3_thresh1.0.fa") #I-5
region_fingerprint(149, 220, 72, alignment_path = "./01_DATA/Amidase_3/04_Multiple_Alignment/alignment_3_thresh1.0.fa") #I-6
region_fingerprint(234, 267, 34, alignment_path = "./01_DATA/Amidase_3/04_Multiple_Alignment/alignment_3_thresh1.0.fa") #I-7
region_fingerprint(314, 351, 38, alignment_path = "./01_DATA/Amidase_3/04_Multiple_Alignment/alignment_3_thresh1.0.fa") #I-8

# this should give a dictionary of 26661 key-value pairs, where each key is the species and each value is a list of 8 0/1 values 
# where 0 indicates no insertion, and 1 indicates the insertion is present
import json
with open ("./01_DATA/Amidase_3/05_1_Region_Conservation/fingerprints.json", "w") as file:
    json.dump(fingerprints, file)
print ("Fingerprints saved!")

# to go here: code that clusters species into groups based on having the same binary fingerprint
## re-reading the dictionary
with open("./01_DATA/Amidase_3/05_1_Region_Conservation/fingerprints.json", "r") as file:
    fingerprints = json.load(file)