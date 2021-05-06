# Python-Vcf-Contacts-Duplicates-Merger
Read a contacts file (.vcf). Compare datasets with identical names. Find unique data fields for each name. If same field with different content found, add another entry to the field. Create merged dataset for each name with all unique fields. Create new vcf with merged contacts (only one vCard per name).

# How to Use
1. Download or clone the source code
2. Open terminal inside the downloaded folder
3. `pip install -r requirements.txt`
4. Change `input_file_path` variable in `line 4` of file `vcf-duplicates-merger.py` to point the target vcf file.
5. `python vcf-duplicates-merger.py`
6. Output file will be created in current directory having filename prefix of `dupmerged_`. 
