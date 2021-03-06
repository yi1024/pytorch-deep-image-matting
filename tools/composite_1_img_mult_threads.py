# composite image with dataset from "deep image matting"

import os 
import cv2
import math
import time
import shutil
import threading
import numpy as np

root_dir = "/media/trtd-ubu-003/data2/data/datasets/matting/Combined_Dataset2"
root_dir_dist = "/media/trtd-ubu-003/data2/data/datasets/matting/Combined_Dataset2"
test_bg_dir = '/media/trtd-ubu-003/data2/data/datasets/matting/VOCdevkit/VOC2012/JPEGImages'
train_bg_dir = '/media/trtd-ubu-003/data2/data/datasets/matting/mscoco/train2017'
threads_cnt = 16

def my_composite_theads(theads_inx,fg_cnt,fg_ids,bg_ids, fg_dir, alpha_dir, bg_dir, num_bg, comp_dir):
    for i in range(fg_cnt):
        #print(i)
        if i % threads_cnt == theads_inx:
            print(str(theads_inx) + '-' + str(i))

            im_name = fg_ids[i].strip("\n").strip("\r")
            fg_path = os.path.join(fg_dir, im_name)
            alpha_path = os.path.join(alpha_dir, im_name)

            # print(fg_path, alpha_path)
            assert (os.path.exists(fg_path))
            assert (os.path.exists(alpha_path))

            fg = cv2.imread(fg_path)
            alpha = cv2.imread(alpha_path)

            # print("alpha shape:", alpha.shape, "image shape:", fg.shape)
            assert (alpha.shape == fg.shape)

            h, w, c = fg.shape
            base = i * num_bg
            for bcount in range(num_bg):
                bg_path = os.path.join(bg_dir, bg_ids[base + bcount].strip("\n").strip("\r"))
                print(base + bcount, fg_path, bg_path)
                assert (os.path.exists(bg_path))
                bg = cv2.imread(bg_path)
                bh, bw, bc = bg.shape

                wratio = float(w) / bw
                hratio = float(h) / bh
                ratio = wratio if wratio > hratio else hratio
                if ratio > 1:
                    new_bw = int(bw * ratio + 1.0)
                    new_bh = int(bh * ratio + 1.0)
                    bg = cv2.resize(bg, (new_bw, new_bh), interpolation=cv2.INTER_LINEAR)
                bg = bg[0: h, 0: w, :]
                # print(bg.shape)
                assert (bg.shape == fg.shape)
                alpha_f = alpha / 255.
                comp = fg * alpha_f + bg * (1. - alpha_f)

                img_save_id = im_name[:len(im_name) - 4] + '_' + str(bcount) + '.png'
                comp_save_path = os.path.join(comp_dir, "image/" + img_save_id)
                fg_save_path = os.path.join(comp_dir, "fg/" + img_save_id)
                bg_save_path = os.path.join(comp_dir, "bg/" + img_save_id)
                alpha_save_path = os.path.join(comp_dir, "alpha/" + img_save_id)

                img_big_save_path = os.path.join(comp_dir, "image_big/" + img_save_id)


                #cv2.imwrite(comp_save_path, comp)
                #cv2.imwrite(fg_save_path, fg)
                #cv2.imwrite(bg_save_path, bg)
                #cv2.imwrite(alpha_save_path, alpha)

                img = np.hstack([comp, fg])
                img = np.hstack([img, bg])
                img = np.hstack([img, alpha])
                cv2.imwrite(img_big_save_path, img)
'''
                img_big = cv2.imread(img_big_save_path)[:, :, :3]
                img_big_w = img_big.shape[1]
                img_big_h = img_big.shape[0]
                img_w = int(img_big_w / 4)
                print(img_w)
                # [y0:y1,x0:x1]
                img1 = img_big[0:img_big_h, img_w * 0:img_w * 0 + img_w]
                img2 = img_big[0:img_big_h, img_w * 1:img_w * 1 + img_w]
                img3 = img_big[0:img_big_h, img_w * 2:img_w * 2 + img_w]
                img4 = img_big[0:img_big_h, img_w * 3:img_w * 3 + img_w]

                cv2.imwrite(comp_save_path, img1)
                cv2.imwrite(fg_save_path, img2)
                cv2.imwrite(bg_save_path, img3)
                cv2.imwrite(alpha_save_path, img4)
'''

def my_composite(fg_names, bg_names, fg_dir, alpha_dir, bg_dir, num_bg, comp_dir):
    fg_ids = open(fg_names).readlines()
    bg_ids = open(bg_names).readlines()

    fg_cnt = len(fg_ids)
    bg_cnt = len(bg_ids)
    print(fg_cnt, bg_cnt)
    assert (fg_cnt * num_bg == bg_cnt)
    for inx in range(threads_cnt):
        print(inx)
        t = threading.Thread(target=my_composite_theads,args=(inx, fg_cnt, fg_ids, bg_ids, fg_dir, alpha_dir, bg_dir, num_bg, comp_dir))
        t.start()


def copy_dir2dir(src_dir, des_dir):
    for img_id in os.listdir(src_dir):
        shutil.copyfile(os.path.join(src_dir, img_id), os.path.join(des_dir, img_id))


def main():

    #test_num_bg = 20
    test_num_bg = 2
    test_fg_names = os.path.join(root_dir, "Test_set/test_fg_names.txt")
    test_bg_names = os.path.join(root_dir, "Test_set/test_bg_names.txt")
    test_fg_dir = os.path.join(root_dir, "Test_set/Adobe-licensed images/fg")
    test_alpha_dir = os.path.join(root_dir, "Test_set/Adobe-licensed images/alpha")
    test_trimap_dir = os.path.join(root_dir, "Test_set/Adobe-licensed images/trimaps")
    test_comp_dir = os.path.join(root_dir_dist, "Test_set/comp")

    #train_num_bg = 100
    train_num_bg = 10
    train_fg_names = os.path.join(root_dir, "Training_set/training_fg_names.txt")
    train_bg_names_coco2014 = os.path.join(root_dir, "Training_set/training_bg_names.txt")
    train_bg_names_coco2017 = os.path.join(root_dir, "Training_set/training_bg_names_coco2017.txt")
    train_fg_dir = os.path.join(root_dir, "Training_set/all/fg")
    train_alpha_dir = os.path.join(root_dir_dist, "Training_set/all/alpha")
    train_comp_dir = os.path.join(root_dir_dist, "Training_set/comp")

    # change the bg names formate if is coco 2017 
    fin =  open(train_bg_names_coco2014, 'r')
    fout =  open(train_bg_names_coco2017, 'w')
    lls = fin.readlines()
    for l in lls:
        fout.write(l[15:])
    fin.close()
    fout.close()

    if not os.path.exists(test_comp_dir):
        os.makedirs(test_comp_dir + '/image_big')
        os.makedirs(test_comp_dir + '/image')
        os.makedirs(test_comp_dir + '/fg')
        os.makedirs(test_comp_dir + '/bg')
        os.makedirs(test_comp_dir + '/alpha')
        os.makedirs(test_comp_dir + '/trimap')

    if not os.path.exists(train_comp_dir):
        os.makedirs(train_comp_dir + '/image_big')
        os.makedirs(train_comp_dir + '/image')
        os.makedirs(train_comp_dir + '/fg')
        os.makedirs(train_comp_dir + '/bg')
        os.makedirs(train_comp_dir + '/alpha')

    if not os.path.exists(train_alpha_dir):
        os.makedirs(train_alpha_dir)

    if not os.path.exists(train_fg_dir):
        os.makedirs(train_fg_dir)

    # copy test trimaps 
    copy_dir2dir(test_trimap_dir, test_comp_dir + '/trimap')
    # copy train images together
    copy_dir2dir(os.path.join(root_dir, "Training_set/Adobe-licensed images/alpha"), train_alpha_dir)
    copy_dir2dir(os.path.join(root_dir, "Training_set/Adobe-licensed images/fg"), train_fg_dir)
    copy_dir2dir(os.path.join(root_dir, "Training_set/Other/alpha"), train_alpha_dir)
    copy_dir2dir(os.path.join(root_dir, "Training_set/Other/fg"), train_fg_dir)

    # composite test image
    my_composite(test_fg_names, test_bg_names, test_fg_dir, test_alpha_dir, test_bg_dir, test_num_bg, test_comp_dir)
    # composite train image
    my_composite(train_fg_names, train_bg_names_coco2017, train_fg_dir, train_alpha_dir, train_bg_dir, train_num_bg, train_comp_dir)

if __name__ == "__main__":
    main()

