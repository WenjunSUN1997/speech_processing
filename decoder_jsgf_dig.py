#!/usr/bin/python

from os import environ, path
from sys import stdout

from pocketsphinx import *
from sphinxbase import *

# Create a decoder with certain model

path = {'man_5bd_1':'td_corpus_digits\SNR05dB\man\seq1digit_200_files\\',
            'man_5bd_3':'td_corpus_digits\SNR05dB\man\seq3digits_100_files\\',
            'man_5bd_5':'td_corpus_digits\SNR05dB\man\seq5digits_100_files\\',
            'man_15bd_1': 'td_corpus_digits\SNR15dB\man\seq1digit_200_files\\',
            'man_15bd_3': 'td_corpus_digits\SNR15dB\man\seq3digits_100_files\\',
            'man_15bd_5': 'td_corpus_digits\SNR15dB\man\seq5digits_100_files\\',
            'man_25bd_1': 'td_corpus_digits\SNR25dB\man\seq1digit_200_files\\',
            'man_25bd_3': 'td_corpus_digits\SNR25dB\man\seq3digits_100_files\\',
            'man_25bd_5': 'td_corpus_digits\SNR25dB\man\seq5digits_100_files\\',
            'man_35bd_1': 'td_corpus_digits\SNR35dB\man\seq1digit_200_files\\',
            'man_35bd_3': 'td_corpus_digits\SNR35dB\man\seq3digits_100_files\\',
            'man_35bd_5': 'td_corpus_digits\SNR35dB\man\seq5digits_100_files\\',
            'woman_35bd_1': 'td_corpus_digits\SNR35dB\woman\seq1digit_200_files\\',
            'woman_35bd_3': 'td_corpus_digits\SNR35dB\woman\seq3digits_100_files\\',
            'woman_35bd_5': 'td_corpus_digits\SNR35dB\woman\seq5digits_100_files\\',
            'boy_35bd_1': 'td_corpus_digits\SNR35dB\\boy\seq1digit_200_files\\',
            'boy_35bd_3': 'td_corpus_digits\SNR35dB\\boy\seq3digits_100_files\\',
            'boy_35bd_5': 'td_corpus_digits\SNR35dB\\boy\seq5digits_100_files\\',
            'girl_35bd_1': 'td_corpus_digits\SNR35dB\girl\seq1digit_200_files\\',
            'girl_35bd_3': 'td_corpus_digits\SNR35dB\girl\seq3digits_100_files\\',
            'girl_35bd_5': 'td_corpus_digits\SNR35dB\girl\seq5digits_100_files\\',
            }

# Switch to JSGF grammar
def get_decoder(method, num_digit):
    config = Decoder.default_config()
    config.set_string('-hmm', 'ps_data/model/en-us')
    config.set_string('-lm', 'ps_data/lm/turtle.lm.bin')
    config.set_string('-dict', 'ps_data/lex/turtle.dic')
    decoder = Decoder(config)
    if method=='sequence':
        path1 = 'ps_data/jsgf/digit_sequence_'+num_digit+'.gram'
        path2 = 'digit_sequence_'+num_digit+'.digit_sequence_'+num_digit
        path3 = 'digit_sequence_'+num_digit+'.fsg'
        path4 = "digit_sequence_" +num_digit
        path5 = "digit_sequence_" +num_digit
        print(path1)
        print(path2)
        print(path3)
        print(path4)
        print(path5)
        jsgf = Jsgf(path1)
        rule = jsgf.get_rule(path2)
        fsg = jsgf.build_fsg(rule, decoder.get_logmath(), 7.5)
        fsg.writefile(path3)
        decoder.set_fsg(path4, fsg)
        decoder.set_search(path5)

    elif method == 'loop':
        jsgf = Jsgf('ps_data/jsgf/digit_loop.gram')
        rule = jsgf.get_rule('digit_loop.digit_loop')
        fsg = jsgf.build_fsg(rule, decoder.get_logmath(), 7.5)
        fsg.writefile('digit_loop.fsg')
        decoder.set_fsg("digit_loop", fsg)
        decoder.set_search("digit_loop")

    return decoder

def get_result(path, decoder):
    decoder.start_utt()
    stream = open(path,  'rb')
    uttbuf = stream.read(-1)
    if uttbuf:
        decoder.process_raw(uttbuf, False, True)
    else:
        print ("Error reading speech data")
        exit ()
    decoder.end_utt()
    print ('Decoding with "digit" grammar:', decoder.hyp().hypstr)
    return decoder.hyp().hypstr

def get_ref(path:dict):
    for key, value in path.items():
        ref_contant = []
        print(key, value)
        all_file_path = [value+temp for temp in os.listdir(value) if 'ref' in temp]
        for file_path in all_file_path:
            with open(file_path, 'r', encoding='utf-8') as file:
                ref_contant.append(file.readline().replace('\n', ''))

        print(ref_contant)

        with open('ref/'+key+'.ref', 'w', encoding='utf-8') as file_write:
            for ref_result in ref_contant:
                file_write.write(ref_result+'\n')

def store_result(path):
    dict_decoder = {'loop':get_decoder('loop', 'key[-1]'),
                    'sequence_1':get_decoder('sequence', '1'),
                    'sequence_3':get_decoder('sequence', '3'),
                    'sequence_5':get_decoder('sequence', '5'),}
    for key, value in path.items():
        result_contant_loop = []
        result_contant_sequence = []
        all_file_path = [value + temp for temp in os.listdir(value) if 'raw' in temp]

        for file_path in all_file_path:
            try:
                result_contant_loop.append(get_result(file_path, dict_decoder['loop']))
                result_contant_sequence.append(get_result(file_path, dict_decoder['sequence_'+key[-1]]))
            except:
                print(file_path)
                with open('wrong.txt', 'a+') as file_wrong:
                    file_wrong.write(key + '\n')

        print(result_contant_loop)
        print(result_contant_sequence)

        with open('result/'+key+'_loop.hyp', 'w', encoding='utf-8') as file_write:
            for result_cell in result_contant_loop:
                file_write.write(result_cell + '\n')

        with open('result/'+key+'_sequence.hyp', 'w', encoding='utf-8') as file_write:
            for result_cell in result_contant_sequence:
                file_write.write(result_cell + '\n')


if __name__ == '__main__':
    # raw_path = 'td_corpus_digits/SNR05dB/man/seq1digit_200_files/SNR05dB_man_seq1digit_002.raw'
    # get_result(raw_path, get_decoder('loop'))
    with open('wrong.txt', 'a+') as file_wrong:
        file_wrong.truncate(0)
    get_ref(path)
    store_result(path)