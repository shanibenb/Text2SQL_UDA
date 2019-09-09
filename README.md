# Text2SQL_UDA
<sub><sup>*This project was done by Shani Ben Baruch and Noam Mann as a part of a TAU cs course*</sub></sup>

This project goal is to train a semi-superveised model using [Spider Dataset](https://yale-lily.github.io/spider).
Our model is based on:
1. [Representing Schema Structure with Graph Neural Networks for Text-to-SQL Parsing](https://arxiv.org/abs/1905.06241)
2. [Unsupervised Data Augmentation](https://arxiv.org/abs/1904.12848)

<p align="center">
  <img src="Picture.png" width="300px" height="250px"/>
</p>

## Train
To train the model you need to follow the next two parts:

### Back Translation
1. Install pytorch version *1.2.0*
2. Install the required packages
    ```
    pip install -r requirements_back_translation.txt
    ```
3. Download the dataset from the [official Spider dataset website](https://yale-lily.github.io/spider)
4. Run
    ```
    python main.py --main_path=dataset/
    ```
    A *cache* folder will be created in the [model](https://github.com/shanibenb/Text2SQL_UDA/tree/master/model) directory.
    
### Model
1. Install pytorch version *1.0.1.post2* 
2. Install the required packages
    ```
    pip install -r requirements_model.txt
    ``` 
3. Run this command to install NLTK punkt.
    ```
    python -c "import nltk; nltk.download('punkt')"
    ```
5. Edit the config file `train_configs/defaults.jsonnet` to update the location of the dataset:
    ```
    local dataset_path = "dataset/";
    ```
6. Use the following AllenNLP command to train:
    ```
    allennlp train train_configs/defaults.jsonnet -s experiments/name_of_experiment \
    --include-package dataset_readers.spider \ 
    --include-package models.semantic_parsing.spider_parser
    ```
