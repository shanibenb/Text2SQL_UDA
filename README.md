# Text2SQL_UDA

## Back Translation
1. Install pytorch version 1.2.0
2. Install the required packages
    ```
    pip install -r requirements_back_translation.txt
    ```
3. Download the dataset from the [official Spider dataset website](https://yale-lily.github.io/spider)
4. Run
    ```
    python main.py --main_path=dataset/
    ```
    A *cache* folder will be created in the [model](https://github.com/shanibenb/Text2SQL_UDA/model) directory.
