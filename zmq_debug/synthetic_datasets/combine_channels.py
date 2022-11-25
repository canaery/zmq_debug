import neo
from pathlib import Path
import numpy as np

from neo.core import Segment, AnalogSignal
from quantities import Hz

original_data_fpath = 'data/Record Node 110/experiment1/recording1/continuous/File_Reader-100.Rhythm_FPGA-100.0/continuous.dat'
fdata = neo.RawBinarySignalIO(Path(original_data_fpath).expanduser().__str__(),
                              sampling_rate=1000.,
                              nb_channel=136
                              )

seg = fdata.read_segment(0, 0)
large_data = np.hstack((np.array(seg.analogsignals[0]), np.array(seg.analogsignals[0]), np.array(seg.analogsignals[0]),
                        np.array(seg.analogsignals[0])))
channel_count = large_data.shape[1]

sig = AnalogSignal(list(large_data), units='uV', sampling_rate=1 * Hz)
sig.ndim
segl = Segment(index=5)
segl.analogsignals.append(sig)
segl.analogsignals[0].ndim
Path('data/open_ephys_data_544ch_12sec/').expanduser().mkdir(exist_ok=True)
Path('data/open_ephys_data_544ch_12sec/Record Node 110/').expanduser().mkdir(exist_ok=True)
Path('data/open_ephys_data_544ch_12sec/Record Node 110/recording1/').expanduser().mkdir(exist_ok=True)
Path('data/open_ephys_data_544ch_12sec/Record Node 110/recording1/continuous').expanduser().mkdir(exist_ok=True)

flarge_data = neo.RawBinarySignalIO(Path(
    'data/open_ephys_data_544ch_12sec/Record Node 110/recording1/continuous').expanduser())
flarge_data.write_segment(segl)
flarge_data

from open_ephys.analysis.formats import BinaryRecording

BinaryRecording.create_oebin_file(Path('data/open_ephys_data_544ch_12sec').expanduser(),
                                  stream_name='Rhythm_FPGA-100.0',
                                  channel_count=channel_count,
                                  sample_rate=1000)
