# PyTorch

# 摘要

本主题页基于为知笔记“PyTorch深度学习快速入门教程”下已入库的 20 篇笔记，覆盖 TensorBoard、transforms、torchvision 数据集、DataLoader、`nn.Module`、卷积/池化/激活/线性层、`Sequential`、损失函数、优化器、模型保存读取、完整训练流程、GPU 训练和模型验证。

# 核心概念

- PyTorch 图像数据流程从 transforms 开始，先关注输入输出类型，再通过 `ToTensor`、`Normalize`、`Resize`、`Compose`、`RandomCrop` 等工具完成预处理和增强。
- `torchvision.datasets` 可加载数据集，原文示例使用 CIFAR10，并通过 `transforms=dataset_transform` 绑定转换流程。
- DataLoader 将 dataset 批量加载到训练流程中，`batch_size` 决定每次取出的样本数量。
- 自定义神经网络以 `nn.Module` 为基本骨架，后续通过卷积层、最大池化、非线性激活、线性层和 `Sequential` 组织网络结构。
- 训练闭环包括前向输出、损失函数计算、`backward()` 反向传播和优化器更新。
- 完整训练流程还需要验证集评估、`no_grad`、模型保存、GPU 设备管理和最终 demo 验证。
- TensorBoard 用于显示图像、训练结果或网络结构，当前笔记多次用它检查 transforms、DataLoader、卷积输出和网络结果。

# 复习顺序

1. [009 tensorboard的使用2](../notes/2026-06-28-009-tensorboard的使用2.md)
2. [010 transforms的使用](../notes/2026-06-28-010-transforms的使用.md)
3. [011 常见的transforms1](../notes/2026-06-28-011-常见的transforms1.md)
4. [011常见的transforms2](../notes/2026-06-28-011-常见的transforms2.md)
5. [014torchvision中的数据集使用](../notes/2026-06-28-014-torchvision中的数据集使用.md)
6. [015dataloader的使用](../notes/2026-06-28-015-dataloader的使用.md)
7. [016 神经网络的基本骨架nn.module的使用](../notes/2026-06-28-016-神经网络的基本骨架nn.module的使用.md)
8. [017卷积操作](../notes/2026-06-28-017-卷积操作.md)
9. [018 神经网络-卷积层](../notes/2026-06-28-018-神经网络-卷积层.md)
10. [019 神经网络-最大池化](../notes/2026-06-28-019-神经网络-最大池化.md)
11. [020 非线性激活](../notes/2026-06-28-020-非线性激活.md)
12. [021 神经网络线性层及其他层介绍](../notes/2026-06-28-021-神经网络线性层及其他层介绍.md)
13. [022 神经网络-搭建小实战和sequential](../notes/2026-06-28-022-神经网络-搭建小实战和sequential.md)
14. [023 损失函数与反向传播](../notes/2026-06-28-023-损失函数与反向传播.md)
15. [024 优化器1](../notes/2026-06-28-024-优化器1.md)
16. [025 现有网络模型的使用及修改](../notes/2026-06-28-025-现有网络模型的使用及修改.md)
17. [026 网络模型的保存与读取](../notes/2026-06-28-026-网络模型的保存与读取.md)
18. [027完整的模型训练套路1](../notes/2026-06-28-027-完整的模型训练套路1.md)
19. [030利用GPU训练](../notes/2026-06-28-030-利用GPU训练.md)
20. [031完整的模型验证(测试，demo)套路](../notes/2026-06-28-031-完整的模型验证-测试-demo套路.md)

# 自测题

- transforms 中为什么要持续关注每一步的输入和输出类型？
- `ToTensor`、`Normalize`、`Resize`、`Compose`、`RandomCrop` 分别解决什么问题？
- Dataset 和 DataLoader 的分工是什么？
- `nn.Module`、卷积层、池化层、激活函数、线性层和 `Sequential` 如何组成一个网络？
- 损失函数、`backward()` 和优化器在训练循环中分别负责什么？
- 验证阶段为什么需要 `no_grad`？
- 使用 GPU 训练时，为什么模型和数据要放到同一设备？
- 模型保存方式和加载方式为什么要成对记忆？

# 缺口

当前材料主要是简短文字加代码截图，完整代码细节需要回查 `raw/为知笔记/PyTorch深度学习快速入门教程/` 下对应 Markdown 和 `_files` 图片。尤其是 TensorBoard 参数、卷积/池化代码、模型保存读取代码、GPU `.to(device)` 的四类对象迁移，以及模型验证 demo 的完整代码，需要从 raw 截图中补全。
