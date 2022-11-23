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
message_num_received = 0
channel_num = 0
from time import time

time_started = time()
save_dict = {}
for i in range(136):
    save_dict[i] = []

save_json = True
missed = []
warmup_till = 51300
path_out = Path('~/sample.json').expanduser()

while True:
    # print(message_num_received)
    message_num_received += 1

    message = data_socket.recv_multipart()

    message_num, channel_num, num_samples, sample_rate, n_arr, channel_nums = decode_one_channel(
        message, message_num, channel_num, channel_nums)

    if (message_num == 10000) or (message_num % 300000 == 0):
        print(f'Found {n_arr.size} samples and {max(channel_nums)} channels')
        missed.append(channel_num)

    # append each channel to a dict and save after 12558 samples or 73710 message
    p = save_dict[int(channel_num)]
    p.extend(n_arr)
    save_dict[int(channel_num)] = p
    print(f"length of channel {channel_num}: ", len(p))
    print("missed message at", missed)
    if message_num_received == 74256:
        print(f"Saving sample file to {path_out}")
        # saving the channels in a json file
        json_object = json.dumps(save_dict, cls=NumpyFloatValuesEncoder)
        with open(str(path_out), "w+") as outfile:
            outfile.write(json_object)
        break
