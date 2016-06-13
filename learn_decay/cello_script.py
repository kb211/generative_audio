from __future__ import print_function
from train_func import train_func

train_dir = 'cello_train'
_, w_mat_name = train_func(train_dir,
                        n_hid=1024,
                        epochs=10,
                        highest_freq=8000,
                        n_to_load=86,
                        down_sampling=True,
                        save_weights=True)


