	import cv2
 import json
 import base64
 import requests
 
 CLOUD_VISION_URL = 'https://vision.googleapis.com/v1/images:annotate'
 
 def encodeToBase64(img):
     _, img_str = cv2.imencode('.jpg', img)
     img_base64 = base64.b64encode(img_str)
 
     return img_base64.decode('utf-8')
 
 def post(img, api_key):
 
     encoded_img = encodeToBase64(img)
 
     params = {'key' : api_key}
     request_body = {
                     "requests": [
                         {
                         "features": [
                             {
                             "type": "TEXT_DETECTION"
                             }
                         ],
                         "imageContext": {
                             "languageHints": [
                             "ja"
                             ]
                         },
                         "image": {
                             "content": encoded_img
                         }
                         }
                     ]
                     }
 
     res = requests.post(CLOUD_VISION_URL, params=params, data=json.dumps(request_body))
     if res.status_code != 200:
         res.raise_for_status()
     else:
         content = res.json()
         return content['responses'][0]['textAnnotations'][0]['description']
 
 if __name__ == "__main__":
     API_KEY = ''
     img = cv2.imread('sample-plate.png')
     print(post(img, API_KEY))
