#/bin/bash
DATA_ROOT=/media/trtd-ubu-003/data2/data/datasets/matting/Combined_Dataset2
TRAIN_DATA_ROOT=$DATA_ROOT/Training_set/comp
TEST_DATA_ROOT=$DATA_ROOT/Test_set/comp

CUDA_VISIBLE_DEVICES=0,1 \
python core/train.py \
    --crop_h=320,480,640 \
    --crop_w=320,480,640 \
    --size_h=320 \
    --size_w=320 \
    --alphaDir=$TRAIN_DATA_ROOT/alpha  \
    --fgDir=$TRAIN_DATA_ROOT/fg \
    --bgDir=$TRAIN_DATA_ROOT/bg \
    --imgDir=$TRAIN_DATA_ROOT/image \
    --imgbigDir=$TRAIN_DATA_ROOT/image_big \
    --saveDir=model/stage1 \
    --batchSize=1 \
    --nEpochs=12 \
    --step=-1 \
    --lr=0.00001 \
    --wl_weight=0.5 \
    --threads=4 \
    --printFreq=10 \
    --ckptSaveFreq=10 \
    --pretrain=model/vgg_state_dict.pth \
    --cuda \
    --stage=1 \
    --testFreq=1 \
    --testImgDir=$TEST_DATA_ROOT/image \
    --testTrimapDir=$TEST_DATA_ROOT/trimap \
    --testAlphaDir=$TEST_DATA_ROOT/alpha \
    --testResDir=result/tmp \
    --crop_or_resize=whole \
    --max_size=1600 \
    --log=stage1.txt \

    #--resume=model/stage1/ckpt_e1.pth \
