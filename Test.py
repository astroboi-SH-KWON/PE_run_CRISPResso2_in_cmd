import time
import os
from Bio import SeqIO
import multiprocessing as mp
import numpy as np
import platform

# import Util
# import Logic
# import LogicPrep
############### start to set env ################
WORK_DIR = os.getcwd() + "/"
PROJECT_NAME = WORK_DIR.split("/")[-2]
SYSTEM_NM = platform.system()

if SYSTEM_NM == 'Linux':
    # REAL
    REF_DIR = "../hg38/"
    DFAM_ANNO = "./input/hg38_dfam.hits"
else:
    # DEV
    REF_DIR = "D:/000_WORK/000_reference_path/human/hg38/Splited/"
    DFAM_ANNO = "D:/000_WORK/ParkJiHye/20200914/hg38_dfam.hits"

PE_PARAM = "./input/FAH_Crispresso_parameter.txt"
FASTQ_LIST = "./input/fastq_list.txt"

TOTAL_CPU = mp.cpu_count()
MULTI_CNT = int(TOTAL_CPU*0.8)
############### end setting env #################

def test():
    pe_pram = read_tsv_ignore_N_line(PE_PARAM, 0)
    fastq_pairs = read_tsv_ignore_N_line(FASTQ_LIST)

    opt = ""
    for pe_opt in pe_pram:
        opt += " --" + pe_opt[0] + " " + pe_opt[1]

    for fastq_pair in fastq_pairs:
        fastq_r1 = "./input/FASTQ/" + fastq_pair[0]
        fastq_r2 = "./input/FASTQ/" + fastq_pair[1]
        outp_dir = "./output/" + fastq_pair[2]
        if not os.path.exists(outp_dir):
            os.makedirs(outp_dir)
        run_sys_cmd('CRISPResso --fastq_r1 ' + fastq_r1 + ' --fastq_r2 ' + fastq_r2 + ' -o ' + outp_dir + opt)

def run_sys_cmd(cmd_query):
    print "query :", cmd_query
    os.system(cmd_query)

def read_tsv_ignore_N_line(path, n_line=1, deli_str="\t"):
    result_list = []
    with open(path, "r") as f:
        for ignr_line in range(n_line):
            header = f.readline()
            print(header)
        while True:
            tmp_line = f.readline().replace("\n", "")
            if tmp_line == '':
                break

            result_list.append(tmp_line.split(deli_str))
    return result_list

if __name__ == '__main__':
    start_time = time.time()
    print("start [ " + PROJECT_NAME + " ]>>>>>>>>>>>>>>>>>>")
    test()
    print("::::::::::: %.2f seconds ::::::::::::::" % (time.time() - start_time))