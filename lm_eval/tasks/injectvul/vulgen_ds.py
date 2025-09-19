import datasets
import glob
import os
import random
import joblib

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
             datasets.SplitGenerator(name=datasets.Split.TEST, gen_kwargs={"filepath": dataset_path}),
        ]

    def _generate_examples(self, filepath):
       
        pattern_paths = "/home1/arasteh/BinVulGen/llm_json_patterns/"
        list_patterns = glob.glob(os.path.join(pattern_paths, "*.txt"))
        

        instruction = "I will give you a pattern of use-after-free in real CVEs and then a C/C++ function body from mupdf project. I want you to carefully follow the orders in the pattern and mimic it to inject use-after-free vulnerability into the function body. Remember not to use any function names in the pattern. for memory allocation or deallocation only use functions in mupdf."
        
        '''vul = "/home1/arasteh/BinVulGen/pattern_functions/cves/comps_mrtree_unite.txt"
        with open(vul, "r") as v:
            vul_content = v.read()

        instruction = "I will give you an exmaple of use-after-free vulnerability including the patch and the vulnerable function. Then I will give you another function from mupdf project. Inspiring from the example, inject use-after-free vulnerability into this function. To use any function (e.g for free ) remember to use functions of mupdf. Vulnerability Example:  "+vul_content'''
        file_list = glob.glob(os.path.join(filepath, "*.txt"))

        for i, file_path in enumerate(file_list):
            try:
                with open(file_path, "r") as f:
                    function_body = f.read().strip()
                filename = os.path.basename(file_path)
                function_name = filename.split(".")[0]
                selected_pattern = random.choice(list_patterns)
                with open(selected_pattern, "r") as pat:
                    pattern_content = pat.read()
                pattern_name = selected_pattern.split("/")[-1].split(".")[0]
                joblib.dump(pattern_content, "/home1/arasteh/BinVulGen/binvulgen_results/qwen/"+function_name+"/selected_pattern/"+pattern_name+".pkl")
                instruction = instruction+ " here is the pattern"+pattern_content
                module_name = filename.split(".")[1]
                if module_name.lower() == ".c":
                    instruction = instruction+" Remember:This function is written in C language.just use C specific keywords and syntax"
                if module_name.lower() == ".cpp" or module_name.lower() == ".cxx":
                    instruction = instruction+" Remember:This function is written in Cplusplus language.just use C++ specific keywords and syntax"

                yield i, {
                    "id": function_name,
                    "function_body": function_body,
                    "instruction": instruction,
                    "expected_output": "",  # Leave blank; model will generate
                }
            except Exception as e:
                print(f"Skipping {file_path} due to error: {e}")
