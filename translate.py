
import deepl
import os
import apikey

# 영어로 기계번역할 deepl 번역함수
def translater(text:str) -> str:
  auth_key = apikey.auth_key
  translator = deepl.Translator(auth_key)
  translated = translator.translate_text(text,target_lang="EN-US")
  return translated.text

languages = ['es','fr']
file_dir = 'resource'
language_data = {}

# language_data를 통해, 수집된 데이터 파일을 읽어서 저장한다.
for language in languages:
  file_name = f"{language}.txt"
  file_path = os.path.join(file_dir,file_name)

  if os.path.exists(file_path):
    with open(file_path,'r',encoding='utf-8') as file:
      data = file.read()
    
    language_data[language] = data
  
# 기계번역을 통해 텍스트 번역 후, translated_resource에 저장
for key, value in language_data.items():
  content = language_data.get(key)
  translated_content = translater(content)
  file_name = "translated_"+key

  file_path = './translated_resource/'+ f"{file_name}.txt" 
  with open(file_path,'w',encoding='utf-8') as file:
    file.write(translated_content)


