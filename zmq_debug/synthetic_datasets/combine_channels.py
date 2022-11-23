import neo
from pathlib import Path
import numpy as np

from neo.core import Segment, SpikeTrain, AnalogSignal
from quantities import Hz, s
#neo.OpenEphysIO(Path('~/data/2022-10-20_11-45-33/Record Node 110/experiment1/recording1/continuous/File_Reader-100.Rhythm_FPGA-100.0/continuous.dat').expanduser().__str__()).read()
fdata=neo.RawBinarySignalIO(Path('~/data/2022-10-20_11-45-33/Record Node 110/experiment1/recording1/continuous/File_Reader-100.Rhythm_FPGA-100.0/continuous.dat').expanduser().__str__(),
                            sampling_rate=1000.,
                            nb_channel=136
                            )

seg=fdata.read_segment(0,0)
large_data= np.hstack((np.array(seg.analogsignals[0]),np.array(seg.analogsignals[0]),np.array(seg.analogsignals[0]),np.array(seg.analogsignals[0])))
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

