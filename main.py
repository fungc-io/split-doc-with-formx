import os
import requests
import json
import cv2
from dotenv import load_dotenv

load_dotenv()

image_path = "image/2.jpg"

endpoint_url = os.getenv("ENDPOINT_URL")

payload=open(image_path, 'rb')
headers = {
  'X-WORKER-TOKEN': os.getenv("ACCESS_TOKEN"),
  'Content-Type': 'image/jpeg'
}

try:
    response_raw = requests.request("POST", endpoint_url, headers=headers, data=payload)
    res = json.loads(response_raw.text)
    if res["status"] == "ok" and len(res["documents"]) >= 1 :
        documents = res["documents"]
        img = cv2.imread(image_path)
        i = 0
        for doc in documents:
            print(doc)
            type = doc["type"]
            [x1, y1, x2, y2] = doc["bbox"]
            doc_img = img[y1:y2,x1:x2]
            cv2.imwrite('output/'+str(i)+'-'+type+'.jpg', doc_img)

            cv2.imshow(type,doc_img)
            cv2.waitKey(0)
            i += 1
except Exception as e:
    print(e)

