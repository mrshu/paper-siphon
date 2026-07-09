## Denoising Diffusion Probabilistic Models

Jonathan Ho UC Berkeley jonathanho@berkeley.edu

Ajay Jain

UC Berkeley

Pieter Abbeel UC Berkeley pabbeel@cs.berkeley.edu

## Abstract

We present high quality image synthesis results using diffusion probabilistic models, a class of latent variable models inspired by considerations from nonequilibrium thermodynamics. Our best results are obtained by training on a weighted variational bound designed according to a novel connection between diffusion probabilistic models and denoising score matching with Langevin dynamics, and our models naturally admit a progressive lossy decompression scheme that can be interpreted as a generalization of autoregressive decoding. On the unconditional CIFAR10 dataset, we obtain an Inception score of 9.46 and a state-of-the-art FID score of 3.17. On 256x256 LSUN, we obtain sample quality similar to ProgressiveGAN. Our implementation is available at https://github.com/hojonathanho/diffusion .

## 1 Introduction

Deep generative models of all kinds have recently exhibited high quality samples in a wide variety of data modalities. Generative adversarial networks (GANs), autoregressive models, flows, and variational autoencoders (VAEs) have synthesized striking image and audio samples [14, 27, 3, 58, 38, 25, 10, 32, 44, 57, 26, 33, 45], and there have been remarkable advances in energy-based modeling and score matching that have produced images comparable to those of GANs [11, 55].

Figure 1: Generated samples on CelebA-HQ 256 × 256 (left) and unconditional CIFAR10 (right)

<!-- image -->

Logo

Figure 2: The directed graphical model considered in this work.

<!-- image -->

This paper presents progress in diffusion probabilistic models [53]. A diffusion probabilistic model (which we will call a "diffusion model" for brevity) is a parameterized Markov chain trained using variational inference to produce samples matching the data after finite time. Transitions of this chain are learned to reverse a diffusion process, which is a Markov chain that gradually adds noise to the data in the opposite direction of sampling until signal is destroyed. When the diffusion consists of small amounts of Gaussian noise, it is sufficient to set the sampling chain transitions to conditional Gaussians too, allowing for a particularly simple neural network parameterization.

Diffusion models are straightforward to define and efficient to train, but to the best of our knowledge, there has been no demonstration that they are capable of generating high quality samples. We show that diffusion models actually are capable of generating high quality samples, sometimes better than the published results on other types of generative models (Section 4). In addition, we show that a certain parameterization of diffusion models reveals an equivalence with denoising score matching over multiple noise levels during training and with annealed Langevin dynamics during sampling (Section 3.2) [55, 61]. We obtained our best sample quality results using this parameterization (Section 4.2), so we consider this equivalence to be one of our primary contributions.

Despite their sample quality, our models do not have competitive log likelihoods compared to other likelihood-based models (our models do, however, have log likelihoods better than the large estimates annealed importance sampling has been reported to produce for energy based models and score matching [11, 55]). We find that the majority of our models' lossless codelengths are consumed to describe imperceptible image details (Section 4.3). We present a more refined analysis of this phenomenon in the language of lossy compression, and we show that the sampling procedure of diffusion models is a type of progressive decoding that resembles autoregressive decoding along a bit ordering that vastly generalizes what is normally possible with autoregressive models.

## 2 Background

Diffusion models [53] are latent variable models of the form p$\_{θ}$ ( x$\_{0}$ ) := ∫ p$\_{θ}$ ( x$\_{0:}$$\_{T}$ ) dx$\_{1:}$$\_{T}$ , where x$\_{1}$ , . . . , x$\_{T}$ are latents of the same dimensionality as the data x$\_{0}$ ∼ q ( x$\_{0}$ ) . The joint distribution p$\_{θ}$ ( x$\_{0:}$$\_{T}$ ) is called the reverse process , and it is defined as a Markov chain with learned Gaussian transitions starting at p ( x$\_{T}$ ) = N ( x$\_{T}$ ; 0 , I ) :

$$p _ { \theta } ( x _ { 0 \colon T } ) \coloneqq p ( x _ { T } ) \prod _ { t = 1 } ^ { T } p _ { \theta } ( x _ { t - 1 } | x _ { t } ) , \quad p _ { \theta } ( x _ { t - 1 } | x _ { t } ) \coloneqq \mathcal { N } ( x _ { t - 1 } ; \mu _ { \theta } ( x _ { t } , t ) , \Sigma _ { \theta } ( x _ { t } , t ) ) \quad ( 1 )$$

What distinguishes diffusion models from other types of latent variable models is that the approximate posterior q ( x$\_{1:}$$\_{T}$ | x$\_{0}$ ) , called the forward process or diffusion process , is fixed to a Markov chain that gradually adds Gaussian noise to the data according to a variance schedule β$\_{1}$, . . . , β$\_{T}$ :

$$q ( x _ { 1 \colon T } | x _ { 0 } ) \coloneqq \prod _ { t = 1 } ^ { T } q ( x _ { t } | x _ { t - 1 } ) , \quad q ( x _ { t } | x _ { t - 1 } ) \coloneqq \mathcal { N } ( x _ { t } ; \sqrt { 1 - \beta _ { t } } x _ { t - 1 } , \beta _ { t } \mathbf I )$$

Training is performed by optimizing the usual variational bound on negative log likelihood:

$$\mathbb { E } \left [ - \log p _ { \theta } ( \mathbf x _ { 0 } ) \right ] \leq \mathbb { E } _ { q } \left [ - \log \frac { p _ { \theta } ( \mathbf x _ { 0 \colon T } ) } { q ( \mathbf x _ { 1 \colon T } | \mathbf x _ { 0 } ) } \right ] = \mathbb { E } _ { q } \left [ - \log p ( \mathbf x _ { T } ) - \sum _ { t \geq 1 } \log \frac { p _ { \theta } ( \mathbf x _ { t - 1 } | \mathbf x _ { t } ) } { q ( \mathbf x _ { t } | \mathbf x _ { t - 1 } ) } \right ] = \colon L \ ( 3 )$$

The forward process variances β$\_{t}$ can be learned by reparameterization [33] or held constant as hyperparameters, and expressiveness of the reverse process is ensured in part by the choice of Gaussian conditionals in p$\_{θ}$ ( x$\_{t}$$\_{-}$$\_{1}$ | x$\_{t}$ ) , because both processes have the same functional form when β$\_{t}$ are small [53]. A notable property of the forward process is that it admits sampling x$\_{t}$ at an arbitrary timestep t in closed form: using the notation α$\_{t}$ := 1 - β$\_{t}$ and ¯ α$\_{t}$ := ∏ t s $\_{=1}$α$\_{s}$ , we have

$$q ( \mathbf x _ { t } | \mathbf x _ { 0 } ) = \mathcal { N } ( \mathbf x _ { t } ; \sqrt { \bar { \alpha } _ { t } } \mathbf x _ { 0 } , ( 1 - \bar { \alpha } _ { t } ) \mathbf I )$$

Efficient training is therefore possible by optimizing random terms of L with stochastic gradient descent. Further improvements come from variance reduction by rewriting L (3) as:

$$\mathbb { E } _ { q } \left [ \underbrace { D _ { K L } ( q ( x _ { T } | x _ { 0 } ) \, \| \, p ( x _ { T } ) ) } _ { L _ { T } } + \sum _ { t > 1 } \underbrace { D _ { K L } ( q ( x _ { t - 1 } | x _ { t } , x _ { 0 } ) \, \| \, p _ { \theta } ( x _ { t - 1 } | x _ { t } ) ) } _ { L _ { t - 1 } } - \log p _ { \theta } ( x _ { 0 } | x _ { 1 } ) } \right ] \, \left ( 5 \right )$$

(See Appendix A for details. The labels on the terms are used in Section 3.) Equation (5) uses KL divergence to directly compare p$\_{θ}$ ( x$\_{t}$$\_{-}$$\_{1}$ | x$\_{t}$ ) against forward process posteriors, which are tractable when conditioned on x$\_{0}$ :

$$q ( x _ { t - 1 } | x _ { t } , x _ { 0 } ) = \mathcal { N } ( x _ { t - 1 } ; \tilde { \mu } _ { t } ( x _ { t } , x _ { 0 } ) , \tilde { \beta } _ { t } \mathbf I ) ,$$

$$\text {where} \ \tilde { \mu } _ { t } ( x _ { t } , x _ { 0 } ) \colon = \frac { \sqrt { \bar { \alpha } _ { t - 1 } } \beta _ { t } } { 1 - \bar { \alpha } _ { t } } x _ { 0 } + \frac { \sqrt { \alpha _ { t } } ( 1 - \bar { \alpha } _ { t - 1 } ) } { 1 - \bar { \alpha } _ { t } } x _ { t } \quad \text {and} \quad \tilde { \beta } _ { t } \colon = \frac { 1 - \bar { \alpha } _ { t - 1 } } { 1 - \bar { \alpha } _ { t } } \beta _ { t } \quad ( 7 )$$

Consequently, all KL divergences in Eq. (5) are comparisons between Gaussians, so they can be calculated in a Rao-Blackwellized fashion with closed form expressions instead of high variance Monte Carlo estimates.

## 3 Diffusion models and denoising autoencoders

Diffusion models might appear to be a restricted class of latent variable models, but they allow a large number of degrees of freedom in implementation. One must choose the variances β$\_{t}$ of the forward process and the model architecture and Gaussian distribution parameterization of the reverse process. To guide our choices, we establish a new explicit connection between diffusion models and denoising score matching (Section 3.2) that leads to a simplified, weighted variational bound objective for diffusion models (Section 3.4). Ultimately, our model design is justified by simplicity and empirical results (Section 4). Our discussion is categorized by the terms of Eq. (5).

## 3.1 Forward process and L$\_{T}$

We ignore the fact that the forward process variances β$\_{t}$ are learnable by reparameterization and instead fix them to constants (see Section 4 for details). Thus, in our implementation, the approximate posterior q has no learnable parameters, so L$\_{T}$ is a constant during training and can be ignored.

## 3.2 Reverse process and L$\_{1:}$$\_{T}$$\_{-}$$\_{1}$

Now we discuss our choices in p$\_{θ}$ ( x$\_{t}$$\_{-}$$\_{1}$ | x$\_{t}$ ) = N ( x$\_{t}$$\_{-}$$\_{1}$ ; µ$\_{θ}$ ( x$\_{t}$ , t ) , Σ$\_{θ}$ ( x$\_{t}$ , t )) for 1

Second, to represent the mean µ$\_{θ}$ ( x$\_{t}$ , t ) , we propose a specific parameterization motivated by the following analysis of L$\_{t}$ . With p$\_{θ}$ ( x$\_{t}$$\_{-}$$\_{1}$ | x$\_{t}$ ) = N ( x$\_{t}$$\_{-}$$\_{1}$ ; µ$\_{θ}$ ( x$\_{t}$ , t ) , σ 2 $\_{t}$I ) , we can write:

$$L _ { t - 1 } = \mathbb { E } _ { q } \left [ \frac { 1 } { 2 \sigma _ { t } ^ { 2 } } \| \tilde { \mu } _ { t } ( x _ { t } , x _ { 0 } ) - \mu _ { \theta } ( x _ { t } , t ) \| ^ { 2 } \right ] + C$$

where C is a constant that does not depend on θ . So, we see that the most straightforward parameterization of µ$\_{θ}$ is a model that predicts ˜ µ$\_{t}$ , the forward process posterior mean. However, we can expand Eq. (8) further by reparameterizing Eq. (4) as x$\_{t}$ ( x$\_{0}$ , ϵ ) = √ α$\_{t}$ x$\_{0}$ + √ 1 - ¯ α$\_{t}$ ϵ for ϵ ∼ N ( 0 , I ) and applying the forward process posterior formula (7):

$$L _ { t - 1 } - C = \mathbb { E } _ { x _ { 0 } , \epsilon } \left [ \frac { 1 } { 2 \sigma _ { t } ^ { 2 } } \left \| \tilde { \mu } _ { t } \left ( x _ { t } ( x _ { 0 } , \epsilon ) , \frac { 1 } { \sqrt { \alpha _ { t } } } ( x _ { t } ( x _ { 0 } , \epsilon ) - \sqrt { 1 - \bar { \alpha } _ { t } } \epsilon ) \right ) - \mu _ { \theta } ( x _ { t } ( x _ { 0 } , \epsilon ) , t ) \right \| ^ { 2 } \right ] \\$$

$$= \mathbb { E } _ { x _ { 0 } , \epsilon } \left [ \frac { 1 } { 2 \sigma _ { t } ^ { 2 } } \left \| \frac { 1 } { \sqrt { \alpha _ { t } } } \left ( x _ { t } ( x _ { 0 } , \epsilon ) - \frac { \beta _ { t } } { \sqrt { 1 - \bar { \alpha } _ { t } } } \epsilon \right ) - \mu _ { \theta } ( x _ { t } ( x _ { 0 } , \epsilon ) , t ) \right \| ^ { 2 } \right ]$$

| Algorithm 1 Training                 | Algorithm 2 Sampling                                                                                             |
|--------------------------------------|------------------------------------------------------------------------------------------------------------------|
| 1: repeat                            | 1: x$_{T}$ ∼ N ( 0 , I )                                                                                         |
| 2: x$_{0}$ ∼ q ( x$_{0}$ )           | 2: for t = T , . . . , 1 do                                                                                      |
| 3: t ∼ Uniform ( { 1 , . . . , T } ) | 3: z ∼ N ( 0 , I ) if t > 1, else z = 0                                                                          |
| 4: ϵ ∼ N ( 0 , I )                   | 4: x$_{t}$$_{-}$$_{1}$ = 1 √ α$_{t}$ ( x$_{t}$ - 1 - α$_{t}$ √ 1 - α$_{t}$ ϵ$_{θ}$ ( x$_{t}$ , t ) ) + σ$_{t}$ z |
| 5: Take gradient descent step on     | 5: end for                                                                                                       |
| 6: until converged                   | 6: return x$_{0}$                                                                                                |

Equation (10) reveals that µ$\_{θ}$ must predict 1 √ α$\_{t}$ ( x$\_{t}$ - β$\_{t}$ √ 1 - α$\_{t}$ ϵ ) given x$\_{t}$ . Since x$\_{t}$ is available as input to the model, we may choose the parameterization

$$\mu _ { \theta } ( x _ { t } , t ) = \tilde { \mu } _ { t } \left ( x _ { t } , \frac { 1 } { \sqrt { \bar { \alpha } _ { t } } } ( x _ { t } - \sqrt { 1 - \bar { \alpha } _ { t } } \epsilon _ { \theta } ( x _ { t } ) ) \right ) = \frac { 1 } { \sqrt { \alpha _ { t } } } \left ( x _ { t } - \frac { \beta _ { t } } { \sqrt { 1 - \bar { \alpha } _ { t } } } \epsilon _ { \theta } ( x _ { t } , t ) \right ) \quad ( 1 1 )$$

where ϵ$\_{θ}$ is a function approximator intended to predict ϵ from x$\_{t}$ . To sample x$\_{t}$$\_{-}$$\_{1}$ ∼ p$\_{θ}$ ( x$\_{t}$$\_{-}$$\_{1}$ | x$\_{t}$ ) is to compute x$\_{t}$$\_{-}$$\_{1}$ = 1 √ α$\_{t}$ ( x$\_{t}$ - β$\_{t}$ √ 1 - α$\_{t}$ ϵ$\_{θ}$ ( x$\_{t}$ , t ) ) + σ$\_{t}$ z , where z ∼ N ( 0 , I ) . The complete sampling procedure, Algorithm 2, resembles Langevin dynamics with ϵ$\_{θ}$ as a learned gradient of the data density. Furthermore, with the parameterization (11), Eq. (10) simplifies to:

$$\mathbb { E } _ { x _ { 0 } , \epsilon } \left [ \frac { \beta _ { t } ^ { 2 } } { 2 \sigma _ { t } ^ { 2 } \alpha _ { t } ( 1 - \bar { \alpha } _ { t } ) } \left \| \epsilon - \epsilon _ { \theta } ( \sqrt { \bar { \alpha } _ { t } } x _ { 0 } + \sqrt { 1 - \bar { \alpha } _ { t } } \epsilon , t ) \right \| ^ { 2 } \right ]$$

which resembles denoising score matching over multiple noise scales indexed by t [55]. As Eq. (12) is equal to (one term of) the variational bound for the Langevin-like reverse process (11), we see that optimizing an objective resembling denoising score matching is equivalent to using variational inference to fit the finite-time marginal of a sampling chain resembling Langevin dynamics.

To summarize, we can train the reverse process mean function approximator µ$\_{θ}$ to predict ˜ µ$\_{t}$ , or by modifying its parameterization, we can train it to predict ϵ . (There is also the possibility of predicting x$\_{0}$ , but we found this to lead to worse sample quality early in our experiments.) We have shown that the ϵ -prediction parameterization both resembles Langevin dynamics and simplifies the diffusion model's variational bound to an objective that resembles denoising score matching. Nonetheless, it is just another parameterization of p$\_{θ}$ ( x$\_{t}$$\_{-}$$\_{1}$ | x$\_{t}$ ) , so we verify its effectiveness in Section 4 in an ablation where we compare predicting ϵ against predicting ˜ µ$\_{t}$ .

## 3.3 Data scaling, reverse process decoder, and L$\_{0}$

We assume that image data consists of integers in { 0 , 1 , . . . , 255 } scaled linearly to [ - 1 , 1 ] . This ensures that the neural network reverse process operates on consistently scaled inputs starting from the standard normal prior p ( x$\_{T}$ ) . To obtain discrete log likelihoods, we set the last term of the reverse process to an independent discrete decoder derived from the Gaussian N ( x$\_{0}$ ; µ$\_{θ}$ ( x$\_{1}$ , 1 ) , σ 2 $\_{1}$I ):

$$p _ { \theta } ( \mathbf x _ { 0 } | \mathbf x _ { 1 } ) & = \prod _ { i = 1 } ^ { D } \int _ { \delta _ { - } ( x _ { 0 } ^ { i } ) } ^ { \delta _ { + } ( x _ { 0 } ^ { i } ) } \mathcal { N } ( x ; \mu _ { \theta } ^ { i } ( \mathbf x _ { 1 } , 1 ) , \sigma _ { 1 } ^ { 2 } ) \, d x \\ & \delta _ { + } ( x ) = \left \{ \begin{array} { c c } \infty & \text {if $x=1$} \\ x + \frac { 1 } { 2 5 5 } & \text {if $x1$} \end{array}$$

where D is the data dimensionality and the i superscript indicates extraction of one coordinate. (It would be straightforward to instead incorporate a more powerful decoder like a conditional autoregressive model, but we leave that to future work.) Similar to the discretized continuous distributions used in VAE decoders and autoregressive models [34, 52], our choice here ensures that the variational bound is a lossless codelength of discrete data, without need of adding noise to the data or incorporating the Jacobian of the scaling operation into the log likelihood. At the end of sampling, we display µ$\_{θ}$ ( x$\_{1}$ , 1 ) noiselessly.

## 3.4 Simplified training objective

With the reverse process and decoder defined above, the variational bound, consisting of terms derived from Eqs. (12) and (13), is clearly differentiable with respect to θ and is ready to be employed for

Table 1: CIFAR10 results. NLL measured in bits/dim.

| Model                          | IS            | FID   | NLL Test (Train)          |                                                                                                                                                                               |
|--------------------------------|---------------|-------|---------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Conditional                    |               |       |                           | Table 2: Unconditional CIFAR10 reverse process parameterization and training objective ablation. Blank entries were unstable to train and generated poor samples with out-of- |
| EBM [11]                       | 8.30          | 37.9  |                           |                                                 