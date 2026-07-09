# Denoising Diffusion Probabilistic Models

Jonathan Ho UC Berkeley jonathanho@berkeley.edu

Ajay Jain UC Berkeley ajayj@berkeley.edu

Pieter Abbeel UC Berkeley pabbeel@cs.berkeley.edu

# Abstract

We present high quality image synthesis results using diffusion probabilistic models, a class of latent variable models inspired by considerations from nonequilibrium thermodynamics. Our best results are obtained by training on a weighted variational bound designed according to a novel connection between diffusion probabilistic models and denoising score matching with Langevin dynamics, and our models naturally admit a progressive lossy decompression scheme that can be interpreted as a generalization of autoregressive decoding. On the unconditional CIFAR10 dataset, we obtain an Inception score of 9.46 and a state-of-the-art FID score of 3.17. On 256x256 LSUN, we obtain sample quality similar to ProgressiveGAN. Our implementation is available at <https://github.com/hojonathanho/diffusion>.

# 1 Introduction

Deep generative models of all kinds have recently exhibited high quality samples in a wide variety of data modalities. Generative adversarial networks (GANs), autoregressive models, flows, and variational autoencoders (VAEs) have synthesized striking image and audio samples [\[14,](#page-9-0) [27,](#page-9-1) [3,](#page-8-0) [58,](#page-11-0) [38,](#page-10-0) [25,](#page-9-2) [10,](#page-9-3) [32,](#page-10-1) [44,](#page-10-2) [57,](#page-11-1) [26,](#page-9-4) [33,](#page-10-3) [45\]](#page-10-4), and there have been remarkable advances in energy-based modeling and score matching that have produced images comparable to those of GANs [\[11,](#page-9-5) [55\]](#page-11-2).

<span id="page-0-0"></span>Figure 1: Generated samples on CelebA-HQ 256 × 256 (left) and unconditional CIFAR10 (right)

34th Conference on Neural Information Processing Systems (NeurIPS 2020), Vancouver, Canada.

Figure 2: The directed graphical model considered in this work.

This paper presents progress in diffusion probabilistic models [53]. A diffusion probabilistic model (which we will call a "diffusion model" for brevity) is a parameterized Markov chain trained using variational inference to produce samples matching the data after finite time. Transitions of this chain are learned to reverse a diffusion process, which is a Markov chain that gradually adds noise to the data in the opposite direction of sampling until signal is destroyed. When the diffusion consists of small amounts of Gaussian noise, it is sufficient to set the sampling chain transitions to conditional Gaussians too, allowing for a particularly simple neural network parameterization.

Diffusion models are straightforward to define and efficient to train, but to the best of our knowledge, there has been no demonstration that they are capable of generating high quality samples. We show that diffusion models actually are capable of generating high quality samples, sometimes better than the published results on other types of generative models (Section 4). In addition, we show that a certain parameterization of diffusion models reveals an equivalence with denoising score matching over multiple noise levels during training and with annealed Langevin dynamics during sampling (Section 3.2) [55, 61]. We obtained our best sample quality results using this parameterization (Section 4.2), so we consider this equivalence to be one of our primary contributions.

Despite their sample quality, our models do not have competitive log likelihoods compared to other likelihood-based models (our models do, however, have log likelihoods better than the large estimates annealed importance sampling has been reported to produce for energy based models and score matching [11, 55]). We find that the majority of our models' lossless codelengths are consumed to describe imperceptible image details (Section 4.3). We present a more refined analysis of this phenomenon in the language of lossy compression, and we show that the sampling procedure of diffusion models is a type of progressive decoding that resembles autoregressive decoding along a bit ordering that vastly generalizes what is normally possible with autoregressive models.

# 2 Background

Diffusion models [53] are latent variable models of the form  $p_{\theta}(\mathbf{x}_0) \coloneqq \int p_{\theta}(\mathbf{x}_{0:T}) d\mathbf{x}_{1:T}$ , where  $\mathbf{x}_1, \dots, \mathbf{x}_T$  are latents of the same dimensionality as the data  $\mathbf{x}_0 \sim q(\mathbf{x}_0)$ . The joint distribution  $p_{\theta}(\mathbf{x}_{0:T})$  is called the *reverse process*, and it is defined as a Markov chain with learned Gaussian transitions starting at  $p(\mathbf{x}_T) = \mathcal{N}(\mathbf{x}_T; \mathbf{0}, \mathbf{I})$ :

$$p_{\theta}(\mathbf{x}_{0:T}) \coloneqq p(\mathbf{x}_{T}) \prod_{t=1}^{T} p_{\theta}(\mathbf{x}_{t-1}|\mathbf{x}_{t}), \qquad p_{\theta}(\mathbf{x}_{t-1}|\mathbf{x}_{t}) \coloneqq \mathcal{N}(\mathbf{x}_{t-1}; \boldsymbol{\mu}_{\theta}(\mathbf{x}_{t}, t), \boldsymbol{\Sigma}_{\theta}(\mathbf{x}_{t}, t))$$
(1)

What distinguishes diffusion models from other types of latent variable models is that the approximate posterior  $q(\mathbf{x}_{1:T}|\mathbf{x}_0)$ , called the *forward process* or *diffusion process*, is fixed to a Markov chain that gradually adds Gaussian noise to the data according to a variance schedule  $\beta_1, \ldots, \beta_T$ :

$$q(\mathbf{x}_{1:T}|\mathbf{x}_0) := \prod_{t=1}^{T} q(\mathbf{x}_t|\mathbf{x}_{t-1}), \qquad q(\mathbf{x}_t|\mathbf{x}_{t-1}) := \mathcal{N}(\mathbf{x}_t; \sqrt{1-\beta_t}\mathbf{x}_{t-1}, \beta_t \mathbf{I})$$
(2)

Training is performed by optimizing the usual variational bound on negative log likelihood:

$$\mathbb{E}\left[-\log p_{\theta}(\mathbf{x}_{0})\right] \leq \mathbb{E}_{q}\left[-\log \frac{p_{\theta}(\mathbf{x}_{0:T})}{q(\mathbf{x}_{1:T}|\mathbf{x}_{0})}\right] = \mathbb{E}_{q}\left[-\log p(\mathbf{x}_{T}) - \sum_{t>1} \log \frac{p_{\theta}(\mathbf{x}_{t-1}|\mathbf{x}_{t})}{q(\mathbf{x}_{t}|\mathbf{x}_{t-1})}\right] =: L \quad (3)$$

The forward process variances  $\beta_t$  can be learned by reparameterization [33] or held constant as hyperparameters, and expressiveness of the reverse process is ensured in part by the choice of Gaussian conditionals in  $p_{\theta}(\mathbf{x}_{t-1}|\mathbf{x}_t)$ , because both processes have the same functional form when  $\beta_t$  are small [53]. A notable property of the forward process is that it admits sampling  $\mathbf{x}_t$  at an arbitrary timestep t in closed form: using the notation  $\alpha_t := 1 - \beta_t$  and  $\bar{\alpha}_t := \prod_{s=1}^t \alpha_s$ , we have

<span id="page-1-2"></span><span id="page-1-1"></span><span id="page-1-0"></span>
$$q(\mathbf{x}_t|\mathbf{x}_0) = \mathcal{N}(\mathbf{x}_t; \sqrt{\bar{\alpha}_t}\mathbf{x}_0, (1 - \bar{\alpha}_t)\mathbf{I})$$
(4)

Efficient training is therefore possible by optimizing random terms of L with stochastic gradient descent. Further improvements come from variance reduction by rewriting L (3) as:

$$\mathbb{E}_{q}\left[\underbrace{D_{\mathrm{KL}}(q(\mathbf{x}_{T}|\mathbf{x}_{0}) \parallel p(\mathbf{x}_{T}))}_{L_{T}} + \sum_{t>1} \underbrace{D_{\mathrm{KL}}(q(\mathbf{x}_{t-1}|\mathbf{x}_{t},\mathbf{x}_{0}) \parallel p_{\theta}(\mathbf{x}_{t-1}|\mathbf{x}_{t}))}_{L_{t-1}} \underbrace{-\log p_{\theta}(\mathbf{x}_{0}|\mathbf{x}_{1})}_{L_{0}}\right]$$
(5)

(See Appendix A for details. The labels on the terms are used in Section 3.) Equation (5) uses KL divergence to directly compare  $p_{\theta}(\mathbf{x}_{t-1}|\mathbf{x}_t)$  against forward process posteriors, which are tractable when conditioned on  $\mathbf{x}_0$ :

<span id="page-2-4"></span><span id="page-2-2"></span>
$$q(\mathbf{x}_{t-1}|\mathbf{x}_t, \mathbf{x}_0) = \mathcal{N}(\mathbf{x}_{t-1}; \tilde{\boldsymbol{\mu}}_t(\mathbf{x}_t, \mathbf{x}_0), \tilde{\beta}_t \mathbf{I}), \tag{6}$$

where 
$$\tilde{\boldsymbol{\mu}}_t(\mathbf{x}_t, \mathbf{x}_0) \coloneqq \frac{\sqrt{\bar{\alpha}_{t-1}}\beta_t}{1 - \bar{\alpha}_t}\mathbf{x}_0 + \frac{\sqrt{\alpha_t}(1 - \bar{\alpha}_{t-1})}{1 - \bar{\alpha}_t}\mathbf{x}_t$$
 and  $\tilde{\beta}_t \coloneqq \frac{1 - \bar{\alpha}_{t-1}}{1 - \bar{\alpha}_t}\beta_t$  (7)

Consequently, all KL divergences in Eq. (5) are comparisons between Gaussians, so they can be calculated in a Rao-Blackwellized fashion with closed form expressions instead of high variance Monte Carlo estimates.

### <span id="page-2-1"></span>3 Diffusion models and denoising autoencoders

Diffusion models might appear to be a restricted class of latent variable models, but they allow a large number of degrees of freedom in implementation. One must choose the variances  $\beta_t$  of the forward process and the model architecture and Gaussian distribution parameterization of the reverse process. To guide our choices, we establish a new explicit connection between diffusion models and denoising score matching (Section 3.2) that leads to a simplified, weighted variational bound objective for diffusion models (Section 3.4). Ultimately, our model design is justified by simplicity and empirical results (Section 4). Our discussion is categorized by the terms of Eq. (5).

### 3.1 Forward process and $L_T$

We ignore the fact that the forward process variances  $\beta_t$  are learnable by reparameterization and instead fix them to constants (see Section 4 for details). Thus, in our implementation, the approximate posterior q has no learnable parameters, so  $L_T$  is a constant during training and can be ignored.

### <span id="page-2-0"></span>3.2 Reverse process and $L_{1:T-1}$

Now we discuss our choices in  $p_{\theta}(\mathbf{x}_{t-1}|\mathbf{x}_t) = \mathcal{N}(\mathbf{x}_{t-1}; \boldsymbol{\mu}_{\theta}(\mathbf{x}_t, t), \boldsymbol{\Sigma}_{\theta}(\mathbf{x}_t, t))$  for  $1 < t \leq T$ . First, we set  $\boldsymbol{\Sigma}_{\theta}(\mathbf{x}_t, t) = \sigma_t^2 \mathbf{I}$  to untrained time dependent constants. Experimentally, both  $\sigma_t^2 = \beta_t$  and  $\sigma_t^2 = \tilde{\beta}_t = \frac{1 - \tilde{\alpha}_{t-1}}{1 - \tilde{\alpha}_t} \beta_t$  had similar results. The first choice is optimal for  $\mathbf{x}_0 \sim \mathcal{N}(\mathbf{0}, \mathbf{I})$ , and the second is optimal for  $\mathbf{x}_0$  deterministically set to one point. These are the two extreme choices corresponding to upper and lower bounds on reverse process entropy for data with coordinatewise unit variance [53].

Second, to represent the mean  $\mu_{\theta}(\mathbf{x}_t,t)$ , we propose a specific parameterization motivated by the following analysis of  $L_t$ . With  $p_{\theta}(\mathbf{x}_{t-1}|\mathbf{x}_t) = \mathcal{N}(\mathbf{x}_{t-1}; \boldsymbol{\mu}_{\theta}(\mathbf{x}_t,t), \sigma_t^2 \mathbf{I})$ , we can write:

<span id="page-2-5"></span><span id="page-2-3"></span>
$$L_{t-1} = \mathbb{E}_q \left[ \frac{1}{2\sigma_t^2} \| \tilde{\boldsymbol{\mu}}_t(\mathbf{x}_t, \mathbf{x}_0) - \boldsymbol{\mu}_{\theta}(\mathbf{x}_t, t) \|^2 \right] + C$$
 (8)

where C is a constant that does not depend on  $\theta$ . So, we see that the most straightforward parameterization of  $\mu_{\theta}$  is a model that predicts  $\tilde{\mu}_{t}$ , the forward process posterior mean. However, we can expand Eq. (8) further by reparameterizing Eq. (4) as  $\mathbf{x}_{t}(\mathbf{x}_{0}, \boldsymbol{\epsilon}) = \sqrt{\bar{\alpha}_{t}}\mathbf{x}_{0} + \sqrt{1-\bar{\alpha}_{t}}\boldsymbol{\epsilon}$  for  $\boldsymbol{\epsilon} \sim \mathcal{N}(\mathbf{0}, \mathbf{I})$  and applying the forward process posterior formula (7):

$$L_{t-1} - C = \mathbb{E}_{\mathbf{x}_0, \epsilon} \left[ \frac{1}{2\sigma_t^2} \left\| \tilde{\boldsymbol{\mu}}_t \left( \mathbf{x}_t(\mathbf{x}_0, \epsilon), \frac{1}{\sqrt{\bar{\alpha}_t}} (\mathbf{x}_t(\mathbf{x}_0, \epsilon) - \sqrt{1 - \bar{\alpha}_t} \epsilon) \right) - \boldsymbol{\mu}_{\theta} (\mathbf{x}_t(\mathbf{x}_0, \epsilon), t) \right\|^2 \right]$$
(9)

$$= \mathbb{E}_{\mathbf{x}_0, \boldsymbol{\epsilon}} \left[ \frac{1}{2\sigma_t^2} \left\| \frac{1}{\sqrt{\alpha_t}} \left( \mathbf{x}_t(\mathbf{x}_0, \boldsymbol{\epsilon}) - \frac{\beta_t}{\sqrt{1 - \bar{\alpha}_t}} \boldsymbol{\epsilon} \right) - \boldsymbol{\mu}_{\theta}(\mathbf{x}_t(\mathbf{x}_0, \boldsymbol{\epsilon}), t) \right\|^2 \right]$$
(10)

# <span id="page-3-1"></span>Algorithm 1 Training 1: repeat 2: $\mathbf{x}_0 \sim q(\mathbf{x}_0)$ 3: $t \sim \text{Uniform}(\{1, \dots, T\})$ 4: $\epsilon \sim \mathcal{N}(\mathbf{0}, \mathbf{I})$ 5: Take gradient descent step on $\nabla_{\theta} \| \boldsymbol{\epsilon} - \boldsymbol{\epsilon}_{\theta}(\sqrt{\bar{\alpha}_t}\mathbf{x}_0 + \sqrt{1 - \bar{\alpha}_t}\boldsymbol{\epsilon}, t) \|^2$ 6: until converged Algorithm 2 Sampling 1: $\mathbf{x}_T \sim \mathcal{N}(\mathbf{0}, \mathbf{I})$ 2: for $t = T, \dots, 1$ do 3: $\mathbf{z} \sim \mathcal{N}(\mathbf{0}, \mathbf{I})$ if t > 1, else $\mathbf{z} = \mathbf{0}$ 4: $\mathbf{x}_{t-1} = \frac{1}{\sqrt{\alpha_t}} \left( \mathbf{x}_t - \frac{1 - \alpha_t}{\sqrt{1 - \bar{\alpha}_t}} \boldsymbol{\epsilon}_{\theta}(\mathbf{x}_t, t) \right) + \sigma_t \mathbf{z}$ 5: end for 6: return $\mathbf{x}_0$

Equation (10) reveals that  $\mu_{\theta}$  must predict  $\frac{1}{\sqrt{\alpha_t}} \left( \mathbf{x}_t - \frac{\beta_t}{\sqrt{1-\bar{\alpha}_t}} \epsilon \right)$  given  $\mathbf{x}_t$ . Since  $\mathbf{x}_t$  is available as input to the model, we may choose the parameterization

$$\boldsymbol{\mu}_{\theta}(\mathbf{x}_{t}, t) = \tilde{\boldsymbol{\mu}}_{t} \left( \mathbf{x}_{t}, \frac{1}{\sqrt{\bar{\alpha}_{t}}} (\mathbf{x}_{t} - \sqrt{1 - \bar{\alpha}_{t}} \boldsymbol{\epsilon}_{\theta}(\mathbf{x}_{t})) \right) = \frac{1}{\sqrt{\alpha_{t}}} \left( \mathbf{x}_{t} - \frac{\beta_{t}}{\sqrt{1 - \bar{\alpha}_{t}}} \boldsymbol{\epsilon}_{\theta}(\mathbf{x}_{t}, t) \right)$$
(11)

where  $\epsilon_{\theta}$  is a function approximator intended to predict  $\epsilon$  from  $\mathbf{x}_t$ . To sample  $\mathbf{x}_{t-1} \sim p_{\theta}(\mathbf{x}_{t-1}|\mathbf{x}_t)$  is to compute  $\mathbf{x}_{t-1} = \frac{1}{\sqrt{\alpha_t}} \left( \mathbf{x}_t - \frac{\beta_t}{\sqrt{1-\alpha_t}} \epsilon_{\theta}(\mathbf{x}_t,t) \right) + \sigma_t \mathbf{z}$ , where  $\mathbf{z} \sim \mathcal{N}(\mathbf{0},\mathbf{I})$ . The complete sampling procedure, Algorithm 2, resembles Langevin dynamics with  $\epsilon_{\theta}$  as a learned gradient of the data density. Furthermore, with the parameterization (11), Eq. (10) simplifies to:

<span id="page-3-3"></span><span id="page-3-2"></span>
$$\mathbb{E}_{\mathbf{x}_{0},\epsilon} \left[ \frac{\beta_{t}^{2}}{2\sigma_{t}^{2}\alpha_{t}(1-\bar{\alpha}_{t})} \left\| \epsilon - \epsilon_{\theta}(\sqrt{\bar{\alpha}_{t}}\mathbf{x}_{0} + \sqrt{1-\bar{\alpha}_{t}}\epsilon, t) \right\|^{2} \right]$$
(12)

which resembles denoising score matching over multiple noise scales indexed by t [55]. As Eq. (12) is equal to (one term of) the variational bound for the Langevin-like reverse process (11), we see that optimizing an objective resembling denoising score matching is equivalent to using variational inference to fit the finite-time marginal of a sampling chain resembling Langevin dynamics.

To summarize, we can train the reverse process mean function approximator  $\mu_{\theta}$  to predict  $\tilde{\mu}_{t}$ , or by modifying its parameterization, we can train it to predict  $\epsilon$ . (There is also the possibility of predicting  $\mathbf{x}_{0}$ , but we found this to lead to worse sample quality early in our experiments.) We have shown that the  $\epsilon$ -prediction parameterization both resembles Langevin dynamics and simplifies the diffusion model's variational bound to an objective that resembles denoising score matching. Nonetheless, it is just another parameterization of  $p_{\theta}(\mathbf{x}_{t-1}|\mathbf{x}_{t})$ , so we verify its effectiveness in Section 4 in an ablation where we compare predicting  $\epsilon$  against predicting  $\tilde{\mu}_{t}$ .

### 3.3 Data scaling, reverse process decoder, and $L_0$

We assume that image data consists of integers in  $\{0, 1, \dots, 255\}$  scaled linearly to [-1, 1]. This ensures that the neural network reverse process operates on consistently scaled inputs starting from the standard normal prior  $p(\mathbf{x}_T)$ . To obtain discrete log likelihoods, we set the last term of the reverse process to an independent discrete decoder derived from the Gaussian  $\mathcal{N}(\mathbf{x}_0; \boldsymbol{\mu}_{\theta}(\mathbf{x}_1, 1), \sigma_1^2 \mathbf{I})$ :

<span id="page-3-4"></span>
$$p_{\theta}(\mathbf{x}_{0}|\mathbf{x}_{1}) = \prod_{i=1}^{D} \int_{\delta_{-}(x_{0}^{i})}^{\delta_{+}(x_{0}^{i})} \mathcal{N}(x; \mu_{\theta}^{i}(\mathbf{x}_{1}, 1), \sigma_{1}^{2}) dx$$

$$\delta_{+}(x) = \begin{cases} \infty & \text{if } x = 1\\ x + \frac{1}{255} & \text{if } x < 1 \end{cases} \quad \delta_{-}(x) = \begin{cases} -\infty & \text{if } x = -1\\ x - \frac{1}{255} & \text{if } x > -1 \end{cases}$$
(13)

where D is the data dimensionality and the i superscript indicates extraction of one coordinate. (It would be straightforward to instead incorporate a more powerful decoder like a conditional autoregressive model, but we leave that to future work.) Similar to the discretized continuous distributions used in VAE decoders and autoregressive models [34, 52], our choice here ensures that the variational bound is a lossless codelength of discrete data, without need of adding noise to the data or incorporating the Jacobian of the scaling operation into the log likelihood. At the end of sampling, we display  $\mu_{\theta}(\mathbf{x}_1, 1)$  noiselessly.

### <span id="page-3-0"></span>3.4 Simplified training objective

With the reverse process and decoder defined above, the variational bound, consisting of terms derived from Eqs. (12) and (13), is clearly differentiable with respect to  $\theta$  and is ready to be employed for

<span id="page-4-2"></span>T