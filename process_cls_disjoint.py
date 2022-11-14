# -*- coding: utf-8 -*-
# @Auther   : Mingsong Li (lms-07)
# @Time     : 2022-Nov
# @Address  : Time Lab @ SDU
# @FileName : process_cls_disjoint.py
# @Project  : CVSSN (HSIC), IEEE TCSVT

# for spatially disjoint data set, e.g., the UH data set,

# main processing file for classical methods,
# i.e., random forest(RF) and SVM

import os
import time
import torch
import random
import numpy as np

from sklearn import metrics
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier

import utils.evaluation as evaluation
import utils.data_load_operate as data_load_operate
import utils.data_load_operate_disjoint as data_load_operate_disjoint
import visual.cls_map_visual as cls_visual

time_current = time.strftime("%y-%m-%d-%H.%M", time.localtime())

# random seed setting
seed = 20

torch.manual_seed(seed)
torch.cuda.manual_seed(seed)
torch.cuda.manual_seed_all(seed)
np.random.seed(seed)  # Numpy module.
random.seed(seed)  # Python random module.
torch.manual_seed(seed)
torch.backends.cudnn.benchmark = False
torch.backends.cudnn.deterministic = True

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

########      0   ###    1   ###
model_list = ['SVM', 'Random Forest']
model_flag = 0

data_set_name_list = ['IP', 'KSC', 'UP', 'HU_tif']
data_set_name = data_set_name_list[3]

# seed_list = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]  #
# seed_list=[0,1,2,3,4]
# seed_list=[0,1,2] #
# seed_list=[0,1]
seed_list = [0]  #

# ratio=1.0
# ratio=5.0
# ratio=7.5
# ratio = 10.0
ratio = "hu13"

data_set_path = os.path.join(os.getcwd(), 'data')
results_save_path = \
    os.path.join(os.path.join(os.getcwd(), 'output/results'), model_list[model_flag] + str("_") +
                 data_set_name + str("_") + str(time_current) + str("_seed") + str(seed)) + str("_ratio") + str(ratio)
cls_map_save_path = \
    os.path.join(os.path.join(os.getcwd(), 'output/cls_maps'), model_list[model_flag] + str("_") +
                 data_set_name + str("_") + str(time_current) + str("_seed") + str(seed)) + str("_ratio") + str(ratio)

if __name__ == '__main__':

    data, gt_train, gt_test = data_load_operate.load_HU_data(data_set_name, data_set_path)
    data = data_load_operate.standardization(data)

    gt_train_re = gt_train.reshape(-1)
    gt_test_re = gt_test.reshape(-1)
    height, width, channels = data.shape
    class_count = max(np.unique(gt_train_re))

    OA_ALL = []
    AA_ALL = []
    KPP_ALL = []
    EACH_ACC_ALL = []
    Train_Time_ALL = []
    Test_Time_ALL = []
    CLASS_ACC = np.zeros([len(seed_list), class_count])

    data_reshape = data.reshape(data.shape[0] * data.shape[1], -1)
    for curr_seed in seed_list:

        train_data_index, val_data_index, test_data_index, all_data_index = data_load_operate_disjoint.sampling_UH_w_val(
            gt_train_re,
            gt_test_re,
            class_count)
        index = (train_data_index, test_data_index, all_data_index)
        x_train, y_train, x_test, y_gt = data_load_operate.generate_data_set_hu(data_reshape, gt_train_re, gt_test_re,
                                                                                index)

        tic1 = time.perf_counter()
        if model_flag == 0:
            clf = SVC(kernel='rbf', gamma='scale', C=20, tol=1e-5, random_state=10).fit(x_train, y_train)
        elif model_flag == 1:
            clf = RandomForestClassifier(n_estimators=150, min_samples_split=2,
                                         max_features='sqrt', max_depth=20, random_state=10).fit(x_train, y_train)

        toc1 = time.perf_counter()
        training_time = toc1 - tic1
        Train_Time_ALL.append(training_time)

        tic2 = time.perf_counter()
        pred_test = clf.predict(x_test)
        toc2 = time.perf_counter()

        testing_time = toc2 - tic2
        Test_Time_ALL.append(testing_time)

        y_gt = gt_test_re[test_data_index] - 1
        OA = metrics.accuracy_score(y_gt, pred_test)
        confusion_matrix = metrics.confusion_matrix(pred_test, y_gt)
        print("confusion_matrix\n{}".format(confusion_matrix))
        ECA, AA = evaluation.AA_ECA(confusion_matrix)
        kappa = metrics.cohen_kappa_score(pred_test, y_gt)
        cls_report = evaluation.claification_report(y_gt, pred_test, data_set_name)
        print("classification_report\n{}".format(cls_report))

        # Visualization for all the labeled samples and total the samples
        # total_pred=clf.predict(data_reshape)
        # sample_list1=[total_pred+1]

        # all_pred=clf.predict(x_all)
        # sample_list2=[all_pred+1,all_data_index]

        # cls_visual.pred_cls_map_cls(sample_list1,gt,cls_map_save_path)
        # cls_visual.pred_cls_map_cls(sample_list2,gt,cls_map_save_path)

        # Output infors
        f = open(results_save_path + '_results.txt', 'a+')
        str_results = '\n======================' \
                      + "\nOA=" + str(OA) \
                      + "\nAA=" + str(AA) \
                      + '\nkpp=' + str(kappa) \
                      + '\nacc per class:' + str(ECA) \
                      + "\ntrain time:" + str(training_time) \
                      + "\ntest time:" + str(testing_time) + "\n"

        f.write(str_results)
        f.write('{}'.format(confusion_matrix))
        f.write('\n\n')
        f.write('{}'.format(cls_report))
        f.close()

        OA_ALL.append(OA)
        AA_ALL.append(AA)
        KPP_ALL.append(kappa)
        EACH_ACC_ALL.append(ECA)

    OA_ALL = np.array(OA_ALL)
    AA_ALL = np.array(AA_ALL)
    KPP_ALL = np.array(KPP_ALL)
    EACH_ACC_ALL = np.array(EACH_ACC_ALL)
    Train_Time_ALL = np.array(Train_Time_ALL)
    Test_Time_ALL = np.array(Test_Time_ALL)

    np.set_printoptions(precision=4)
    print("\n====================Mean result of {} times runs ==========================".format(len(seed_list)))
    print('List of OA:', list(OA_ALL))
    print('List of AA:', list(AA_ALL))
    print('List of KPP:', list(KPP_ALL))
    print('OA=', round(np.mean(OA_ALL) * 100, 2), '+-', round(np.std(OA_ALL) * 100, 2))
    print('AA=', round(np.mean(AA_ALL) * 100, 2), '+-', round(np.std(AA_ALL) * 100, 2))
    print('Kpp=', round(np.mean(KPP_ALL) * 100, 2), '+-', round(np.std(KPP_ALL) * 100, 2))
    print('Acc per class=', np.mean(EACH_ACC_ALL, 0), '+-', np.std(EACH_ACC_ALL, 0))

    print("Average training time=", round(np.mean(Train_Time_ALL), 2), '+-', round(np.std(Train_Time_ALL), 3))
    print("Average testing time=", round(np.mean(Test_Time_ALL), 5), '+-', round(np.std(Test_Time_ALL), 5))

    # Output infors
    f = open(results_save_path + '_results.txt', 'a+')
    str_results = '\n\n***************Mean result of ' + str(len(seed_list)) + 'times runs ********************' \
                  + '\nList of OA:' + str(list(OA_ALL)) \
                  + '\nList of AA:' + str(list(AA_ALL)) \
                  + '\nList of KPP:' + str(list(KPP_ALL)) \
                  + '\nOA=' + str(round(np.mean(OA_ALL) * 100, 2)) + '+-' + str(round(np.std(OA_ALL) * 100, 2)) \
                  + '\nAA=' + str(round(np.mean(AA_ALL) * 100, 2)) + '+-' + str(round(np.std(AA_ALL) * 100, 2)) \
                  + '\nKpp=' + str(round(np.mean(KPP_ALL) * 100, 2)) + '+-' + str(round(np.std(KPP_ALL) * 100, 2)) \
                  + '\nAcc per class=' + str(np.mean(EACH_ACC_ALL, 0)) + '+-' + str(np.std(EACH_ACC_ALL, 0)) \
                  + "\nAverage training time=" + str(round(np.mean(Train_Time_ALL), 2)) + '+-' + str(
        round(np.std(Train_Time_ALL), 3)) \
                  + "\nAverage testing time=" + str(round(np.mean(Test_Time_ALL), 5)) + '+-' + str(
        round(np.std(Test_Time_ALL), 5))
    f.write(str_results)
    f.close()
