import neo
from pathlib import Path
import numpy as np

from neo.core import Segment, SpikeTrain, AnalogSignal
from quantities import Hz, s
large_data = np.linspace(0, 20000, 30*1000)  # 30 sec
large_data = np.stack(list([large_data])*544).T
channel_count = large_data.shape[1]

sig = neo.AnalogSignal(list(large_data), units='uV', sampling_rate=1 * Hz)
sig.ndim
segl = Segment(index=5)
segl.analogsignals.append(sig)
segl.analogsignals[0].ndim
Path('~/oebin/continuous/').expanduser().mkdir(exist_ok=True)
Path('~/oebin/continuous/stream1/').expanduser().mkdir(exist_ok=True)

flarge_data=neo.RawBinarySignalIO(Path('~/oebin/continuous/stream1/continuous.dat').expanduser())
flarge_data.write_segment(segl)
flarge_data


from open_ephys.analysis.formats import BinaryRecording
BinaryRecording.create_oebin_file(Path('~/oebin/').expanduser(),
                                  stream_name='stream1',
                                  channel_count=channel_count,
                                  sample_rate=1000)

