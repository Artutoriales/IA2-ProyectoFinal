export interface BoundingBox {
  x1: number;
  y1: number;
  x2: number;
  y2: number;
}

export interface Detection {
  class_name: string;
  confidence: number;
  bounding_box: BoundingBox;
}

export interface DetectionResponse {
  total_people: number;
  detections: Detection[];
  image_result: string;
}

export interface HealthResponse {
  status: string;
}
