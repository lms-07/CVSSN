# Exploring the Relationship between Center and Neighborhoods: Central Vector oriented Self-Similarity Network for Hyperspectral Image Classification

[Mingsong Li](https://orcid.org/0000-0001-6133-3923), Yikun Liu, Guangkuo Xue, [Yuwen Huang](https://jsj.hezeu.edu.cn/info/1302/6525.htm), and [Gongping Yang](https://faculty.sdu.edu.cn/gpyang)

[Time Lab](https://time.sdu.edu.cn/), [SDU](https://www.sdu.edu.cn/)

-----------
This repository is the official implementation of our paper:
[Exploring the Relationship between Center and Neighborhoods: Central Vector oriented Self-Similarity Network for
Hyperspectral Image Classification](https://doi.org/10.1109/TCSVT.2022.3218284), IEEE TCSVT 2022.

## Contents
1. [Brief Introduction](#Brief-Introduction)
1. [Environment](#Environment)
1. [Data Sets](#Data-Sets)
1. [Citation](#Citation)
1. [License and Acknowledgement](License-and-Acknowledgement)

## Brief Introduction
> To mine the spectral-spatial information of target pixel in hyperspectral image classification (HSIC), convolutional neural network (CNN)-based models widely adopt patch-based input pattern, where a patch represents its central pixel and the neighbor pixels play auxiliary roles in the classification process. However, compared to the central pixel, its neighbor pixels often have different contributions for classification. Although many existing patch-based CNNs could adaptively emphasize the spatial neighbor information, most of them ignore the latent relationship between the center pixel and its neighbor pixels. Moreover, efficient spectral-spatial feature extraction has been a difficult yet vital topic for HSIC. To address the mentioned problems, a central vector oriented self-similarity network (CVSSN) is proposed for HSIC. Specifically, based on two similarity measures, we firstly design an adaptive weight addition based spectral vector self-similarity module (AWA-SVSS) in input space and a Euclidean distance based feature vector self-similarity module (ED-FVSS) in feature space to fully mine the central vector oriented spatial relationships. Besides, a spectral-spatial information fusion module (SSIF) is formulated as a new pattern to fuse the central 1D spectral vector and the corresponding 3D patch for efficient spectral-spatial feature learning of the subsequent modules. Moreover, we implement a channel spatial separation convolution module (CSS-Conv) and a scale information complementary convolution module (SIC-Conv) for efficient spectral-spatial feature learning. Extensive experimental results on four popular HSI data sets demonstrate the effectiveness and efficiency of the proposed method compared with other state-of-the-art methods. The source code is available at https://github.com/lms-07/CVSSN.

|                   CVSSN Framwork
| :-----------------------------------------: |
| <img src="./src/CVSSN.png"  >  |

|              AWA-SVSS Module                |               ED-FVSS Module                |
| :-----------------------------------------: | :-----------------------------------------: |
|   <img src="./src/AWA-SVSS.png" >    | <img src="./src/ED-FVSS.png" >  |


## Environment
- The software environment is Ubuntu 18.04.5 LTS 64 bit.
- This project is running on a single Nvidia GeForce RTX 3090 GPU based on Cuda 11.0.
- We adopt Python 3.8.5, PyTorch 1.8.1+cu111.
- The py+torch combination may not limietd by our adopted one.


## Data Sets

Four popular HSI data sets are adopted in our experiments, i.e., Indian Pines (IP), Kennedy Space Center (KSC), University of Pavia (UP), and University of Houston 13 (UH).
The first three data sets could be access through [link1](http://www.ehu.eus/ccwintco/index.php?title=Hyperspectral_Remote_Sensing_Scenes##anomaly_detection), 
and the UH data set through [link2](https://hyperspectral.ee.uh.edu/?page_id=459). 
Our project is organized as follows:

```text
CVSSN
|-- process_xxx  // main files, cls for two classic methods, and dl for eight deep learning based methods. disjoint for the disjoint dataset (UH).
|-- data                    
|   |-- IP
|   |   |-- Indian_pines_corrected.mat
|   |   |-- Indian_pines_gt.mat
|   |-- KSC
|   |   |-- KSC.mat
|   |   |-- KSC_gt.mat
|   |-- UP
|   |   |-- PaviaU.mat
|   |   |-- PaviaU_gt.mat
|   |-- HU13_tif
|   |   |--Houston13_data.mat
|   |   |--Houston13_gt_train.mat
|   |   |--Houston13_gt_test.mat
|-- model                   // the compared methodes and our proposed method
|-- output
|   |-- cls_maps            // classification map visualizations 
|   |-- results             // classification result files
|-- src                     // source files
|-- utils                   // data loading, processing, and evaluating
|-- visual                  // cls maps visual
```

## Citation

Please kindly cite our work if this work is helpful for your research.

[1] M. Li, Y. Liu, G. Xue, Y. Huang and G. Yang, "Exploring the Relationship Between Center and Neighborhoods: Central Vector Oriented Self-Similarity Network for Hyperspectral Image Classification," in IEEE Transactions on Circuits and Systems for Video Technology, vol. 33, no. 4, pp. 1979-1993, April 2023, doi: 10.1109/TCSVT.2022.3218284.

BibTex entry:
```text
@article{li2022exploring,
   title={Exploring the Relationship between Center and Neighborhoods: Central Vector oriented Self-Similarity Network for Hyperspectral Image Classification},
   author={Li, Mingsong and Liu, Yikun and Xue, Guangkuo and Huang, Yuwen and Yang, Gongping},
   journal={IEEE Transactions on Circuits and Systems for Video Technology},
   year={2023},
   volume={33},
   number={4},
   pages={1979-1993},
   doi={10.1109/TCSVT.2022.3218284},
   publisher={IEEE}
}
```

## Contact information

If you have any problem, please do not hesitate to contact us `msli@mail.sdu.edu.cn`.

## License and Acknowledgement
This project is released under [GPLv3](http://www.gnu.org/licenses/) license.

- We would like to thank the Hyperspectral Image Analysis group and the NSF Funded Center for
   Airborne Laser Mapping (NCALM) at the University of Houston for providing the UH dataset used in this work.
- Part of our HSIC framework is referred to [HybridSN](https://github.com/gokriznastic/HybridSN), [A2S2K-ResNet](https://github.com/suvojit-0x55aa/A2S2K-ResNet), and [CNN_Enhanced_GCN](https://github.com/qichaoliu/CNN_Enhanced_GCN). Please also follow their licenses. Thanks for their awesome works.        
- Among the adopted compared methods, we also would like to thank Assistant Professor [Xiangtao Zheng](https://xiangtaozheng.github.io/) and 
   Dr. Xuming Zhang for providing the source tensorflow code of [SSAN](https://ieeexplore.ieee.org/document/8909379) and
   the part of source keras code of [SSSAN](https://ieeexplore.ieee.org/document/9508777?arnumber=9508777), respectively.










