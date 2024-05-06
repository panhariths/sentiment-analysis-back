import re

def preprocess(translated_text, remove_stop_word=True):

  stop_words = ["ទាំង", "ដ៏", "បើ", "ក៏", "ដែរ", "ទេ", "អ្នកណា", "អ្វី", "នៅឯណា", "ពេលណា", "ហេតុអ្វី", "យ៉ាងម៉េច", "ពេលខ្លះ", "មិនដែល", "ទីនេះ", "ទីនោះ", "គ្រប់ទីកន្លែង", "កន្លែងណាមួយ", "នៅទីណាមួយ", "ណាស់", "មែន", "មែនទែន", "ពិតប្រាកដ", "ឥឡូវនេះ", "ពេលក្រោយ", "យប់នេះ", "យប់ម្សិលមិញ", "ព្រឹកនេះ", "ម្សិលមិញ", "ថ្ងៃនេះ",
                    "ថ្ងៃស្អែក", "អាទិត្យក្រោយ", "រួចរាល់", "រួចហើយ", "នៅតែ", "និង", "ដែល", "ជា", "តែ", "ដើម្បី", "ប៉ុន្តែ", "ដោយសារ", "ពេលដែល", "ហើយ", "ដូចជា", "ដូច្នេះ", "ពេលណាមួយ", "ទៅវិញ", "តែម្តង", "ជាមួយ",  "ដូចគ្នានឹង", "រួចហើយទេ", "ឬ", "ដោយ", "ខ្ញុំ", "អ្នក", "នាង", "ពួក", "យើង", "ពួកគេ", "លោក", "គាត់", "គេ", "នេះ", "នោះ", "ណា"]

  pattern = r'[។៘ៗ៕៚៙៖។...()+=»«-]'

  # Remove URLs
  translated_text = re.sub(r'http\S+', '', translated_text)

  # Remove special characters (excluding digits and numbers)
  translated_text = re.sub(r'[^ក-៹\s0-9]', '', translated_text)

  # Replace multiple spaces with a single space
  translated_text = re.sub(r'\s+', ' ', translated_text).strip()

  # Remove English letters and numbers
  translated_text = re.sub(r'[a-zA-Z0-9]', '', translated_text)

  # Remove English punctuation and special characters
  translated_text = re.sub(
      r'[!"#$%&\'()*+,-./:;<=>?@\[\\]^_`{|}~]', '', translated_text)

  # Replace multiple spaces with a single space
  translated_text = re.sub(r'\s+', ' ', translated_text).strip()

  # Remove Khmer special characters
  translated_text = re.sub(pattern, '', translated_text)

  # Remove specific Khmer words
  if remove_stop_word:
    for word in stop_words:
        translated_text = translated_text.replace(word, '')

  # Remove space in between words
  translated_text = translated_text.replace(" ", "")

  return translated_text
