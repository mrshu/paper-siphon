# AN IMAGE IS WORTH 16X16 WORDS: TRANSFORMERS FOR IMAGE RECOGNITION AT SCALE

Alexey Dosovitskiy∗,† , Lucas Beyer<sup>∗</sup> , Alexander Kolesnikov<sup>∗</sup> , Dirk Weissenborn<sup>∗</sup> , Xiaohua Zhai<sup>∗</sup> , Thomas Unterthiner, Mostafa Dehghani, Matthias Minderer, Georg Heigold, Sylvain Gelly, Jakob Uszkoreit, Neil Houlsby∗,†

> ∗ equal technical contribution, † equal advising Google Research, Brain Team {adosovitskiy, neilhoulsby}@google.com

# ABSTRACT

While the Transformer architecture has become the de-facto standard for natural language processing tasks, its applications to computer vision remain limited. In vision, attention is either applied in conjunction with convolutional networks, or used to replace certain components of convolutional networks while keeping their overall structure in place. We show that this reliance on CNNs is not necessary and a pure transformer applied directly to sequences of image patches can perform very well on image classification tasks. When pre-trained on large amounts of data and transferred to multiple mid-sized or small image recognition benchmarks (ImageNet, CIFAR-100, VTAB, etc.), Vision Transformer (ViT) attains excellent results compared to state-of-the-art convolutional networks while requiring substantially fewer computational resources to train.[1](#page-0-0)

# 1 INTRODUCTION

Self-attention-based architectures, in particular Transformers [\(Vaswani et al., 2017\)](#page-11-0), have become the model of choice in natural language processing (NLP). The dominant approach is to pre-train on a large text corpus and then fine-tune on a smaller task-specific dataset [\(Devlin et al., 2019\)](#page-9-0). Thanks to Transformers' computational efficiency and scalability, it has become possible to train models of unprecedented size, with over 100B parameters [\(Brown et al., 2020;](#page-9-1) [Lepikhin et al., 2020\)](#page-10-0). With the models and datasets growing, there is still no sign of saturating performance.

In computer vision, however, convolutional architectures remain dominant [\(LeCun et al., 1989;](#page-10-1) [Krizhevsky et al., 2012;](#page-10-2) [He et al., 2016\)](#page-9-2). Inspired by NLP successes, multiple works try combining CNN-like architectures with self-attention [\(Wang et al., 2018;](#page-11-1) [Carion et al., 2020\)](#page-9-3), some replacing the convolutions entirely [\(Ramachandran et al., 2019;](#page-10-3) [Wang et al., 2020a\)](#page-11-2). The latter models, while theoretically efficient, have not yet been scaled effectively on modern hardware accelerators due to the use of specialized attention patterns. Therefore, in large-scale image recognition, classic ResNetlike architectures are still state of the art [\(Mahajan et al., 2018;](#page-10-4) [Xie et al., 2020;](#page-11-3) [Kolesnikov et al.,](#page-10-5) [2020\)](#page-10-5).

Inspired by the Transformer scaling successes in NLP, we experiment with applying a standard Transformer directly to images, with the fewest possible modifications. To do so, we split an image into patches and provide the sequence of linear embeddings of these patches as an input to a Transformer. Image patches are treated the same way as tokens (words) in an NLP application. We train the model on image classification in supervised fashion.

When trained on mid-sized datasets such as ImageNet without strong regularization, these models yield modest accuracies of a few percentage points below ResNets of comparable size. This seemingly discouraging outcome may be expected: Transformers lack some of the inductive biases

<span id="page-0-0"></span><sup>1</sup> Fine-tuning code and pre-trained models are available at [https://github.com/](https://github.com/google-research/vision_transformer) [google-research/vision\\_transformer](https://github.com/google-research/vision_transformer)

inherent to CNNs, such as translation equivariance and locality, and therefore do not generalize well when trained on insufficient amounts of data.

However, the picture changes if the models are trained on larger datasets (14M-300M images). We find that large scale training trumps inductive bias. Our Vision Transformer (ViT) attains excellent results when pre-trained at sufficient scale and transferred to tasks with fewer datapoints. When pre-trained on the public ImageNet-21k dataset or the in-house JFT-300M dataset, ViT approaches or beats state of the art on multiple image recognition benchmarks. In particular, the best model reaches the accuracy of 88.55% on ImageNet, 90.72% on ImageNet-ReaL, 94.55% on CIFAR-100, and 77.63% on the VTAB suite of 19 tasks.

# 2 RELATED WORK

Transformers were proposed by [Vaswani et al.](#page-11-0) [\(2017\)](#page-11-0) for machine translation, and have since become the state of the art method in many NLP tasks. Large Transformer-based models are often pre-trained on large corpora and then fine-tuned for the task at hand: BERT [\(Devlin et al., 2019\)](#page-9-0) uses a denoising self-supervised pre-training task, while the GPT line of work uses language modeling as its pre-training task [\(Radford et al., 2018;](#page-10-6) [2019;](#page-10-7) [Brown et al., 2020\)](#page-9-1).

Naive application of self-attention to images would require that each pixel attends to every other pixel. With quadratic cost in the number of pixels, this does not scale to realistic input sizes. Thus, to apply Transformers in the context of image processing, several approximations have been tried in the past. [Parmar et al.](#page-10-8) [\(2018\)](#page-10-8) applied the self-attention only in local neighborhoods for each query pixel instead of globally. Such local multi-head dot-product self attention blocks can completely replace convolutions [\(Hu et al., 2019;](#page-9-4) [Ramachandran et al., 2019;](#page-10-3) [Zhao et al., 2020\)](#page-11-4). In a different line of work, Sparse Transformers [\(Child et al., 2019\)](#page-9-5) employ scalable approximations to global selfattention in order to be applicable to images. An alternative way to scale attention is to apply it in blocks of varying sizes [\(Weissenborn et al., 2019\)](#page-11-5), in the extreme case only along individual axes [\(Ho](#page-9-6) [et al., 2019;](#page-9-6) [Wang et al., 2020a\)](#page-11-2). Many of these specialized attention architectures demonstrate promising results on computer vision tasks, but require complex engineering to be implemented efficiently on hardware accelerators.

Most related to ours is the model of [Cordonnier et al.](#page-9-7) [\(2020\)](#page-9-7), which extracts patches of size 2 × 2 from the input image and applies full self-attention on top. This model is very similar to ViT, but our work goes further to demonstrate that large scale pre-training makes vanilla transformers competitive with (or even better than) state-of-the-art CNNs. Moreover, [Cordonnier et al.](#page-9-7) [\(2020\)](#page-9-7) use a small patch size of 2 × 2 pixels, which makes the model applicable only to small-resolution images, while we handle medium-resolution images as well.

There has also been a lot of interest in combining convolutional neural networks (CNNs) with forms of self-attention, e.g. by augmenting feature maps for image classification [\(Bello et al., 2019\)](#page-9-8) or by further processing the output of a CNN using self-attention, e.g. for object detection [\(Hu et al., 2018;](#page-9-9) [Carion et al., 2020\)](#page-9-3), video processing [\(Wang et al., 2018;](#page-11-1) [Sun et al., 2019\)](#page-10-9), image classification [\(Wu](#page-11-6) [et al., 2020\)](#page-11-6), unsupervised object discovery [\(Locatello et al., 2020\)](#page-10-10), or unified text-vision tasks [\(Chen](#page-9-10) [et al., 2020c;](#page-9-10) [Lu et al., 2019;](#page-10-11) [Li et al., 2019\)](#page-10-12).

Another recent related model is image GPT (iGPT) [\(Chen et al., 2020a\)](#page-9-11), which applies Transformers to image pixels after reducing image resolution and color space. The model is trained in an unsupervised fashion as a generative model, and the resulting representation can then be fine-tuned or probed linearly for classification performance, achieving a maximal accuracy of 72% on ImageNet.

Our work adds to the increasing collection of papers that explore image recognition at larger scales than the standard ImageNet dataset. The use of additional data sources allows to achieve state-ofthe-art results on standard benchmarks [\(Mahajan et al., 2018;](#page-10-4) [Touvron et al., 2019;](#page-11-7) [Xie et al., 2020\)](#page-11-3). Moreover, [Sun et al.](#page-10-13) [\(2017\)](#page-10-13) study how CNN performance scales with dataset size, and [Kolesnikov](#page-10-5) [et al.](#page-10-5) [\(2020\)](#page-10-5); [Djolonga et al.](#page-9-12) [\(2020\)](#page-9-12) perform an empirical exploration of CNN transfer learning from large scale datasets such as ImageNet-21k and JFT-300M. We focus on these two latter datasets as well, but train Transformers instead of ResNet-based models used in prior works.

<span id="page-2-0"></span>Figure 1: Model overview. We split an image into fixed-size patches, linearly embed each of them, add position embeddings, and feed the resulting sequence of vectors to a standard Transformer encoder. In order to perform classification, we use the standard approach of adding an extra learnable "classification token" to the sequence. The illustration of the Transformer encoder was inspired by Vaswani et al. (2017).

#### 3 Method

In model design we follow the original Transformer (Vaswani et al., 2017) as closely as possible. An advantage of this intentionally simple setup is that scalable NLP Transformer architectures – and their efficient implementations – can be used almost out of the box.

#### 3.1 VISION TRANSFORMER (VIT)

An overview of the model is depicted in Figure 1. The standard Transformer receives as input a 1D sequence of token embeddings. To handle 2D images, we reshape the image  $\mathbf{x} \in \mathbb{R}^{H \times W \times C}$  into a sequence of flattened 2D patches  $\mathbf{x}_p \in \mathbb{R}^{N \times (P^2 \cdot C)}$ , where (H, W) is the resolution of the original image, C is the number of channels, (P, P) is the resolution of each image patch, and  $N = HW/P^2$  is the resulting number of patches, which also serves as the effective input sequence length for the Transformer. The Transformer uses constant latent vector size D through all of its layers, so we flatten the patches and map to D dimensions with a trainable linear projection (Eq. 1). We refer to the output of this projection as the patch embeddings.

Similar to BERT's [class] token, we prepend a learnable embedding to the sequence of embedded patches ( $\mathbf{z}_0^0 = \mathbf{x}_{\text{class}}$ ), whose state at the output of the Transformer encoder ( $\mathbf{z}_L^0$ ) serves as the image representation  $\mathbf{y}$  (Eq. 4). Both during pre-training and fine-tuning, a classification head is attached to  $\mathbf{z}_L^0$ . The classification head is implemented by a MLP with one hidden layer at pre-training time and by a single linear layer at fine-tuning time.

Position embeddings are added to the patch embeddings to retain positional information. We use standard learnable 1D position embeddings, since we have not observed significant performance gains from using more advanced 2D-aware position embeddings (Appendix D.4). The resulting sequence of embedding vectors serves as input to the encoder.

The Transformer encoder (Vaswani et al., 2017) consists of alternating layers of multiheaded self-attention (MSA, see Appendix A) and MLP blocks (Eq. 2, 3). Layernorm (LN) is applied before every block, and residual connections after every block (Wang et al., 2019; Baevski & Auli, 2019).

The MLP contains two layers with a GELU non-linearity.

$$\mathbf{z}_0 = [\mathbf{x}_{\text{class}}; \, \mathbf{x}_p^1 \mathbf{E}; \, \mathbf{x}_p^2 \mathbf{E}; \cdots; \, \mathbf{x}_p^N \mathbf{E}] + \mathbf{E}_{pos}, \qquad \mathbf{E} \in \mathbb{R}^{(P^2 \cdot C) \times D}, \, \mathbf{E}_{pos} \in \mathbb{R}^{(N+1) \times D}$$
(1)

$$\mathbf{z}'_{\ell} = \text{MSA}(\text{LN}(\mathbf{z}_{\ell-1})) + \mathbf{z}_{\ell-1}, \qquad \qquad \ell = 1 \dots L$$
 (2)

<span id="page-3-0"></span>
$$\mathbf{z}_{\ell} = \text{MLP}(\text{LN}(\mathbf{z'}_{\ell})) + \mathbf{z'}_{\ell}, \qquad \qquad \ell = 1 \dots L$$
 (3)

<span id="page-3-3"></span><span id="page-3-2"></span><span id="page-3-1"></span>
$$\mathbf{y} = \mathrm{LN}(\mathbf{z}_L^0) \tag{4}$$

Inductive bias. We note that Vision Transformer has much less image-specific inductive bias than CNNs. In CNNs, locality, two-dimensional neighborhood structure, and translation equivariance are baked into each layer throughout the whole model. In ViT, only MLP layers are local and translationally equivariant, while the self-attention layers are global. The two-dimensional neighborhood structure is used very sparingly: in the beginning of the model by cutting the image into patches and at fine-tuning time for adjusting the position embeddings for images of different resolution (as described below). Other than that, the position embeddings at initialization time carry no information about the 2D positions of the patches and all spatial relations between the patches have to be learned from scratch.

Hybrid Architecture. As an alternative to raw image patches, the input sequence can be formed from feature maps of a CNN [\(LeCun et al., 1989\)](#page-10-1). In this hybrid model, the patch embedding projection E (Eq. [1\)](#page-3-0) is applied to patches extracted from a CNN feature map. As a special case, the patches can have spatial size 1x1, which means that the input sequence is obtained by simply flattening the spatial dimensions of the feature map and projecting to the Transformer dimension. The classification input embedding and position embeddings are added as described above.

### 3.2 FINE-TUNING AND HIGHER RESOLUTION

Typically, we pre-train ViT on large datasets, and fine-tune to (smaller) downstream tasks. For this, we remove the pre-trained prediction head and attach a zero-initialized D × K feedforward layer, where K is the number of downstream classes. It is often beneficial to fine-tune at higher resolution than pre-training [\(Touvron et al., 2019;](#page-11-7) [Kolesnikov et al., 2020\)](#page-10-5). When feeding images of higher resolution, we keep the patch size the same, which results in a larger effective sequence length. The Vision Transformer can handle arbitrary sequence lengths (up to memory constraints), however, the pre-trained position embeddings may no longer be meaningful. We therefore perform 2D interpolation of the pre-trained position embeddings, according to their location in the original image. Note that this resolution adjustment and patch extraction are the only points at which an inductive bias about the 2D structure of the images is manually injected into the Vision Transformer.

# 4 EXPERIMENTS

We evaluate the representation learning capabilities of ResNet, Vision Transformer (ViT), and the hybrid. To understand the data requirements of each model, we pre-train on datasets of varying size and evaluate many benchmark tasks. When considering the computational cost of pre-training the model, ViT performs very favourably, attaining state of the art on most recognition benchmarks at a lower pre-training cost. Lastly, we perform a small experiment using self-supervision, and show that self-supervised ViT holds promise for the future.

#### 4.1 SETUP

Datasets. To explore model scalability, we use the ILSVRC-2012 ImageNet dataset with 1k classes and 1.3M images (we refer to it as ImageNet in what follows), its superset ImageNet-21k with 21k classes and 14M images [\(Deng et al., 2009\)](#page-9-14), and JFT [\(Sun et al., 2017\)](#page-10-13) with 18k classes and 303M high-resolution images. We de-duplicate the pre-training datasets w.r.t. the test sets of the downstream tasks following [Kolesnikov et al.](#page-10-5) [\(2020\)](#page-10-5). We transfer the models trained on these dataset to several benchmark tasks: ImageNet on the original validation labels and the cleaned-up ReaL labels [\(Beyer et al., 2020\)](#page-9-15), CIFAR-10/100 [\(Krizhevsky, 2009\)](#page-10-14), Oxford-IIIT Pets [\(Parkhi et al.,](#page-10-15) [2012\)](#page-10-15), and Oxford Flowers-102 [\(Nilsback & Zisserman, 2008\)](#page-10-16). For these datasets, pre-processing follows [Kolesnikov et al.](#page-10-5) [\(2020\)](#page-10-5).

| Model     | Layers | Hidden size D | MLP size | Heads | Params |
|-----------|--------|---------------|----------|-------|--------|
| ViT-Base  | 12     | 768           | 3072     | 12    | 86M    |
| ViT-Large | 24     | 1024          | 4096     | 16    | 307M   |
| ViT-Huge  | 32     | 1280          | 5120     | 16    | 632M   |

<span id="page-4-0"></span>Table 1: Details of Vision Transformer model variants.

We also evaluate on the 19-task VTAB classification suite [\(Zhai et al., 2019b\)](#page-11-9). VTAB evaluates low-data transfer to diverse tasks, using 1 000 training examples per task. The tasks are divided into three groups: *Natural* – tasks like the above, Pets, CIFAR, etc. *Specialized* – medical and satellite imagery, and *Structured* – tasks that require geometric understanding like localization.

Model Variants. We base ViT configurations on those used for BERT [\(Devlin et al., 2019\)](#page-9-0), as summarized in Table [1.](#page-4-0) The "Base" and "Large" models are directly adopted from BERT and we add the larger "Huge" model. In what follows we use brief notation to indicate the model size and the input patch size: for instance, ViT-L/16 means the "Large" variant with 16×16 input patch size. Note that the Transformer's sequence length is inversely proportional to the square of the patch size, thus models with smaller patch size are computationally more exp