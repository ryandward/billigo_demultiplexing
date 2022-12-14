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
