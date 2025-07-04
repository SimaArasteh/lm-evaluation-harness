import datasets
import glob
import os

class PatternDataset(datasets.GeneratorBasedBuilder):
    def _info(self):
        return datasets.DatasetInfo(
            description="Dataset of vulnerable functions that contain a specific vulnerability type",
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
        dataset_path = "/home1/arasteh/BinVulGen/pattern_functions/juliet"  # Folder with .txt files
        return [
            datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"filepath": dataset_path}),
            datasets.SplitGenerator(name=datasets.Split.TEST, gen_kwargs={"filepath": dataset_path}),

        ]

    def _generate_examples(self, filepath):
        instruction = (
            "You are given a C/C++ function. can you describe the pattern of use-after-free"
            "vulnerability of this function"
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
