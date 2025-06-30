import datasets
import glob
import os

class FuzzGenDataset(datasets.GeneratorBasedBuilder):
    def _info(self):
        return datasets.DatasetInfo(
            description="Dataset of fake main bodies with instructions to generate libfuzzer harness.",
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
        dataset_path = "/home1/arasteh/BinVulGen/external/lm-evaluation-harness/lm_eval/tasks/injectvul/injected_bodies/"  # Folder with .txt files
        return [
            datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"filepath": dataset_path}),
            datasets.SplitGenerator(name=datasets.Split.TEST, gen_kwargs={"filepath": dataset_path}),

        ]

    def _generate_examples(self, filepath):
        instruction = (
            "You are given a C/C++ function. Write a LibFuzzer-compatible fuzzing harness for it."

            "Requirements:"
            "1. The harness must define `extern C int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size)`."
            "2. Do NOT define the function you are fuzzing; instead, declare it using `extern C` so it can be linked from another object file."
            "3. Use `extern C` for both `LLVMFuzzerTestOneInput` and the target function to prevent C++ name mangling and ensure the harness links correctly with C code."
            "4. Include minimal and necessary headers (`<stdint.h>`, `<stddef.h>`, etc.)."
            "5. If the function uses structs, enums, or typedefs, provide placeholder or mock definitions OR leave a comment indicating they must be included."
            "6. Always check `size` before accessing `data` to avoid buffer overflows."
            "7. Convert `data` into appropriate argument types for the target function (e.g., arrays, integers, enums)."
            "8. Return 0 from `LLVMFuzzerTestOneInput`."
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
