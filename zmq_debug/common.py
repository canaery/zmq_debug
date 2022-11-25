import json
import numpy as np


class NumpyFloatValuesEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.float32):
            return float(obj)
        return json.JSONEncoder.default(self, obj)


def decode_one_channel(msg, msg_num=None, ch_num=None, channel_nums=None):
    """
    Check and decode Json message from open ephys
    :param msg:
    :param msg_num:
    :param ch_num:
    :return:
    """
    if len(msg) < 2:
        raise ValueError("no frames for message: ", msg[0])
    header = json.loads(msg[1].decode('utf-8'))
    if header['type'] != 'data':
        raise NotImplementedError('Only data allowed')
    if msg_num is not None and header['message_num'] != msg_num + 1:
        print("missing a message at number", msg_num)
    c = header['content']
    # Check that not missing channels unless this is a first or last channel
    if ch_num != 0 and ch_num != 135 and ch_num != 543 and (c['channel_num'] != ch_num + 1):
        print("missing a channel at number", ch_num)
    channel_nums.append(ch_num)
    n_arr = np.frombuffer(msg[2], dtype=np.float32)
    n_arr = np.reshape(n_arr, c['num_samples'])
    if msg_num is not None:
        if (msg_num == 10000) or (msg_num % 300000 == 0):
            print(f'Found {n_arr.size} samples and {max(channel_nums)} channels')

    return header['message_num'], c['channel_num'], c['num_samples'], int(c['sample_rate']), n_arr, channel_nums
