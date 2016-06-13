import os.path
from audio_preprocessing.cconfig import config
from audio_preprocessing.pipeline import load_matrix, AudioPipeline
from learn_decay.lstm_utils import create_lstm_network


def train_func(train_dir, matrix_file='', n_hid=1024, epochs=100, batch_size=10,
               n_to_load=1, highest_freq=5000, clip_len=2, mat_dirs=None, chunks_per_sec=4,
               down_sampling=False, root_to_folder='/instrument_samples/'):

    if matrix_file is '':
        matrix_file = train_dir
    dpath = config.datapath + root_to_folder + train_dir
    fpath = dpath + matrix_file + '.npy'

    d_mat_name = '/' + matrix_file + '_' + str(n_to_load) + 'files_'
    if down_sampling:
        d_mat_name = d_mat_name + str(chunks_per_sec) + 'res_'
        d_mat_name = d_mat_name + str(highest_freq) + 'maxf'
    else:
        d_mat_name = d_mat_name + 'raw'

    # see if matrix file exists
    if not os.path.isfile(fpath):
        # if not, create it from data
        dpath = config.datapath + root_to_folder + train_dir
        if os.path.isdir(dpath):
            audios = AudioPipeline((root_to_folder + train_dir), n_to_load=n_to_load, highest_freq=highest_freq,
                                   clip_len=clip_len, mat_dirs=mat_dirs, chunks_per_sec=chunks_per_sec,
                                   down_sampling=down_sampling)

            audios.create_train_matrix(f_name_out=d_mat_name)
        else:
            print('both entered paths are invalid. No data loaded')
            return

    x_data, y_data = load_matrix(root_to_folder + train_dir + '/', d_mat_name)
    num_frequency_dimensions = x_data.shape[2]

    # create model
    model = create_lstm_network(num_frequency_dimensions, n_hid)
    print(model.summary())
    print('Start Training')
    model.fit(x_data, y_data, batch_size=batch_size, nb_epoch=epochs, verbose=1, validation_split=0.0)

    print('Training complete')
    w_mat_name = d_mat_name + '_' + str(n_hid) + 'hid_' + str(epochs) + 'ep'
    model_output = config.datapath + '/weight_matrices/' + w_mat_name
    model.save_weights(model_output, overwrite=True)



# train_dir = 'cello_train'
# train_func(train_dir, n_hid=10, epochs=1, n_to_load=10, down_sampling=True)