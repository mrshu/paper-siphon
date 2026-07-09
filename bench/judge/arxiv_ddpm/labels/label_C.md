## Denoising Diffusion Probabilistic Models

Jonathan Ho

UC Berkeley jonathanho@berkeley.edu

Ajay Jain

UC Berkeley ajayj@berkeley.edu

## Abstract

Wepresent high quality image synthesis results using diffusion probabilistic models, a class of latent variable models inspired by considerations from nonequilibrium thermodynamics. Our best results are obtained by training on a weighted variational bound designed according to a novel connection between diffusion probabilistic models and denoising score matching with Langevin dynamics, and our models naturally admit a progressive lossy decompression scheme that can be interpreted as a generalization of autoregressive decoding. On the unconditional CIFAR10 dataset, we obtain an Inception score of 9.46 and a state-of-the-art FID score of 3.17. On 256x256 LSUN, we obtain sample quality similar to ProgressiveGAN. Our implementation is available at https://github.com/hojonathanho/diffusion .

## 1 Introduction

Deep generative models of all kinds have recently exhibited high quality samples in a wide variety of data modalities. Generative adversarial networks (GANs), autoregressive models, flows, and variational autoencoders (VAEs) have synthesized striking image and audio samples [14, 27, 3, 58, 38, 25, 10, 32, 44, 57, 26, 33, 45], and there have been remarkable advances in energy-based modeling and score matching that have produced images comparable to those of GANs [11, 55].

Figure 1: Generated samples on CelebA-HQ 256 × 256 (left) and unconditional CIFAR10 (right)

<!-- image -->

34th Conference on Neural Information Processing Systems (NeurIPS 2020), Vancouver, Canada.

## Pieter Abbeel

UC Berkeley pabbeel@cs.berkeley.edu

<!-- image -->

|

-

Figure 2: The directed graphical model considered in this work.

This paper presents progress in diffusion probabilistic models [53]. A diffusion probabilistic model (which we will call a 'diffusion model' for brevity) is a parameterized Markov chain trained using variational inference to produce samples matching the data after finite time. Transitions of this chain are learned to reverse a diffusion process, which is a Markov chain that gradually adds noise to the data in the opposite direction of sampling until signal is destroyed. When the diffusion consists of small amounts of Gaussian noise, it is sufficient to set the sampling chain transitions to conditional Gaussians too, allowing for a particularly simple neural network parameterization.

Diffusion models are straightforward to define and efficient to train, but to the best of our knowledge, there has been no demonstration that they are capable of generating high quality samples. We show that diffusion models actually are capable of generating high quality samples, sometimes better than the published results on other types of generative models (Section 4). In addition, we show that a certain parameterization of diffusion models reveals an equivalence with denoising score matching over multiple noise levels during training and with annealed Langevin dynamics during sampling (Section 3.2) [55, 61]. We obtained our best sample quality results using this parameterization (Section 4.2), so we consider this equivalence to be one of our primary contributions.

Despite their sample quality, our models do not have competitive log likelihoods compared to other likelihood-based models (our models do, however, have log likelihoods better than the large estimates annealed importance sampling has been reported to produce for energy based models and score matching [11, 55]). We find that the majority of our models' lossless codelengths are consumed to describe imperceptible image details (Section 4.3). We present a more refined analysis of this phenomenon in the language of lossy compression, and we show that the sampling procedure of diffusion models is a type of progressive decoding that resembles autoregressive decoding along a bit ordering that vastly generalizes what is normally possible with autoregressive models.

## 2 Background

Diffusion models [53] are latent variable models of the form p θ ( x 0 ) := ∫ p θ ( x 0: T ) d x 1: T , where x 1 , . . . , x T are latents of the same dimensionality as the data x 0 ∼ q ( x 0 ) . The joint distribution p θ ( x 0: T ) is called the reverse process , and it is defined as a Markov chain with learned Gaussian transitions starting at p ( x T ) = N ( x T ; 0 , I ) :

<!-- formula-not-decoded -->

What distinguishes diffusion models from other types of latent variable models is that the approximate posterior q ( x 1: T | x 0 ) , called the forward process or diffusion process , is fixed to a Markov chain that gradually adds Gaussian noise to the data according to a variance schedule β 1 , . . . , β T :

<!-- formula-not-decoded -->

Training is performed by optimizing the usual variational bound on negative log likelihood:

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

The forward process variances β t can be learned by reparameterization [33] or held constant as hyperparameters, and expressiveness of the reverse process is ensured in part by the choice of Gaussian conditionals in p θ ( x t -1 | x t ) , because both processes have the same functional form when β t are small [53]. A notable property of the forward process is that it admits sampling x t at an arbitrary timestep t in closed form: using the notation α t := 1 -β t and ¯ α t := ∏ t s =1 α s , we have

Efficient training is therefore possible by optimizing random terms of L with stochastic gradient descent. Further improvements come from variance reduction by rewriting L (3) as:

<!-- formula-not-decoded -->

(See Appendix A for details. The labels on the terms are used in Section 3.) Equation (5) uses KL divergence to directly compare p θ ( x t -1 | x t ) against forward process posteriors, which are tractable when conditioned on x 0 :

<!-- formula-not-decoded -->

Consequently, all KL divergences in Eq. (5) are comparisons between Gaussians, so they can be calculated in a Rao-Blackwellized fashion with closed form expressions instead of high variance Monte Carlo estimates.

<!-- formula-not-decoded -->

## 3 Diffusion models and denoising autoencoders

Diffusion models might appear to be a restricted class of latent variable models, but they allow a large number of degrees of freedom in implementation. One must choose the variances β t of the forward process and the model architecture and Gaussian distribution parameterization of the reverse process. To guide our choices, we establish a new explicit connection between diffusion models and denoising score matching (Section 3.2) that leads to a simplified, weighted variational bound objective for diffusion models (Section 3.4). Ultimately, our model design is justified by simplicity and empirical results (Section 4). Our discussion is categorized by the terms of Eq. (5).

## 3.1 Forward process and L T

We ignore the fact that the forward process variances β t are learnable by reparameterization and instead fix them to constants (see Section 4 for details). Thus, in our implementation, the approximate posterior q has no learnable parameters, so L T is a constant during training and can be ignored.

## 3.2 Reverse process and L 1: T -1

Now we discuss our choices in p θ ( x t -1 | x t ) = N ( x t -1 ; µ θ ( x t , t ) , Σ θ ( x t , t )) for 1 &lt; t ≤ T . First, we set Σ θ ( x t , t ) = σ 2 t I to untrained time dependent constants. Experimentally, both σ 2 t = β t and σ 2 t = ˜ β t = 1 -¯ α t -1 1 -¯ α t β t had similar results. The first choice is optimal for x 0 ∼ N ( 0 , I ) , and the second is optimal for x 0 deterministically set to one point. These are the two extreme choices corresponding to upper and lower bounds on reverse process entropy for data with coordinatewise unit variance [53].

Second, to represent the mean µ θ ( x t , t ) , we propose a specific parameterization motivated by the following analysis of L t . With p θ ( x t -1 | x t ) = N ( x t -1 ; µ θ ( x t , t ) , σ 2 t I ) , we can write:

<!-- formula-not-decoded -->

where C is a constant that does not depend on θ . So, we see that the most straightforward parameterization of µ θ is a model that predicts ˜ µ t , the forward process posterior mean. However, we can expand Eq. (8) further by reparameterizing Eq. (4) as x t ( x 0 , glyph[epsilon1] ) = √ ¯ α t x 0 + √ 1 -¯ α t glyph[epsilon1] for glyph[epsilon1] ∼ N ( 0 , I ) and applying the forward process posterior formula (7):

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

| Algorithm 1 Training                                                                                                                                                                                                                                    | Algorithm 2 Sampling                                                                                                                                                                                       |
|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 1: repeat 2: x 0 ∼ q ( x 0 ) 3: t ∼ Uniform( { 1 , . . .,T } ) 4: glyph[epsilon1] ∼ N ( 0 , I ) 5: Take gradient descent step on ∇ θ ∥ ∥ glyph[epsilon1] - glyph[epsilon1] θ ( √ ¯ α t x 0 + √ 1 - ¯ α t glyph[epsilon1] , t ) ∥ ∥ 2 6: until converged | 1: x T ∼ N ( 0 , I ) 2: for t = T, . . . , 1 do 3: z ∼ N ( 0 , I ) if t > 1 , else z = 0 4: x t - 1 = 1 √ α t ( x t - 1 - α t √ 1 - ¯ α t glyph[epsilon1] θ ( x t , t ) ) + σ t z 5: end for 6: return x 0 |

Equation (10) reveals that µ θ must predict 1 √ α t ( x t -β t √ 1 -¯ α t glyph[epsilon1] ) given x t . Since x t is available as input to the model, we may choose the parameterization

<!-- formula-not-decoded -->

where glyph[epsilon1] θ is a function approximator intended to predict glyph[epsilon1] from x t . To sample x t -1 ∼ p θ ( x t -1 | x t ) is to compute x t -1 = 1 √ α t ( x t -β t √ 1 -¯ α t glyph[epsilon1] θ ( x t , t ) ) + σ t z , where z ∼ N ( 0 , I ) . The complete sampling procedure, Algorithm 2, resembles Langevin dynamics with glyph[epsilon1] θ as a learned gradient of the data density. Furthermore, with the parameterization (11), Eq. (10) simplifies to:

<!-- formula-not-decoded -->

which resembles denoising score matching over multiple noise scales indexed by t [55]. As Eq. (12) is equal to (one term of) the variational bound for the Langevin-like reverse process (11), we see that optimizing an objective resembling denoising score matching is equivalent to using variational inference to fit the finite-time marginal of a sampling chain resembling Langevin dynamics.

To summarize, we can train the reverse process mean function approximator µ θ to predict ˜ µ t , or by modifying its parameterization, we can train it to predict glyph[epsilon1] . (There is also the possibility of predicting x 0 , but we found this to lead to worse sample quality early in our experiments.) We have shown that the glyph[epsilon1] -prediction parameterization both resembles Langevin dynamics and simplifies the diffusion model's variational bound to an objective that resembles denoising score matching. Nonetheless, it is just another parameterization of p θ ( x t -1 | x t ) , so we verify its effectiveness in Section 4 in an ablation where we compare predicting glyph[epsilon1] against predicting ˜ µ t .

## 3.3 Data scaling, reverse process decoder, and L 0

We assume that image data consists of integers in { 0 , 1 , . . . , 255 } scaled linearly to [ -1 , 1] . This ensures that the neural network reverse process operates on consistently scaled inputs starting from the standard normal prior p ( x T ) . To obtain discrete log likelihoods, we set the last term of the reverse process to an independent discrete decoder derived from the Gaussian N ( x 0 ; µ θ ( x 1 , 1) , σ 2 1 I ) :

where D is the data dimensionality and the i superscript indicates extraction of one coordinate. (It would be straightforward to instead incorporate a more powerful decoder like a conditional autoregressive model, but we leave that to future work.) Similar to the discretized continuous distributions used in V AE decoders and autoregressive models [34, 52], our choice here ensures that the variational bound is a lossless codelength of discrete data, without need of adding noise to the data or incorporating the Jacobian of the scaling operation into the log likelihood. At the end of sampling, we display µ θ ( x 1 , 1) noiselessly.

<!-- formula-not-decoded -->

## 3.4 Simplified training objective

With the reverse process and decoder defined above, the variational bound, consisting of terms derived from Eqs. (12) and (13), is clearly differentiable with respect to θ and is ready to be employed for

Table 1: CIFAR10 results. NLL measured in bits/dim.

| Model                                         | IS              | FID            | NLL Test (Train)   |                                               |                                                                    |                                               |                                               |
|-----------------------------------------------|-----------------|----------------|--------------------|-----------------------------------------------|--------------------------------------------------------------------|-----------------------------------------------|-----------------------------------------------|
|                                               |                 |                |                    | Conditional                                   | Unconditional CIFAR10 reverse parameterization and training objec- |                                               |                                               |
| EBM [11]                                      | 8 . 30          | 37 . 9         |                    | tive ablation. Blank entries were unstable to | tive ablation. Blank entries were unstable to                      | tive ablation. Blank entries were unstable to | tive ablation. Blank entries were unstable to |
| JEM [17] BigGAN [3]                           | 8 . 76 9 . 22   | 38 . 4 14 . 73 |                    |                                               | poor samples with IS                                               |                                               |                                               |
| Unconditional                                 |                 |                |                    |                                               |                                                                    |                                               |                                               |
|                                               |                 |                | 5 . 40             |                                               |                                                                    |                                               |                                               |
| Diffusion (original) [53] Gated PixelCNN [59] | 4 . 60          |                | ≤ 3 . 03 (2 .      |                                               |                                                                    |                                               |                                               |
| Sparse Transformer [7]                        |                 | 65 . 93        | 90) 2 . 80         |                                               | 7 . 28 ± 0 . 10 8 . 06 0 . 09                                      |                                               |                                               |
|                                               |                 |                |                    |                                               | ±                                                                  |                                               |                                               |
| PixelIQN [43]                                 | 5 . 29          | 49 . 46        |                    |                                               | -                                                                  |                                               |                                               |
| EBM [11]                                      | 6 . 78          | 38 . 2         |                    |                                               |                                                                    |                                               |                                               |
| NCSNv2 [56]                                   |                 | 31 . 75        |                    |                                               |                                                                    |                                               |                                               |
| NCSN [55]                                     | 8 . 87 ± 0 . 12 | 25 . 32        |                    |                                               | -                                                                  |                                               |                                               |
| SNGAN [39]                                    | 8 . 22 ± 0 . 05 | 21 . 7         |                    |                                               | 7 . 67 ± 0 . 13                                                    |                                               |                                     