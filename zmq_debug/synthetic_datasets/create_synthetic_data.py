import neo
from pathlib import Path
import numpy as np

from neo.core import Segment, AnalogSignal
from quantities import Hz, s

large_data = np.linspace(0, 20000, 30 * 1000).astype('float32')  # 30 sec
large_data = np.stack(list([large_data]) * 544).T

sig = AnalogSignal(list(large_data), units='uV', sampling_rate=1 * Hz)
sig.ndim
segl = Segment(index=5)
segl.analogsignals.append(sig)
segl.analogsignals[0].ndim
Path('data/open_ephys_data_544ch_30sec_synthetic/').expanduser().mkdir(exist_ok=True)
Path('data/open_ephys_data_544ch_30sec_synthetic/continuous/').expanduser().mkdir(exist_ok=True)
Path('data/open_ephys_data_544ch_30sec_synthetic/continuous/stream1/').expanduser().mkdir(exist_ok=True)

flarge_data = neo.RawBinarySignalIO(
    Path('data/open_ephys_data_544ch_30sec_synthetic/continuous/stream1/continuous.dat').expanduser())
flarge_data.write_segment(segl)
flarge_data

from open_ephys.analysis.formats import BinaryRecording

BinaryRecording.create_oebin_file('data/open_ephys_data_544ch_30sec_synthetic/',
                                  stream_name='stream1',
                                  channel_count=large_data.shape[1],
                                  sample_rate=1000)
