## NEURAL MACHINE TRANSLATION BY JOINTLY LEARNING TO ALIGN AND TRANSLATE

## Dzmitry Bahdanau

Jacobs University Bremen, Germany

KyungHyun Cho Yoshua Bengio ∗

Universit'e de Montr'eal

## ABSTRACT

Neural machine translation is a recently proposed approach to machine translation. Unlike the traditional statistical machine translation, the neural machine translation aims at building a single neural network that can be jointly tuned to maximize the translation performance. The models proposed recently for neural machine translation often belong to a family of encoder-decoders and encode a source sentence into a fixed-length vector from which a decoder generates a translation. In this paper, we conjecture that the use of a fixed-length vector is a bottleneck in improving the performance of this basic encoder-decoder architecture, and propose to extend this by allowing a model to automatically (soft-)search for parts of a source sentence that are relevant to predicting a target word, without having to form these parts as a hard segment explicitly. With this new approach, we achieve a translation performance comparable to the existing state-of-the-art phrase-based system on the task of English-to-French translation. Furthermore, qualitative analysis reveals that the (soft-)alignments found by the model agree well with our intuition.

## 1 INTRODUCTION

Neural machine translation is a newly emerging approach to machine translation, recently proposed by Kalchbrneren and Blunsom (2013), Sutskever et al. (2014) and Cho et al. (2014b). Unlike the traditional phrase-based translation system (see, e.g., Koehn et al. , 2003) which consists of many small sub-components that are tuned separately, neural machine translation attempts to build and train a single, large neural network that reads a sentence and outputs a correct translation.

Most of the proposed neural machine translation models belong to a family of encoderdecoders (Sutskever et al. , 2014; Cho et al. , 2014a), with an encoder and a decoder for each language, or involve a language-specific encoder applied to each sentence whose outputs are then compared (Hermann and Blunsom, 2014). An encoder neural network reads and encodes a source sentence into a fixed-length vector. A decoder then outputs a translation from the encoded vector. The whole encoder-decoder system, which consists of the encoder and the decoder for a language pair, is jointly trained to maximize the probability of a correct translation given a source sentence.

A potential issue with this encoder-decoder approach is that a neural network needs to be able to compress all the necessary information of a source sentence into a fixed-length vector. This may make it difficult for the neural network to cope with long sentences, especially those that are longer than the sentences in the training corpus. Cho et al. (2014b) showed that indeed the performance of a basic encoder-decoder deteriorates rapidly as the length of an input sentence increases.

In order to address this issue, we introduce an extension to the encoder-decoder model which learns to align and translate jointly. Each time the proposed model generates a word in a translation, it (soft-)searches for a set of positions in a source sentence where the most relevant information is concentrated. The model then predicts a target word based on the context vectors associated with these source positions and all the previous generated target words.

$^{∗}$CIFAR Senior Fellow

The most important distinguishing feature of this approach from the basic encoder-decoder is that it does not attempt to encode a whole input sentence into a single fixed-length vector. Instead, it encodes the input sentence into a sequence of vectors and chooses a subset of these vectors adaptively while decoding the translation. This frees a neural translation model from having to squash all the information of a source sentence, regardless of its length, into a fixed-length vector. We show this allows a model to cope better with long sentences.

In this paper, we show that the proposed approach of jointly learning to align and translate achieves significantly improved translation performance over the basic encoder-decoder approach. The improvement is more apparent with longer sentences, but can be observed with sentences of any length. On the task of English-to-French translation, the proposed approach achieves, with a single model, a translation performance comparable, or close, to the conventional phrase-based system. Furthermore, qualitative analysis reveals that the proposed model finds a linguistically plausible (soft-)alignment between a source sentence and the corresponding target sentence.

## 2 BACKGROUND: NEURAL MACHINE TRANSLATION

From a probabilistic perspective, translation is equivalent to finding a target sentence y that maximizes the conditional probability of y given a source sentence x , i.e., arg max y p ( y | x ) . In neural machine translation, we fit a parameterized model to maximize the conditional probability of sentence pairs using a parallel training corpus. Once the conditional distribution is learned by a translation model, given a source sentence a corresponding translation can be generated by searching for the sentence that maximizes the conditional probability.

Recently, a number of papers have proposed the use of neural networks to directly learn this conditional distribution (see, e.g., Kalchbrenner and Blunsom, 2013; Cho et al. , 2014a; Sutskever et al. , 2014; Cho et al. , 2014b; Forcada and Èneco, 1997). This neural machine translation approach typically consists of two components, the first of which encodes a source sentence x and the second decodes to a target sentence y . For instance, two recurrent neural networks (RNN) were used by (Cho et al. , 2014a) and (Sutskever et al. , 2014) to encode a variable-length source sentence into a fixed-length vector and to decode the vector into a variable-length target sentence.

Despite being a quite new approach, neural machine translation has already shown promising results. Sutskever et al. (2014) reported that the neural machine translation based on RNNs with long shortterm memory (LSTM) units achieves close to the state-of-the-art performance of the conventional phrase-based machine translation system on an English-to-French translation task. 1 Adding neural components to existing translation systems, for instance, to score the phrase pairs in the phrase table (Cho et al. , 2014a) or to re-rank candidate translations (Sutskever et al. , 2014), has allowed to surpass the previous state-of-the-art performance level.

## 2.1 RNN ENCODER-DECODER

Here, we describe briefly the underlying framework, called RNN Encoder-Decoder , proposed by Cho et al. (2014a) and Sutskever et al. (2014) upon which we build a novel architecture that learns to align and translate simultaneously.

In the Encoder-Decoder framework, an encoder reads the input sentence, a sequence of vectors x = ( x$\_{1}$ , · · · , x$\_{T}$$\_{x}$ ) , into a vector c . 2 The most common approach is to use an RNN such that

$$h _ { t } = f \left ( x _ { t } , h _ { t - 1 } \right )$$

and

$$c = q \left ( \left \{ h _ { 1 } , \cdots , h _ { T _ { x } } \right \} \right ) ,$$

where h$\_{t}$ ∈ R n is a hidden state at time t , and c is a vector generated from the sequence of the hidden states. f and q are some nonlinear functions. Sutskever et al. (2014) used an LSTM as f and q ( { h$\_{1}$ , · · · , h$\_{T}$ } ) = h$\_{T}$ , for instance.

1 We mean by the state-of-the-art performance, the performance of the conventional phrase-based system without using any neural network-based component.

2 Although most of the previous works (see, e.g., Cho et al. , 2014a; Sutskever et al. , 2014; Kalchbrenner and Blunsom, 2013) used to encode a variable-length input sentence into a fixed-length vector, it is not necessary, and even it may be beneficial to have a variable-length vector, as we will show later.

The decoder is often trained to predict the next word y$\_{t}$ ' given the context vector c and all the previously predicted words { y$\_{1}$, · · · , y$\_{t}$ $^{'}$- $\_{1}$} . In other words, the decoder defines a probability over the translation y by decomposing the joint probability into the ordered conditionals:

$$p ( y ) = \prod _ { t = 1 } ^ { T } p ( y _ { t } \, | \, \{ y _ { 1 } , \cdots , y _ { t - 1 } \} \, , c ) ,$$

where y = $^{(}$y$\_{1}$ , · · · , y$\_{T}$$\_{y}$ $^{)}$. With an RNN, each conditional probability is modeled as

$$p ( y _ { t } \, | \, \{ y _ { 1 } , \cdots , y _ { t - 1 } \} \, , c ) = g ( y _ { t - 1 } , s _ { t } , c ) ,$$

where g is a nonlinear, potentially multi-layered, function that outputs the probability of y$\_{t}$ , and s$\_{t}$ is the hidden state of the RNN. It should be noted that other architectures such as a hybrid of an RNN and a de-convolutional neural network can be used (Kalchbrenner and Blunsom, 2013).

## 3 LEARNING TO ALIGN AND TRANSLATE

In this section, we propose a novel architecture for neural machine translation. The new architecture consists of a bidirectional RNN as an encoder (Sec. 3.2) and a decoder that emulates searching through a source sentence during decoding a translation (Sec. 3.1).

## 3.1 DECODER: GENERAL DESCRIPTION

In a new model architecture, we define each conditional probability in Eq. (2) as:

$$p ( y _ { i } | y _ { 1 } , \dots , y _ { i - 1 } , \mathbf x ) = g ( y _ { i - 1 } , s _ { i } , c _ { i } ) ,$$

where s$\_{i}$ is an RNN hidden state for time i , computed by

$$s _ { i } = f ( s _ { i - 1 } , y _ { i - 1 } , c _ { i } ) .$$

It should be noted that unlike the existing encoder-decoder approach (see Eq. (2)), here the probability is conditioned on a distinct context vector c$\_{i}$ for each target word y$\_{i}$ .

The context vector c$\_{i}$ depends on a sequence of annotations ( h$\_{1}$, · · · , h$\_{T}$$\_{x}$ ) to which an encoder maps the input sentence. Each annotation h$\_{i}$ contains information about the whole input sequence with a strong focus on the parts surrounding the i -th word of the input sequence. We explain in detail how the annotations are computed in the next section.

The context vector c$\_{i}$ is, then, computed as a weighted sum of these annotations h$\_{i}$ :

$$c _ { i } = \sum _ { j = 1 } ^ { T _ { x } } \alpha _ { i j } h _ { j } .$$

The weight α$\_{ij}$ of each annotation h$\_{j}$ is computed by

$$\alpha _ { i j } = \frac { \exp \left ( e _ { i j } \right ) } { \sum _ { k = 1 } ^ { T _ { x } } \exp \left ( e _ { i k } \right ) } ,$$

where

$$e _ { i j } = a ( s _ { i - 1 } , h _ { j } )$$

is an alignment model which scores how well the inputs around position j and the output at position i match. The score is based on the RNN hidden state s$\_{i}$$\_{-}$$\_{1}$ (just before emitting y$\_{i}$ , Eq. (4)) and the j -th annotation h$\_{j}$ of the input sentence.

We parametrize the alignment model a as a feedforward neural network which is jointly trained with all the other components of the proposed system. Note that unlike in traditional machine translation,

Line chart

Figure 1: The graphical illustration of the proposed model trying to generate the t -th target word y$\_{t}$ given a source sentence ( x$\_{1}$, x$\_{2}$, . . . , x$\_{T}$ ) .

<!-- image -->

the alignment is not considered to be a latent variable. Instead, the alignment model directly computes a soft alignment, which allows the gradient of the cost function to be backpropagated through. This gradient can be used to train the alignment model as well as the whole translation model jointly.

We can understand the approach of taking a weighted sum of all the annotations as computing an expected annotation , where the expectation is over possible alignments. Let α$\_{ij}$ be a probability that the target word y$\_{i}$ is aligned to, or translated from, a source word x$\_{j}$ . Then, the i -th context vector c$\_{i}$ is the expected annotation over all the annotations with probabilities α$\_{ij}$ .

The probability α$\_{ij}$ , or its associated energy e$\_{ij}$ , reflects the importance of the annotation h$\_{j}$ with respect to the previous hidden state s$\_{i}$$\_{-}$$\_{1}$ in deciding the next state s$\_{i}$ and generating y$\_{i}$ . Intuitively, this implements a mechanism of attention in the decoder. The decoder decides parts of the source sentence to pay attention to. By letting the decoder have an attention mechanism, we relieve the encoder from the burden of having to encode all information in the source sentence into a fixedlength vector. With this new approach the information can be spread throughout the sequence of annotations, which can be selectively retrieved by the decoder accordingly.

## 3.2 ENCODER: BIDIRECTIONAL RNN FOR ANNOTATING SEQUENCES

The usual RNN, described in Eq. (1), reads an input sequence x in order starting from the first symbol x$\_{1}$ to the last one x$\_{T}$$\_{x}$ . However, in the proposed scheme, we would like the annotation of each word to summarize not only the preceding words, but also the following words. Hence, we propose to use a bidirectional RNN (BiRNN, Schuster and Paliwal, 1997), which has been successfully used recently in speech recognition (see, e.g., Graves et al. , 2013).

A BiRNN consists of forward and backward RNN's. The forward RNN → f reads the input sequence as it is ordered (from x$\_{1}$ to x$\_{T}$$\_{x}$ ) and calculates a sequence of forward hidden states ( → h$\_{1}$ , · · · , → h$\_{T}$$\_{x}$ ) . The backward RNN ← f reads the sequence in the reverse order (from x$\_{T}$$\_{x}$ to x$\_{1}$ ), resulting in a sequence of backward hidden states ( ← h$\_{1}$ , · · · , ← h$\_{T}$$\_{x}$ ) .

We obtain an annotation for each word x$\_{j}$ by concatenating the forward hidden state → h$\_{j}$ and the backward one ← h$\_{j}$ , i.e., h$\_{j}$ = [ → h ⊤ j ; ← h ⊤ j ] ⊤ . In this way, the annotation h$\_{j}$ contains the summaries of both the preceding words and the following words. Due to the tendency of RNNs to better represent recent inputs, the annotation h$\_{j}$ will be focused on the words around x$\_{j}$ . This sequence of annotations is used by the decoder and the alignment model later to compute the context vector (Eqs. (5)-(6)).

See Fig. 1 for the graphical illustration of the proposed model.

## 4 EXPERIMENT SETTINGS

We evaluate the proposed approach on the task of English-to-French translation. We use the bilingual, parallel corpora provided by ACL WMT '14. 3 As a comparison, we also report the performance of an RNN Encoder-Decoder which was proposed recently by Cho et al. (2014a). We use the same training procedures and the same dataset for both models. 4

## 4.1 DATASET

WMT '14 contains the following English-French parallel corpora: Europarl (61M words), news commentary (5.5M), UN (421M) and two crawled corpora of 90M and 272.5M words respectively, totaling 850M words. Following the procedure described in Cho et al. (2014a), we reduce the size of the combined corpus to have 348M words using the data selection method by Axelrod et al. (2011). 5 We do not use any monolingual data other than the mentioned parallel corpora, although it may be possible to use a much larger monolingual corpus to pretrain an encoder. We concatenate news-test-

$^{3}$http://www.statmt.org/wmt14/translation-task.html

$^{4}$Implementations are available at https://github.com/lisa-groundhog/GroundHog .

$^{5}$Available online at http://www-lium.univ-lemans.fr/~schwenk/cslm\_joint\_paper/ .

<!-- image -->

2012 and news-test-2013 to make a development (validation) set, and evaluate the models on the test set (news-test-2014) from WMT '14, which consists of 3003 sentences not present in the training data.

After a usual tokenization$^{6}$, we use a shortlist of 30,000 most frequent words in each language to train our models. Any word not included in the shortlist is mapped to a special token ([UNK]). We do not apply any other special preprocessing, such as lowercasing or stemming, to the data.

## 4.2 MODELS

We train two types of models. The first one is an RNN Encoder-Decoder (RNNencdec, Cho et al. , 2014a), and the other is the proposed model, to which we refer as RNNsearch. We train each model twice: first with the sentences of length up to 30 words (RNNencdec-30, RNNsearch-30) and then with the sentences of length up to 50 word (RNNencdec-50, RNNsearch-50).

The encoder and decoder of the RNNencdec have 1000 hidden units each. 7 The encoder of the RNNsearch consists of forward and backward recurrent neural networks (RNN) each having 1000 hidden units. Its decoder has 1000 hidden units. In both cases, we use a multilayer network with a single maxout (Goodfellow et al. , 2013) hidden layer to compute the conditional probability of each target word (Pascanu et al. , 2014).

We use a minibatch stochastic gradient descent (SGD) algorithm together with Adadelta (Zeiler, 2012) to train each model. Each SGD update direction is computed using a minibatch of 80 sentences. We trained each model for approximately 5 days.

Once a model is trained, we use a beam search to find a translation that approximately maximizes the conditional probability (see, e.g., Graves, 2012; Boulanger-Lewandowski et al. , 2013). Sutskever et al. (2014) used this approach to generate translations from their neural machine translation model.

For more details on the architectures of the models and training procedure used in the experiments, see Appendices A and B.

## 5 RESULTS

## 5.1 QUANTITATIVE RESULTS

In Table 1, we list the translation performances measured in BLEU score. It is clear from the table that in all the cases, the proposed RNNsearch outperforms the conventional RNNencdec. More importantly, the performance of the RNNsearch is as high as that of the conventional phrase-based translation system (Moses), when only the sentences consisting of known words are considered. 