#!/usr/bin/python

from os import environ, path


from pocketsphinx import *
from sphinxbase import *

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

def get_decoder():
  # Create a decoder with certain model
  config = Decoder.default_config()
  config.set_string('-hmm',  'ps_data/model/en-us')
  config.set_string('-lm',   'ps_data/lm/en-us.lm.bin')
  config.set_string('-dict', 'ps_data/lex/cmudict-en-us.dict')

  # Decode streaming data.
  decoder = Decoder(config)
  decoder.start_utt()
  return decoder

def get_result(path, decoder):
  stream = open(path, 'rb')
  while True:
    buf = stream.read(1024)
    if buf:
      decoder.process_raw(buf, False, False)
    else:
      break
  decoder.end_utt()

  hypothesis = decoder.hyp()
  logmath = decoder.get_logmath()
  print ('Best hypothesis: ', hypothesis.hypstr, " model score: ", hypothesis.best_score, " confidence: ", logmath.exp(hypothesis.prob))

  print ('Best hypothesis segments: ', [seg.word for seg in decoder.seg()])

  # Access N best decodings.
  print ('Best 10 hypothesis: ')
  for best, i in zip(decoder.nbest(), range(10)):
      print (best.hypstr, best.score)

  return hypothesis.hypstr

def store_result():
  decoder = get_decoder()
  for key, value in path.items():
    result = []
    all_file_path = [value + temp for temp in os.listdir(value) if 'raw' in temp]

    for file_path in all_file_path:
      try:
        result.append(get_result(file_path, decoder))
      except:
        print(file_path)
        with open('wrong_ngram.txt', 'a+') as file_wrong:
          file_wrong.write(file_path + '\n')

    with open('result/' + key + '_ngram.hyp', 'w', encoding='utf-8') as file_write:
      for result_cell in result:
        file_write.write(result_cell + '\n')


if __name__ == '__main__':
  store_result()


