from collections import deque
from datetime import datetime, timedelta
import uuid

class QueueService:
    def __init__(self):
        self.emergency_queue = deque()
        self.normal_queue = deque()
        self.waiting_buffer = []
        self.missed_pool = []
        self.buffer_size = 3
        self.default_consult_time = 10  # in minutes
        self.doctor_paused_at = None
        self.total_pause_duration = timedelta()

    def _generate_id(self):
        return str(uuid.uuid4())

    def register_patient(self, name, age, gender, mobile, location, is_emergency=False):
        patient = {
            "id": self._generate_id(),
            "name": name,
            "age": age,
            "gender": gender,
            "mobile": mobile,
            "location": location,
            "emergency": is_emergency,
            "registered_at": datetime.now()
        }
        queue = self.emergency_queue if is_emergency else self.normal_queue
        queue.append(patient)
        self.fill_buffer()
        return patient["id"]

    def fill_buffer(self):
        self.waiting_buffer = []

        # 1 Emergency
        if self.emergency_queue:
            self.waiting_buffer.append(self.emergency_queue.popleft())

        # 2 Normal
        while len(self.waiting_buffer) < self.buffer_size and self.normal_queue:
            self.waiting_buffer.append(self.normal_queue.popleft())

    def mark_missed(self, patient_id):
        for i, patient in enumerate(self.waiting_buffer):
            if patient["id"] == patient_id:
                self.missed_pool.append(self.waiting_buffer.pop(i))
                self.fill_buffer()
                return True
        return False

    def requeue_missed(self, patient_id):
        for i, patient in enumerate(self.missed_pool):
            if patient["id"] == patient_id:
                self.missed_pool.pop(i)
                self.register_patient(**patient)
                return True
        return False

    def pause_doctor(self):
        self.doctor_paused_at = datetime.now()

    def resume_doctor(self):
        if self.doctor_paused_at:
            pause_time = datetime.now() - self.doctor_paused_at
            self.total_pause_duration += pause_time
            self.doctor_paused_at = None

    def calculate_eta(self):
        now = datetime.now() + self.total_pause_duration
        etas = []
        for i, patient in enumerate(self.waiting_buffer):
            eta_time = now + timedelta(minutes=i * self.default_consult_time)
            etas.append({
                "patient_id": patient["id"],
                "name": patient["name"],
                "eta": eta_time.strftime("%H:%M")
            })
        return etas

    def get_queue_state(self):
        return {
            "buffer": list(self.waiting_buffer),
            "emergency_queue": list(self.emergency_queue),
            "normal_queue": list(self.normal_queue),
            "missed_pool": list(self.missed_pool),
            "etas": self.calculate_eta()
        }
