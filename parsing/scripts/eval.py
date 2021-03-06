"""Evaulate a parser.

Usage:
  eval.py -i <file> [-n <n>] [-m <n>]
  eval.py -h | --help

Options:
  -i <file>     Parsing model file.
  -n <n>        Eval the first n sentences [default: inf].
  -m <n>        Eval only sentences of length at most m [default: inf].
  -h --help     Show this screen.
"""
from docopt import docopt
import pickle
import sys

from corpus.ancora import SimpleAncoraCorpusReader

from parsing.util import spans


def progress(msg, width=None):
    """Ouput the progress of something on the same line."""
    if not width:
        width = len(msg)
    print('\b' * width + msg, end='')
    sys.stdout.flush()


if __name__ == '__main__':
    opts = docopt(__doc__)

    print('Loading model...')
    filename = opts['-i']
    f = open(filename, 'rb')
    model = pickle.load(f)
    f.close()
    # if we want to eval all sentences, `n` arg must be `inf`
    n = float(opts['-n'])
    # same for sentences length
    m = float(opts['-m'])
    print('Loading corpus...')
    files = '3LB-CAST/.*\.tbf\.xml'
    corpus = SimpleAncoraCorpusReader('ancora/ancora-2.0/', files)
    parsed_sents = [ps for ps in corpus.parsed_sents() if len(ps.leaves()) <= m]

    print('Parsing...')
    hits, total_gold, total_model = 0, 0, 0
    unl_hits, unl_total_gold, unl_total_model = 0, 0, 0
    other_n = len(parsed_sents)
    format_str = '{:3.1f}% ({}/{}) (P={:2.2f}%, R={:2.2f}%, F1={:2.2f}%)'
    progress(format_str.format(0.0, 0, n, 0.0, 0.0, 0.0))
    for i, gold_parsed_sent in enumerate(parsed_sents):
        tagged_sent = gold_parsed_sent.pos()

        # parse
        model_parsed_sent = model.parse(tagged_sent)

        # compute labeled scores
        gold_spans = spans(gold_parsed_sent, unary=False)
        model_spans = spans(model_parsed_sent, unary=False)
        hits += len(gold_spans & model_spans)
        total_gold += len(gold_spans)
        total_model += len(model_spans)
        # compute unlabeled scores
        unl_gold_spans = set([p[1:] for p in gold_spans])
        unl_model_spans = set([p[1:] for p in model_spans])
        unl_hits += len(unl_gold_spans & unl_model_spans)
        unl_total_gold += len(unl_gold_spans)
        unl_total_model += len(unl_model_spans)
        # compute labeled partial results
        prec = float(hits) / total_model * 100
        rec = float(hits) / total_gold * 100
        f1 = 2 * prec * rec / (prec + rec)
        # compute unlabeled partial results
        unl_prec = unl_hits / unl_total_model * 100
        unl_rec = unl_hits / unl_total_gold * 100
        unl_f1 = 2 * unl_prec * unl_rec / (unl_prec + unl_rec)
        progress(format_str.format(float(i+1) * 100 /
                                   other_n, i+1, other_n, prec, rec, f1))

        if i > n - 2:
            break

    print('')
    print('Parsed {} sentences'.format(other_n))
    print('Labeled')
    print('  Precision: {:2.2f}% '.format(prec))
    print('  Recall: {:2.2f}% '.format(rec))
    print('  F1: {:2.2f}% '.format(f1))

    print('')
    print('Parsed {} sentences'.format(other_n))
    print('Unlabeled')
    print('  Precision: {:2.2f}% '.format(unl_prec))
    print('  Recall: {:2.2f}% '.format(unl_rec))
    print('  F1: {:2.2f}% '.format(unl_f1))
