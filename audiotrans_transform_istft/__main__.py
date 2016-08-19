# -*- coding: utf-8 -*-

from argparse import ArgumentParser, RawTextHelpFormatter
import numpy as np
from logging import getLogger, StreamHandler, Formatter, DEBUG
from audiotrans import Transform

logger = getLogger(__package__)
handler = StreamHandler()
handler.setFormatter(Formatter('[%(asctime)s %(levelname)s %(name)s] %(message)s'))
logger.addHandler(handler)


class ISTFTTransform(Transform):

    def __init__(self, argv=[]):
        parser = ArgumentParser(
            prog='istft',
            description="""audiotrans transform module for Short-Time Fourier Transformation (ISTFT)

Transform wave array as np.ndarray shaped (1,) to ISTFT matrix as
np.ndarray shaped (1 + widnow_size/2, (len(wave) - window_size) / hop-size + 1).""",
            formatter_class=RawTextHelpFormatter)

        parser.add_argument('-v', '--verbose', dest='verbose',
                            action='store_true',
                            help='Run as verbose mode')

        parser.add_argument('-H', '--hop-size', dest='hop_size', default='256',
                            help='Hop size to FFT. Default is 256')

        args = parser.parse_args(argv)

        if args.verbose:
            logger.setLevel(DEBUG)
            logger.info('Start as verbose mode')

        self.window_size = None
        self.hop_size = int(args.hop_size)
        self.prev_remixed = np.zeros(0)
        self.prev_win_sum = np.zeros(0)

    def transform(self, stft_matrix):

        # restore symmetoric spectrum
        stft_matrix = np.concatenate((stft_matrix, stft_matrix[-2:0:-1].conj()), 0)

        if self.window_size is None:
            self.window_size = stft_matrix.shape[0]
            self.win = np.hamming(self.window_size)
            self.win_sqr = self.win ** 2

        cols = stft_matrix.shape[1]

        # initialize buffer for remixed wave and win with zeros
        x = np.zeros(self.window_size + (cols - 1) * self.hop_size)
        win_sum = np.zeros(self.window_size + (cols - 1) * self.hop_size)

        # sum previous remixed wave and window
        x[:len(self.prev_remixed)] += self.prev_remixed
        win_sum[:len(self.prev_win_sum)] += self.prev_win_sum

        # ISTFT
        for i in range(cols):
            offset = i * self.hop_size
            x[offset:offset + self.window_size] += np.fft.ifft(stft_matrix[:, i]).real * self.win
            win_sum[offset:offset + self.window_size] += self.win_sqr

        # split remixed to returns and cache for next
        x, self.prev_remixed = np.split(x, [cols * self.hop_size])
        win_sum, self.prev_win_sum = np.split(win_sum, [cols * self.hop_size])

        nonzero = win_sum > np.spacing(1)
        x[nonzero] /= win_sum[nonzero]

        logger.info('ISTFT from {} form STFT matrix to {} form wave'
                    .format(stft_matrix.shape, x.shape))

        return x
