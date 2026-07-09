## ADAM: A METHOD FOR STOCHASTIC OPTIMIZATION

Diederik P. Kingma * University of Amsterdam, OpenAI dpkingma@openai.com

## ABSTRACT

We introduce Adam , an algorithm for first-order gradient-based optimization of stochastic objective functions, based on adaptive estimates of lower-order moments. The method is straightforward to implement, is computationally efficient, has little memory requirements, is invariant to diagonal rescaling of the gradients, and is well suited for problems that are large in terms of data and/or parameters. The method is also appropriate for non-stationary objectives and problems with very noisy and/or sparse gradients. The hyper-parameters have intuitive interpretations and typically require little tuning. Some connections to related algorithms, on which Adam was inspired, are discussed. We also analyze the theoretical convergence properties of the algorithm and provide a regret bound on the convergence rate that is comparable to the best known results under the online convex optimization framework. Empirical results demonstrate that Adam works well in practice and compares favorably to other stochastic optimization methods. Finally, we discuss AdaMax , a variant of Adam based on the infinity norm.

## 1 INTRODUCTION

Stochastic gradient-based optimization is of core practical importance in many fields of science and engineering. Many problems in these fields can be cast as the optimization of some scalar parameterized objective function requiring maximization or minimization with respect to its parameters. If the function is differentiable w.r.t. its parameters, gradient descent is a relatively efficient optimization method, since the computation of first-order partial derivatives w.r.t. all the parameters is of the same computational complexity as just evaluating the function. Often, objective functions are stochastic. For example, many objective functions are composed of a sum of subfunctions evaluated at different subsamples of data; in this case optimization can be made more efficient by taking gradient steps w.r.t. individual subfunctions, i.e. stochastic gradient descent (SGD) or ascent. SGD proved itself as an efficient and effective optimization method that was central in many machine learning success stories, such as recent advances in deep learning (Deng et al., 2013; Krizhevsky et al., 2012; Hinton &amp; Salakhutdinov, 2006; Hinton et al., 2012a; Graves et al., 2013). Objectives may also have other sources of noise than data subsampling, such as dropout (Hinton et al., 2012b) regularization. For all such noisy objectives, efficient stochastic optimization techniques are required. The focus of this paper is on the optimization of stochastic objectives with high-dimensional parameters spaces. In these cases, higher-order optimization methods are ill-suited, and discussion in this paper will be restricted to first-order methods.

We propose Adam , a method for efficient stochastic optimization that only requires first-order gradients with little memory requirement. The method computes individual adaptive learning rates for different parameters from estimates of first and second moments of the gradients; the name Adam is derived from adaptive moment estimation. Our method is designed to combine the advantages of two recently popular methods: AdaGrad (Duchi et al., 2011), which works well with sparse gradients, and RMSProp (Tieleman &amp; Hinton, 2012), which works well in on-line and non-stationary settings; important connections to these and other stochastic optimization methods are clarified in section 5. Some of Adam's advantages are that the magnitudes of parameter updates are invariant to rescaling of the gradient, its stepsizes are approximately bounded by the stepsize hyperparameter, it does not require a stationary objective, it works with sparse gradients, and it naturally performs a form of step size annealing.

∗ Equal contribution. Author ordering determined by coin flip over a Google Hangout.

Jimmy Lei Ba ∗ University of Toronto jimmy@psi.utoronto.ca

Algorithm 1: Adam , our proposed algorithm for stochastic optimization. See section 2 for details, and for a slightly more efficient (but less clear) order of computation. g 2 t indicates the elementwise square g t /circledot g t . Good default settings for the tested machine learning problems are α = 0 . 001 , β 1 = 0 . 9 , β 2 = 0 . 999 and /epsilon1 = 10 -8 . All operations on vectors are element-wise. With β t 1 and β t 2 we denote β 1 and β 2 to the power t .

```
Require: α : Stepsize Require: β 1 , β 2 ∈ [0 , 1) : Exponential decay rates for the moment estimates Require: f ( θ ) : Stochastic objective function with parameters θ Require: θ 0 : Initial parameter vector m 0 ← 0 (Initialize 1 st moment vector) v 0 ← 0 (Initialize 2 nd moment vector) t ← 0 (Initialize timestep) while θ t not converged do t ← t +1 g t ←∇ θ f t ( θ t -1 ) (Get gradients w.r.t. stochastic objective at timestep t ) m t ← β 1 · m t -1 +(1 -β 1 ) · g t (Update biased first moment estimate) v t ← β 2 · v t -1 +(1 -β 2 ) · g 2 t (Update biased second raw moment estimate) ̂ m t ← m t / (1 -β t 1 ) (Compute bias-corrected first moment estimate) ̂ v t ← v t / (1 -β t 2 ) (Compute bias-corrected second raw moment estimate) θ t ← θ t -1 -α · ̂ m t / ( √ ̂ v t + /epsilon1 ) (Update parameters) end while return θ t (Resulting parameters)
```

In section 2 we describe the algorithm and the properties of its update rule. Section 3 explains our initialization bias correction technique, and section 4 provides a theoretical analysis of Adam's convergence in online convex programming. Empirically, our method consistently outperforms other methods for a variety of models and datasets, as shown in section 6. Overall, we show that Adam is a versatile algorithm that scales to large-scale high-dimensional machine learning problems.

## 2 ALGORITHM

See algorithm 1 for pseudo-code of our proposed algorithm Adam . Let f ( θ ) be a noisy objective function: a stochastic scalar function that is differentiable w.r.t. parameters θ . We are interested in minimizing the expected value of this function, E [ f ( θ )] w.r.t. its parameters θ . With f 1 ( θ ) , ..., , f T ( θ ) we denote the realisations of the stochastic function at subsequent timesteps 1 , ..., T . The stochasticity might come from the evaluation at random subsamples (minibatches) of datapoints, or arise from inherent function noise. With g t = ∇ θ f t ( θ ) we denote the gradient, i.e. the vector of partial derivatives of f t , w.r.t θ evaluated at timestep t .

The algorithm updates exponential moving averages of the gradient ( m t ) and the squared gradient ( v t ) where the hyper-parameters β 1 , β 2 ∈ [0 , 1) control the exponential decay rates of these moving averages. The moving averages themselves are estimates of the 1 st moment (the mean) and the 2 nd raw moment (the uncentered variance) of the gradient. However, these moving averages are initialized as (vectors of) 0's, leading to moment estimates that are biased towards zero, especially during the initial timesteps, and especially when the decay rates are small (i.e. the β s are close to 1). The good news is that this initialization bias can be easily counteracted, resulting in bias-corrected estimates m t and v t . See section 3 for more details.

<!-- formula-not-decoded -->

̂ ̂ Note that the efficiency of algorithm 1 can, at the expense of clarity, be improved upon by changing the order of computation, e.g. by replacing the last three lines in the loop with the following lines:

## 2.1 ADAM'S UPDATE RULE

An important property of Adam's update rule is its careful choice of stepsizes. Assuming /epsilon1 = 0 , the effective step taken in parameter space at timestep t is ∆ t = α · ̂ m t / √ ̂ v t . The effective stepsize has two upper bounds: | ∆ t | ≤ α · (1 -β 1 ) / √ 1 -β 2 in the case (1 -β 1 ) &gt; √ 1 -β 2 , and | ∆ t | ≤ α

otherwise. The first case only happens in the most severe case of sparsity: when a gradient has been zero at all timesteps except at the current timestep. For less sparse cases, the effective stepsize will be smaller. When (1 -β 1 ) = √ 1 -β 2 we have that | ̂ m t / √ ̂ v t | &lt; 1 therefore | ∆ t | &lt; α . In more common scenarios, we will have that ̂ m t / √ ̂ v t ≈ ± 1 since | E [ g ] / √ E [ g 2 ] | ≤ 1 . The effective magnitude of the steps taken in parameter space at each timestep are approximately bounded by the stepsize setting α , i.e., | ∆ t | /lessorapproxeql α . This can be understood as establishing a trust region around the current parameter value, beyond which the current gradient estimate does not provide sufficient information. This typically makes it relatively easy to know the right scale of α in advance. For many machine learning models, for instance, we often know in advance that good optima are with high probability within some set region in parameter space; it is not uncommon, for example, to have a prior distribution over the parameters. Since α sets (an upper bound of) the magnitude of steps in parameter space, we can often deduce the right order of magnitude of α such that optima can be reached from θ 0 within some number of iterations. With a slight abuse of terminology, we will call the ratio ̂ m t / √ ̂ v t the signal-to-noise ratio ( SNR ). With a smaller SNR the effective stepsize ∆ t will be closer to zero. This is a desirable property, since a smaller SNR means that there is greater uncertainty about whether the direction of ̂ m t corresponds to the direction of the true gradient. For example, the SNR value typically becomes closer to 0 towards an optimum, leading to smaller effective steps in parameter space: a form of automatic annealing. The effective stepsize ∆ t is also invariant to the scale of the gradients; rescaling the gradients g with factor c will scale ̂ m t with a factor c and ̂ v t with a factor c 2 , which cancel out: ( c · ̂ m t ) / ( √ c 2 · ̂ v t ) = ̂ m t / √ ̂ v t .

## 3 INITIALIZATION BIAS CORRECTION

As explained in section 2, Adam utilizes initialization bias correction terms. We will here derive the term for the second moment estimate; the derivation for the first moment estimate is completely analogous. Let g be the gradient of the stochastic objective f , and we wish to estimate its second raw moment (uncentered variance) using an exponential moving average of the squared gradient, with decay rate β 2 . Let g 1 , ..., g T be the gradients at subsequent timesteps, each a draw from an underlying gradient distribution g t ∼ p ( g t ) . Let us initialize the exponential moving average as v 0 = 0 (a vector of zeros). First note that the update at timestep t of the exponential moving average v t = β 2 · v t -1 +(1 -β 2 ) · g 2 t (where g 2 t indicates the elementwise square g t /circledot g t ) can be written as a function of the gradients at all previous timesteps:

<!-- formula-not-decoded -->

We wish to know how E [ v t ] , the expected value of the exponential moving average at timestep t , relates to the true second moment E [ g 2 t ] , so we can correct for the discrepancy between the two. Taking expectations of the left-hand and right-hand sides of eq. (1):

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

where ζ = 0 if the true second moment E [ g 2 i ] is stationary; otherwise ζ can be kept small since the exponential decay rate β 1 can (and should) be chosen such that the exponential moving average assigns small weights to gradients too far in the past. What is left is the term (1 -β t 2 ) which is caused by initializing the running average with zeros. In algorithm 1 we therefore divide by this term to correct the initialization bias.

In case of sparse gradients, for a reliable estimate of the second moment one needs to average over many gradients by chosing a small value of β 2 ; however it is exactly this case of small β 2 where a lack of initialisation bias correction would lead to initial steps that are much larger.

## 4 CONVERGENCE ANALYSIS

We analyze the convergence of Adam using the online learning framework proposed in (Zinkevich, 2003). Given an arbitrary, unknown sequence of convex cost functions f 1 ( θ ) , f 2 ( θ ) ,..., f T ( θ ) . At each time t , our goal is to predict the parameter θ t and evaluate it on a previously unknown cost function f t . Since the nature of the sequence is unknown in advance, we evaluate our algorithm using the regret, that is the sum of all the previous difference between the online prediction f t ( θ t ) and the best fixed point parameter f t ( θ ∗ ) from a feasible set X for all the previous steps. Concretely, the regret is defined as:

<!-- formula-not-decoded -->

Theorem 4.1. Assume that the function f t has bounded gradients, ‖∇ f t ( θ ) ‖ 2 ≤ G , ‖∇ f t ( θ ) ‖ ∞ ≤ G ∞ for all θ ∈ R d and distance between any θ t generated by Adam is bounded, ‖ θ n -θ m ‖ 2 ≤ D , ‖ θ m -θ n ‖ ∞ ≤ D ∞ for any m,n ∈ { 1 , ..., T } , and β 1 , β 2 ∈ [0 , 1) satisfy β 2 1 √ β 2 &lt; 1 . Let α t = α √ t and β 1 ,t = β 1 λ t -1 , λ ∈ (0 , 1) . Adam achieves the following guarantee, for all T ≥ 1 .

where θ ∗ = arg min θ ∈X ∑ T t =1 f t ( θ ) . We show Adam has O ( √ T ) regret bound and a proof is given in the appendix. Our result is comparable to the best known bound for this general convex online learning problem. We also use some definitions simplify our notation, where g t /defines ∇ f t ( θ t ) and g t,i as the i th element. We define g 1: t,i ∈ R t as a vector that contains the i th dimension of the gradients over all iterations till t , g 1: t,i = [ g 1 ,i , g 2 ,i , · · · , g t,i ] . Also, we define γ /defines β 2 1 √ β 2 . Our following theorem holds when the learning rate α t is decaying at a rate of t -1 2 and first moment running average coefficient β 1 ,t decay exponentially with λ , that is typically close to 1, e.g. 1 -10 -8 .

<!-- formula-not-decoded -->

Our Theorem 4.1 implies when the data features are sparse and bounded gradients, the summation term can be much smaller than its upper bound ∑ d i =1 ‖ g 1: T,i ‖ 2 &lt;&lt; dG ∞ √ T and ∑ d i =1 √ T ̂ v T,i &lt;&lt; dG ∞ √ T , in particular if the class of function and data features are in the form of section 1.2 in (Duchi et al., 2011). Their results for the expected value E [ ∑ d i =1 ‖ g 1: T,i ‖ 2 ] also apply to Adam. In particular, the adaptive method, such as Adam and Adagrad, can achieve O (log d √ T ) , an improvement over O ( √ dT ) for the non-adaptive method. Decaying β 1 ,t towards zero is important in our theoretical analysis and also matches previous empirical findings, e.g. (Sutskever et al., 2013) suggests reducing the momentum coefficient in the end of training can improve convergence.

Finally, we can show the average regret of Adam converges,

Corollary 4.2. Assume that the function f t has bounded gradients, ‖∇ f t ( θ ) ‖ 2 ≤ G , ‖∇ f t ( θ ) ‖ ∞ ≤ G ∞ for all θ ∈ R d and distance between any θ t generated by Adam is bounded, ‖ θ n -θ m ‖ 2 ≤ D , ‖ θ m -θ n ‖ ∞ ≤ D ∞ for any m,n ∈ { 1 , ..., T } . Adam achieves the following guarantee, for all T ≥ 1 .

<!-- formula-not-decoded -->

This result can be obtained by using Theorem 4.1 and ∑ d i =1 ‖ g 1: T,i ‖ 2 ≤ dG ∞ √ T . Thus, lim T →∞ R ( T ) T = 0 .

## 5 RELATED WORK

Optimization methods bearing a direct relation to Adam are RMSProp (Tieleman &amp; Hinton, 2012; Graves, 2013) and AdaGrad (Duchi et al., 2011); these relationships are discussed below. Other stochastic optimization methods include vSGD (Schaul et al., 2012), AdaDelta (Zeiler, 2012) and the natural Newton method from Roux &amp; Fitzgibbon (2010), all setting stepsizes by estimating curvature

from first-order information. The Sum-of-Functions Optimizer (SFO) (Sohl-Dickstein et al., 2014) is a quasi-Newton method based on minibatches, but (unlike Adam) has memory requirements linear in the number of minibatch partitions of a dataset, which is often infeasible on memory-constrained systems such as a GPU. Like natural gradient descent (NGD) (Amari, 1998), Adam employs a preconditioner that adapts to the geometry of the data, since ̂ v t is an approximation to the diagonal of the Fisher information matrix (Pascanu &amp; Bengio, 2013); however, Adam's preconditioner (like AdaGrad's) is more conservative in its adaption than vanilla NGD by preconditioning with the square root of the inverse of the diagonal Fisher information matrix approximation.

RMSProp: An optimization method closely related to Adam is RMSProp (Tieleman &amp; Hinton, 2012). A version with momentum has sometimes been used (Graves, 2013). There are a few important differences between RMSProp with momentum and Adam: RMSProp with momentum generates its parameter updates using a momentum on the rescaled gradient, whereas Adam updates are directly estimated using a running average of first and second moment of the gradient. RMSProp also lacks a bias-correction term; this matters most in case of a value of β 2 close to 1 (required in case of sparse gradients), since in that case not correcting the bias leads to very large stepsizes and often divergence, as we also empirically demonstrate in section 6.4.

AdaGrad: An algorithm that works well for sparse gradients is AdaGrad (Duchi et al., 2011). Its basic version updates parameters as θ t +1 = θ t -α · g t / √ ∑ t i =1 g 2 t . Note that if we choose β 2 to be infinitesimally close to 1 from below, then lim β 2 → 1 ̂ v t = t -1 · ∑ t i =1 g 2 t . AdaGrad corresponds to a version of Adam with β 1 = 0 , infinitesimal (1 -β 2 ) and a replacement of α by an annealed version α t = α · t -1 / 2 , namely θ t -α · t -1 / 2 · ̂ m t / √ lim β 2 → 1 ̂ v t = θ t -α · t -1 / 2 · g t / √ t -1 · ∑ t i =1 g 2 t = θ t -α · g t / √ ∑ t i =1 g 2 t . Note that this direct correspondence between Adam and Adagrad does not hold when removing the bias-correction terms; without bias correction, like in RMSProp, a β 2 infinites