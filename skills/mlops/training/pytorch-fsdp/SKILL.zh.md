---
name: pytorch-fsdp
description: 使用PyTorch FSDP进行完全分片数据并行训练的专家指导 - 参数分片、混合精度、CPU卸载、FSDP2
version: 1.0.0
author: Orchestra Research
license: MIT
dependencies: [torch>=2.0, transformers]
metadata:
  hermes:
    tags: [分布式训练, PyTorch, FSDP, 数据并行, 分片, 混合精度, CPU卸载, FSDP2, 大规模训练]

---

# Pytorch-Fsdp 技能

使用pytorch-fsdp开发的全面帮助，从官方文档生成。

## 何时使用此技能

当出现以下情况时应触发此技能：
- 正在使用pytorch-fsdp
- 询问pytorch-fsdp功能或API
- 实现pytorch-fsdp解决方案
- 调试pytorch-fsdp代码
- 学习pytorch-fsdp最佳实践

## 快速参考

### 常见模式

**模式1：** 通用Join上下文管理器# 创建时间：2025年6月6日 | 最后更新：2025年6月6日 通用join上下文管理器便于在不均匀输入上进行分布式训练。本页概述了相关类的API：Join、Joinable和JoinHook。有关教程，请参阅使用Join上下文管理器进行不均匀输入的分布式训练。class torch.distributed.algorithms.Join(joinables, enable=True, throw_on_early_termination=False, **kwargs)[source]# 此类定义了通用join上下文管理器，允许在进程join后调用自定义钩子。这些钩子应该模拟非join进程的集合通信，以防止挂起和出错并确保算法正确性。有关钩子定义的详细信息，请参阅JoinHook。警告 上下文管理器要求每个参与的Joinable在其自己的每轮集合通信之前调用notify_join_context()方法，以确保正确性。警告 上下文管理器要求JoinHook对象中的所有process_group属性都相同。如果有多个JoinHook对象，则使用第一个的设备。进程组和设备信息用于检查非join进程并通知进程如果启用了throw_on_early_termination则抛出异常，两者都使用all-reduce。参数 joinables (List[Joinable]) – 参与的Joinable列表；它们的钩子按给定顺序迭代。enable (bool) – 启用不均匀输入检测的标志；设置为False禁用上下文管理器的功能，只有当用户知道输入不会不均匀时才应设置（默认：True）。throw_on_early_termination (bool) – 控制在检测到不均匀输入时是否抛出异常的标志（默认：False）。示例：>>> import os >>> import torch >>> import torch.distributed as dist >>> import torch.multiprocessing as mp >>> import torch.nn.parall

```
Join
```

**模式2：** 分布式通信包 - torch.distributed# 创建时间：2017年7月12日 | 最后更新：2025年9月4日 注意 请参阅PyTorch分布式概述，简要介绍与分布式训练相关的所有功能。后端# torch.distributed支持四个内置后端，每个都有不同的功能。下表显示了每个后端在CPU或GPU上可用的函数。对于NCCL，GPU指的是CUDA GPU，而对于XCCL则指XPU GPU。MPI仅在用于构建PyTorch的实现支持CUDA时才支持CUDA。后端 gloo mpi nccl xccl 设备 CPU GPU CPU GPU CPU GPU CPU GPU send ✓ ✘ ✓ ? ✘ ✓ ✘ ✓ recv ✓ ✘ ✓ ? ✘ ✓ ✘ ✓ broadcast ✓ ✓ ✓ ? ✘ ✓ ✘ ✓ all_reduce ✓ ✓ ✓ ? ✘ ✓ ✘ ✓ reduce ✓ ✓ ✓ ? ✘ ✓ ✘ ✓ all_gather ✓ ✓ ✓ ? ✘ ✓ ✘ ✓ gather ✓ ✓ ✓ ? ✘ ✓ ✘ ✓ scatter ✓ ✓ ✓ ? ✘ ✓ ✘ ✓ reduce_scatter ✓ ✓ ✘ ✘ ✘ ✓ ✘ ✓ all_to_all ✓ ✓ ✓ ? ✘ ✓ ✘ ✓ barrier ✓ ✘ ✓ ? ✘ ✓ ✘ ✓ PyTorch附带的后端# PyTorch分布式包支持Linux（稳定）、MacOS（稳定）和Windows（原型）。对于Linux，默认情况下构建并包含Gloo和NCCL后端（仅在使用CUDA构建时包含NCCL）。MPI是一个可选后端，只有从源代码构建PyTorch时才能包含。（例如，在安装了MPI的主机上构建PyTorch。）注意 从PyTorch v1.8开始，Windows支持除NCCL外的所有集合通信后端，如果init_process_group()的init_method参数指向文件，则必须符合以下模式：本地文件系统，init_method="file:///d:/tmp/some_file" 共享文件系统，init_method="file://////{machine_name}/{share_folder_name}/some_file" 与Linux平台相同，您可以通过设置环境变量MASTER_ADDR和MASTER_PORT来启用TcpStore。使用哪个后端？# 过去，我们经常被问到："我应该使用哪个后端？" 经验法则 使用NCCL后端进行CUDA GPU的分布式训练。使用XCCL后端进行

```
torch.distributed
```

**模式3：** 初始化# 在调用任何其他方法之前，需要使用torch.distributed.init_process_group()或torch.distributed.device_mesh.init_device_mesh()函数初始化包。两者都会阻塞，直到所有进程都join。警告 初始化不是线程安全的。进程组创建应从单个线程执行，以防止跨rank分配不一致的'UUID'，并防止初始化期间的竞争条件导致挂起。torch.distributed.is_available()[source]# 如果分布式包可用，则返回True。否则，torch.distributed不公开任何其他API。目前，torch.distributed在Linux、MacOS和Windows上可用。从源代码构建PyTorch时，设置USE_DISTRIBUTED=1以启用它。目前，Linux和Windows的默认值为USE_DISTRIBUTED=1，MacOS为USE_DISTRIBUTED=0。返回类型 bool torch.distributed.init_process_group(backend=None, init_method=None, timeout=None, world_size=-1, rank=-1, store=None, group_name='', pg_options=None, device_id=None)[source]# 初始化默认分布式进程组。这也将初始化分布式包。初始化进程组有2种主要方法：显式指定store、rank和world_size。指定init_method（一个URL字符串），指示在哪里/如何发现peer。可以选择指定rank和world_size，或者在URL中编码所有必需参数并省略它们。如果两者都未指定，则假定init_method为"env://"。参数 backend (str或Backend，可选) – 要使用的后端。根据构建时配置，有效值包括mpi、gloo、nccl、ucc、xccl或第三方插件注册的后端。从2.6开始，如果未提供backend，c10d将使用为device_id kwarg指示的设备类型注册的后端（如果提供）。今天已知的默认注册是：cuda使用nccl，cpu使用gloo，xpu使用xccl。如果既没有提供backend也没有提供device_id

```
torch.distributed.init_process_group()
```

**模式4：** 示例：

```
>>> from torch.distributed.device_mesh import init_device_mesh
>>>
>>> mesh_1d = init_device_mesh("cuda", mesh_shape=(8,))
>>> mesh_2d = init_device_mesh("cuda", mesh_shape=(2, 8), mesh_dim_names=("dp", "tp"))
```

**模式5：** 组# 默认情况下，集合操作在默认组（也称为world）上运行，并且需要所有进程进入分布式函数调用。然而，某些工作负载可以从更细粒度的通信中受益。这就是分布式组的用武之地。new_group()函数可用于创建新组，包含所有进程的任意子集。它返回一个不透明的组句柄，可以作为group参数提供给所有集合（集合是在某些众所周知的编程模式中交换信息的分布式函数）。torch.distributed.new_group(ranks=None, timeout=None, backend=None, pg_options=None, use_local_synchronization=False, group_desc=None, device_id=None)[source]# 创建新的分布式组。此函数要求主组中的所有进程（即属于分布式作业的所有进程）都进入此函数，即使它们不会成为该组的成员。此外，组应该在所有进程中以相同的顺序创建。警告 安全并发使用：当使用多个带有NCCL后端的进程组时，用户必须确保跨rank的集合执行顺序全局一致。如果进程中的多个线程发出集合，则需要显式同步以确保一致的排序。当使用torch.distributed通信API的异步变体时，返回一个work对象，并且通信内核在单独的CUDA流上排队，允许通信和计算重叠。一旦在一个进程组上发出了一个或多个异步操作，在使用另一个进程组之前，必须通过调用work.wait()将它们与其他cuda流同步。有关更多详细信息，请参阅同时使用多个NCCL通信器 <https://docs.nvidia.com/deeplearning/nccl/user-guide/docs/usage/communicators.html#using-multiple-nccl-communicators-concurrently>。参数 ranks (list[int]) – 组成员的rank列表。如果

```
new_group()
```

**模式6：** 警告 安全并发使用：当使用多个带有NCCL后端的进程组时，用户必须确保跨rank的集合执行顺序全局一致。如果进程中的多个线程发出集合，则需要显式同步以确保一致的排序。当使用torch.distributed通信API的异步变体时，返回一个work对象，并且通信内核在单独的CUDA流上排队，允许通信和计算重叠。一旦在一个进程组上发出了一个或多个异步操作，在使用另一个进程组之前，必须通过调用work.wait()将它们与其他cuda流同步。有关更多详细信息，请参阅同时使用多个NCCL通信器 <https://docs.nvidia.com/deeplearning/nccl/user-guide/docs/usage/communicators.html#using-multiple-nccl-communicators-concurrently>。

```
NCCL
```

**模式7：** 注意 如果您将DistributedDataParallel与Distributed RPC Framework一起使用，您应该始终使用torch.distributed.autograd.backward()来计算梯度，并使用torch.distributed.optim.DistributedOptimizer来优化参数。示例：>>> import torch.distributed.autograd as dist_autograd >>> from torch.nn.parallel import DistributedDataParallel as DDP >>> import torch >>> from torch import optim >>> from torch.distributed.optim import DistributedOptimizer >>> import torch.distributed.rpc as rpc >>> from torch.distributed.rpc import RRef >>> >>> t1 = torch.rand((3, 3), requires_grad=True) >>> t2 = torch.rand((3, 3), requires_grad=True) >>> rref = rpc.remote("worker1", torch.add, args=(t1, t2)) >>> ddp_model = DDP(my_model) >>> >>> # 设置优化器 >>> optimizer_params = [rref] >>> for param in ddp_model.parameters(): >>> optimizer_params.append(RRef(param)) >>> >>> dist_optim = DistributedOptimizer( >>> optim.SGD, >>> optimizer_params, >>> lr=0.05, >>> ) >>> >>> with dist_autograd.context() as context_id: >>> pred = ddp_model(rref.to_here()) >>> loss = loss_func(pred, target) >>> dist_autograd.backward(context_id, [loss]) >>> dist_optim.step(context_id)

```
torch.distributed.autograd.backward()
```

**模式8：** static_graph (bool) – 当设置为True时，DDP知道训练的图是静态的。静态图意味着1）在整个训练循环中，使用和未使用的参数集不会改变；在这种情况下，用户是否设置find_unused_parameters = True并不重要。2）图的训练方式在整个训练循环中不会改变（意味着没有依赖于迭代的控制流）。当static_graph设置为True时，DDP将支持过去无法支持的情况：1）可重入反向传播。2）多次激活检查点。3）当模型有未使用的参数时进行激活检查点。4）有模型参数在forward函数之外。5）当有未使用的参数时可能会提高性能，因为当static_graph设置为True时，DDP不会在每次迭代中搜索图来检测未使用的参数。要检查是否可以将static_graph设置为True，一种方法是在之前的模型训练结束时检查ddp日志数据，如果ddp_logging_data.get("can_set_static_graph") == True，大多数情况下您也可以将static_graph设置为True。示例：>>> model_DDP = torch.nn.parallel.DistributedDataParallel(model) >>> # 训练循环 >>> ... >>> ddp_logging_data = model_DDP._get_ddp_logging_data() >>> static_graph = ddp_logging_data.get("can_set_static_graph")

```
True
```

## 参考文件

此技能在`references/`中包含全面的文档：

- **other.md** - 其他文档

当需要详细信息时，使用`view`读取特定的参考文件。

## 使用此技能

### 对于初学者
从getting_started或tutorials参考文件开始，了解基础概念。

### 对于特定功能
使用适当的类别参考文件（api、guides等）获取详细信息。

### 对于代码示例
上面的快速参考部分包含从官方文档中提取的常见模式。

## 资源

### references/
从官方来源提取的有组织文档。这些文件包含：
- 详细说明
- 带有语言注释的代码示例
- 原始文档的链接
- 用于快速导航的目录

### scripts/
在此处添加用于常见自动化任务的辅助脚本。

### assets/
在此处添加模板、样板或示例项目。

## 注意

- 此技能是从官方文档自动生成的
- 参考文件保留了源文档的结构和示例
- 代码示例包括语言检测以获得更好的语法高亮
- 快速参考模式是从文档中的常见使用示例中提取的

## 更新

要使用更新的文档刷新此技能：
1. 使用相同的配置重新运行爬虫
2. 技能将使用最新信息重建
