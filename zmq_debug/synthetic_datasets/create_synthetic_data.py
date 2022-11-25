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

data_path = Path('~/PycharmProjects/zmq_debug/data').expanduser()
Path(data_path / 'open_ephys_data_544ch_30sec_synthetic/').mkdir(exist_ok=True)
Path(data_path / 'open_ephys_data_544ch_30sec_synthetic/Record Node 110/').mkdir(exist_ok=True)
Path(data_path / 'open_ephys_data_544ch_30sec_synthetic/Record Node 110/experiment1/').mkdir(exist_ok=True)
Path(data_path / 'open_ephys_data_544ch_30sec_synthetic/Record Node 110/experiment1/recording1/').mkdir(exist_ok=True)
Path(data_path / 'open_ephys_data_544ch_30sec_synthetic/Record Node 110/experiment1/recording1/continuous').mkdir(exist_ok=True)
full_path = data_path / 'open_ephys_data_544ch_30sec_synthetic/Record Node 110//experiment1/recording1/continuous/File_Reader-100.Rhythm_FPGA-100.0/'
full_path.mkdir(exist_ok=True)

flarge_data = neo.RawBinarySignalIO(full_path / 'continuous.dat')
flarge_data.write_segment(segl)
flarge_data

from open_ephys.analysis.formats import BinaryRecording

BinaryRecording.create_oebin_file(data_path / 'open_ephys_data_544ch_30sec_synthetic/Record Node 110/experiment1/recording1/',
                                  stream_name='Rhythm_FPGA-100.0',
                                  channel_count=large_data.shape[1],
                                  sample_rate=1000)
