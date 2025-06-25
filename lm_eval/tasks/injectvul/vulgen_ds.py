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
        '''instruction = (
           "You are given a C/C++ function. Inject a use-after-free vulnerability in to the following function by using one of the techniques below."
           "Technique1: apply these steps in order. 1. Choose one of the existing pointers in the function. Do not create a new variable."
           "2. use function free to free the allocated memory. 3. reuse that pointer after function free. try to put this line as far as possible to function free"
           "Technique2: 1.Identify an existing pointer in the function. 2. Create a pointer alias by assigning the existing pointer to another pointer variable within the function"
           "3.Free the original pointer to deallocate the memory it points to using free function. 4.After the memory is freed, access it again using the alias pointer. This access can be a read, write."
           "You are only allowed to modify the function body. Do not remove or rename the function. "
            "Preserve the original structure as much as possible."
           )'''
        import joblib
        list_prompts = joblib.load("/home1/arasteh/BinVulGen/ai_agent/use-after-free-listprompts.pkl")
        selected_prompt = random.choice(list_prompts)
        instruction = selected_prompt
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
