# billigo_demultiplexing
Several strategies for demultiplexing experiments from a 96-well plate using i7 adapters

Make sure conda is set up to retrieve the most current versions of cutadapt (4+)

```
conda config --add channels defaults
conda config --add channels bioconda
conda config --add channels conda-forge
conda config --set channel_priority strict
```

(Create and) activate cutadapt environment in conda

```
conda create -n cutadapt cutadapt
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

This code creates a directory called `Demux` and then processes a set of paired-end FASTQ files in that directory using the `cutadapt` tool. The code is setting up a loop to process all files ending in `R1` and `gz` in the current directory. For each of these files, the code sets up a number of environment variables:

* `forward`: the file name of the forward reads (the file ending in `R1` and `gz`)
* `reverse`: the file name of the reverse reads (the file corresponding to the forward reads, but ending in `R2` and `gz`)
* `forward_out`: the file name for the output of the cutadapt processing of the forward reads (with the `.fastq.gz` suffix removed)
* `reverse_out`: the file name for the output of the cutadapt processing of the reverse reads (with the `.fastq.gz` suffix removed)

The code then echoes a command that will be run by the cutadapt tool to process the forward and reverse reads files. The command uses the `-g` option to specify a `barcode file` called `billigos.fasta` that is used to demultiplex the reads. The output of the processing will be written to the `Demux` directory using file names derived from the input file names. 

Finally, the echoed command is written to a file called `cutadapt_demultiplex.sh`. 

After the loop finishes, the code then runs the `cutadapt_demultiplex.sh` script to actually process the files.

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
