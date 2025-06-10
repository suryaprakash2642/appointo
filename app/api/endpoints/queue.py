from fastapi import APIRouter, HTTPException
from app.services.queue_service import QueueService

router = APIRouter()
queue_service = QueueService()

@router.post("/register/")
def register_patient(name: str, age: int, gender: str, mobile: str, location: str, emergency: bool = False):
    patient_id = queue_service.register_patient(name, age, gender, mobile, location, emergency)
    return {"message": "Patient registered", "id": patient_id}

@router.get("/status/")
def get_queue_status():
    return queue_service.get_queue_state()

@router.post("/pause/")
def pause_doctor():
    queue_service.pause_doctor()
    return {"message": "Doctor paused"}

@router.post("/resume/")
def resume_doctor():
    queue_service.resume_doctor()
    return {"message": "Doctor resumed"}

@router.post("/missed/")
def mark_patient_missed(patient_id: str):
    if not queue_service.mark_missed(patient_id):
        raise HTTPException(status_code=404, detail="Patient not in buffer")
    return {"message": "Patient marked as missed"}

@router.post("/requeue/")
def requeue_missed_patient(patient_id: str):
    if not queue_service.requeue_missed(patient_id):
        raise HTTPException(status_code=404, detail="Patient not found in missed pool")
    return {"message": "Patient requeued"}
