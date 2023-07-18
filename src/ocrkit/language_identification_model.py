import fasttext

## fasttext language identification model used for the identification of languages in the documents

class Language_Identification_Model:

    def __init__(self):
        pretrained_lang_model = "/RIDSS2023/src/ocrkit/lid.176 (1).bin"
        self.model = fasttext.load_model(pretrained_lang_model)
    
    # Function to identify the languages in a text
    def predict_lang(self, text):
        predictions = self.model.predict(text, k=3) # k determines the amount of matching languages returned, here it returns the top 3 matching languages 
        return predictions 
