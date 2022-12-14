# billigo_demultiplexing
Several strategies for demultiplexing experiments from a 96-well plate using i7 adapters

Make sure conda is set up to retrieve the most current versions of cutadapt (4+)

```
conda config --add channels defaults
conda config --add channels bioconda
conda config --add channels conda-forge
conda config --set channel_priority strict
```

Activate cutadapt environment in conda

```
conda activate cutadapt
```

Run cutadapt (4+) with the following settings:

```
cutadapt -j12 \
--no-indels \
-g file:billigos.fasta \
-o trimmed-R1-{name}.fastq.gz \
-p trimmed-R2-{name}.fastq.gz \
BillPlate_S66_L003_R1_001.fastq \
BillPlate_S66_L003_R2_001.fastq
```

# To do everything in a directory: 

```
mkdir Demux

for i in *R1*gz; do
    export forward=$i;
    export reverse=$(echo $forward | sed 's/R1/R2/g');
    export forward_out=${forward%%.fastq.gz}
    export reverse_out=${reverse%%.fastq.gz}
    echo cutadapt -j12 --no-indels -g file:billigos.fasta -o Demux/${forward_out}-{name}.fastq.gz -p Demux/${reverse_out}-{name}.fastq.gz $forward $reverse

done > cutadapt_demultiplex.sh

bash cutadapt_demultiplex.sh
```
