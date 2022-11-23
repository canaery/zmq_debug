import zmq
import json
import numpy as np
import pandas as pd

do_arithmetic = True
do_plots = False

poller = zmq.Poller()

context = zmq.Context()
data_socket = context.socket(zmq.SUB)
data_socket.connect("tcp://localhost:5556")
data_socket.setsockopt(zmq.SUBSCRIBE, b'')
poller.register(data_socket, zmq.POLLIN)
message_num = None
debug = True
buffer_size = None
channel_nums = []
secondly = []
message_num_received = 0
big_buffer = []
channel_num = 0
n_small_buffers = 0


def consume(url, source):
    ctx = zmq.Context()
    s = ctx.socket(zmq.PULL)
    s.connect(url)

    while True:
        socks = dict(poller.poll(1))
        if not socks:
            continue

        message = data_socket.recv_multipart(zmq.NOBLOCK)
        df = decode_one_channel(message)

        source.emit(df)
    s.close()


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
    channel_nums.append(ch_num)
    n_arr = np.frombuffer(msg[2], dtype=np.float32)
    n_arr = np.reshape(n_arr, c['num_samples'])
    # df = pd.DataFrame({'message_num': header['message_num'], 'data': n_arr,'channel_num': c['channel_num']})
    df = pd.DataFrame({'data': n_arr})
    return df


if __name__ == '__main__':
    from reporter_multithreaded import consume, decode_one_channel
    import numpy as np
    from collections import deque
    from streamz import Stream
    from threading import Thread

    from holoviews.streams import Pipe, Buffer
    import holoviews as hv
    import pandas as pd
    hv.extension('bokeh')

    source = Stream()

    out_url ="tcp://localhost:3557"

    consumer = Thread(target=consume, args=(out_url, source))
    consumer.start()

    buffered = source.buffer(500000)

    buffered.sink(print)
    # Prints a non-blocking stream

    results = deque(maxlen=100000)
    # buffered.map(lambda x: print(decode_one_channel(x)['message_num']))


    consumer.join()
