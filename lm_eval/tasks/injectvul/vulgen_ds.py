import datasets
import glob
import os
import random

class InjectUAFDataset(datasets.GeneratorBasedBuilder):
    def _info(self):
        return datasets.DatasetInfo(
            description="Dataset of C/C++ function bodies with instructions to inject a use-after-free vulnerability.",
            features=datasets.Features(
                {
                    "id": datasets.Value("string"),
                    "function_body": datasets.Value("string"),
                    "instruction": datasets.Value("string"),
                    "expected_output": datasets.Value("string"),
                }
            ),
            supervised_keys=None,
            citation="",
        )

    def _split_generators(self, dl_manager):
        dataset_path = "/home1/arasteh/BinVulGen/external/lm-evaluation-harness/lm_eval/tasks/injectvul/func_bodies"  # Folder with .txt files
        return [
            datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"filepath": dataset_path}),
            datasets.SplitGenerator(name=datasets.Split.TEST, gen_kwargs={"filepath": dataset_path}),

        ]

    def _generate_examples(self, filepath):
       
        pattern_paths = "/home1/arasteh/BinVulGen/llm_json_patterns/"
        list_patterns = glob.glob(os.path.join(pattern_paths, "*.txt"))
        selected_pattern = random.choice(list_patterns)
        with open(selected_pattern, "r") as pat:
            pattern_content = pat.read()

        instruction = "I will give you a pattern of use-after-free. use this pattern to inject vulnerability in the following function. Pattern:"+pattern_content
        
        file_list = glob.glob(os.path.join(filepath, "*.txt"))

        for i, file_path in enumerate(file_list):
            try:
                with open(file_path, "r") as f:
                    function_body = f.read().strip()
                filename = os.path.basename(file_path)
                function_name = filename.split(".")[0]
                yield i, {
                    "id": function_name,
                    "function_body": function_body,
                    "instruction": instruction,
                    "expected_output": "",  # Leave blank; model will generate
                }
            except Exception as e:
                print(f"Skipping {file_path} due to error: {e}")
