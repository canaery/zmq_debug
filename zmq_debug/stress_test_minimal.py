import json
from pathlib import Path

import zmq
from common import decode_one_channel, NumpyFloatValuesEncoder

poller = zmq.Poller()

context = zmq.Context()
data_socket = context.socket(zmq.SUB)
data_socket.connect("tcp://localhost:5556")
data_socket.setsockopt(zmq.SUBSCRIBE, b'')
poller.register(data_socket, zmq.POLLIN)
message_num = None
channel_nums = []
channel_num = 0

save_dict = {}
for i in range(136):
    save_dict[i] = []

missed_channels = []
missed_messages = []
path_out = Path('~/PycharmProjects/zmq_debug/zmq_data').expanduser()

fname = input('Please enter the folder name which you are streaming with open-ephys, eg 2022-10-20_11-45-33')
# fname = 'open_ephys_data_544ch_30sec_synthetic'
conditions = input('Please enter info about streaming conditions, eg stream_first')
# conditions = 'stream_first'

for message_num_received in range(74256):

    message = data_socket.recv_multipart()

    message_num, channel_num, num_samples, sample_rate, n_arr, channel_nums = decode_one_channel(
        message, message_num, channel_num, channel_nums)
    if message_num_received == 0:
        print(f'First message_num in header I received is {message_num}')

    header = json.loads(message[1].decode('utf-8'))
    # Check that not missing channels unless this is a first or last channel
    if channel_num != 0 and channel_num != 135 and channel_num != 543 and (header['content']['channel_num'] !=
                                                                           channel_num + 1):
        missed_channels.append(channel_num)
    if message_num is not None and json.loads(message[1].decode('utf-8'))['message_num'] != message_num + 1:
        missed_messages.append(message_num)

    # append each channel to a dict and save after 12558 samples or 73710 message
    p = save_dict[int(channel_num)]
    p.extend(n_arr)
    save_dict[int(channel_num)] = p


print(f"Saving sample file to {path_out}")
# saving the channels in a json file
json_object = json.dumps(save_dict, cls=NumpyFloatValuesEncoder)
with open(str(path_out / f'{fname}`{conditions}`_stress_test_minimal.json'), "w+") as outfile:
    outfile.write(json_object)
with open(str(path_out / f'{fname}`{conditions}`_stress_test_minimal_missed.json'), "w+") as outfile:
    outfile.write(str(missed_messages + missed_channels))

