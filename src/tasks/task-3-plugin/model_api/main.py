from fastapi import FastAPI, HTTPException
from utils import get_logger, SetFitPipeline, PredictInput, PredictResponse
from setfit import SetFitModel


logger = get_logger(__name__)
app = FastAPI()
#model = SetFitPipeline("./model_artifacts")
model = SetFitModel.from_pretrained("IsaacRodgz/setfit-stance-prediction-spanish-news-headlines")

#
# Endpoints
#

@app.get("/health")
def health_check():
    """
    Regular Health endpoint
    """
    return {"health":True}

@app.post("/predict", response_model=PredictResponse)
def upload_document(item: PredictInput):
    """
    Endpoint used to save reported web article info into DB
    """
    logger.info(f"Processing predict request for: {item.text}")
    try:
        predicted_label = model([item.text]).tolist()
        prediction = {
            "text": item.text,
            "label": predicted_label,
            "status": "OK"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

    return prediction
