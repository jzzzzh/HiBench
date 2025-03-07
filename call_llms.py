import transformers
import torch
from huggingface_hub import login
import os
import openai
from openai import AzureOpenAI  
import requests
import json
from transformers import AutoModelForCausalLM, AutoTokenizer
import regex as re
import warnings
os.environ['PYTORCH_CUDA_ALLOC_CONF'] = 'expandable_segments:True'

def read_hf_token():
    with open(".hfkey", "r") as f:
        token = f.read()
    return token

class Checker:
    def __init__(self) -> None:
        pass

    def check_json(self, str):
        pattern =  r'.*\{"answer":\s*".*?"\}.*'
        if re.search(pattern, str):
            return True
        else:
            return False
        
    def check_formate(self, str, template):
        pattern = template
        if re.search(pattern, str):
            return True
        else:
            return False
        

class LLMModel:
    def __init__(self, model_id, api_key=None, endpoint=None, device_map='auto'):
        self.model_id = model_id
        self.model_list = ["meta-llama/Meta-Llama-3.1-8B-Instruct", "meta-llama/Llama-3.2-1B-Instruct","meta-llama/Llama-3.2-3B-Instruct", "Qwen/Qwen2.5-0.5B-Instruct", "Qwen/Qwen2.5-1.5B-Instruct", "Qwen/Qwen2.5-3B-Instruct", "Qwen/Qwen2.5-7B-Instruct", "Qwen/Qwen2.5-14B-Instruct",  "Qwen/Qwen2.5-32B-Instruct"]
        self.Large_language_model_list = ["Qwen/Qwen2.5-72B-Instruct", "meta-llama/Llama-3.1-70B-Instruct", "meta-llama/Llama-3.1-405B-Instruct", "deepseek/deepseek-v3", "deepseek/deepseek-R1"]
        self.openai_list = ["gpt-3.5-turbo", "gpt-3.5-turbo-davinci", "gpt-3.5-turbo-davinci-codex", "gpt-3.5-turbo-davinci-instruct", "gpt-3.5-turbo-davinci-codex-instruct", "gpt-3.5-turbo-davinci-codex-instruct-turbo", "gpt-4o", "gpt-4o-mini", "gpt-4-turbo"]
        self.old_model_list = ["THUDM/glm-4-9b-chat", "01-ai/Yi-1.5-9B-Chat","baichuan-inc/Baichuan-7B", "baichuan-inc/Baichuan2-7B-Chat", "microsoft/Phi-3.5-mini-instruct", "internlm/internlm2_5-7b-chat", "mistralai/Mistral-7B-Instruct-v0.3"]
        self.api_key = api_key
        self.endpoint = endpoint
        self.device = device_map
        self.device_map = device_map
        print(f"Loading model: {model_id}")
        if model_id in self.model_list:
            company_name, model_name = model_id.split("/")
            hf_home = os.getenv("HF_HOME")
            model_path = os.path.join(hf_home, f"models--{company_name}--{model_name}") if hf_home else None
            if company_name == "meta-llama" and (hf_home is None or not os.path.exists(model_path)):
                login(token=read_hf_token())
                # login(token="")   
                print(f"Downloading model: {model_id}")
            self.pipeline = transformers.pipeline("text-generation", model=model_id, model_kwargs={"torch_dtype": torch.bfloat16}, device_map=self.device_map)
            self.terminators = [
                self.pipeline.tokenizer.eos_token_id,
                self.pipeline.tokenizer.convert_tokens_to_ids("<|eot_id|>")
            ]
        elif model_id in self.old_model_list:
            # print("Loading old model")
            self.tokenizer = AutoTokenizer.from_pretrained(model_id, trust_remote_code=True)
            self.model = AutoModelForCausalLM.from_pretrained(
                model_id,
                torch_dtype=torch.bfloat16,
                low_cpu_mem_usage=True,
                trust_remote_code=True
            ).to(self.device).eval()
        # self.gen_kwargs = {"max_length": 3000, "do_sample": True, "top_k": 1}
        self.gen_kwargs = {"max_new_tokens": 256, "do_sample": True, "top_k": 1}
    
    def get_response_fireworks(self, system_prompt, question):
        fireworks_model_id = self.transfer_to_fireworks(self.model_id)
        if self.api_key is None:
            print("Error: Please provide the Fireworks API key.")
        else:
            url = "https://api.fireworks.ai/inference/v1/chat/completions"
            payload = {
                "model": f"accounts/fireworks/models/{fireworks_model_id}",
                # "model": f"accounts/fireworks/models/llama-v3p1-8b-instruct",
                "max_tokens": self.gen_kwargs["max_new_tokens"],
                "top_p": 1,
                "top_k": 40,
                "presence_penalty": 0,
                "frequency_penalty": 0,
                "temperature": 0.0,
                "messages": [
                    {
                        "role": "system",
                        "content": system_prompt
                    },
                    {
                        "role": "user",
                        "content": question
                    }
                    ]
                }
            headers = {
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": "Bearer " + self.api_key   
                }
            
            response = requests.request("POST", url, headers=headers, data=json.dumps(payload))
                # Check the response
            if response.status_code == 200:
                data = response.json()
                return data["choices"][0]["message"]["content"]
            else:
                print(f"Error: {response.status_code} - {response.text}")                         
    
    def call_openai_api(self, system_setting, prompt):
        openai_model_list = ["gpt-3.5-turbo", "gpt-3.5-turbo-davinci", "gpt-3.5-turbo-davinci-codex", "gpt-3.5-turbo-davinci-instruct", "gpt-3.5-turbo-davinci-codex-instruct", "gpt-3.5-turbo-davinci-codex-instruct-turbo", "gpt-4", "gpt-4o", "gpt-4o-mini", "gpt-4-turbo"]
        if self.model_id not in openai_model_list:
            print(f"Warning: The model_id '{self.model_id}' is not in the OpenAI model list.")
            exit(1)
        if self.api_key is None:
            print("Error: Please provide the OpenAI API key.")
        
        model_map = {
            "gpt-3.5-turbo" : "gpt-35-turbo",
            "gpt-4-turbo" : "gpt-4-turbo-2024-0409"
        }
        model_engine = model_map[self.model_id] if self.model_id in model_map else self.model_id
        endpoint = os.getenv("ENDPOINT_URL", self.endpoint)  
        deployment = os.getenv("DEPLOYMENT_NAME", model_engine)  
        subscription_key = os.getenv("AZURE_OPENAI_API_KEY", self.api_key)

        # 使用基于密钥的身份验证初始化 Azure OpenAI 服务客户端    
        client = AzureOpenAI(  
            azure_endpoint=endpoint,  
            api_key=subscription_key,  
            api_version="2024-02-01",
        )

        res1 = client.chat.completions.create(  
            model=deployment,
            messages=[
                            {"role": "system", "content": system_setting},
                            {"role": "user", "content": prompt},
                        ],
            max_tokens=self.gen_kwargs["max_new_tokens"],  
            temperature=0.0,  
            top_p=0.95,  
            frequency_penalty=0,  
            presence_penalty=0,
            stop=None,  
            stream=False
        )
        
        # return res1['choices'][0]['message']['content'].strip('\n')
        # print(res1)
        return res1.choices[0].message.content.strip('\n')
    
    def call_api(self, system_setting, prompt, api_platform="fireworks"):
        if api_platform == "fireworks":
            return self.get_response_fireworks(system_setting, prompt)
        elif api_platform == "openai":
            return self.call_openai_api(system_setting, prompt)
        
    def transfer_to_fireworks(self, model_name):
        if model_name == "Qwen/Qwen2.5-72B-Instruct":
            return "qwen2p5-72b-instruct"
        elif model_name == "meta-llama/Llama-3.1-70B-Instruct":
            return "llama-v3p1-70b-instruct"
        elif model_name == "meta-llama/Llama-3.1-405B-Instruct":
            return "llama-v3p1-405b-instruct"
        elif model_name == "deepseek/deepseek-v3":
            return "deepseek-v3"
        elif model_name == "deepseek/deepseek-R1":
            return "deepseek-r1"
        else:
            return model_name

    def get_local_response(self, system_setting = "use english", prompt = "Who are you?"):
        messages = [
            {"role": "system", "content": system_setting},
            {"role": "user", "content": prompt},
        ]
        company_name, model_name = self.model_id.split("/")
        if company_name == "meta-llama":
            outputs = self.pipeline(
                messages,
                max_new_tokens=self.gen_kwargs["max_new_tokens"],
                eos_token_id=self.terminators,
                do_sample=True,
                temperature=0.0,
                top_p=0.9,
                pad_token_id = self.pipeline.tokenizer.eos_token_id
            )
        else:
            outputs = self.pipeline(
            messages,
            max_new_tokens=self.gen_kwargs["max_new_tokens"],
            )
        return outputs[0]["generated_text"][-1]["content"]

    def run_old_model(self, query, system_setting):
        if self.model_id == "baichuan-inc/Baichuan-7B":
            inputs = self.tokenizer(f'{system_setting}{query}', return_tensors='pt')
        else:
            inputs = self.tokenizer.apply_chat_template(
                [
                {"role": "system", "content": system_setting},
                {"role": "user", "content": query}
                ],
                add_generation_prompt=True,
                tokenize=True,
                return_tensors="pt",
                return_dict=True
            )
        inputs = inputs.to(self.device)
        # print("-----------------")
        # print(inputs)
        with torch.no_grad():
            outputs = self.model.generate(**inputs, **self.gen_kwargs)
            # print(outputs)
            outputs = outputs[:, inputs['input_ids'].shape[1]:]
            return self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        
    def get_response(self, system_setting = "use english", prompt = "Who are you?", check_response=True, max_steps=1, template="json"):
        if check_response:
            checker = Checker()
            step = 0
            while step < max_steps:
                ans = self.get_response(system_setting, prompt, check_response=False)
                if template == "json":
                    # if checker.check_json(ans):
                    if True:
                        return ans
                else:
                    # if checker.check_formate(ans, template):
                    if True:
                        return ans
                step += 1
            warnings.warn("The response does not match the template.")
            return ans
        else:
            if self.model_id in self.openai_list:
                ans = self.call_api(system_setting, prompt, api_platform="openai")
            else:
                if self.model_id in self.model_list:
                    ans = self.get_local_response(system_setting=system_setting, prompt=prompt)
                elif self.model_id in self.Large_language_model_list:
                    
                    ans = self.call_api(system_setting, prompt, api_platform="fireworks")
                elif self.model_id in self.old_model_list:
                    
                    ans = self.run_old_model(prompt, system_setting)
                else:
                    print(f"Warning: The model_id '{self.model_id}' is not in the Large language model list.")
                    exit(1)
            return ans
        
    
if __name__ == "__main__":
    # model_id = "THUDM/glm-4-9b-chat"
    # model_id = "01-ai/Yi-1.5-9B-Chat"
    # model_id = "baichuan-inc/Baichuan-7B"
    # model_id = "baichuan-inc/Baichuan2-7B-Chat"
    # model_id = "microsoft/Phi-3.5-mini-instruct"
    # model_id = "internlm/internlm2_5-7b-chat"
    # model_id = "mistralai/Mistral-7B-Instruct-v0.3"
    # model_id = "Qwen/Qwen2.5-0.5B-Instruct"
    # model_id = "meta-llama/Meta-Llama-3.1-8B-Instruct"
    # model_id = "Qwen/Qwen2.5-72B-Instruct"
    model_id = "deepseek/deepseek-v3"
    # model_id = "gpt-4-turbo"
    system_setting = "You are a helpful assistant."
    prompt = "hello? "
    llm = LLMModel(model_id, api_key=None)
    ans = llm.get_response(system_setting, prompt)
    print(ans)    
