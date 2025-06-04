import fitz  
import json
import re

def extract_qa_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    
    qa_pairs = re.findall(r"س\.(.*?)ج\.(.*?)(?=س\.|$)", text, re.DOTALL)

    qa_list = []
    for question, answer in qa_pairs:
        question = question.strip().replace("\n", " ")
        answer = answer.strip().replace("\n", " ")
        qa_list.append({"question": question, "answer": answer})
    
    return qa_list

def save_to_json(data, output_path):
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

pdf_path = "qa_data.pdf"          
output_json = "qa_data_ar.json"

qa_data = extract_qa_from_pdf(pdf_path)
save_to_json(qa_data, output_json)

print("✅ تم حفظ البيانات في qa_data_ar.json")
