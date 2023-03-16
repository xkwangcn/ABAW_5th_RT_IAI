#!/usr/bin/env python
import torch
import torch.nn as nn
import torch.nn.functional as F
from emonet_split import EmoNet, EmoNet_
nn.InstanceNorm2d = nn.BatchNorm2d


def get_emonet():
    net = torch.load('model_8.pth')
    return net


class Model_fan(nn.Module):
    def __init__(self):
        super(Model_fan, self).__init__()
        self.emonet = get_emonet()
        self.emonet.module.predictor.emo_fc_2 = nn.Sequential(nn.Linear(in_features=256, out_features=128, bias=True),
                                                              nn.BatchNorm1d(128, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True),
                                                              nn.ReLU(inplace=True),
                                                              nn.Linear(in_features=128, out_features=8, bias=True))
        # self.emonet.eval()
        # self.predictor = EmoNet_(n_expression=0, n_reg=2)
        # self.transformer = Transformer()
        # self.softmax = nn.Softmax(dim=1)

    def forward(self, imgs):
        out = self.emonet(imgs)
        # print(emo_feat.shape)
        return out


if __name__ == '__main__':
    model = Model_fan().cuda()
    print(model)
    imgs = torch.rand(2, 3, 256, 256).cuda()
    logits = model(imgs)
    print(logits)
