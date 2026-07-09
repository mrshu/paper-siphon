## ADAM: A METHOD FOR STOCHASTIC OPTIMIZATION

Diederik P. Kingma * University of Amsterdam, OpenAI

dpkingma@openai.com

Jimmy Lei Ba *

University of Toronto

jimmy@psi.utoronto.ca

## ABSTRACT

We introduce Adam , an algorithm for first-order gradient-based optimization of stochastic objective functions, based on adaptive estimates of lower-order moments. The method is straightforward to implement, is computationally efficient, has little memory requirements, is invariant to diagonal rescaling of the gradients, and is well suited for problems that are large in terms of data and/or parameters. The method is also appropriate for non-stationary objectives and problems with very noisy and/or sparse gradients. The hyper-parameters have intuitive interpretations and typically require little tuning. Some connections to related algorithms, on which Adam was inspired, are discussed. We also analyze the theoretical convergence properties of the algorithm and provide a regret bound on the convergence rate that is comparable to the best known results under the online convex optimization framework. Empirical results demonstrate that Adam works well in practice and compares favorably to other stochastic optimization methods. Finally, we discuss AdaMax , a variant of Adam based on the infinity norm.

## 1 INTRODUCTION

Stochastic gradient-based optimization is of core practical importance in many fields of science and engineering. Many problems in these fields can be cast as the optimization of some scalar parameterized objective function requiring maximization or minimization with respect to its parameters. If the function is differentiable w.r.t. its parameters, gradient descent is a relatively efficient optimization method, since the computation of first-order partial derivatives w.r.t. all the parameters is of the same computational complexity as just evaluating the function. Often, objective functions are stochastic. For example, many objective functions are composed of a sum of subfunctions evaluated at different subsamples of data; in this case optimization can be made more efficient by taking gradient steps w.r.t. individual subfunctions, i.e. stochastic gradient descent (SGD) or ascent. SGD proved itself as an efficient and effective optimization method that was central in many machine learning success stories, such as recent advances in deep learning (Deng et al., 2013; Krizhevsky et al., 2012; Hinton &amp; Salakhutdinov, 2006; Hinton et al., 2012a; Graves et al., 2013). Objectives may also have other sources of noise than data subsampling, such as dropout (Hinton et al., 2012b) regularization. For all such noisy objectives, efficient stochastic optimization techniques are required. The focus of this paper is on the optimization of stochastic objectives with high-dimensional parameters spaces. In these cases, higher-order optimization methods are ill-suited, and discussion in this paper will be restricted to first-order methods.

We propose Adam , a method for efficient stochastic optimization that only requires first-order gradients with little memory requirement. The method computes individual adaptive learning rates for different parameters from estimates of first and second moments of the gradients; the name Adam is derived from adaptive moment estimation. Our method is designed to combine the advantages of two recently popular methods: AdaGrad (Duchi et al., 2011), which works well with sparse gradients, and RMSProp (Tieleman &amp; Hinton, 2012), which works well in on-line and non-stationary settings; important connections to these and other stochastic optimization methods are clarified in section 5. Some of Adam's advantages are that the magnitudes of parameter updates are invariant to rescaling of the gradient, its stepsizes are approximately bounded by the stepsize hyperparameter, it does not require a stationary objective, it works with sparse gradients, and it naturally performs a form of step size annealing.

$^{*}$Equal contribution. Author ordering determined by coin flip over a Google Hangout.

Algorithm 1: Adam , our proposed algorithm for stochastic optimization. See section 2 for details, and for a slightly more efficient (but less clear) order of computation. g 2 t indicates the elementwise square g$\_{t}$ ⊙ g$\_{t}$ . Good default settings for the tested machine learning problems are α = 0 . 001 , β$\_{1}$ = 0 . 9 , β$\_{2}$ = 0 . 999 and ϵ = 10 - $^{8}$. All operations on vectors are element-wise. With β t 1 and β t 2 we denote β$\_{1}$ and β$\_{2}$ to the power t .

```
we denote \beta_1 and \beta_2 to the power t.

    Require:  \alpha: Stepsize
    Require:  \beta_1, \beta_2 = [0, 1] : Exponential decay rates for the moment estimates
    Require:  f( \theta) : Stochastic objective function with parameters \theta
    Require:  \theta_0: Initial parameter vector
        m_0
```

In section 2 we describe the algorithm and the properties of its update rule. Section 3 explains our initialization bias correction technique, and section 4 provides a theoretical analysis of Adam's convergence in online convex programming. Empirically, our method consistently outperforms other methods for a variety of models and datasets, as shown in section 6. Overall, we show that Adam is a versatile algorithm that scales to large-scale high-dimensional machine learning problems.

## 2 ALGORITHM

See algorithm 1 for pseudo-code of our proposed algorithm Adam . Let f ( θ ) be a noisy objective function: a stochastic scalar function that is differentiable w.r.t. parameters θ . We are interested in minimizing the expected value of this function, $\_{E}$[ f ( θ )] w.r.t. its parameters θ . With f$\_{1}$ ( θ ) , ..., , f$\_{T}$ ( θ ) we denote the realisations of the stochastic function at subsequent timesteps 1 , ..., T . The stochasticity might come from the evaluation at random subsamples (minibatches) of datapoints, or arise from inherent function noise. With g$\_{t}$ = ∇$\_{θ}$ f$\_{t}$ ( θ ) we denote the gradient, i.e. the vector of partial derivatives of f$\_{t}$ , w.r.t θ evaluated at timestep t .

The algorithm updates exponential moving averages of the gradient ( m$\_{t}$ ) and the squared gradient ( v$\_{t}$ ) where the hyper-parameters β$\_{1}$, β$\_{2}$ ∈ [0 , 1) control the exponential decay rates of these moving averages. The moving averages themselves are estimates of the 1 st moment (the mean) and the 2 nd raw moment (the uncentered variance) of the gradient. However, these moving averages are initialized as (vectors of) 0's, leading to moment estimates that are biased towards zero, especially during the initial timesteps, and especially when the decay rates are small (i.e. the β s are close to 1). The good news is that this initialization bias can be easily counteracted, resulting in bias-corrected estimates ̂ m$\_{t}$ and ̂ v$\_{t}$ . See section 3 for more details.

Note that the efficiency of algorithm 1 can, at the expense of clarity, be improved upon by changing the order of computation, e.g. by replacing the last three lines in the loop with the following lines: α$\_{t}$ = α · √ 1 - β t $\_{2}$/ (1 - β t $\_{1}$) and θ$\_{t}$ ← θ$\_{t}$$\_{-}$$\_{1}$ - α$\_{t}$ · m$\_{t}$/ ( √ v$\_{t}$ + ˆ ε ) .

## 2.1 ADAM'S UPDATE RULE

An important property of Adam's update rule is its careful choice of timesteps. Assuming ϵ = 0 , the effective step taken in parameter space at timestep t is Δ$\_{t}$ = α · ̂ m$\_{t}$/ √ ̂ v$\_{t}$ . The effective stepsize has two upper bounds: | Δ$\_{t}$ | ≤ α · (1 - β$\_{1}$ ) / √ 1 - β$\_{2}$ in the case (1 - β$\_{1}$ ) &gt; √ 1 - β$\_{2}$ , and | Δ$\_{t}$ | ≤ α

otherwise. The first case only happens in the most severe case of sparsity: when a gradient has been zero at all timesteps except at the current timestep. For less sparse cases, the effective stepsize will be smaller. When (1 - β$\_{1}$ ) = √ 1 - β$\_{2}$ we have that | ̂ m$\_{t}$/ √ ̂ v$\_{t}$ |

## 3 INITIALIZATION BIAS CORRECTION

As explained in section 2, Adam utilizes initialization bias correction terms. We will here derive the term for the second moment estimate; the derivation for the first moment estimate is completely analogous. Let g be the gradient of the stochastic objective f , and we wish to estimate its second raw moment (uncentered variance) using an exponential moving average of the squared gradient, with decay rate β$\_{2}$ . Let g$\_{1}$, ..., g$\_{T}$ be the gradients at subsequent timesteps, each a draw from an underlying gradient distribution g$\_{t}$ ∼ p ( g$\_{t}$ ) . Let us initialize the exponential moving average as v$\_{0}$ = 0 (a vector of zeros). First note that the update at timestep t of the exponential moving average v$\_{t}$ = β$\_{2}$ · v$\_{t}$$\_{-}$$\_{1}$ + (1 - β$\_{2}$ ) · g 2 t (where g 2 t indicates the elementwise square g$\_{t}$ ⊙ g$\_{t}$ ) can be written as a function of the gradients at all previous timesteps:

$$v _ { t } = ( 1 - \beta _ { 2 } ) \sum _ { i = 1 } ^ { t } \beta _ { 2 } ^ { t - i } \cdot g _ { i } ^ { 2 }$$

We wish to know how$\_{E}$ [ v$\_{t}$ ] , the expected value of the exponential moving average at timestep t , relates to the true second moment$\_{E}$ [ g 2 $\_{t}$] , so we can correct for the discrepancy between the two. Taking expectations of the left-hand and right-hand sides of eq. (1):

$$\mathbb { E } [ v _ { t } ] = \mathbb { E } \left [ ( 1 - \beta _ { 2 } ) \sum _ { i = 1 } ^ { t } \beta _ { 2 } ^ { t - i } \cdot g _ { i } ^ { 2 } \right ]$$

$$= \mathbb { E } [ g _ { t } ^ { 2 } ] \cdot ( 1 - \beta _ { 2 } ) \sum _ { i = 1 } ^ { t } \beta _ { 2 } ^ { t - i } + \zeta$$

$$= \mathbb { E } [ g _ { t } ^ { 2 } ] \cdot ( 1 - \beta _ { 2 } ^ { t } ) + \zeta$$

where ζ = 0 if the true second moment$\_{E}$ [ g 2 $\_{i}$] is stationary; otherwise ζ can be kept small since the exponential decay rate β$\_{1}$ can (and should) be chosen such that the exponential moving average assigns small weights to gradients too far in the past. What is left is the term (1 - β t $\_{2}$) which is caused by initializing the running average with zeros. In algorithm 1 we therefore divide by this term to correct the initialization bias.

In case of sparse gradients, for a reliable estimate of the second moment one needs to average over many gradients by choosing a small value of β$\_{2}$ ; however it is exactly this case of small β$\_{2}$ where a lack of initialisation bias correction would lead to initial steps that are much larger.

## 4 CONVERGENCE ANALYSIS

We analyze the convergence of Adam using the online learning framework proposed in (Zinkevich, 2003). Given an arbitrary, unknown sequence of convex cost functions f$\_{1}$ ( θ ) , f$\_{2}$ ( θ ) ,..., f$\_{T}$ ( θ ) . At each time t , our goal is to predict the parameter θ$\_{t}$ and evaluate it on a previously unknown cost function f$\_{t}$ . Since the nature of the sequence is unknown in advance, we evaluate our algorithm using the regret, that is the sum of all the previous difference between the online prediction f$\_{t}$ ( θ$\_{t}$ ) and the best fixed point parameter f$\_{t}$ ( θ $^{∗}$) from a feasible set X for all the previous steps. Concretely, the regret is defined as:

$$R ( T ) = \sum _ { t = 1 } ^ { T } [ f _ { t } ( \theta _ { t } ) - f _ { t } ( \theta ^ { * } ) ]$$

where θ ∗ = arg min$\_{θ}$$\_{∈X}$ ∑ T t =1 f$\_{t}$ ( θ ) . We show Adam has O ( √ T ) regret bound and a proof is given in the appendix. Our result is comparable to the best known bound for this general convex online learning problem. We also use some definitions simplify our notation, where g$\_{t}$ ≜ ∇ f$\_{t}$ ( θ$\_{t}$ ) and g$\_{t,i}$ as the i th element. We define g$\_{1:}$$\_{t,i}$ ∈$\_{R}$ t as a vector that contains the i th dimension of the gradients over all iterations till t , g$\_{1:}$$\_{t,i}$ = [ g$\_{1:}$$\_{i}$, g$\_{2:}$$\_{i}$, · · · , g$\_{t,i}$ ] . Also, we define γ ≜ β 2 1 √ $\_{β$\_{2}$}$. Our following

Theorem 4.1. Assume that the function f$\_{t}$ has bounded gradients, ∥∇ f$\_{t}$ ( θ ) ∥$\_{2}$ ≤ G , ∥∇ f$\_{t}$ ( θ ) ∥$\_{∞}$ ≤ G$\_{∞}$ for all θ ∈ R d and distance between any θ$\_{t}$ generated by Adam is bounded, ∥ θ$\_{n}$ - θ$\_{m}$ ∥$\_{2}$ ≤ D , ∥ θ$\_{m}$ - θ$\_{n}$ ∥$\_{∞}$ ≤ D$\_{∞}$ for any m, n ∈ { 1 , ..., T } , and β$\_{1}$, β$\_{2}$ ∈ [ 0 , 1 ) satisfying β 2 1 √ β$\_{2}$

$$R ( T ) \leq \frac { D ^ { 2 } } { 2 \alpha ( 1 - \beta _ { 1 } ) } \sum _ { i = 1 } ^ { d } \sqrt { T \widehat { \overline { t } } _ { i , t } + \frac { \alpha ( 1 + \beta _ { 1 } ) G _ { \infty } } { 1 - \beta _ { 1 } ) \sqrt { 1 - \beta _ { 2 } } } \sum _ { i = 1 } ^ { d } \| g _ { 1 \colon T , i } \| _ { 2 } + \sum _ { i = 1 } ^ { d } \frac { D _ { \infty } ^ { 2 } G _ { \infty } \sqrt { 1 - \beta _ { 2 } } } { 2 \alpha ( 1 - \beta _ { 1 } ) ( 1 - \lambda ) ^ { 2 } }$$

Our Theorem 4.1 implies when the data features are sparse and bounded gradients, the summation term can be much smaller than its upper bound ∑ d i =1 ∥ g$\_{1:}$$\_{T,i}$ ∥$\_{2}$

Finally, we can show the average regret of Adam converges,

Corollary 4.2. Assume that the function f$\_{t}$ has bounded gradients, ∥∇ f$\_{t}$ ( θ ) ∥$\_{2}$ ≤ G , ∥∇ f$\_{t}$ ( θ ) ∥$\_{∞}$ ≤ G$\_{∞}$ for all θ ∈ R d and distance between any θ$\_{t}$ generated by Adam is bounded, ∥ θ$\_{n}$ - θ$\_{m}$ ∥$\_{2}$ ≤ D , ∥ θ$\_{m}$ - θ$\_{n}$ ∥$\_{∞}$ ≤ D$\_{∞}$ for any m, n ∈ { 1 , ..., T } . Adam achieves the following guarantee, for all T ≥ 1 .

$$\frac { R ( T ) } { T } = O ( \frac { 1 } { \sqrt { T } } )$$

This result can be obtained by using Theorem 4.1 and ∑ d i =1 ∥ g$\_{1:}$$\_{T,i}$ ∥$\_{2}$ ≤ dG$\_{∞}$ √ T . Thus, lim$\_{T}$$\_{→∞}$ R ( T ) T = 0 .

## 5 RELATED WORK

Optimization methods bearing a direct relation to Adam are RMSProp (Tieleman &amp; Hinton, 2012; Graves, 2013) and AdaGrad (Duchi et al., 2011); these relationships are discussed below. Other stochastic optimization methods include vSGD (Schaul et al., 2012), AdaDelta (Zeiler, 2012) and the natural Newton method from Roux &amp; Fitzgibbon (2010), all setting stepsizes by estimating curvature

from first-order information. The Sum-of-Functions Optimizer (SFO) (Sohl-Dickstein et al., 2014) is a quasi-Newton method based on minibatches, but (unlike Adam) has memory requirements linear in the number of minibatch partitions of a dataset, which is often infeasible on memory-constrained systems such as a GPU. Like natural gradient descent (NGD) (Amari, 1998), Adam employs a preconditioner that adapts to the geometry of the data, since ̂ v$\_{t}$ is an approximation to the diagonal of the Fisher information matrix (Pascanu &amp; Bengio, 2013); however, Adam's preconditioner (like AdaGrad's) is more conservative in its adaption than vanilla NGD by preconditioning with the square root of the inverse of the diagonal Fisher information matrix approximation.

RMSProp: An optimization method closely related to Adam is RMSProp (Tieleman &amp; Hinton, 2012). A version with momentum has sometimes been used (Graves, 2013). There are a few important differences between RMSProp with momentum and Adam: RMSProp with momentum generates its parameter updates using a momentum on the rescaled gradient, whereas Adam updates are directly estimated using a running average of first and second moment of the gradient. RMSProp also lacks a bias-correction term; this matters most in case of a value of β$\_{2}$ close to 1 (required in case of sparse gradients), since in that case not correcting the bias leads to very large stepsizes and often divergence, as we also empirically demonstrate in section 6.4.

AdaGrad: An algorithm that works well for sparse gradients is AdaGrad (Duchi et al., 2011). Its basic version updates parameters as θ$\_{t}$$\_{+1}$ = θ$\_{t}$ - α · g$\_{t}$ / √ ∑ t i $\_{=1}$g 2 $\_{t}$. Note that if we choose β$\_{2}$ to be infinitesimally close to from below, then lim$\_{β}$$\_{2}$$\_{→}$$\_{1}$ ̂ v$\_{t}$ = t - 1 ∑ t i $\_{=1}$g 2 $\_{t}$. AdaGrad corresponds to a version of Adam with β$\_{1}$ = 0 , infinitesimally (1 - β$\_{2}$ ) and a replacement of α by an annealed version α$\_{t}$ = α · t - 1 / $^{2}$, namely θ$\_{t}$ - α · t - 1 / $^{2}$· ̂ m$\_{t}$ / √ lim$\_{β}$$\_{2}$$\_{→}$$\_{1}$ ̂ v$\_{t}$ = θ$\_{t}$ - α · t - 1 / $^{2}$· g$\_{t}$ / √ t - 1 ∑ t i $\_{=1}$g 2 t = θ$\_{t}$ - α · g$\_{t}$ / √ ∑ t i $\_{=1}$g 2 t . Note that this direct correspondence between Adam and Adagrad does not hold when removing the bias-correction terms; without bias correction, like in RMSProp, a β$\_{2}$ infinitesimally close to would lead to infinitely large bias, and infinitely large parameter updates.

## 6 EXPERIMENTS

To empirically evaluate the proposed method, we investigated different popular machine learning models, including logistic regression, multilayer fully connected neural networks and deep convolutional neural networks. Using large models and datasets, we demonstrate Adam can efficiently solve practical deep learning problems.

We use the same parameter initialization when comparing different optimization algorithms. The hyper-parameters, such as learning rate and momentum, are searched over a dense grid and the results are reported using the best hyper-parameter setting.

## 6.1 EXPERIMENT: LOGISTIC REGRESSION

We evaluate our proposed method on L2-regularized multi-class logistic regression using the MNIST dataset. Logistic regression has a well-studied convex objective, making it suitable for comparison of different optimizers without worrying about local minimum issues. The stepsize α in our logistic regression experiments is adjusted by 1 / √ t decay, namely α$\_{t}$ = α √ t that matches with our theoretical prediction from section 4. The logistic regression classifies the class label directly on the 784 dimension image vectors. We compare Adam to accelerated SGD with Nesterov momentum and Adagrad using minibatch size of 128. According to Figure 1, we found that the Adam yields similar convergence as SGD with momentum and both converge fas