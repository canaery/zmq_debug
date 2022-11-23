from pathlib import Path

import matplotlib.pyplot as plt
import zmq
import numpy as np
import json

do_arithmetic = False
do_plots = False

poller = zmq.Poller()

context = zmq.Context()
data_socket = context.socket(zmq.SUB)
data_socket.connect("tcp://localhost:5556")
data_socket.setsockopt(zmq.SUBSCRIBE, b'')
poller.register(data_socket, zmq.POLLIN)
message_num = None
buffer_size = None
channel_nums = []
small_buffer = []
message_num_received = 0
big_buffer = []
channel_num = 0
n_small_buffers = 0
# plt.ion()
from time import time
time_started = time()
save_dict = {}
for i in range(136):
    save_dict[i] = []

save_json = True
timestamps = []
warmup_till = 51300


class NumpyFloatValuesEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.float32):
            return float(obj)
        return json.JSONEncoder.default(self, obj)


def decode_one_channel(msg, msg_num=None, ch_num=None):
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
    return header['message_num'], c['channel_num'], c['num_samples'], int(c['sample_rate']), n_arr


message_num_received_in_10_sec = 0
while True:
    # print(message_num_received)
    message_num_received += 1
    message_num_received_in_10_sec += 1

    # This is somehow wrong!
    # socks = dict(poller.poll(1))
    # if not socks:
    #     continue

    message = data_socket.recv_multipart()
    if message_num_received < 3e4:
        # Crucial to avoid missing packets! Must be no fewer than 25000 packets or ~8 sec warmup
        continue
    message_num, channel_num, num_samples, sample_rate, n_arr = decode_one_channel(message, message_num, channel_num)

    if message_num_received < warmup_till:
        # Collect some info about samples and channels for a second first
        n_chans = max(channel_nums) + 1
        buffer_size = n_arr.size
        size_full_buffer = n_chans * buffer_size
        n_small_buffers = 0
        final_channel_51K = channel_num
        continue

    # this part will help us catch the messages from the beginning of the samples i.e. from channel 0
    if message_num_received == warmup_till:
       if final_channel_51K < 135:
            chan_left = 135 - final_channel_51K
            warmup_till += chan_left

    now = time() - time_started
    if now > 1 and now % 1 < 0.1:
        # print(f'Received {message_num_received_in_10_sec * num_samples / n_chans} samples per channel in {now} seconds')
        print(f'Received {message_num_received_in_10_sec * num_samples / n_chans/now} samples per channel per second')
        time_started = time()
        message_num_received_in_10_sec = 0

    if (message_num == 10000) or (message_num % 300000 == 0):
        print(f'Found {n_arr.size} samples and {max(channel_nums)} channels')

    # Size check
    if buffer_size:
        if not buffer_size == n_arr.size:
            raise ValueError('Inconsistent array sizes between packets!')
    if do_arithmetic:
        np.mean(n_arr)
        np.sqrt(n_arr)

    if channel_num == 4:
        # saving the timestamps for every complete 23 samples recieved
        timestamps.append(time())
        small_buffer = []
    small_buffer.extend(n_arr)
    
    #append each channel to a dict and save after 12558 samples or 73710 message
    if save_json:
        p = save_dict[int(channel_num)]
        p.extend(n_arr)
        save_dict[int(channel_num)] = p
        # print(f"length of channel {channel_num}: ", len(p))
        if message_num_received == 73710:
            plt.hist(np.diff(timestamps),100)
            plt.show()

            import time
            time.sleep(5)
            # saving the channels in a json file
            json_object = json.dumps(save_dict, cls=NumpyFloatValuesEncoder)
            with open(Path("~/data/sample.json").expanduser(), "w+") as outfile:
                outfile.write(json_object)
            # saving the timestamps
            save_times = {"timestamps": timestamps}
            json_object_1 = json.dumps(save_times, cls=NumpyFloatValuesEncoder)
            with open("times.json", "w+") as outfile:
                outfile.write(json_object_1)
            break

    if do_plots and message_num_received > 200000:
        if message_num_received > size_full_buffer:
            if channel_num == n_chans - 1:
                arr = np.reshape(small_buffer, [n_chans, buffer_size])
                big_buffer.append(arr)
                n_small_buffers += 1
        if n_small_buffers > 5:
            big_buffer = np.hstack(big_buffer)

            # Plot big buffer
            plt.plot(big_buffer.T)
            plt.draw()
            plt.pause(0.0001)
            plt.clf()

            # Clear big buffer
            big_buffer = []
            n_small_buffers = 0

