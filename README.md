### Description
This is the skin-deep version of Trimmomatic tool realised in Python 3.7.

### Getting starred and basic usage
For callig short help message:

`python3 trimmomatic_clone.py -help`

For detailed help:

`python3 trimmomatic_clone.py -h`

### Input and output format

This tool requires file in **four-line** type FASTQ format as an input file with phred33 encoding. All reads are recignised by the program as **single-end** reads. Tool return output in the same **four-line** type FASTQ format with phred33 encoding.
Output reads are written in the file with the same name, but without **'.fq'** file extension.
If you specified keeping filtered reads into separate file, the passed files store into file with **'_passed.fq'** postfix. Reads which do not pass filterig store into a separate file are stored into **'_failed.fq'** postfix.

### Optional arguments

#### Bref description

Tools could perform read trimming and / or filter the result.

Trimming options, derived from Trimmomatic:

`-crop <CUSTOM_LENGTH>` or `--crop <CUSTOM_LENGTH>`

`-headcrop <CUSTOM_NUMBER_OF_BASES>`

`-leading <CUSTOM_THRESHOLD_QUALITY>`

`-trailing <CUSTOM_THRESHOLD_QUALITY>`

`-sliding_window <CUSTOM_WINDOW_SIZE> <CUSTOM_THRESHOLD_QUALITY>`

The tools could classify results on failed and passed reads depending on length of GC-content. By default it does nothing of them.




#### Full description

Cut the read to a specified length:

`-crop <CUSTOM_LENGTH>` or `--crop <CUSTOM_LENGTH>`

Number or range of GC-content in reads for surviving. One value to indicate a lower threshold. Two values to set the minimum and maximum percentage:

`-gc <CUSTOM_BOUND_FROM> <CUSTOM_BOUND_TO>`
`-gc <CUSTOM_BOUND_FROM>`

or

`--gc_bounds <CUSTOM_BOUND_ONE> <CUSTOM_BOUND_TWO>`
`--gc_bounds <CUSTOM_BOUND_ONE>`
 
Cut the specified number of bases from the start of the read:

`-headcrop <CUSTOM_NUMBER_OF_BASES>`

Save reads that do not pass filtering into a separate file:

`-k` or `--keep_filtered`

Cut bases off the start of a read, if below a threshold quality:

`-leading <CUSTOM_THRESHOLD_QUALITY>`

Minimum read length to survive filtration:

`-min` or `--min_length`

Output reads are written in the file under the same name, but without **'.fq'** file extension. To specify the prefix of output files:
 
 `-o` or ` --output_base_name`
 
Performs a sliding window trimming approach. It starts scanning at the 5' end andclips the read once the average quality within the window falls below a threshold.First value to set window size as the number of bases.Second value to set quality threshold:

`-sliding_window <CUSTOM_WINDOW_SIZE> <CUSTOM_THRESHOLD_QUALITY>`

Cut bases off the end of a read, if below a threshold quality:

`-trailing <CUSTOM_THRESHOLD_QUALITY>`

#### Other information
Tool was written during the course of Python, when I've been a student of Bioinformatic Institute in 2019-2020. Feel free to use this code and mention this repository as a link:
https://github.com/Yulia-Yakovleva/BI_2019_Python/tree/master/PyTrimm
