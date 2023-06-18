import fasttext

class Language_Identification_Model:

    def __init__(self):
        pretrained_lang_model = "/RIDSS2023/inputfolder/lid.176.bin"
        self.model = fasttext.load_model(pretrained_lang_model)

    def predict_lang(self, text):
        predictions = self.model.predict(text, k=3) # returns top 3 matching languages
        return predictions 
