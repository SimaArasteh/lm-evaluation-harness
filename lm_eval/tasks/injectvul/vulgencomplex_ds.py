import datasets
import glob
import os
import random

class ComplexUAFDataset(datasets.GeneratorBasedBuilder):
    def _info(self):
        return datasets.DatasetInfo(
            description="Dataset of C/C++ function bodies with instructions to make a use-after-free vulnerability more real.",
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
        dataset_path = "/home1/arasteh/BinVulGen/ai_agent/llm_response/complex_vul"  # Folder with .txt files
        return [
            datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"filepath": dataset_path}),
            datasets.SplitGenerator(name=datasets.Split.TEST, gen_kwargs={"filepath": dataset_path}),

        ]

    def _generate_examples(self, filepath):
        instruction = (
           "You are given a C/C++ function that contains a use-after-free (UAF) vulnerability."
            "Your task is to maximize the distance between the lines responsible for triggering this vulnerability."
            "Do not change the order of the lines. This is very important."
            "You must not add any new code or modify the structure of the function beyond rearranging existing lines. "
            "Do not introduce new variables, function calls, or logic."
           )
        
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
