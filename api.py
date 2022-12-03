from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from reorder_adj import ReorderADJ

class RequestSentence(BaseModel):
    text: str
    feature: str

app = FastAPI()
reodering = ReorderADJ()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/reorder_adj")
def translate(request_sentence: RequestSentence):
    text = request_sentence.text
    if text[-1] in 'qwertyuiopasdfghjklzxcvbnm':
        text += '.'
    print(f"Reorder adj: {text}")
    feature = request_sentence.feature
    if feature == 'reorder_adj':
        reordered_sentence = reodering.reorder_adj(text)
        return {
            'IsSuccessed': True,
            'Message': 'Success',
            'ResultObj': {
                'src': text,
                'result': reordered_sentence
            }
        }
    else:
        return {
            'IsSuccessed': False,
            'Message': 'Fail',
            'ResultObj': {
                'src': text,
                'result': ""
            }
        }