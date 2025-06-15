import datasets
import glob
import os

class FixHarnessError(datasets.GeneratorBasedBuilder):
    def _info(self):
        return datasets.DatasetInfo(
            description="Dataset of harnesses with build errors",
            features=datasets.Features(
                {
                    "id": datasets.Value("string"),
                    "function_body": datasets.Value("string"),
                    "builderror": datasets.Value("string"),
                    "instruction": datasets.Value("string"),
                    "expected_output": datasets.Value("string"),
                }
            ),
            supervised_keys=None,
            citation="",
        )

    def _split_generators(self, dl_manager):
        dataset_path = "/home1/arasteh/BinVulGen/ai_agent/fixed_error/harness_errors/"  # Folder with .txt files
        return [
            datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"filepath": dataset_path}),
            datasets.SplitGenerator(name=datasets.Split.TEST, gen_kwargs={"filepath": dataset_path}),

        ]

    def _generate_examples(self, filepath):
        instruction = (
            "You are a security-focused code assistant helping with fuzzing infrastructure."

            "I have generated the following fuzzing harness for a C/C++ function. However, when I attempt to build the harness using the OSS-Fuzz build system (with clang and AddressSanitizer), I encounter these build errors."

            "Please analyze the harness and the build errors. rewrite the fuzzing harness and try to fix the build errors."
        )

        file_list = glob.glob(os.path.join(filepath, "*.txt"))

        for i, file_path in enumerate(file_list):
            try:
                with open(file_path, "r") as f:
                    content = f.read().strip()
                
                filename = os.path.basename(file_path)
                function_name = filename.split(".")[0]
                content_parts = content.split("++++++++++")
                function_body = content_parts[0]
                builderror = content_parts[1]
                yield i, {
                    "id": function_name,
                    "function_body": function_body,
                    "builderror": builderror,
                    "instruction": instruction,
                    "expected_output": "",  # Leave blank; model will generate
                }
            except Exception as e:
                print(f"Skipping {file_path} due to error: {e}")
