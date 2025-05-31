import datasets
import glob
import os

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
        dataset_path = "/home1/arasteh/BinVulGen/lm-evaluation-harness/lm_eval/tasks/injectvul/func_bodies"  # Folder with .txt files
        return [
            datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"filepath": dataset_path}),
            datasets.SplitGenerator(name=datasets.Split.TEST, gen_kwargs={"filepath": dataset_path}),

        ]

    def _generate_examples(self, filepath):
        instruction = (
            "Inject a use-after-free vulnerability into the following function. "
            "Use only variables and pointers inside the function. Do not generate a new variable."
            "You are only allowed to modify the function body. Do not remove or rename the function. "
            "Preserve the original structure as much as possible."
        )

        file_list = glob.glob(os.path.join(filepath, "*.txt"))

        for i, file_path in enumerate(file_list):
            try:
                with open(file_path, "r") as f:
                    function_body = f.read().strip()

                yield i, {
                    "id": f"func_{i}",
                    "function_body": function_body,
                    "instruction": instruction,
                    "expected_output": "",  # Leave blank; model will generate
                }
            except Exception as e:
                print(f"Skipping {file_path} due to error: {e}")
