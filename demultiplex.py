import sys
import os
import glob
import re
import subprocess
from collections import defaultdict
from rich.progress import track
from rich.console import Console

console = Console()

def load_adapters(adapter_file):
    adapters = []
    with open(adapter_file) as f:
        for line in f:
            if not line.startswith(">"):
                adapters.append("^" + line.strip())
    return "file:" + adapter_file

def demultiplex(adapter_file, adapter_in_read, input_dir=".", output_dir="demultiplexed"):
    os.makedirs(output_dir, exist_ok=True)

    adapter_sequences = load_adapters(adapter_file)
    r1_files = glob.glob(f"{input_dir}/*_R1_001.fastq.gz")

    # Group files by lane
    lanes = defaultdict(list)
    for r1_file in r1_files:
        lane = re.search("_L\d{3}_", r1_file).group(0)
        lanes[lane].append(r1_file)

    for lane, files in lanes.items():
        for r1_file in track(files, description="Processing files..."):
            r2_file = r1_file.replace("_R1_001.fastq.gz", "_R2_001.fastq.gz")
            prefix = os.path.splitext(os.path.basename(r1_file))[0].replace("_R1_001", "")
            sample_name = prefix.split("_")[0]
            lane_number = re.search("L\d{3}", lane).group(0)

            console.print(f"Demultiplexing {sample_name} on Lane {lane_number}")

            if adapter_in_read == "read1":
                cutadapt_command = [
                    "cutadapt",
                    "--action=none",
                    "-g", f"^{adapter_sequences}",
                    "-j", "12", "--no-indels", "--error-rate=0",
                    "-o", f"{output_dir}/{prefix}_{{name}}_R1.fastq.gz",
                    "-p", f"{output_dir}/{prefix}_{{name}}_R2.fastq.gz",
                    r1_file,
                    r2_file
                ]
            elif adapter_in_read == "read2":
                cutadapt_command = [
                    "cutadapt",
                    "--action=none",
                    "-g", f"^{adapter_sequences}",
                    "-j", "12", "--no-indels", "--error-rate=0",
                    "-o", f"{output_dir}/{prefix}_{{name}}_R2.fastq.gz",
                    "-p", f"{output_dir}/{prefix}_{{name}}_R1.fastq.gz",
                    r2_file,
                    r1_file
                ]

            result = subprocess.run(cutadapt_command, check=True, capture_output=True, text=True)
            console.print(result.stdout)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        console.print("Usage: python demultiplex.py <adapter_file.fasta> <read1|read2>")
        sys.exit(1)

    adapter_file = sys.argv[1]
    adapter_in_read = sys.argv[2]

    if adapter_in_read not in ("read1", "read2"):
        console.print("Error: Second argument must be either 'read1' or 'read2'")
        sys.exit(1)

    demultiplex(adapter_file, adapter_in_read)
