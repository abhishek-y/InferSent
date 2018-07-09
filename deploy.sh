#!/bin/bash
nohup python -u train_nli.py --glovec_path='/mnt/data/abhishek.y/Datasets/token_vec_all_big_30k_num_100d.txt' --nlipath="mydataset/all_num_30k_big/" --outputdir='savedir_all_big_num_eudot/encoder_steps/test1/' --outputmodelname='all_big_num_eudot.model.pickle' --cont_path='savedir_all_big_num_eudot/encoder_steps/test1/all_big_num_eudot.model.pickle' --word_emb_dim=100 --n_epochs=20 --batch_size=64 --dpout_model=0. --dpout_fc=0.3 --nonlinear_fc=1 --optimizer="sgd,lr=0.1" --lrshrink=5 --decay=0.5 --minlr=1e-6 --max_norm=5. --encoder_type="InferSent" --enc_lstm_dim=512 --n_enc_layers=1 --fc_dim=256 --n_classes=2 --pool_type="max" --gpu_id=-1 --seed=1234 --cont=0 >> train.log 2>&1 &