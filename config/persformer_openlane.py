# ==============================================================================
# Copyright (c) 2022 The PersFormer Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

import numpy as np
import os
import os.path as ops

def config(args):
    # 300 sequence
    # args.dataset_name = 'openlane'
    # args.dataset_dir = '/mnt/disk01/openlane/images/'
    # args.data_dir = '/mnt/disk01/openlane/lane3d_300/'

    # 1000 sequence
    # args.dataset_name = 'openlane'
    # args.dataset_dir = '/mnt/disk01/openlane/images/'
    # args.data_dir = '/mnt/disk01/openlane/lane3d_1000/'
    
    # AMAN
    # 300 sequence
    args.dataset_name = 'openlane'
    args.dataset_dir = '/mnt/ssd/aman/CS280_Project/datasets/OpenLane_source_compressed_images/images/'
    args.data_dir = '/mnt/ssd/aman/CS280_Project/datasets/OpenLane_source_compressed_lane3d_300/lane3d_300/'

    # 1000 sequence
    # args.dataset_name = 'openlane'
    # args.dataset_dir = '/mnt/ssd/aman/CS280_Project/datasets/OpenLane_source_compressed_images/images/'
    # args.data_dir = '/mnt/ssd/aman/CS280_Project/datasets/OpenLane_source_compressed_lane3d_1000/lane3d_1000/'
    
    if 'openlane' in args.dataset_name:
        openlane_config(args)
    else:
        sim3d_config(args)

    args.save_prefix = ops.join(os.getcwd(), 'data_splits')
    args.save_path = ops.join(args.save_prefix, args.dataset_name)

    # load configuration for certain dataset
    args.prob_th = 0.5

    # define the network model
    args.num_class = 2  # 1 background + n lane labels
    # args.mod = 'debug'
    args.y_ref = 5  # new anchor prefer closer range gt assign

    # for the case only running evaluation
    # AMAN
    args.evaluate = True
    args.evaluate_case = False

    # settings for save and visualize
    args.print_freq = 50
    args.save_freq = 50

    # args.nepochs = 1
    # run the training

    # change encoder, "EfficientNet-B7"
    args.encoder = "EfficientNet-B7"
    
    # ddp related
    args.dist = True
    args.sync_bn = True

    args.cudnn = True
    args.port = 29666

    # ddp init
    args.use_slurm = False

    # attention
    args.position_embedding = 'learned'
    args.use_att = True
    args.use_proj = True
    args.num_proj = 4
    args.num_att = 1
    args.use_top_pathway = False
    args.npoints = 8
    args.nhead = 8
    args.use_fpn = False

    # data loader
    # AMAN
    args.nworkers = 1

    # grad clip
    args.clip_grad_norm = 35.0
    args.loss_threshold = 1e5

    # scheduler
    args.lr_policy = "cosine"
    args.T_max = 8
    args.eta_min = 1e-5

    # optimizer
    args.optimizer = 'adam'
    args.learning_rate = 2e-4
    args.weight_decay = 0.001

    # 2d loss, used if not learnable_weight_on
    args.loss_att_weight = 100.0

    # 3d loss, vis | prob | reg, default 1.0 | 1.0 | 1.0,  suggest 10.0 | 4.0 | 1.0
    # used if not learnable_weight_on
    args.loss_dist = [10.0, 4.0, 1.0]

    # config
    args.use_el = True

    # init
    # args.weight_init = 'xavier'
    
    # segmentation setting
    args.lane_width = 2
    args.loss_seg_weight = 0.0
    args.seg_start_epoch = 1

    # learnable weight
    # in best model setting, they are 10, 4, 1, 100, 100, 100, 10
    # factor = 1 / exp(weight)
    args.learnable_weight_on = True
    args._3d_vis_loss_weight = 0.0 # -2.3026
    args._3d_prob_loss_weight = 0.0 # -1.3863
    args._3d_reg_loss_weight = 0.0
    args._2d_vis_loss_weight = 0.0 # -4.6052
    args._2d_prob_loss_weight = 0.0 # -4.6052
    args._2d_reg_loss_weight = 0.0 # -4.6052
    args._seg_loss_weight = 0.0 # -2.3026

    # ipm related
    args.top_view_region = np.array([[-10, 103], [10, 103], [-10, 3], [10, 3]])
    args.anchor_y_steps = np.array([5, 10, 15, 20, 30, 40, 50, 60, 80, 100])
    args.num_y_steps = len(args.anchor_y_steps)

    # memcache
    args.use_memcache = False


def sim3d_config(args):
    # set dataset parameters
    args.org_h = 1080
    args.org_w = 1920
    args.crop_y = 0
    args.no_centerline = True
    args.no_3d = False
    args.fix_cam = False
    args.pred_cam = False

    # set camera parameters for the test datasets
    args.K = np.array([[2015., 0., 960.],
                       [0., 2015., 540.],
                       [0., 0., 1.]])

    # specify model settings
    """
    paper presented params:
        args.top_view_region = np.array([[-10, 85], [10, 85], [-10, 5], [10, 5]])
        args.anchor_y_steps = np.array([5, 20, 40, 60, 80, 100])
    """
    args.top_view_region = np.array([[-10, 103], [10, 103], [-10, 3], [10, 3]])
    args.anchor_y_steps = np.array([5, 10, 15, 20, 30, 40, 50, 60, 80, 100])
    args.num_y_steps = len(args.anchor_y_steps)

    args.max_lanes = 6
    args.num_category = 2

    # initialize with pre-trained vgg weights
    args.pretrained = False
    # apply batch norm in network
    args.batch_norm = True


def openlane_config(args):
    # set dataset parameters
    args.org_h = 1280
    args.org_w = 1920
    args.crop_y = 0
    args.no_centerline = True
    args.no_3d = False
    args.fix_cam = False
    args.pred_cam = False

    # Placeholder, shouldn't be used
    args.K = np.array([[1000., 0., 960.],
                       [0., 1000., 640.],
                       [0., 0., 1.]])

    # specify model settings
    args.top_view_region = np.array([[-10, 103], [10, 103], [-10, 3], [10, 3]])
    args.anchor_y_steps = np.array([5, 10, 15, 20, 30, 40, 50, 60, 80, 100])
    args.num_y_steps = len(args.anchor_y_steps)

    # TODO: constrain max lanes in gt
    args.max_lanes = 20
    args.num_category = 21

    # initialize with pre-trained vgg weights
    args.pretrained = False
    # apply batch norm in network
    args.batch_norm = True
