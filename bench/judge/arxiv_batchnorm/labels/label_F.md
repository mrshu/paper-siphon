## Batch Normalization: Accelerating Deep Network Training by Reducing Internal Covariate Shift

Sergey Ioffe Google Inc., sioffe@google.com

Christian Szegedy

Google Inc., szegedy@google.com

Using mini-batches of examples, as opposed to one example at a time, is helpful in several ways. First, the gradient of the loss over a mini-batch is an estimate of the gradient over the training set, whose quality improves as the batch size increases. Second, computation over a batch can be much more efficient than m computations for individual examples, due to the parallelism afforded by the modern computing platforms.

While stochastic gradient is simple and effective, it requires careful tuning of the model hyper-parameters, specifically the learning rate used in optimization, as well as the initial values for the model parameters. The training is complicated by the fact that the inputs to each layer are affected by the parameters of all preceding layers - so that small changes to the network parameters amplify as the network becomes deeper.

The change in the distributions of layers' inputs presents a problem because the layers need to continuously adapt to the new distribution. When the input distribution to a learning system changes, it is said to experience covariate shift (Shimodaira, 2000). This is typically handled via domain adaptation (Jiang, 2008). However, the notion of covariate shift can be extended beyond the learning system as a whole, to apply to its parts, such as a sub-network or a layer. Consider a network computing

<!-- formula-not-decoded -->

where F 1 and F 2 are arbitrary transformations, and the parameters Θ 1 , Θ 2 are to be learned so as to minimize the loss /lscript . Learning Θ 2 can be viewed as if the inputs x = F 1 (u , Θ 1 ) are fed into the sub-network

<!-- formula-not-decoded -->

For example, a gradient descent step

<!-- formula-not-decoded -->

(for batch size m and learning rate α ) is exactly equivalent to that for a stand-alone network F 2 with input x . Therefore, the input distribution properties that make training more efficient - such as having the same distribution between the training and test data - apply to training the sub-network as well. As such it is advantageous for the distribution of x to remain fixed over time. Then, Θ 2 does

## Abstract

Training Deep Neural Networks is complicated by the fact that the distribution of each layer's inputs changes during training, as the parameters of the previous layers change. This slows down the training by requiring lower learning rates and careful parameter initialization, and makes it notoriously hard to train models with saturating nonlinearities. We refer to this phenomenon as internal covariate shift , and address the problem by normalizing layer inputs. Our method draws its strength from making normalization a part of the model architecture and performing the normalization for each training mini-batch . Batch Normalization allows us to use much higher learning rates and be less careful about initialization. It also acts as a regularizer, in some cases eliminating the need for Dropout. Applied to a state-of-the-art image classification model, Batch Normalization achieves the same accuracy with 14 times fewer training steps, and beats the original model by a significant margin. Using an ensemble of batchnormalized networks, we improve upon the best published result on ImageNet classification: reaching 4.9% top-5 validation error (and 4.8% test error), exceeding the accuracy of human raters.

## 1 Introduction

Deep learning has dramatically advanced the state of the art in vision, speech, and many other areas. Stochastic gradient descent (SGD) has proved to be an effective way of training deep networks, and SGD variants such as momentum (Sutskever et al., 2013) and Adagrad (Duchi et al., 2011) have been used to achieve state of the art performance. SGD optimizes the parameters Θ of the network, so as to minimize the loss

<!-- formula-not-decoded -->

where x 1 ...N is the training data set. With SGD, the training proceeds in steps, and at each step we consider a minibatch x 1 ...m of size m . The mini-batch is used to approximate the gradient of the loss function with respect to the parameters, by computing

<!-- formula-not-decoded -->

not have to readjust to compensate for the change in the distribution of x .

Fixed distribution of inputs to a sub-network would have positive consequences for the layers outside the subnetwork, as well. Consider a layer with a sigmoid activation function z = g ( W u + b) where u is the layer input, the weight matrix W and bias vector b are the layer parameters to be learned, and g ( x ) = 1 1+exp( -x ) . As | x | increases, g ′ ( x ) tends to zero. This means that for all dimensions of x = W u+b except those with small absolute values, the gradient flowing down to u will vanish and the model will train slowly. However, since x is affected by W, b and the parameters of all the layers below, changes to those parameters during training will likely move many dimensions of x into the saturated regime of the nonlinearity and slow down the convergence. This effect is amplified as the network depth increases. In practice, the saturation problem and the resulting vanishing gradients are usually addressed by using Rectified Linear Units (Nair &amp; Hinton, 2010) ReLU ( x ) = max( x, 0) , careful initialization (Bengio &amp; Glorot, 2010; Saxe et al., 2013), and small learning rates. If, however, we could ensure that the distribution of nonlinearity inputs remains more stable as the network trains, then the optimizer would be less likely to get stuck in the saturated regime, and the training would accelerate.

We refer to the change in the distributions of internal nodes of a deep network, in the course of training, as Internal Covariate Shift . Eliminating it offers a promise of faster training. We propose a new mechanism, which we call Batch Normalization , that takes a step towards reducing internal covariate shift, and in doing so dramatically accelerates the training of deep neural nets. It accomplishes this via a normalization step that fixes the means and variances of layer inputs. Batch Normalization also has a beneficial effect on the gradient flow through the network, by reducing the dependence of gradients on the scale of the parameters or of their initial values. This allows us to use much higher learning rates without the risk of divergence. Furthermore, batch normalization regularizes the model and reduces the need for Dropout (Srivastava et al., 2014). Finally, Batch Normalization makes it possible to use saturating nonlinearities by preventing the network from getting stuck in the saturated modes.

In Sec. 4.2, we apply Batch Normalization to the bestperforming ImageNet classification network, and show that we can match its performance using only 7% of the training steps, and can further exceed its accuracy by a substantial margin. Using an ensemble of such networks trained with Batch Normalization, we achieve the top-5 error rate that improves upon the best known results on ImageNet classification.

## 2 Towards Reducing Internal Covariate Shift

We define Internal Covariate Shift as the change in the distribution of network activations due to the change in network parameters during training. To improve the training, we seek to reduce the internal covariate shift. By fixing the distribution of the layer inputs x as the training progresses, we expect to improve the training speed. It has been long known (LeCun et al., 1998b; Wiesler &amp; Ney, 2011) that the network training converges faster if its inputs are whitened - i.e., linearly transformed to have zero means and unit variances, and decorrelated. As each layer observes the inputs produced by the layers below, it would be advantageous to achieve the same whitening of the inputs of each layer. By whitening the inputs to each layer, we would take a step towards achieving the fixed distributions of inputs that would remove the ill effects of the internal covariate shift.

We could consider whitening activations at every training step or at some interval, either by modifying the network directly or by changing the parameters of the optimization algorithm to depend on the network activation values (Wiesler et al., 2014; Raiko et al., 2012; Povey et al., 2014; Desjardins &amp; Kavukcuoglu). However, if these modifications are interspersed with the optimization steps, then the gradient descent step may attempt to update the parameters in a way that requires the normalization to be updated, which reduces the effect of the gradient step. For example, consider a layer with the input u that adds the learned bias b , and normalizes the result by subtracting the mean of the activation computed over the training data: ̂ x = x -E [ x ] where x = u + b , X = { x 1 ...N } is the set of values of x over the training set, and E [ x ] = 1 N ∑ N i =1 x i . If a gradient descent step ignores the dependence of E [ x ] on b , then it will update b ← b + ∆ b , where ∆ b ∝ -∂/lscript/∂ ̂ x . Then u + ( b + ∆ b ) -E [ u + ( b + ∆ b )] = u + b -E [ u + b ] . Thus, the combination of the update to b and subsequent change in normalization led to no change in the output of the layer nor, consequently, the loss. As the training continues, b will grow indefinitely while the loss remains fixed. This problem can get worse if the normalization not only centers but also scales the activations. We have observed this empirically in initial experiments, where the model blows up when the normalization parameters are computed outside the gradient descent step.

The issue with the above approach is that the gradient descent optimization does not take into account the fact that the normalization takes place. To address this issue, we would like to ensure that, for any parameter values, the network always produces activations with the desired distribution. Doing so would allow the gradient of the loss with respect to the model parameters to account for the normalization, and for its dependence on the model parameters Θ . Let again x be a layer input, treated as a

vector, and X be the set of these inputs over the training data set. The normalization can then be written as a transformation

̂ x = Norm (x , X ) which depends not only on the given training example x but on all examples X - each of which depends on Θ if x is generated by another layer. For backpropagation, we would need to compute the Jacobians

<!-- formula-not-decoded -->

ignoring the latter term would lead to the explosion described above. Within this framework, whitening the layer inputs is expensive, as it requires computing the covariance matrix Cov [x] = E x ∈X [xx T ] -E [x] E [x] T and its inverse square root, to produce the whitened activations Cov [x] -1 / 2 (x -E [x]) , as well as the derivatives of these transforms for backpropagation. This motivates us to seek an alternative that performs input normalization in a way that is differentiable and does not require the analysis of the entire training set after every parameter update.

Some of the previous approaches (e.g. (Lyu &amp; Simoncelli, 2008)) use statistics computed over a single training example, or, in the case of image networks, over different feature maps at a given location. However, this changes the representation ability of a network by discarding the absolute scale of activations. We want to a preserve the information in the network, by normalizing the activations in a training example relative to the statistics of the entire training data.

## 3 Normalization via Mini-Batch Statistics

Since the full whitening of each layer's inputs is costly and not everywhere differentiable, we make two necessary simplifications. The first is that instead of whitening the features in layer inputs and outputs jointly, we will normalize each scalar feature independently, by making it have the mean of zero and the variance of 1. For a layer with d -dimensional input x = ( x (1) . . . x ( d ) ) , we will normalize each dimension

<!-- formula-not-decoded -->

where the expectation and variance are computed over the training data set. As shown in (LeCun et al., 1998b), such normalization speeds up convergence, even when the features are not decorrelated.

Note that simply normalizing each input of a layer may change what the layer can represent. For instance, normalizing the inputs of a sigmoid would constrain them to the linear regime of the nonlinearity. To address this, we make sure that the transformation inserted in the network can represent the identity transform . To accomplish this, weintroduce, for each activation x ( k ) , a pair of parameters γ ( k ) , β ( k ) , which scale and shift the normalized value:

y ( k ) = γ ( k ) ̂ x ( k ) + β ( k ) . These parameters are learned along with the original model parameters, and restore the representation power of the network. Indeed, by setting γ ( k ) = √ Var [ x ( k ) ] and β ( k ) = E [ x ( k ) ] , we could recover the original activations, if that were the optimal thing to do.

In the batch setting where each training step is based on the entire training set, we would use the whole set to normalize activations. However, this is impractical when using stochastic optimization. Therefore, we make the second simplification: since we use mini-batches in stochastic gradient training, each mini-batch produces estimates of the mean and variance of each activation. This way, the statistics used for normalization can fully participate in the gradient backpropagation. Note that the use of minibatches is enabled by computation of per-dimension variances rather than joint covariances; in the joint case, regularization would be required since the mini-batch size is likely to be smaller than the number of activations being whitened, resulting in singular covariance matrices.

Consider a mini-batch B of size m . Since the normalization is applied to each activation independently, let us focus on a particular activation x ( k ) and omit k for clarity. We have m values of this activation in the mini-batch,

<!-- formula-not-decoded -->

Let the normalized values be ̂ x 1 ...m , and their linear transformations be y 1 ...m . We refer to the transform

<!-- formula-not-decoded -->

as the Batch Normalizing Transform . We present the BN Transform in Algorithm 1. In the algorithm, /epsilon1 is a constant added to the mini-batch variance for numerical stability.

<!-- formula-not-decoded -->

Algorithm 1: Batch Normalizing Transform, applied to activation x over a mini-batch.

The BN transform can be added to a network to manipulate any activation. In the notation y = BN γ,β ( x ) , we

indicate that the parameters γ and β are to be learned, but it should be noted that the BN transform does not independently process the activation in each training example. Rather, BN γ,β ( x ) depends both on the training example and the other examples in the mini-batch . The scaled and shifted values y are passed to other network layers. The normalized activations ̂ x are internal to our transformation, but their presence is crucial. The distributions of values of any ̂ x has the expected value of 0 and the variance of 1 , as long as the elements of each mini-batch are sampled from the same distribution, and if we neglect /epsilon1 . This can be seen by observing that ∑ m i =1 ̂ x i = 0 and 1 m ∑ m i =1 ̂ x 2 i = 1 , and taking expectations. Each normalized activation ̂ x ( k ) can be viewed as an input to a sub-network composed of the linear transform y ( k ) = γ ( k ) ̂ x ( k ) + β ( k ) , followed by the other processing done by the original network. These sub-network inputs all have fixed means and variances, and although the joint distribution of these normalized ̂ x ( k ) can change over the course of training, we expect that the introduction of normalized inputs accelerates the training of the sub-network and, consequently, the network as a whole.

During training we need to backpropagate the gradient of loss /lscript through this transformation, as well as compute the gradients with respect to the parameters of the BN transform. We use chain rule, as follows (before simplification):

<!-- formula-not-decoded -->

Thus, BN transform is a differentiable transformation that introduces normalized activations into the network. This ensures that as the model is training, layers can continue learning on input distributions that exhibit less internal covariate shift, thus accelerating the training. Furthermore, the learned affine transform applied to these normalized activations allows the BN transform to represent the identity transformation and preserves the network capacity.

## 3.1 Training and Inference with BatchNormalized Networks

To Batch-Normalize a network, we specify a subset of activations and insert the BN transform for each of them, according to Alg. 1. Any layer that previously received x as the input, now receives BN ( x ) . A model employing Batch Normalization can be trained using batch gradient descent, or Stochastic Gradient Descent with a mini-batch size m &gt; 1 , or with any of its variants such as Adagrad

(Duchi et al., 2011). The normalization of activations that depends on the mini-batch allows efficient training, but is neither necessary nor desirable during inference; we want the output to depend only on the input, deterministically. For this, once the network has been trained, we use the normalization using the population, rather than mini-batch, statistics. Neglecting /epsilon1 , these normalized activations have the same mean 0 and variance 1 as during training. We use the unbiased variance estimate Var [ x ] = m m -1 · E B [ σ 2 B ] , where the expectation is over training mini-batches of size m and σ 2 B are their sample variances. Using moving averages instead, we can track the accuracy of a model as it trains. Since the means and va