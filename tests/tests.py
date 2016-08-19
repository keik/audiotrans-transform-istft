# -*- coding: utf-8 -*-

import pytest
import wave
import numpy as np
from audiotrans_transform_stft import STFTTransform
from audiotrans_transform_istft import ISTFTTransform


def test_accept_arg_of_verbose():
    ISTFTTransform(['-v'])  # no error would be raised


def test_accept_args_of_window_and_hop_sizes():

    tr = ISTFTTransform('-H 256'.split())
    stft_matrix = np.random.rand(513, 1)
    transformed = tr.transform(stft_matrix)
    print(transformed.shape)
    assert transformed.shape == (256,)

    tr = ISTFTTransform('-H 256'.split())
    stft_matrix = np.random.rand(513, 4)
    transformed = tr.transform(stft_matrix)
    print(transformed.shape)
    assert transformed.shape == (256 * 4,)

    tr = ISTFTTransform('-H 128'.split())
    stft_matrix = np.random.rand(513, 4)
    transformed = tr.transform(stft_matrix)
    assert transformed.shape == (128 * 4,)

    tr = ISTFTTransform('-H 128'.split())
    stft_matrix = np.random.rand(513, 8)
    transformed = tr.transform(stft_matrix)
    assert transformed.shape == (128 * 8,)


@pytest.mark.parametrize('buf_size, win_size, hop_size', [(1024, 1024, 256),
                                                          (160, 100, 30)])
def test_repeatedly_transform_should_be_connected_smoothly(buf_size, win_size, hop_size):

    tr_stft = STFTTransform('-w {} -H {}'.format(win_size, hop_size).split())
    tr_istft = ISTFTTransform('-H {}'.format(hop_size).split())
    wf = wave.open('tests/fixture/drums+bass.wav')
    all_data = np.fromstring(wf.readframes(wf.getnframes()), np.int16)
    stft_matrix = np.reshape([], (win_size // 2 + 1, -1))
    transformed = np.array([])
    for idx, s in enumerate(range(0, len(all_data), buf_size)):

        # STFT and cache STFT matrix
        tmp = tr_stft.transform(all_data[s:s + buf_size])
        stft_matrix = np.concatenate((stft_matrix, tmp), 1)

        # ISTFT and cache ISTFT wave
        tmp = tr_istft.transform(tmp)
        transformed = np.concatenate((transformed, tmp))

    # ISTFT on batch
    istft_wave = istft(stft_matrix, hop_size)

    # assert equal between ISTFT on batch and stream
    assert (transformed == istft_wave[:len(transformed)]).all()


def istft(stft_matrix, hop_size):
    stft_matrix = np.concatenate((stft_matrix, stft_matrix[-2:0:-1].conj()), 0)
    window_size, cols = stft_matrix.shape

    win = np.hamming(window_size)
    win_square = win ** 2

    x = np.zeros(window_size + (cols - 1) * hop_size)
    win_sum = np.zeros(window_size + (cols - 1) * hop_size)
    for col in range(cols):
        s = col * hop_size
        x[s:s + window_size] += (np.fft.ifft(stft_matrix[:, col]).real * win)
        win_sum[s:s + window_size] += win_square

    nonzero_indices = win_sum > np.spacing(1)
    x[nonzero_indices] /= win_sum[nonzero_indices]

    return x
