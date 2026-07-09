Published as a conference paper at ICLR 2015

# ADAM: A METHOD FOR STOCHASTIC OPTIMIZATION

**Diederik P. Kingma**$^*$  
University of Amsterdam, OpenAI  
dpkingma@openai.com

**Jimmy Lei Ba**$^*$  
University of Toronto  
jimmy@psi.utoronto.ca

## ABSTRACT

We introduce *Adam*, an algorithm for first-order gradient-based optimization of stochastic objective functions, based on adaptive estimates of lower-order moments. The method is straightforward to implement, is computationally efficient, has little memory requirements, is invariant to diagonal rescaling of the gradients, and is well suited for problems that are large in terms of data and/or parameters. The method is also appropriate for non-stationary objectives and problems with very noisy and/or sparse gradients. The hyper-parameters have intuitive interpretations and typically require little tuning. Some connections to related algorithms, on which *Adam* was inspired, are discussed. We also analyze the theoretical convergence properties of the algorithm and provide a regret bound on the convergence rate that is comparable to the best known results under the online convex optimization framework. Empirical results demonstrate that Adam works well in practice and compares favorably to other stochastic optimization methods. Finally, we discuss *AdaMax*, a variant of *Adam* based on the infinity norm.

## 1 INTRODUCTION

Stochastic gradient-based optimization is of core practical importance in many fields of science and engineering. Many problems in these fields can be cast as the optimization of some scalar parameterized objective function requiring maximization or minimization with respect to its parameters. If the function is differentiable w.r.t. its parameters, gradient descent is a relatively efficient optimization method, since the computation of first-order partial derivatives w.r.t. all the parameters is of the same computational complexity as just evaluating the function. Often, objective functions are stochastic. For example, many objective functions are composed of a sum of subfunctions evaluated at different subsamples of data; in this case optimization can be made more efficient by taking gradient steps w.r.t. individual subfunctions, i.e. stochastic gradient descent (SGD) or ascent. SGD proved itself as an efficient and effective optimization method that was central in many machine learning success stories, such as recent advances in deep learning (Deng et al., 2013; Krizhevsky et al., 2012; Hinton & Salakhutdinov, 2006; Hinton et al., 2012a; Graves et al., 2013). Objectives may also have other sources of noise than data subsampling, such as dropout (Hinton et al., 2012b) regularization. For all such noisy objectives, efficient stochastic optimization techniques are required. The focus of this paper is on the optimization of stochastic objectives with high-dimensional parameters spaces. In these cases, higher-order optimization methods are ill-suited, and discussion in this paper will be restricted to first-order methods.

We propose *Adam*, a method for efficient stochastic optimization that only requires first-order gradients with little memory requirement. The method computes individual adaptive learning rates for different parameters from estimates of first and second moments of the gradients; the name *Adam* is derived from adaptive moment estimation. Our method is designed to combine the advantages of two recently popular methods: AdaGrad (Duchi et al., 2011), which works well with sparse gradients, and RMSProp (Tieleman & Hinton, 2012), which works well in on-line and non-stationary settings; important connections to these and other stochastic optimization methods are clarified in section 5. Some of Adam’s advantages are that the magnitudes of parameter updates are invariant to rescaling of the gradient, its stepsizes are approximately bounded by the stepsize hyperparameter, it does not require a stationary objective, it works with sparse gradients, and it naturally performs a form of step size annealing.

---

$^*$Equal contribution. Author ordering determined by coin flip over a Google Hangout.

arXiv:1412.6980v9 [cs.LG] 30 Jan 2017

Published as a conference paper at ICLR 2015

---

**Algorithm 1**: Adam, our proposed algorithm for stochastic optimization. See section 2 for details, and for a slightly more efficient (but less clear) order of computation. $g_t^2$ indicates the elementwise square $g_t \odot g_t$ . Good default settings for the tested machine learning problems are $\alpha = 0.001$ , $\beta_1 = 0.9$ , $\beta_2 = 0.999$ and $\epsilon = 10^{-8}$ . All operations on vectors are element-wise. With $\beta_1^t$ and $\beta_2^t$ we denote $\beta_1$ and $\beta_2$ to the power $t$ .

Require: $\alpha$ : Stepsize  
Require: $\beta_1, \beta_2 \in [0, 1)$ : Exponential decay rates for the moment estimates  
Require: $f(\theta)$ : Stochastic objective function with parameters $\theta$  
Require: $\theta_0$ : Initial parameter vector  

$m_0 \leftarrow 0$ (Initialize 1st moment vector)  
$v_0 \leftarrow 0$ (Initialize 2nd moment vector)  
$t \leftarrow 0$ (Initialize timestep)  

while $\theta_t$ not converged do  
$\quad t \leftarrow t + 1$  
$\quad g_t \leftarrow \nabla_\theta f_t(\theta_{t-1})$ (Get gradients w.r.t. stochastic objective at timestep $t$ )  
$\quad m_t \leftarrow \beta_1 \cdot m_{t-1} + (1 - \beta_1) \cdot g_t$ (Update biased first moment estimate)  
$\quad v_t \leftarrow \beta_2 \cdot v_{t-1} + (1 - \beta_2) \cdot g_t^2$ (Update biased second raw moment estimate)  
$\quad \widehat{m}_t \leftarrow m_t / (1 - \beta_1^t)$ (Compute bias-corrected first moment estimate)  
$\quad \widehat{v}_t \leftarrow v_t / (1 - \beta_2^t)$ (Compute bias-corrected second raw moment estimate)  
$\quad \theta_t \leftarrow \theta_{t-1} - \alpha \cdot \widehat{m}_t / (\sqrt{\widehat{v}_t} + \epsilon)$ (Update parameters)  
end while  

return $\theta_t$ (Resulting parameters)

---

In section 2 we describe the algorithm and the properties of its update rule. Section 3 explains our initialization bias correction technique, and section 4 provides a theoretical analysis of Adam’s convergence in online convex programming. Empirically, our method consistently outperforms other methods for a variety of models and datasets, as shown in section 6. Overall, we show that Adam is a versatile algorithm that scales to large-scale high-dimensional machine learning problems.

## 2 ALGORITHM

See algorithm 1 for pseudo-code of our proposed algorithm Adam. Let $f(\theta)$ be a noisy objective function: a stochastic scalar function that is differentiable w.r.t. parameters $\theta$ . We are interested in minimizing the expected value of this function, $\mathbb{E}[f(\theta)]$ w.r.t. its parameters $\theta$ . With $f_1(\theta), ..., f_T(\theta)$ we denote the realisations of the stochastic function at subsequent timesteps $1, ..., T$ . The stochasticity might come from the evaluation at random subsamples (minibatches) of datapoints, or arise from inherent function noise. With $g_t = \nabla_\theta f_t(\theta)$ we denote the gradient, i.e. the vector of partial derivatives of $f_t$ , w.r.t $\theta$ evaluated at timestep $t$ .

The algorithm updates exponential moving averages of the gradient ( $m_t$ ) and the squared gradient ( $v_t$ ) where the hyper-parameters $\beta_1, \beta_2 \in [0, 1)$ control the exponential decay rates of these moving averages. The moving averages themselves are estimates of the 1st moment (the mean) and the 2nd raw moment (the uncentered variance) of the gradient. However, these moving averages are initialized as (vectors of) 0’s, leading to moment estimates that are biased towards zero, especially during the initial timesteps, and especially when the decay rates are small (i.e. the $\beta$ s are close to 1). The good news is that this initialization bias can be easily counteracted, resulting in bias-corrected estimates $\widehat{m}_t$ and $\widehat{v}_t$ . See section 3 for more details.

Note that the efficiency of algorithm 1 can, at the expense of clarity, be improved upon by changing the order of computation, e.g. by replacing the last three lines in the loop with the following lines: $\alpha_t = \alpha \cdot \sqrt{1 - \beta_2^t} / (1 - \beta_1^t)$ and $\theta_t \leftarrow \theta_{t-1} - \alpha_t \cdot m_t / (\sqrt{v_t} + \epsilon)$ .

### 2.1 ADAM’S UPDATE RULE

An important property of Adam’s update rule is its careful choice of stepsizes. Assuming $\epsilon = 0$ , the effective step taken in parameter space at timestep $t$ is $\Delta_t = \alpha \cdot \widehat{m}_t / \sqrt{\widehat{v}_t}$ . The effective stepsize has two upper bounds: $|\Delta_t| \leq \alpha \cdot (1 - \beta_1) / \sqrt{1 - \beta_2}$ in the case $(1 - \beta_1) > \sqrt{1 - \beta_2}$ , and $|\Delta_t| \leq \alpha$

Published as a conference paper at ICLR 2015

otherwise. The first case only happens in the most severe case of sparsity: when a gradient has been zero at all timesteps except at the current timestep. For less sparse cases, the effective stepsize will be smaller. When $(1 - \beta_1) = \sqrt{1 - \beta_2}$ we have that $|\widehat{m}_t / \sqrt{\widehat{v}_t}| < 1$ therefore $|\Delta_t| < \alpha$ . In more common scenarios, we will have that $\widehat{m}_t / \sqrt{\widehat{v}_t} \approx \pm 1$ since $|\mathbb{E}[g] / \sqrt{\mathbb{E}[g^2]}| \leq 1$ . The effective magnitude of the steps taken in parameter space at each timestep are approximately bounded by the stepsize setting $\alpha$ , i.e., $|\Delta_t| \lesssim \alpha$ . This can be understood as establishing a *trust region* around the current parameter value, beyond which the current gradient estimate does not provide sufficient information. This typically makes it relatively easy to know the right scale of $\alpha$ in advance. For many machine learning models, for instance, we often know in advance that good optima are with high probability within some set region in parameter space; it is not uncommon, for example, to have a prior distribution over the parameters. Since $\alpha$ sets (an upper bound of) the magnitude of steps in parameter space, we can often deduce the right order of magnitude of $\alpha$ such that optima can be reached from $\theta_0$ within some number of iterations. With a slight abuse of terminology, we will call the ratio $\widehat{m}_t / \sqrt{\widehat{v}_t}$ the *signal-to-noise ratio* ( $SNR$ ). With a smaller SNR the effective stepsize $\Delta_t$ will be closer to zero. This is a desirable property, since a smaller SNR means that there is greater uncertainty about whether the direction of $\widehat{m}_t$ corresponds to the direction of the true gradient. For example, the SNR value typically becomes closer to 0 towards an optimum, leading to smaller effective steps in parameter space: a form of automatic annealing. The effective stepsize $\Delta_t$ is also invariant to the scale of the gradients; rescaling the gradients $g$ with factor $c$ will scale $\widehat{m}_t$ with a factor $c$ and $\widehat{v}_t$ with a factor $c^2$ , which cancel out: $(c \cdot \widehat{m}_t) / (\sqrt{c^2 \cdot \widehat{v}_t}) = \widehat{m}_t / \sqrt{\widehat{v}_t}$ .

# Initialization Bias Correction

As explained in section 2, Adam utilizes initialization bias correction terms. We will here derive the term for the second moment estimate; the derivation for the first moment estimate is completely analogous. Let $g$ be the gradient of the stochastic objective $f$ , and we wish to estimate its second raw moment (uncentered variance) using an exponential moving average of the squared gradient, with decay rate $\beta_2$ . Let $g_1, ..., g_T$ be the gradients at subsequent timesteps, each a draw from an underlying gradient distribution $g_t \sim p(g_t)$ . Let us initialize the exponential moving average as $v_0 = 0$ (a vector of zeros). First note that the update at timestep $t$ of the exponential moving average $v_t = \beta_2 \cdot v_{t-1} + (1 - \beta_2) \cdot g_t^2$ (where $g_t^2$ indicates the elementwise square $g_t \odot g_t$ ) can be written as a function of the gradients at all previous timesteps:

$$
v_t = (1 - \beta_2) \sum_{i=1}^{t} \beta_2^{t-i} \cdot g_i^2
$$

We wish to know how $\mathbb{E}[v_t]$ , the expected value of the exponential moving average at timestep $t$ , relates to the true second moment $\mathbb{E}[g_t^2]$ , so we can correct for the discrepancy between the two. Taking expectations of the left-hand and right-hand sides of eq. (1):

$$
\mathbb{E}[v_t] = \mathbb{E}\left[(1 - \beta_2) \sum_{i=1}^{t} \beta_2^{t-i} \cdot g_i^2\right]
$$

$$
= \mathbb{E}[g_t^2] \cdot (1 - \beta_2) \sum_{i=1}^{t} \beta_2^{t-i} + \zeta
$$

$$
= \mathbb{E}[g_t^2] \cdot (1 - \beta_2^t) + \zeta
$$

where $\zeta = 0$ if the true second moment $\mathbb{E}[g_t^2]$ is stationary; otherwise $\zeta$ can be kept small since the exponential decay rate $\beta_1$ can (and should) be chosen such that the exponential moving average assigns small weights to gradients too far in the past. What is left is the term $(1 - \beta_2^t)$ which is caused by initializing the running average with zeros. In algorithm 1 we therefore divide by this term to correct the initialization bias.

In case of sparse gradients, for a reliable estimate of the second moment one needs to average over many gradients by chosing a small value of $\beta_2$ ; however it is exactly this case of small $\beta_2$ where a lack of initialisation bias correction would lead to initial steps that are much larger.

Published as a conference paper at ICLR 2015

# 4 CONVERGENCE ANALYSIS

We analyze the convergence of Adam using the online learning framework proposed in (Zinkevich, 2003). Given an arbitrary, unknown sequence of convex cost functions $f_1(\theta)$ , $f_2(\theta)$ ,..., $f_T(\theta)$ . At each time $t$ , our goal is to predict the parameter $\theta_t$ and evaluate it on a previously unknown cost function $f_t$ . Since the nature of the sequence is unknown in advance, we evaluate our algorithm using the regret, that is the sum of all the previous difference between the online prediction $f_t(\theta_t)$ and the best fixed point parameter $f_t(\theta^*)$ from a feasible set $\mathcal{X}$ for all the previous steps. Concretely, the regret is defined as:

$$
R(T) = \sum_{t=1}^{T} [f_t(\theta_t) - f_t(\theta^*)]
\quad \text{(5)}
$$

where $\theta^* = \arg \min_{\theta \in \mathcal{X}} \sum_{t=1}^{T} f_t(\theta)$ . We show Adam has $O(\sqrt{T})$ regret bound and a proof is given in the appendix. Our result is comparable to the best known bound for this general convex online learning problem. We also use some definitions simplify our notation, where $g_t \triangleq \nabla f_t(\theta_t)$ and $g_{t,i}$ as the $i^{\text{th}}$ element. We define $g_{1:t,i} \in \mathbb{R}^t$ as a vector that contains the $i^{\text{th}}$ dimension of the gradients over all iterations till $t$ , $g_{1:t,i} = [g_{1,i}, g_{2,i}, \cdots, g_{t,i}]$ . Also, we define $\gamma \triangleq \frac{\beta_1^2}{\sqrt{\beta_2}}$ . Our following theorem holds when the learning rate $\alpha_t$ is decaying at a rate of $t^{-\frac{1}{2}}$ and first moment running average coefficient $\beta_{1,t}$ decay exponentially with $\lambda$ , that is typically close to 1, e.g. $1 - 10^{-8}$ .

**Theorem 4.1.** Assume that the function $f_t$ has bounded gradients, $\|\nabla f_t(\theta)\|_2 \leq G$ , $\|\nabla f_t(\theta)\|_\infty \leq G_\infty$ for all $\theta \in R^d$ and distance between any $\theta_t$ generated by Adam is bounded, $\|\theta_n - \theta_m\|_2 \leq D$ , $\|\theta_m - \theta_n\|_\infty \leq D_\infty$ for any $m, n \in \{1, ..., T\}$ , and $\beta_1, \beta_2 \in [0, 1)$ satisfy $\frac{\beta_1^2}{\sqrt{\beta_2}} < 1$ . Let $\alpha_t = \frac{\alpha}{\sqrt{t}}$ and $\beta_{1,t} = \beta_1 \lambda^{t-1}, \lambda \in (0, 1)$ . Adam achieves the following guarantee, for all $T \geq 1$ .

$$
R(T) \leq \frac{D^2}{2\alpha(1 - \beta_1)} \sum_{i=1}^{d} \sqrt{T \hat{v}_{T,i}} + \frac{\alpha(1 + \beta_1)G_\infty}{(1 - \beta_1)\sqrt{1 - \beta_2}(1 - \gamma)^2} \sum_{i=1}^{d} \|g_{1:T,i}\|_2 + \sum_{i=1}^{d} \frac{D_\infty^2 G_\infty \sqrt{1 - \beta_2}}{2\alpha(1 - \beta_1)(1 - \lambda)^2}
$$

Our Theorem 4.1 implies when the data features are sparse and bounded gradients, the summation term can be much smaller than its upper bound $\sum_{i=1}^{d} \|g_{1:T,i}\|_2 << dG_\infty \sqrt{T}$ and $\sum_{i=1}^{d} \sqrt{T \hat{v}_{T,i}} << dG_\infty \sqrt{T}$ , in particular if the class of function and data features are in the form of section 1.2 in (Duchi et al., 2011). Their results for the expected value $\mathbb{E}[\sum_{i=1}^{d} \|g_{1:T,i}\|_2]$ also apply to Adam. In particular, the adaptive method, such as Adam and Adagrad, can achieve $O(\log d\sqrt{T})$ , an improvement over $O(\sqrt{dT})$ for the non-adaptive method. Decaying $\beta_{1,t}$ towards zero is important in our theoretical analysis and also matches previous empirical findings, e.g. (Sutskever et al., 2013) suggests reducing the momentum coefficient in the end of training can improve convergence.

Finally, we can show the average regret of Adam converges,

**Corollary 4.2.** Assume that the function $f_t$ has bounded gradients, $\|\nabla f_t(\theta)\|_2 \leq G$ , $\|\nabla f_t(\theta)\|_\infty \leq G_\infty$ for all $\theta \in R^d$ and distance between any $\theta_t$ generated by Adam is bounded, $\|\theta_n - \theta_m\|_2 \leq D$ , $\|\theta_m - \theta_n\|_\infty \leq D_\infty$ for any $m, n \in \{1, ..., T\}$ . Adam achieves the following guarantee, for all $T \geq 1$ .

$$
\frac{R(T)}{T} = O\left(\frac{1}{\sqrt{T}}\right)
$$

This result can be obtained by using Theorem 4.1 and $\sum_{i=1}^{d} \|g_{1:T,i}\|_2 \leq dG_\infty \sqrt{T}$ . Thus, $\lim_{T \to \infty} \frac{R(T)}{T} = 0$ .

# 5 RELATED WORK

Optimization methods bearing a direct relation to Adam are RMSProp (Tieleman & Hinton, 2012; Graves, 2013) and AdaGrad (Duchi et al., 2011); these relationships are discussed below. Other 