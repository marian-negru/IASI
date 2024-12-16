# BIOSINF, IASI Lab 5 - Speech Denoising & Model Pruning

In this lab we will test a speech denoising algorithm and apply different pruning methods over the model. Audio examples will be recorded by the students for inference.

Clone this repo in your local Jetson:
```bash
git clone https://github.com/marian-negru/IASI.git
```

## Python packages

For this lab, run the following script for dependencies:

```bash
sudo bash install_dependencies.sh
```

After that, run the command:

```bash
pip3 install -r requirements.txt
```

## Speech Denoising

After installing the pre-requirements, follow the following steps (assume path is git folder):

1. Record an audio using:

```bash 
cd src 
python3 record.py
```
Be careful to select the right sample rate and number of channels.

**Question**: How should we set sample rate and number of channels?

2. Listen to the recording:
```bash
cd src
python3 listen.py
```
If everything is ok, proceed to next step. If not, record again.

**Question**: How can we tell that everything is ok?

3. Apply denoising model:
```bash
cd MP-SENet
python3 inference_iasi.py
```
Be sure to change paths and methods accordingly.

**Question** Does the model run succesfully? If yes, why? If not, why?

**Ideas to modify code** -- to be discussed 


## Model Pruning

Tutorial available [here](https://www.datature.io/blog/a-comprehensive-guide-to-neural-network-model-pruning).

Torch Pruning documentation available [here](https://pytorch.org/tutorials/intermediate/pruning_tutorial.html).

**Question** Is this implementation of pruning efficient?

**Question** Which type of pruning do we want in this case?

**Exercise**: apply local pruning and save prediction. Use L1 and Random pruning (make sure to change output dir when switcing functions)

**Exercise**: apply global pruning and save prediction. Use L1 and Random pruning (make sure to change output dir when switcing functions)

**Exercise** compare methods and decide what is the best one. Call L1 (MAE) and L2 (MSE) functions from torch separatelly. Also listen to the samples! Make a comparison table!

## Discussion

**Talk about other methods**
