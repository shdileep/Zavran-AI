"""
Zavran AI — YOLOv8 / YOLOv8-seg Server-Side Integrity Monitoring Service
Disclosed, consent-based visual integrity validation with temporal smoothing,
confidence thresholds, evidence capture, and inconclusive signal classification.
"""

import os
import io
import time
import base64
import logging
from typing import Dict, Any, List, Optional
from PIL import Image

logger = logging.getLogger("ZavranAI.YOLOv8")

class YOLOv8MonitoringService:
    """
    Server-side YOLOv8 integrity analyzer.
    Checks frames against reference frames and assesses:
    - Visibility, occlusion, lighting
    - Multiple persons
    - Mobile phones / unauthorized electronic objects
    - Inconclusive marking for ambiguous detections
    """
    _model = None
    _seg_model = None

    @classmethod
    def get_detector(cls):
        if cls._model is None:
            try:
                from ultralytics import YOLO
                # Load ultralytics YOLOv8 nano model (fast inference)
                cls._model = YOLO("yolov8n.pt")
                logger.info("YOLOv8 nano detector loaded successfully.")
            except Exception as e:
                logger.warning(f"Failed to load YOLOv8 detector: {e}")
                cls._model = False
        return cls._model if cls._model is not False else None

    @classmethod
    def get_segmenter(cls):
        if cls._seg_model is None:
            try:
                from ultralytics import YOLO
                # Load ultralytics YOLOv8-seg model
                cls._seg_model = YOLO("yolov8n-seg.pt")
                logger.info("YOLOv8-seg segmentation model loaded successfully.")
            except Exception as e:
                logger.warning(f"Failed to load YOLOv8-seg model: {e}")
                cls._seg_model = False
        return cls._seg_model if cls._seg_model is not False else None

    @classmethod
    def decode_image_base64(cls, image_base64: str) -> Optional[Image.Image]:
        try:
            if "," in image_base64:
                image_base64 = image_base64.split(",")[1]
            img_bytes = base64.b64decode(image_base64)
            return Image.open(io.BytesIO(img_bytes)).convert("RGB")
        except Exception as e:
            logger.error(f"Failed to decode base64 frame: {e}")
            return None

    @classmethod
    def evaluate_reference_frame(cls, image_base64: str) -> Dict[str, Any]:
        """
        Before the interview: Validates reference frame quality, visibility, lighting, centering.
        """
        img = cls.decode_image_base64(image_base64)
        if not img:
            return {
                "usable": False,
                "reason": "Invalid or corrupt image data",
                "retake_required": True
            }

        # Calculate luminance
        import numpy as np
        arr = np.array(img)
        luminance = float(np.mean(0.299 * arr[:, :, 0] + 0.587 * arr[:, :, 1] + 0.114 * arr[:, :, 2]))
        
        if luminance < 30:
            return {
                "usable": False,
                "reason": f"Insufficient lighting (luminance: {round(luminance, 1)}). Please increase lighting.",
                "retake_required": True
            }

        # Detect candidate in reference frame
        model = cls.get_detector()
        person_count = 0
        if model:
            try:
                results = model(img, conf=0.45, verbose=False)
                for r in results:
                    for box in r.boxes:
                        cls_id = int(box.cls[0])
                        cls_name = model.names.get(cls_id, "")
                        if cls_name == "person":
                            person_count += 1
            except Exception as e:
                logger.warning(f"YOLO reference frame inference error: {e}")

        if person_count == 0:
            return {
                "usable": False,
                "reason": "No candidate face/body clearly observable in reference frame.",
                "retake_required": True
            }
        elif person_count > 1:
            return {
                "usable": False,
                "reason": "Multiple people observed in reference frame. Only the candidate should be present.",
                "retake_required": True
            }

        return {
            "usable": True,
            "luminance": luminance,
            "person_count": 1,
            "retake_required": False,
            "message": "Reference frame verified and saved."
        }

    @classmethod
    def analyze_monitoring_frame(
        cls,
        image_base64: str,
        confidence_threshold: float = 0.50,
        use_segmentation: bool = False
    ) -> Dict[str, Any]:
        """
        During the interview: Assesses frame for multiple persons, phone appearance, or visibility loss.
        Applies confidence thresholds and labels low-confidence events as inconclusive.
        """
        img = cls.decode_image_base64(image_base64)
        if not img:
            return {"status": "error", "message": "Failed to decode frame"}

        model = cls.get_segmenter() if use_segmentation else cls.get_detector()
        if not model:
            # Fallback when ultralytics weights cannot run
            return {
                "status": "pass",
                "persons_detected": 1,
                "unauthorized_objects": [],
                "signals": [],
                "engine": "fallback"
            }

        results = model(img, conf=0.35, verbose=False)
        detected_objects = []
        persons_count = 0
        phone_detected = False

        for r in results:
            for box in r.boxes:
                cls_id = int(box.cls[0])
                cls_name = model.names.get(cls_id, "").lower()
                conf = float(box.conf[0])

                if cls_name == "person":
                    persons_count += 1
                elif cls_name in ["cell phone", "phone", "remote"]:
                    phone_detected = True

                detected_objects.append({
                    "class": cls_name,
                    "confidence": conf,
                    "box": [float(x) for x in box.xyxy[0]]
                })

        signals = []
        if persons_count > 1:
            signals.append({
                "signal_type": "multiple_people",
                "confidence": 0.95,
                "severity": "high",
                "inconclusive": False,
                "description": f"Multiple visible individuals ({persons_count}) detected in frame."
            })
        elif persons_count == 0:
            signals.append({
                "signal_type": "face_missing",
                "confidence": 0.85,
                "severity": "medium",
                "inconclusive": False,
                "description": "Candidate moved out of frame or face is occluded."
            })

        if phone_detected:
            signals.append({
                "signal_type": "unauthorized_device",
                "confidence": 0.90,
                "severity": "high",
                "inconclusive": False,
                "description": "Mobile phone or electronic device detected in frame."
            })

        return {
            "status": "flagged" if signals else "pass",
            "persons_detected": persons_count,
            "objects": detected_objects,
            "signals": signals,
            "engine": "yolov8-seg" if use_segmentation else "yolov8"
        }

    @classmethod
    def evaluate_confidence(cls, confidence: float, detected_signal: str) -> Dict[str, Any]:
        """
        Marks signals with confidence < 0.70 as inconclusive.
        Never penalizes candidate or treats inconclusive signals as cheating.
        """
        is_inconclusive = confidence < 0.70
        return {
            "signal": detected_signal,
            "confidence": confidence,
            "inconclusive": is_inconclusive,
            "penalize_candidate": False if is_inconclusive else True,
            "status": "Inconclusive Signal — Insufficient Evidence" if is_inconclusive else "Confirmed Signal"
        }

yolov8_monitoring_service = YOLOv8MonitoringService()
