from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers.generation import GenerationConfig
import torch
torch.manual_seed(1234)
tokenizer = AutoTokenizer.from_pretrained("/home/ucfnwzh/workspace/model/Qwen-VL", trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained("/home/ucfnwzh/workspace/model/Qwen-VL", device_map="cuda", trust_remote_code=True).eval()


